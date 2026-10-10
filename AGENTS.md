# gd26-skills Collaboration Rules

> 本项目使用 Project Cairn 组织项目知识：`AGENTS.md` 是规则与导航入口，`cairn/` 是项目知识/状态层。
> 同目录下的 `CLAUDE.md` 应只含一行 `@AGENTS.md`，以便 Claude Code 读取同一套规则；Codex 直接读本文件。

## Project one-liner

Shuxl的skills技能仓库

> 本文件由 `cairn init` 生成，已填入本项目的定位与 provider 配置；其他项目应各自运行 init，勿直接复用本文件。

## Init configuration

- Graduation provider(s): Obsidian (vault: dev-diary)
- Knowledge base index: knowledge/01-inbox/skills/INDEX.md
- Graduation target: knowledge/01-inbox/skills

## Reading order after entering the project

1. 先读本文件（AGENTS.md）。
2. 若存在 `cairn/ROADMAP.md`，再读其中的路线图、当前焦点与开放问题（ROADMAP 可选；最小初始化的项目可能没有）。
3. 读 `cairn/LOG.md` 最近几条（最新条目在顶部），了解近期进展与关键决策。
4. 按当前任务需要，读相关的 `cairn/` 知识专题文档。



## Document responsibilities


| File               | Role                | Maintenance                               |
| ------------------ | ------------------- | ----------------------------------------- |
| `AGENTS.md` (root) | 规则与导航               | 很少改动，≤ 60 行                               |
| `CLAUDE.md` (root) | 一行 `@AGENTS.md` 桩文件 | 写一次后不再改                                   |
| `cairn/ROADMAP.md` | 路线图与进度              | 原地更新，保持精炼                                 |
| `cairn/LOG.md`     | 时间线日志               | 新条目加在顶部（最新在前），每条 ≤ 20 行，仅摘要 + 指针          |
| `cairn/<topic>.md` | 知识专题文档（当前真相）        | 原地更新；踩坑写入正文段落，用 `contains` 标记；修订在 LOG 留指针 |
| `cairn/Reference/` | 外部原始输入              | 按需创建；只追加                                  |
| `cairn/Cited.md`   | 知识库引用清单             | 仅指针，从不复制原文                                |


> 其余文件只在出现具体信号时才创建（需要记录决策、踩坑已解决、目标跨过单次会话）——不预先造空壳。工程资产（被代码或流程直接消费的契约/配置/规格）不由本系统管理；它们留在代码树，不进 `cairn/`。



## Working-note naming rule

非骨架工作笔记（`cairn/` 以外、且不是上表固定名的文件）须遵循项目 `.cairn/config.yaml` 中的 `cairn.language`：

- `language: zh` → slug 用中文（如 `修复-登录bug`、`需求评审-会议纪要`）。
- `language: en` → slug 用英文（如 `fix-login-bug`、`requirements-review`）。

路径通过 `save-md-artifact` 生成（得到 `YYMMDD-NN-<slug>.md`）；不要自造 `0-` / `1-` 前缀、裸 `note.md` 或仅阶段名。阶段/期次写在 frontmatter 的 `stage`，不进文件名。审计会标记绕过该规则的工作笔记。

## Conflict arbitration rules

- 优先级：**知识专题文档 > LOG 历史**；规则级冲突以本文件为准。
- 业务/设计结论以 `cairn/` 知识专题文档中的最新记录为准，不以更早的 LOG 条目为准。



## Knowledge base consumption reflex

- 在动手做其可复用内核——它将产生或依赖的任何结论——够格毕业的工作之前，先查 knowledge/01-inbox/skills/INDEX.md；仅对真正塑造了产出的笔记在 `cairn/Cited.md` 追加条目（仅指针，从不复制正文）。



## Document collaboration rules

- 改动前先判断用户要的是「讨论/建议」还是「直接改文档」；若说「先看看 / 先评估」，先给分析——不要直接改写正式文档。
- 纠正既往判断时追加更正说明；不要静默覆盖。
- 不要把未确认的判断写成已定事实。



## Knowledge distillation rules

- 每有实质进展，在 `cairn/LOG.md` 顶部追加一条（摘要 + 指针）；让结论沉淀进 `cairn/` 知识专题文档。
- **Completion reply gate：** 在任何完成性宣称之前——包括但不限于工作已完成或已实现、已定稿、已更新、已同步、已验证或测试通过；问题已修复或已解决；交付物可用；声明工作结束；以及语义等价的说法——先跑 `references/maintenance.md` 中的 Cairn checkpoint；只更新其触发矩阵要求的记录，核对后再回复。用户明确要求只读 / 禁止编辑时，禁止写入 Cairn。
- 跨项目可复用经验经毕业机制沉淀进 knowledge/01-inbox/skills。

