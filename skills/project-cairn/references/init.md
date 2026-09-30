# init

在项目中初始化或改造接入 Project Cairn。这是交互式配置流程；写入前先询问。

## 需收集的决策

1. 项目名称与一句话摘要。
2. `cairn/` 是提交、忽略，还是私有同步（`git_policy`：`track` | `ignore` | `private_sync`）。**按项目决策——每次必问，永不继承**（见下方「按项目决策」）。若预期 `cairn/Reference/`（见 `assets/templates/config.yaml` 中的决策列表）会存放外部所有权或敏感原始材料——客户 PDF、通话记录——可单独为其提供可选的、更保守的 `reference_git_policy`；省略则 Reference/ 直接继承 `git_policy`。解析后的答案不仅写入记录——还会通过 `.gitignore` 强制执行（见下方「强制执行 git_policy」）。
3. 毕业 provider（可多个）：收集零个或多个目标（如 Obsidian、飞书/Lark CLI、Notion）。「暂不对接」是一等答案——用户可推迟到首次毕业再连接任何知识库（见下方「暂缓对接毕业 provider」）。
4. 对每个 provider，收集目标与索引位置。不要硬编码具体的 Obsidian vault 路径或目录名；那些由用户/项目自行决定。
5. 历史知识策略（`migration_mode`）。默认：`start_fresh`。
6. 生成文件时使用的文档语言（`AGENTS.md`、`cairn/LOG.md`、`cairn/ROADMAP.md`、知识专题文档）。默认：`en`。

通过下方分级默认值解析每项决策，而不是每个项目都从零开始重问。

## 分级默认值

配置通过三层解析，高者优先（与 git/npm/eslint 同一模型）：

1. **项目级** — 项目内的 `.cairn/config.yaml`。覆盖一切。
2. **用户级** — `~/.config/cairn/config.yaml`，形态同 `assets/templates/user-config.yaml`。个人默认：按 provider 类型键控的 `providers` 目录（按名称查找，如 `providers.notion`——是字典，不是待扫描列表），存放用户通常毕业到的目标，以及 `defaults` 下惯用的 `migration_mode` / `language`。`git_policy` / `reference_git_policy` **按设计排除**——见下方「按项目决策」。
3. **内置** — `assets/templates/config.yaml` 中随包提供的模板默认值（`knowledge_dir: cairn`、`migration_mode: start_fresh`、`language: en`）。

凭证（token、vault 密钥、飞书应用密钥）永不进入任一配置文件。放在 `.env` 或密钥库中并按名称引用；永不提交。

### 首次运行 vs. 后续运行

- **首次运行（尚无用户级配置）：** 询问上述完整问题集。收集答案后，提议将它们保存为用户级默认值到 `~/.config/cairn/config.yaml`——**排除下方按项目决策**，那些永不写入该处。
- **后续运行（用户级配置已存在）：** 展示已解析的默认值，并提供一键复用，措辞使用项目已解析的 `language`（例如英文："Reuse usual config? [Enter]"）。只重问用户想改的决策。复用面板仅覆盖 `migration_mode`、`language` 与 providers；用户接受后，**仍须单独询问按项目决策**——多一次按键，而不是重新面谈。
- **非交互模式：** 当用户级配置存在时，静默应用已解析值，不提示（用于脚本化或无人值守安装）。按项目决策没有可应用的已解析值——见其下方回退规则。

### 按项目决策（永不继承）

`git_policy` 与 `reference_git_policy` 在每个项目中重新收集。它们不出现在 `~/.config/cairn/config.yaml` 中，不进入一键复用面板，且没有任何分级层为其供值。

划入此类的判据：**这是仓库的属性，还是人的习惯？** `language`（我用中文写文档）、`migration_mode`（我从零开始）、providers（我的 vault 在这里）跟人走，值得复用。`cairn/` 是否进入版本控制是仓库的属性——公开 OSS、客户私密工作、一次性沙箱——所以上一个项目的答案对下一个没有预测价值。

错误方向也不对称，因此此类没有低摩擦的「与上次相同」路径：

