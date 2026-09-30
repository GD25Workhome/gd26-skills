# Obsidian 适配器

> 先阅读 [`../graduation.md`](../graduation.md)——共享的人工确认晋升工作流由它负责；本文件只承载 Obsidian 执行路径。
> 仅在新增或修改适配器时阅读 [`../provider-interface.md`](../provider-interface.md)，仅为执行本流程时不必读。

**步骤 0 — 预检（任何写入之前先运行）。** `scripts/obsidian-preflight.sh --vault "<vault name>" [--target "<folder>"] [--index "<folder>/INDEX.md"]` 只读，返回 JSON 判定：`cli_missing`、`app_unreachable`、`vault_unknown`、`vault_unreachable` 或 `ok`。未到 `ok` 不要写入。

经验证的晋升到 Obsidian vault 路径：

- **`obsidian` CLI 仅用于解析 vault 路径（读依赖），以及可选地回读笔记做校验——不用于写入笔记。** `obsidian create` 把内容当作 shell 参数传入，与 Lark 适配器用 stdin 绕开的长度/引号脆弱性同类；此处改为直接写入 vault 文件系统。
- **Frontmatter 是嵌入笔记的原生 YAML**，不是外部属性（Notion），也不留给调用方手工嵌入（Lark）。适配器根据 flags 自行构造 frontmatter，方式与 `notion-graduate.sh` 自行负责 DB properties 相同。
- **`graduated_from` 是 `{project, path}` 条目的结构化列表**，不是标量——见 `frontmatter.md` → "`graduated_from` shape"。已对照生产环境中的笔记验证；多条笔记会引用不止一个来源。
- **`[[wikilinks]]` 原样透传。** Obsidian 是唯一原生支持 WikiLink 的 provider（`config.yaml` 的 `link_format: wikilink`）——无需改写步骤，不像 Notion 的两遍 mention 转换。
- **覆盖保护与更新模式。** 直接写文件系统会静默覆盖同名标题的已有笔记，因此创建模式拒绝覆盖。再次晋升有意传入 `--force`，以当前完整笔记原子替换同一 vault 相对路径；幂等的 INDEX 检查保证只保留一条 `[[Title]]` 条目。
- **构建时发现的两处真实 CLI 可靠性缺口**（修复见 `obsidian-preflight.sh`）：切换 CLI 的活动 vault 是异步的（切换后第一次查询可能以 `rc=0` 返回空结果，而非报错）；若干命令（例如读取不存在的文件）失败时也返回 `rc=0`，错误只出现在打印文本里。不要信任对该 CLI 的单次检查或裸退出码。
- **可执行适配器**（`--dry-run` 预览 frontmatter 与目标路径，不触碰文件系统）：
  - `scripts/obsidian-graduate.sh --vault "<name>" --title T --target "<folder>" [--content body.md] [--index "<folder>/INDEX.md"] [--summary …] [--contains a,b] [--tags a,b] --graduated-from "<project>|<path>" [--graduated-from … repeatable] --contributor Alice --graduated-by Alice [--authoring-mode …] [--force]` — 写入笔记，并可选地向 INDEX 文件追加一行 `[[WikiLink]]`（文件尚不存在时会创建）。
