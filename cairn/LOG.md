# Project Cairn Log

本文件按倒序记录实质进展——最新条目在顶部、紧接本行下方。每条保持简短——仅摘要与指针；结论沉淀进 `cairn/<topic>.md`。

## 2026-10-11 · 本机装上 mattpocock 的 grill 四项技能

- 用户级安装到 `~/.agents/skills/`：`grill-me`、`grilling`、`grill-with-docs`、`domain-modeling`。未写入本仓库，未装 `find-skills`。
- `/grill-me` 只追问、不落文件；`/grill-with-docs` 把术语写入当前仓库的 `GLOSSARY.md`，难改的取舍才写 ADR。追问收在业务规则、边界、输入输出和例子。
- 用法与安装位置见 `cairn/grill技能.md`。

## 2026-10-11 · 本机已安装的 project-cairn 补上分隔线空行

- `~/.cursor/skills/project-cairn` 与 `~/.claude/skills/project-cairn` 的专题模板在结束 `---` 前已有空行。
- 两处的 `obsidian-graduate.sh`、`lark-wiki-graduate.sh` 仍紧贴，已补上同一空行。Notion 脚本不拼这段 Markdown，未改。
- 依据见 `cairn/frontmatter分隔线.md`。

## 2026-10-11 · frontmatter 结束分隔线前加空行

- 专题模板和 Obsidian、飞书毕业脚本拼出的 YAML，结束 `---` 紧贴最后一字段。CommonMark 会把该行加 `---` 当成二级标题，分隔线被吃掉，frontmatter 渲染成正文。
- 三处都在 `authoring_mode` 与结束 `---` 之间加了一空行：`assets/templates/topic.md`、`scripts/obsidian-graduate.sh`、`scripts/lark-wiki-graduate.sh`。
- 依据见 `cairn/frontmatter分隔线.md`。已有笔记 `cairn/技能目录.md` 仍是紧贴写法，这次没改。

## 2026-10-10 · 技能介绍拆成 README 摘要与 skills 分述

- 根 `README.md` 只展开 project-cairn、analizy-code、agent-diary；其余技能一句话，并指向 `skills/README.md`。
- `skills/README.md` 按总分写全部技能：总览分组与配合，分述何时用、怎么说、文档。
- 分工见 `cairn/技能目录.md`。此前 README 里的长段 agent-diary 摘要已收进该分述；技能设计仍在 `cairn/agent-diary.md`。

## 2026-10-10 · README 按当前技能收紧 agent-diary 摘要

- `README.md`「开发日记」按 `skills/agent-diary/SKILL.md` 重写：三栏目输出、只整理日报、用户级配置与 `agentdiary.md` 名单、点名才触发、写回只合并工作记录。
- 设计结论仍在 `cairn/agent-diary.md`。

## 2026-10-10 · agent-diary 项目名单移到日记目录的 agentdiary.md

- 项目名单从 `~/.agentdiary/config.yaml` 的 `projects` 移到 `<diary_dir>/agentdiary.md`：一节一个项目，`## 名称` 下用 `- 类型：`、`- 部门：`，`- 路径：`、`- 别名：` 可选。用户级配置只剩日记目录、时区、文件名和缺日报的两个开关。
- 新增 `agentdiary.example.md` 作形态示例；`SKILL.md` 的配置、步骤、归类、排序、安装各节与 `config.example.yaml`、`examples.md`、`README.md` 同步。
- 本机已建 `dev-diary/diary/agentdiary.md`（含 gd26-skills 一节），并从 `~/.agentdiary/config.yaml` 去掉 `projects`。
- 依据见 `cairn/agent-diary.md`。

## 2026-10-10 · agent-diary 配置去宿主化、新建日报改用最近日记骨架

- 用户级配置不再按宿主分开，统一 `~/.agentdiary/config.yaml`；删掉「当前宿主 / 其它宿主 / 判断不出宿主就停」的描述，以及「一次只覆盖当前这个编程工具」的范围限制与输出里的工具名行。
- 旧的两份宿主机配置保留一次性迁移规则：新路径不存在而旧的还在时读旧的迁过来，两份都在以 `projects` 更全的为准。本机已建 `~/.agentdiary/config.yaml`，旧两份未删。
- 缺日报选「新建」时不再读 `diary_dir/template/日记-天.md`，改为照最近一篇已有日报的骨架写（前行言、两个标题、`# 2 总结` 的小节标题，清掉内容）。
- 同步 `examples.md`、`config.example.yaml`、`README.md`。依据见 `cairn/agent-diary.md`。

## 2026-10-10 · agent-diary 推测改为先问、归类理由升到项目层、path 可选