- 本应保持私有的 `cairn/`，被静默提交并推到公开远程 → **不可逆**。一旦推送即被镜像、索引与缓存；事后删除无法召回。
- 本应提交的 `cairn/` 却被忽略 → **可恢复**。文件仍在工作树中；改为 `track` 并提交即可。

**非交互回退：** 当无人可答时，将 `git_policy` 解析为 `ignore`，并在输出中明确说明——例如「未询问 git_policy（非交互）；默认采用保守的 `ignore`。确认后请在 `.cairn/config.yaml` 中设为 `track`。」这是唯一未经确认即落地取值的地方，且钉在可恢复一侧。

### 强制执行 `git_policy`

`git_policy` 不只是记录的意图：写入 `.cairn/config.yaml` 后，init 会让项目的 `.gitignore` 与所选策略一致，使 `git add .` 无法静默违背它。

**策略覆盖范围。** `ignore` / `private_sync` 表示「本仓库历史不留任何 Cairn 痕迹」——不是「仅知识目录不进库」。因此规则覆盖 init 落地的每一条路径：`<knowledge_dir>/`、`.cairn/`，以及——仅当由本次 init 创建时——`AGENTS.md` 与 `CLAUDE.md`。私有的 `cairn/` 旁若有已提交的 `AGENTS.md`，泄露的远不止被藏起的目录名：项目一句话定位、毕业 provider、知识目录、整个 Cairn 段落。同理，`.cairn/config.yaml` 也携带 provider 目标与索引路径。

| 已解析策略 | 动作 |
|---|---|
| `track` | 不写忽略规则。若已有规则已忽略其中某路径，暴露冲突并让用户决定——永不静默删除或覆盖。 |
| `ignore` / `private_sync` | 向项目 `.gitignore` 追加一块，覆盖 `<knowledge_dir>/`、`.cairn/`，以及本次 init 创建的 `AGENTS.md` / `CLAUDE.md`（若有）。 |
| `reference_git_policy` 严于 `git_policy` | 仅追加 `<knowledge_dir>/Reference/`。 |

- **规则无法保护 git 已跟踪的路径——应直说而非假装。** `.gitignore` 对已跟踪文件无效，因此在改造接入且 `AGENTS.md`（或 `CLAUDE.md`）已提交时，为其写规则只会制造虚假安全感。用 `git ls-files --error-unmatch <path>` 测试每条路径；若已跟踪，则不为该路径写规则，并明确告知用户——例如「`AGENTS.md` 已在版本控制中，因此 init 写入其中的 Cairn 段落会随你下次提交出去。若应保持本地，请运行 `git rm --cached AGENTS.md`。」由用户决定；init 从不自行取消跟踪。
- **中性注释。** 块首注释既不点名 Cairn，也不点名策略或原因：`# Local working files, not part of the project`。公开仓库中 `.gitignore` 是公开的；注释若点名工具与策略，恰好广告了策略想藏起的内容。
- **幂等**：任一路径若已被等价规则覆盖则跳过；重 init 或升级时永不写重复项。
- **用项目的 `.gitignore`，不用 `.git/info/exclude`**：规则随仓库走，协作者克隆后行为一致。残留成本——路径名本身仍可见——相对协作者误提交被忽略的 `cairn/` 可接受。
- **在 `track` 下，`.cairn/config.yaml` 从不单独被忽略。** 它是配置而非知识，协作者需要其可移植（见「需创建或更新的文件」）。在 `ignore` / `private_sync` 下它随整块一起忽略。无论哪种，凭证都不放其中——留在 `.env` 并按名称引用。

### 文档语言

决策 #6 同样通过上述三层解析。另有一条规则约束首次运行（尚无用户级默认值）时的*建议*——按序检查，命中即停：

1. **显式全局语言指令** — 若当前 agent 自身的用户级指令已声明一种语言（例如 Codex 的 `~/.codex/AGENTS.md` 或 Claude Code 的 `~/.claude/CLAUDE.md` 写有 "respond in Chinese" / "用中文回答"），建议该语言。
2. **对话语言** — 否则，建议用户最近一条消息所用的语言。
3. **英语** — 否则（极短的首次指令、混语输入，或非交互/脚本化 init），回退到英语。

