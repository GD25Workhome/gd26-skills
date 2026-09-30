---
name: project-cairn
description: 标准化 AI 协作项目把工作沉淀为可复用知识的方式。在以下场景使用：在一个项目中初始化或改造 Project Cairn；在完成有实质进展的工作后记录进度；维护 AGENTS/CLAUDE/cairn 文档；审计项目知识以发现漂移或缺漏；从配置好的知识库中引用或使用外部知识；将已验证的项目经验毕业到可复用的知识库。
---

# Project Cairn（项目路标石堆）

Project Cairn 为 AI 协作项目提供一种持久化方式，让项目在真实工作中把「学到的东西」保留下来并供后续复用。**Skill** 提供方法论，**AGENTS.md** 承担项目始终读取的规则，**`.cairn/config.yaml`** 保存机器可读配置。

本 Skill 以文档为先。它提供操作说明、模板、参考文档以及 provider 适配器。没有 CLI、MCP server、后台 hook、聊天结束触发器、provider 自动写入，也没有任何历史自动迁移机制。日常维护在正常工作中进行，因为 `AGENTS.md` 本身承担规则。写入 provider 必须经过人工确认。

## 路由

按需只加载正好对应的那一份参考文档：

- `references/init.md` — 在一个项目中初始化、改造、引导或搭建 Project Cairn。
- `references/consume.md` — 从已配置的知识库中拉取、引用、复用或应用外部知识。
- `references/maintenance.md` — 记录进度、更新 LOG、更新 ROADMAP、维护知识专题文档，或在工作后应用 Cairn 规则。
- `references/audit.md` — 检查、审计、验证、清理项目知识，或找出缺漏的项目知识记录。
- `references/upgrade.md` — 把已初始化的项目实例升级到当前 skill 规范；或检查它已漂移多少（skill 自身演进后实例的漂移）。
- `references/graduation.md` — 毕业知识、把可复用经验搬到知识库、或判断毕业是否成熟；若要写入 provider，则只额外读取所选的 `references/graduation/<provider>.md`。
- `references/frontmatter.md` — 创建或审阅 Cairn 知识专题文档或知识库笔记。
- `references/branch-closure.md` — 在探索性分支即将关闭、放弃或回滚前，复盘并抢救其中的 `cairn/` 知识。
- `references/zh-glossary.md` — 用中文写项目文档（或决定某个中文术语应如何落地）时使用；Project Cairn 自身词汇的中英文固定对照表。也用于从中文模板翻译为英文项目文档时保持术语一致。

frontmatter 中的 description 描述触发场景，不是流程细节。

## 模板

`assets/templates/` 保存 `init` 与后续动作触发时使用的模板：`AGENTS.md`、`CLAUDE.md`、`config.yaml`、`user-config.yaml`、`LOG.md`、`ROADMAP.md`、`topic.md`、`Cited.md`。`init` 只会搭出核心集合（`AGENTS.md`、`CLAUDE.md`、`.cairn/config.yaml`、`cairn/LOG.md`，以及可选的 `cairn/ROADMAP.md`）；也可从 `user-config.yaml` 种子生成可选的 `~/.config/cairn/config.yaml`。`topic.md`、`Cited.md` 与 `Reference/` 在首次触发时再创建，不预先落空壳。模板使用 `{{PLACEHOLDER}}` 占位符，绝不把具体 provider 或知识库路径硬编码进模板。模板正文默认是中文；若项目 `language` 不是中文，按 `references/init.md` 的文档语言规则翻译后再写入。

## 边界

- 不假设有后台 hook，也不假设有聊天结束触发器。
- 日常维护之所以能发生，是因为 `AGENTS.md` 被当作项目规则持续读取。
- 审计是漏记录的兜底。
- 毕业 = 候选检测 + 人工确认。
- 历史迁移是可选的，与 init 分开。
- `scripts/*.sh` 是 bash 适配器脚本，已在 macOS/Linux 验证；Windows 用户需要 WSL 或 Git Bash。`scripts/*.py` 只需 Python 3 解释器；`notion-graduate-batch.py` 还需要 PyYAML。