- 当前工作区不在 `projects` 里时不再静默写入：先推测 `type`、`name`、`department` 并问用户确认，本轮不整理；确认后按用户给的值写入，用户说不用记就只在本次用。
- `归类理由` 从 `#### 事项` 挪到 `### 项目名称` 层——理由描述的是项目为何落在该栏目，原先按事项重复。
- `path` 改为可选：不知道仓库路径的项目可按 `name`（配 `aliases`）只记一条，归类时照样对上，避免「展厅商机发现」这类项目每次重新猜栏目。
- 同步 `examples.md`、`config.example.yaml`、`README.md`。依据见 `cairn/agent-diary.md`。

## 2026-10-10 · agent-diary 去掉 disable-model-invocation，补别名与扁平写法

- 去掉 `disable-model-invocation: true`：Claude Code 下该字段让模型不能自行调用、且 description 不进上下文，与「用户点名或明确要求整理日记」的触发口径冲突；改由 description 承担该约束，`/agent-diary` 仍可直接敲。frontmatter 只剩 `name`/`description`，落回通用 Agent Skills 规范。
- `projects` 增加可选 `aliases`；归类补扁平写法（按事项自身条目匹配名称与别名）与容器条目处理；时间写法归一化、注释块按正文读；去重把已有 `# 3 工作记录` 一起算。
- 同步 `examples.md`（新增扁平写法与别名示例）、`config.example.yaml`、`README.md`。
- 依据与遗留项见 `cairn/agent-diary.md`。

## 2026-10-10 · agent-diary 改为用户级路径名单

- 去掉项目根 `.agentdiary/config.yaml`。类型、名称、部门记在用户级 `projects`。
- 当前路径没有记录时推测并写入，然后继续整理。不知道路径的项目不入库。
- 更正见 `cairn/agent-diary.md`。

## 2026-10-10 · agent-diary 不再询问仓库名单

- 首次只问当前项目的 `type`、`name`、`department`。
- 不询问 `project_dirs`。其它项目按日记自己判断，不向用户要仓库。
- 更正见 `cairn/agent-diary.md`。

## 2026-10-10 · agent-diary 默认跨项目跨会话

- 未明确限制范围时，整理同一工具下的跨项目、跨会话日报。
- 相同内容去重；时间、投入或完成状态冲突时先问用户。
- 更正见 `cairn/agent-diary.md`。

## 2026-10-10 · agent-diary 只保留日报

- 按周汇总不在本技能内，已从 `skills/agent-diary/SKILL.md` 去掉相关描述。
- 仍可按日期区间汇总多天日报。更正见 `cairn/agent-diary.md`。

## 2026-10-10 · agent-diary 增加跨项目统一日志

- 同一编程工具下，可按时间段把多个项目的日报合成一份工作日志。项目名单在该工具的用户级 `project_dirs`。
- 类型、名称、部门仍只读各仓库的 `.agentdiary/config.yaml`。写回按日期拆进各天日报。
- 详情见 `cairn/agent-diary.md`。

## 2026-10-10 · agent-diary 缺日报询问与合并写回

- 当天日报不存在时，`ask_create_diary` 默认必须问是否新建；`false` 表示不再问。项目级优先于用户级。
- 写回改为把总结合并追加进已有工作记录，不覆盖流水、总结，也不整节替换。
- 更正见 `cairn/agent-diary.md`。

## 2026-10-10 · agent-diary 项目类型改到项目级

- 用户级只留日记目录、时区、文件名；缺文件时先询问再写入。
- 每个项目的 `.agentdiary/config.yaml` 必填 `type`、`name`、`department`。类型决定公司、个人或其它日志。
- 用户级 `work_projects` 名单作废。更正见 `cairn/agent-diary.md`。

## 2026-10-10 · agent-diary 配置改为两层

- 用户级默认改到 `~/.cursor/.agentdiary/config.yaml` 与 `~/.claude/.agentdiary/config.yaml`。
- 项目定制为项目根 `.agentdiary/config.yaml`，只覆盖写出的键。
- 技能目录不再保留运行时 `config.yaml`。更正见 `cairn/agent-diary.md`。

## 2026-10-10 · 技能改名为 agent-diary

- 原名 `obsidian-diary` 改为 `agent-diary`，表示给 AI 编程代理用，不绑定笔记软件或某一个 IDE。
- 目录为 `skills/agent-diary/`。当时写的 `~/.config/agent-diary/config.yaml` 同日已作废，配置改为上一条的两层路径。
- 更正见 `cairn/agent-diary.md`。

## 2026-10-10 · 新增 obsidian-diary

- 在 `skills/obsidian-diary/` 写了只可主动触发的单日日记整理技能。同日已改名为 `agent-diary`，目录现为 `skills/agent-diary/`。
- 公司项目名单放配置；项目内是否算公司工作由技能判断。没写的工时保持「未记录」。
- 结论见 `cairn/agent-diary.md`。

## 2026-09-30 · Project Cairn initialized

- 已初始化 Project Cairn 结构。
- 历史迁移模式：`selective_migrate`。
- 详情见 `AGENTS.md` 与 `.cairn/config.yaml`。