这是建议默认值，不是静默决定：用户仍像其他 init 问题一样确认或覆盖。一旦确认，`language` 与 `migration_mode` 一样写入 `~/.config/cairn/config.yaml`；下次 `cairn init`——无论哪个 agent、本项目或新项目——通过上方「后续运行」一键流程复用，而不再重新探测或重问。

`assets/templates/` 下的技能模板以中文为先（正文已是中文）。按已解析的 `language` 从中文模板生成文件：

- 当 `language` 为中文（`zh`）时：直接使用中文模板原文（正文已是中文）；保留模板定义的 `{{PLACEHOLDER}}`、frontmatter 键与文件名，并保持相同标题顺序。
- 当 `language` 为英语（`en`）或其他非中文时：将中文模板中的正文与章节标题翻译为目标语言；`{{PLACEHOLDER}}`、frontmatter 键与文件名仍严格按 `assets/templates/` 中文模板定义保留，并保持相同标题顺序。英语术语一致性可反向查阅 `references/zh-glossary.md`。

### 落地到项目中的内容

项目级 `.cairn/config.yaml` 存放**完全解析（冻结）的配置**，而不仅是相对用户级默认值的 diff——这样克隆仓库的协作者无需作者的 `~/.config/cairn` 也能得到完整、可移植的配置。（稀疏「仅 diff」形式是可能的后续优化；当前格式冻结完整结果。）

### 多个 provider

启用多个 provider 时，将 `graduation.providers` 写成列表，而不是单个 `provider`/`target`/`index` 键（形态见 `assets/templates/config.yaml`）。每条需要 `target` + `index`，外加写入方所需的**provider 专属适配设置**——各 provider 并不统一：

- Obsidian：`link_format: wikilink`，vault 相对的 `target`/`index`。
- 飞书/Lark wiki：`space_id`、`index_node_token`、`scope: wiki:wiki`、`api: native`、`identity: user`、`link_format: url`（见 `graduation/lark-wiki.md`）。

在 init 时逐个收集这些 per-provider 细节；不要假定某一 provider 的字段适用于另一 provider。

### 多 provider 的 `AGENTS.md` 渲染

启用多个 provider 时，`AGENTS.md`「初始化配置」中三行占位符各自列出所有已启用 provider，而非仅一个：

- `{{GRADUATION_PROVIDER}}` → `<Provider1> (<primary identifying value>), <Provider2> (<primary identifying value>)`
- `{{KNOWLEDGE_INDEX}}` 与 `{{GRADUATION_TARGET}}` → `<Provider1> → <value>; <Provider2> → <value>`，分号分隔，每个 provider 一句

示例（Obsidian + Notion）：`毕业 provider：Obsidian (vault: ExampleVault), Notion (database: example-db-id-0000)`。若项目 `language` 为英语，再按文档语言规则把标签译为英文等价物。

这种拼接多值形式专门用于「初始化配置」三行要点。同一 `{{KNOWLEDGE_INDEX}}` / `{{GRADUATION_TARGET}}` 令牌还出现在另外两处模板句——「知识库消费反射」与「知识沉淀规则」。对多 provider 项目，不要在那里重复完整拼接值；改为回指该节：将「先查 {{KNOWLEDGE_INDEX}}」替换为「先查已配置的各 provider 索引（见上方「初始化配置」）」，将「通过毕业机制沉淀到 {{GRADUATION_TARGET}}」替换为「通过毕业机制沉淀到已配置的 provider 目标（见上方「初始化配置」）」。单 provider 项目在四处均保持直接替换不变。若项目 `language` 非中文，先按文档语言规则翻译模板，再对译后文本做与上等价的替换。

### 暂缓对接毕业 provider（稍后连接）

若 init 时强制要求 provider，会把首次接触卡在 Obsidian/Notion/飞书已就绪上——但核心机制（LOG、知识专题文档、audit、消费项目自身笔记）完全不需要 provider；毕业是跨项目能力，不是首次接触前提。因此「暂不对接」是决策 #3 的有效答案。用户暂缓时：

