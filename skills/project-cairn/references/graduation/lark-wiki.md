# Lark / 飞书 wiki 适配器

> 先阅读 [`../graduation.md`](../graduation.md)——共享的人工确认晋升工作流由它负责；本文件只承载 Lark/飞书 wiki 执行路径。
> 仅在新增或修改适配器时阅读 [`../provider-interface.md`](../provider-interface.md)，仅为执行本流程时不必读。

**步骤 0 — 预检（任何写入之前先运行）。** `scripts/lark-preflight.sh` 只读，返回 JSON 判定：`cli_missing`（未安装 → 给出文档链接并暂停）、`not_authed`（运行 `lark-cli auth login`）、`missing_wiki_scope`（在控制台为用户身份开启 `wiki:wiki`，然后重新鉴权）或 `ok`（可安全晋升）。在报告 `ok` 之前不要尝试写入循环。

经验证的、用 `lark-cli` 用户身份晋升到飞书知识库的路径：

- **Scope：** 申请粗粒度的 `wiki:wiki`（覆盖读 + 写）。细粒度读 scope（`wiki:space:retrieve` / `wiki:space:read` / `wiki:node:read`）在 CLI 类应用上可能永远进不了用户 token（用户授权页上看不到）；具备写能力的 `wiki:wiki` 会出现且能可靠落地。诊断：若 `--as bot` 可用而 `--as user` 报告缺 scope，阻塞在用户授权路径，而非应用已发布权限。
- **API：** 使用原生资源命令（`wiki spaces get`、`wiki nodes create`、`wiki nodes list`、`wiki spaces get_node`）+ `docs +update`/`docs +fetch`。`wiki +space-list` / `+node-create` 快捷方式会做严格字面 scope 预检，不认 `wiki:wiki` 覆盖，并在本地拒绝。
- **写入循环：** 创建模式解析目标 space（`my_library` 或团队 `space_id`）→ `wiki nodes create`（用 `parent_node_token` 建目录树）→ 追加初始正文 + frontmatter。更新模式接收原始 node/document 标识，并用本地已验证的 `docs +update --command overwrite` 操作替换该文档。两种模式随后都 `docs +fetch` 做校验，并维护可选的 INDEX/容器链接。父节点 = 目录/索引容器；子节点 = 各条晋升笔记。
- **可执行适配器：** `scripts/lark-wiki-graduate.sh` 端到端编码上述两个循环，并强制上述约束。内容经 stdin 管道传入，以绕开 CLI 相对 cwd 的 `@file` 限制。用 `--dry-run` 可在写入前预览确切的原生 API 调用。
  - Frontmatter flags（`--type`/`--summary`/`--contains`/`--tags`/`--graduated-from`/`--contributor`/`--graduated-by`/`--authoring-mode`）可选但推荐：只要传入任一，脚本会组装成 YAML 格式块并前置到正文（已确认飞书 markdown 转换后**不会**作为可解析 YAML 保留——见 `references/provider-interface.md` 与 `cairn/LOG.md` 2026-07-02）。全部不传则保持旧的精确行为（内容原样写入）。
  - `--index-doc` 追加是幂等的：追加前会检查 index doc 是否已有 `[$TITLE](` 条目。再次晋升走更新模式，因此不会重复创建 node 或 INDEX 条目。
  - 创建：`scripts/lark-wiki-graduate.sh --title T --content body.md --space-id <id|my_library> [--parent-node-token TOK] [--index-doc OBJ_TOKEN] [frontmatter flags…]`
  - 更新：加上 `--update-node-token NODE_TOKEN --update-obj-token OBJ_TOKEN --update-url URL`，并传入调用方已并集好的完整 provenance flags；三个目标值必须同时提供。
