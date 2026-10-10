# gd26-skills

日常开发用的 Cursor / Claude Code skills。`skills/` 放技能正文，`scripts/` 负责同步到本机。

这里只展开三条常用技能。全部技能的分述在 [skills/README.md](skills/README.md)。

## 安装

在仓库根目录执行：

```bash
# 同步全部技能。目标已有同名目录时，可备份到 ~/.cursor/skills-back/ 再覆盖
./scripts/sync-skills-to-cursor.sh

# 只安装本机还没有的技能。已有的直接跳过，不备份、不覆盖
./scripts/sync-skills-to-cursor-skip-existing.sh
```

Cursor 的目标目录是 `~/.cursor/skills/`。Claude Code 把需要的技能目录复制到 `~/.claude/skills/<技能名>`。

## 常用技能

| 技能 | 什么时候用 | 文档 |
| --- | --- | --- |
| [project-cairn](#project-cairn) | 把协作进展沉淀进项目，确认后再毕业到知识库 | [SKILL.md](skills/project-cairn/SKILL.md) |
| [analizy-code](#analizy-code) | 从给定代码入口写中文技术解读，默认落到 `ai_docs/` | [SKILL.md](skills/analizy-code/SKILL.md) |
| [agent-diary](#agent-diary) | 把按日期存放的开发日报整理成工作记录 | [SKILL.md](skills/agent-diary/SKILL.md) |

### project-cairn

把 AI 协作里的进展、决策和教训留在项目里：规则在 `AGENTS.md`，状态在 `cairn/`。可复用经验经确认后，再毕业到 Obsidian、Notion 或飞书知识库。文档优先，没有独立 CLI；写入外部知识库前会先问。

| 意图 | 示例说法 |
| --- | --- |
| 初始化 | 在本项目中初始化 Project Cairn |
| 日常沉淀 | 把刚才的结论记进 cairn |
| 审计 | 审计本项目的 Cairn，查漂移和缺漏 |
| 升级 | 把本项目的 Cairn 升级到当前 skill 规范 |
| 毕业 | 准备毕业候选 / 把这条经验毕业到知识库 |
| 消费知识库 | 先查知识库再做 / 引用这条笔记到 Cited |
| 分支收尾 | 这条探索分支要关了，做分支关闭复盘 |

<details>
<summary>配合与文档</summary>

- 非骨架工作笔记的文件名配合 [save-md-artifact](skills/README.md#save-md-artifact)，形如 `YYMMDD-NN-<slug>.md`。
- 文档：[SKILL.md](skills/project-cairn/SKILL.md)、[README.md](skills/project-cairn/README.md)、[references/](skills/project-cairn/references/)。
- 分述：[skills/README.md](skills/README.md#project-cairn)。

</details>

### analizy-code

从文件与行范围、函数、路由或 CLI 等入口往下读。先用几句话说明这段代码在业务里做什么，再写入口与入参、出参与外部依赖、流程、实体关系、用例，以及文末的待确认项。Java / Spring REST 会补 HTTP、注解和 Mapper。默认把完整解读写到仓库 `ai_docs/`，文件名按 [ai-docs-md-naming](skills/README.md#ai-docs-md-naming)。技能名是 `analyze-code`，目录名是 `analizy-code`。

| 意图 | 示例说法 |
| --- | --- |
| 解读入口 | 从 `OrderController.create` 解读这段代码，写到 ai_docs |
| 只要对话 | 解读这个函数，不要生成文件 |
| 指定路径 | 把这个接口的技术说明写到 `doc/订单创建.md` |

<details>
<summary>配合与文档</summary>

- 大接口要往下拆时，按 [scan-1](skills/README.md#scan-1-code-analizy-output) → [scan-2](skills/README.md#scan-2-output-field-logic) → [scan-3](skills/README.md#scan-3-output-field-logic-drilldown)。
- 文档：[SKILL.md](skills/analizy-code/SKILL.md)、[examples.md](skills/analizy-code/examples.md)。
- 分述：[skills/README.md](skills/README.md#analizy-code)。

</details>

### agent-diary

读取按日期存放的开发日报，整理成时间段、事项、投入、完成项和未完成项，并分成公司日志、个人日志、其它。判断不了的放进待确认。默认汇总一段时间内的跨项目、跨会话记录；相同内容去重，冲突先问。只在点名 `agent-diary`、敲 `/agent-diary`，或明确要求总结 / 整理开发日记、工作日志时运行。

配置与编程工具无关：`~/.agentdiary/config.yaml` 放日记目录、时区和文件名；项目名单在 `<diary_dir>/agentdiary.md`。默认先在对话里给出结果。要求写回时，把总结合并进对应日期的「工作记录」。

| 意图 | 示例说法 |
| --- | --- |
| 总结今天 | 用 agent-diary 总结今天的工作日志 |
| 指定日期 | 用 agent-diary 整理 261009 的开发日记 |
| 一段时间 | 用 agent-diary 整理最近 3 天的开发日记 |
| 只看当前项目 | 用 agent-diary，只要当前项目 |
| 直接调用 | `/agent-diary` |
| 写回 | 把刚才的工作记录写回日记 |

<details>
<summary>配合与文档</summary>

- 还没有用户级配置时，先问日记目录并确认时区与文件名，这一轮不整理。
- 文档：[SKILL.md](skills/agent-diary/SKILL.md)、[examples.md](skills/agent-diary/examples.md)、[config.example.yaml](skills/agent-diary/config.example.yaml)、[agentdiary.example.md](skills/agent-diary/agentdiary.example.md)。
- 分述：[skills/README.md](skills/README.md#agent-diary)。

</details>

## 其它技能

各用一句话。何时启用、产物和配合关系见 [skills/README.md](skills/README.md)。

| 技能 | 一句话 |
| --- | --- |
| [save-md-artifact](skills/save-md-artifact/SKILL.md) | 存 Markdown 时算出唯一文件名和路径，不写正文、不建文件 |
| [ai-docs-md-naming](skills/ai-docs-md-naming/SKILL.md) | 写入 `ai_docs/` 时按 `YYMMDDNN-描述.md` 取下一个序号 |
| [scan-1-code-analizy-output](skills/scan-1-code-analizy-output/SKILL.md) | 扫一个入口的全部输出：返回、库表变更、外部调用 |
| [scan-2-output-field-logic](skills/scan-2-output-field-logic/SKILL.md) | 拆指定字段从哪来、怎么算 |
| [scan-3-output-field-logic-drilldown](skills/scan-3-output-field-logic-drilldown/SKILL.md) | 在已有分析上，把复杂字段的计算链路写细 |
| [python-comments](skills/python-comments/SKILL.md) | 写 Python 时使用可折叠的中文 docstring 和步骤注释 |
| [leetcode-1-download-content](skills/leetcode-1-download-content/SKILL.md) | 从 leetcode.cn 抓原题，并维护题目索引 |
| [leetcode-2-analizy-solution](skills/leetcode-2-analizy-solution/SKILL.md) | 把题解截图或网页整理成中文题解 |