- 跳过决策 #4 与所有 provider 预检。
- 将暂缓状态冻结进 `.cairn/config.yaml`，在 `graduation:` 下写 `provider: none`（`assets/templates/config.yaml` 中的形态 (c)）——无 `target`/`index` 键，无 `providers:` 列表。
- 不要把 `none` 写入 `~/.config/cairn/config.yaml`：暂缓是按项目选择，用户级 `providers` 目录只存放真实目标。当存在已保存 providers 的用户级配置时，仍提供一键复用——但明确的「暂不对接」优先于已存默认值。
- init 其余部分照常进行。

延迟绑定：provider 决策（#3–#4）改在首次毕业时收集——见 `graduation.md` →「暂缓对接 provider」。在此之前，`consume.md` 的外部 INDEX 检查无目标，退化为仅查项目自身的 `cairn/` 笔记；`audit.md` 会标出已确认但仍在等待的候选。

**暂缓时的 `AGENTS.md` 渲染** —「初始化配置」三行：

- `毕业 provider：` → `尚未配置（暂缓对接 — 首次毕业时连接知识库）`
- `知识库索引：` 与 `毕业目标：` → `尚未配置`

以及复用同一令牌的两处正文句：

- 「知识库消费反射」要点变为：`在开始一项工作之前——若其可复用内核（它将产出或依赖的任何结论）具备毕业价值——先查阅本项目自身的 cairn/ 知识专题文档；尚未对接外部知识库（provider 暂缓对接 — 见上方「初始化配置」），因此外部索引检查与 cairn/Cited.md 引用在对接后再生效。`
- 在「知识沉淀规则」要点中，将「通过毕业机制沉淀到 {{GRADUATION_TARGET}}」替换为「一旦对接知识库，再通过毕业机制沉淀（provider 暂缓对接 — 见上方「初始化配置」）」。

稍后连接 provider 时，将所有这些位置恢复为上方标准的单/多 provider 渲染。若项目 `language` 非中文，按文档语言规则翻译上述中文替换文本（术语见 `references/zh-glossary.md`）。

### Provider 目标命名

毕业目标的任何人读名称——Obsidian 文件夹、Notion 数据库标题、飞书/Lark wiki 空间——由**用户**选择，而非 Project Cairn。在收集 provider 时（决策 #4）显式询问，并将答案冻结进 `.cairn/config.yaml`；即使正在初始化的项目本身就是 Project Cairn，也永不默认成 "Project Cairn" 或任何其他工具撰写的字符串。当 provider 适配脚本需要该名称来创建新对象（如 `notion-init-db.sh --title`）时，传入已收集的值——脚本应拒绝自行发明。

### 依赖工具的 provider 预检

依赖外部工具的 provider（飞书/Lark CLI、Notion API、同步二进制……）有项目无法假定的带外准备：工具已安装、已授权、已授予正确权限。用户一旦选定此类 provider，**自动探测依赖——不要问用户「装了吗？」**。运行该 provider 的预检并按结论行动：

1. **依赖齐全 → 继续** 下一步 init。
2. **缺失 → 给出官方安装/文档链接，并提议代为安装**："Want me to install it now?"
   - 用户确认 → agent 直接运行文档中的安装命令，然后重跑预检并继续。
   - 用户拒绝 → 暂停；让其手动安装后再恢复。
3. **已安装但未授权 / 缺权限 → 引导** 走完预检 `next` 字段中的确切授权/控制台步骤（不要在第一次真实写入时才失败）。

**飞书/Lark wiki provider：**
- 探测：运行 `scripts/lark-preflight.sh`（只读）→ JSON `status` ∈ `cli_missing` / `not_authed` / `missing_wiki_scope` / `ok`，各自在 `next` 中带确切下一步。
- 安装（确认后提议代跑）：`npm install -g @larksuite/cli && npx skills add larksuite/cli -y -g`，然后 `lark-cli config init` 与 `lark-cli auth login --recommend`。文档：<https://github.com/larksuite/cli>。
- 控制台步骤（为**用户**身份打开粗粒度 `wiki:wiki` 权限）本质需人工——转达预检指示；agent 无法代点。见 `graduation/lark-wiki.md`。

