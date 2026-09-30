# Notion 适配器

> 先阅读 [`../graduation.md`](../graduation.md)——共享的人工确认晋升工作流由它负责；本文件只承载 Notion 执行路径。
> 仅在新增或修改适配器时阅读 [`../provider-interface.md`](../provider-interface.md)，仅为执行本流程时不必读。

**步骤 0 — 预检（任何写入之前先运行）。** `scripts/notion-preflight.sh --db <DATABASE_ID>` 只读，返回 JSON 判定：`not_authed`（`NOTION_API_TOKEN` 未设置/无效）、`db_unshared`（集成看不到该 DB——在 Notion → ••• → Connections 中分享）、`db_props_missing`（缺少必需的 property 名称）、`db_prop_type_mismatch`（名称存在但一个或多个 Notion property 类型不兼容；检查 `property_type_mismatches`）、`net_error`（代理/SSL 放弃）或 `ok`。未到 `ok` 不要写入。

经验证的晋升到 Notion 知识库路径：

- **数据模型 = database。** DB 既是知识库容器也是 INDEX（其视图/属性即索引）——因此**没有 `update_index` 步骤**，也没有可追加的 INDEX 页面。每条晋升笔记对应一行 DB（一个 page）。Frontmatter 映射为 DB **properties**，而非 YAML：`type`/`authoring_mode`→Select，`contains`/`tags`/`contributors`/`graduated_by`→Multi-select，`graduated_from`→Text，`graduated_at`→Date。已有 database 不会自动迁移：预检报告缺失属性，schema 变更需确认。
- **传输 = 直接 REST（curl），而非 `ntn` CLI。** `ntn` 会拉取 OpenAPI 规范来解析端点，不遵守 `HTTPS_PROXY`，在代理后对 `PATCH`/`query` 会失败。经 curl 的直接 REST 遵守代理；每次请求用退避 **retry** 包住，以扛住随机 SSL EOF。
- **鉴权 = 内部集成 token**，放在 `NOTION_API_TOKEN`（保存在 `.env`，在配置中按名称引用——绝不写入 `.cairn/config.yaml`）。DB（或其父页面）必须**与该集成共享**——这是 `create_note` 的读依赖。
- **钉死 `Notion-Version: 2022-06-28`**（经典单源 database；避免 2025-09-03+ 的 data-source 语义）。
- **写入循环：** 创建模式发送一次带 `properties` + `children` 的 `POST /v1/pages`。更新模式接收已有 page ID，PATCH 其 properties，归档所有现有顶层 child blocks，再 PATCH 替换后的 children。两种模式都用 `GET /v1/pages/{id}` 回读，校验标题往返一致。
- **原文引用保持原生。** 连续的 Markdown `>` 组（直接摘录加署名）变为一个 Notion `quote` block，两段一并保留。没有引用仍然有效，不创建占位 block。
- **`[[wikilinks]]` → 真正的 page mention 需要批量两遍**（先创建所有页面、收集 title→id，再写入带 `mention` blocks 的正文）。单笔记适配器把 wikilink 渲染为粗体标题文本；整套互链一并晋升时用批量工具。
- **可执行适配器**（均为 curl/REST + retry，钉死版本；`--dry-run` 可预览）：
  - `scripts/notion-init-db.sh --parent-page-id PAGE_ID --title "<knowledge base name>"` — 在已共享的父页面下，用 Cairn property schema 创建 KB database。`--title` 必填——是 database 的显示名，在 init 时向用户收集（见 `init.md` → provider target naming），绝非硬编码默认值。
  - `scripts/notion-graduate.sh --db ID [--page-id EXISTING_PAGE_ID] --title T --content body.md [properties/provenance flags…]` — 无 `--page-id` 时创建一页；有则替换该页的 properties/正文。重复的 provenance 名称→Multi-select，quote 组→原生 quote blocks，wikilinks→粗体文本。`--props-json` 仍为专家覆盖项；调用方传入完整的当前 properties。
  - `scripts/notion-graduate-batch.py --db ID --graduated-at DATE --src-dir DIR [--repo-prefix P]` — 互链集合，两遍处理使 `[[wikilinks]]` 成为真正的 page mentions；frontmatter→properties（容忍旧式标量 provenance 名称，但始终写成去重后的 Multi-select 数组）；quote 组→原生 quote blocks。`DIR` 必须包含已由共享晋升流程准备好的知识库笔记，而非原始 `cairn/` 项目主题：每条输入须有 `type: knowledge_note` 以及非空的 `graduated_from` 与 `graduated_by`。脚本在首次 Notion 请求前校验每条输入，拒绝 `project_topic` 而非静默改标，并以源文件与位置报告 YAML 错误。已有标题就地更新（properties 用 PATCH 合并，正文替换），不跳过。用 Python（urllib+retry），因为 title→id 图在 bash 里不好写。