**Notion provider：**
- 探测：运行 `scripts/notion-preflight.sh --db <DATABASE_ID>`（只读）→ JSON `status` ∈ `not_authed` / `db_unshared` / `db_props_missing` / `db_prop_type_mismatch` / `net_error` / `ok`，各自在 `next` 中带确切下一步；类型不匹配含稳定的 `{property,expected,actual}` 细节。
- 设置（多为手动——agent 无法代做的凭证/账户步骤）：在 <https://www.notion.so/profile/integrations> 创建内部 integration（Read+Insert+Update content）→ 将其 `ntn_` token 以 `NOTION_API_TOKEN` 放入 `.env` → 创建/选定知识库**数据库**并**与 integration 共享**（••• → Connections）。token 已设且父页面已共享后，agent **可以** 通过 REST 创建 DB 与属性列。
- 传输：经 curl 直连 REST（`ntn` CLI 在 HTTPS 代理后不可靠）。见 `graduation/notion.md`。

**Obsidian provider：**
- 探测：运行 `scripts/obsidian-preflight.sh --vault "<vault name>" [--target "<folder>"] [--index "<folder>/INDEX.md"]`（只读）→ JSON `status` ∈ `cli_missing` / `app_unreachable` / `vault_unknown` / `vault_unreachable` / `ok`，各自在 `next` 中带确切下一步。
- 安装：与飞书/Notion 不同，**没有 agent 可运行的安装命令**——`obsidian` CLI 随 Obsidian.app 本体捆绑（1.12+），并由 GUI 开关启用：Settings → General → "Command line interface"。转达该确切步骤后停止；步骤 2 的「提议代为安装」此处不适用。文档：<https://help.obsidian.md/cli>。
- 设置：目标 **vault** 须已在 Obsidian 中注册（至少通过 File → Open vault 打开过一次），且预检/毕业运行时桌面应用须在运行——CLI 与存活实例通信，而非直接读写 vault 文件。
- 可靠性说明：切换 CLI 活动 vault 是异步的，其退出码一般不能可靠指示成败——`obsidian-preflight.sh` 会重试已知的空响应与「非零退出但实际已失败」情形；不要在别处对该 CLI 重写单次检查。
- 写入：`scripts/obsidian-graduate.sh` 直接写到 vault 文件系统（不经 CLI），并负责 YAML frontmatter 构造（含结构化 `graduated_from` 列表）。见 `graduation/obsidian.md`。

## 需创建或更新的文件

- `AGENTS.md` — 来自 `assets/templates/AGENTS.md`，替换五个占位符。
- `CLAUDE.md` — 来自 `assets/templates/CLAUDE.md`（一行 `@AGENTS.md`）。
- `.cairn/config.yaml` — 来自 `assets/templates/config.yaml`，冻结已收集的值。`{{SKILL_SPEC_DATE}}` 自动从 `references/upgrade.md` 的「Current spec date」盖章——非用户决策，永不询问；用于锚定后续实例漂移检查（见 `upgrade.md`）。
- `cairn/LOG.md` — 来自 `assets/templates/LOG.md`。
- `cairn/ROADMAP.md` — 可选；仅当项目有跨会话目标时。
- `.gitignore` — 仅当已解析的 `git_policy` / `reference_git_policy` 需要规则时；若不存在则创建，否则幂等追加。块覆盖 `<knowledge_dir>/`、`.cairn/`，以及本次 init 创建的任何 `AGENTS.md` / `CLAUDE.md`，并带中性注释（见「强制执行 `git_policy`」）。

不要预创建空的知识专题文档、`Reference/` 或 `Cited.md`。它们在首次触发时创建。

## 历史处理

不要自动改写历史文档。若已有历史内容，将清单（`inventory_only`）或选择性迁移（`selective_migrate`）作为用户确认的、独立显式动作提供——永不作为 init 本身的一部分。

`.cairn/config.yaml` 是机器真相源。`AGENTS.md` 可为人类摘要相同的 provider 目标，但工具读取配置文件。
