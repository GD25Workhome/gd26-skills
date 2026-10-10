# 技能介绍

本目录是技能正文。根目录 [README.md](../README.md) 只展开三条常用技能：project-cairn、analizy-code、agent-diary。这里先给总览，再按技能分述。每条技能怎么执行，以该目录下的 `SKILL.md` 为准。

## 总览

技能按用途分成四组。

| 分组 | 技能 | 关系 |
| --- | --- | --- |
| 项目协作 | [project-cairn](#project-cairn)、[agent-diary](#agent-diary) | 一个把项目知识留在仓库里，一个把跨项目日报整理成工作记录 |
| 代码解读 | [analizy-code](#analizy-code)，以及 [scan-1](#scan-1-code-analizy-output)、[scan-2](#scan-2-output-field-logic)、[scan-3](#scan-3-output-field-logic-drilldown) | 先按固定章节解读入口；大接口再按输出、字段、计算链路三步下钻 |
| 落盘命名 | [save-md-artifact](#save-md-artifact)、[ai-docs-md-naming](#ai-docs-md-naming) | 前者给工作笔记算 `YYMMDD-NN-` 路径，后者给 `ai_docs/` 取 `YYMMDDNN-` 序号 |
| 专项 | [python-comments](#python-comments)、[leetcode-1-download-content](#leetcode-1-download-content)、[leetcode-2-analizy-solution](#leetcode-2-analizy-solution) | 注释风格，以及先抓原题、再写题解 |

配合只发生在这几处：

- project-cairn 写 `cairn/` 以外的工作笔记时，文件名走 save-md-artifact。
- analizy-code 默认落盘时，文件名走 ai-docs-md-naming。
- scan-1、scan-2、scan-3 按这个顺序用，是 analizy-code 的细化。
- leetcode-2 要链到同目录原题时，先有 leetcode-1 抓下来的原文。

安装仍用仓库根目录的同步脚本，目标是 `~/.cursor/skills/`。Claude Code 把技能目录复制到 `~/.claude/skills/<技能名>`。说明见 [根 README 的安装](../README.md#安装)。

## 分述

### project-cairn

标准化 AI 协作项目的知识沉淀。正常协作时，agent 按 `AGENTS.md` 把进展写入 `cairn/LOG.md`，把稳定结论写入 `cairn/<topic>.md`。一条经验要拿到别的项目用，先成为毕业候选，确认后写入 Obsidian、Notion 或飞书。

- **何时用**：初始化或改造 Project Cairn；记进度；维护 AGENTS / CLAUDE / cairn；审计漂移和缺漏；引用外部知识库；毕业；探索分支关闭前复盘。
- **边界**：文档优先，没有独立 CLI，也没有聊天结束自动写入。写入外部知识库必须人工确认。
- **怎么说**：

  | 意图 | 示例说法 |
  | --- | --- |
  | 初始化 | 在本项目中初始化 Project Cairn |
  | 日常沉淀 | 把刚才的结论记进 cairn |
  | 审计 | 审计本项目的 Cairn，查漂移和缺漏 |
  | 升级 | 把本项目的 Cairn 升级到当前 skill 规范 |
  | 毕业 | 准备毕业候选 / 把这条经验毕业到知识库 |
  | 消费知识库 | 先查知识库再做 / 引用这条笔记到 Cited |
  | 分支收尾 | 这条探索分支要关了，做分支关闭复盘 |

- **文档**：[SKILL.md](project-cairn/SKILL.md)、[README.md](project-cairn/README.md)、[references/](project-cairn/references/)。
- **命名配合**：工作笔记经 [save-md-artifact](#save-md-artifact) 生成 `YYMMDD-NN-<slug>.md`。

### analizy-code

从用户给出的代码入口下钻，输出中文技术解读。技能名是 `analyze-code`，目录名是 `analizy-code`。有锚点就按章节写完；没有锚点先问入口。用户只要对话、禁止生成文件，或已经指定路径时，按用户的要求，不默认落盘。

输出顺序固定：代码概要，入口与入参，出参、数据变更与外部依赖，流程（概括、纵向链路、图），实体清单与关系，用例，文末横切与待确认。不适用的章节写「本入口不涉及」。Java / Spring REST 补充 HTTP 方法、完整路径、注解和 Mapper。

- **何时用**：需要解读代码、调用链、技术设计、ER、数据流或时序，并且要生成或落盘 Markdown。
- **怎么说**：

  | 意图 | 示例说法 |
  | --- | --- |
  | 解读入口 | 从 `OrderController.create` 解读这段代码，写到 ai_docs |
  | 只要对话 | 解读这个函数，不要生成文件 |
  | 指定路径 | 把这个接口的技术说明写到 `doc/订单创建.md` |

- **文档**：[SKILL.md](analizy-code/SKILL.md)、[examples.md](analizy-code/examples.md)。
- **落盘**：默认 `ai_docs/YYMMDDNN-描述.md`，序号规则见 [ai-docs-md-naming](#ai-docs-md-naming)。
- **下钻**：大接口继续用 [scan-1](#scan-1-code-analizy-output)、[scan-2](#scan-2-output-field-logic)、[scan-3](#scan-3-output-field-logic-drilldown)。

### agent-diary

把开发日记整理成工作记录。栏目按项目类型分成公司日志、个人日志、其它；每条含时间段、事项、投入、完成项与未完成项。默认范围是一段时间、跨项目、跨会话。相同内容去重。时间、投入或完成状态对不上时先问，问完之前不写回这一条。

只整理日报。用户要按周汇总时，说明本技能只处理日报后停止。用户没点名、也没要求整理日记时，不读日记、不写文件。

- **配置**：`~/.agentdiary/config.yaml` 放 `diary_dir`、`timezone`、`daily_name`，以及缺日报时的 `ask_create_diary`、`create_if_missing`。项目名单在 `<diary_dir>/agentdiary.md`，一节一个项目，写类型和部门，路径与别名可选。两份配置都跟具体编程工具无关。
- **第一次**：用户级配置不存在时，先问日记目录，并确认时区与文件名，这一轮不整理。
- **写回**：默认只在对话里给结果。用户要求写回时，按日期把总结合并进对应日报的「工作记录」；流水和总结保持原样。当天日报不存在时，默认先问是否新建。
- **怎么说**：

  | 意图 | 示例说法 |
  | --- | --- |
  | 总结今天 | 用 agent-diary 总结今天的工作日志 |
  | 指定日期 | 用 agent-diary 整理 261009 的开发日记 |
  | 一段时间 | 用 agent-diary 整理最近 3 天的开发日记 |
  | 只看当前项目 | 用 agent-diary，只要当前项目 |
  | 直接调用 | `/agent-diary` |
  | 写回 | 把刚才的工作记录写回日记 |

- **文档**：[SKILL.md](agent-diary/SKILL.md)、[examples.md](agent-diary/examples.md)、[config.example.yaml](agent-diary/config.example.yaml)、[agentdiary.example.md](agent-diary/agentdiary.example.md)。

### save-md-artifact

在要把内容存成 Markdown、又还没有最终路径时，算出唯一文件名和存放路径。脚本打印 `FILEPATH` 和 `FRONTMATTER_DATE`，由主 agent 再写入。本技能不写正文，也不创建文件。

- **何时用**：用户要把内容存到 md 文件，需要推荐文件名和路径。
- **文件名**：`YYMMDD-NN-<中文slug>.md`。slug 用中文概括内容。
- **文档**：[SKILL.md](save-md-artifact/SKILL.md)。脚本：[createMdFile.py](save-md-artifact/scripts/createMdFile.py)。
- **配合**：[project-cairn](#project-cairn) 写工作笔记时走这条命名。与 [ai-docs-md-naming](#ai-docs-md-naming) 分工不同：那边只负责 `ai_docs/` 的 `YYMMDDNN-` 序号。

### ai-docs-md-naming

用户没指定文件名、又要把 Markdown 写入仓库时，生成 `YYMMDDNN-描述.md`。先列出目标目录，只统计当天前缀，取最大 `NN` 再加一。

- **何时用**：新建 `ai_docs/` 文档、保存技术说明或设计文档，或 analizy-code 即将落盘。
- **文档**：[SKILL.md](ai-docs-md-naming/SKILL.md)。
- **配合**：默认被 [analizy-code](#analizy-code) 在落盘前调用。

### scan-1-code-analizy-output

扫一个代码入口的全部输出。先用几句话说明这段代码在做什么，再列出返回结果、数据库变更，以及第三方接口与组件调用。普通日志不算输出。调用了异步接口时，异步链路里的输出也要扫进来。

- **何时用**：要求扫描某个入口的所有输出，或要求按输出驱动、不要漏写。
- **顺序**：深度分析的第 1 步。后面接 [scan-2](#scan-2-output-field-logic)、[scan-3](#scan-3-output-field-logic-drilldown)。
- **文档**：[SKILL.md](scan-1-code-analizy-output/SKILL.md)。

### scan-2-output-field-logic

针对指定入口里的字段，写清每个字段的含义、输入来源和基础计算。复杂字段标出来，留给下一步。

- **何时用**：已经有入口或一份基线文档，要看字段怎么算出来。
- **顺序**：深度分析的第 2 步。建议放在 scan-1 之后。L3 / L4 字段交给 [scan-3](#scan-3-output-field-logic-drilldown)。
- **文档**：[SKILL.md](scan-2-output-field-logic/SKILL.md)。

### scan-3-output-field-logic-drilldown

在已有字段分析上继续下钻。用文字、时序图和流程图写清关键字段的计算链路与依赖。

- **何时用**：基础分析已经有了，还要挖尚未写清的计算过程。
- **不用**：第一次泛泛读代码，或还没有字段范围。
- **顺序**：深度分析的第 3 步。需要 [scan-1](#scan-1-code-analizy-output) / [scan-2](#scan-2-output-field-logic) 或等价基线。
- **文档**：[SKILL.md](scan-3-output-field-logic-drilldown/SKILL.md)、[examples.md](scan-3-output-field-logic-drilldown/examples.md)。

### python-comments

在简体中文 docstring 和类型提示之上，规定注释怎么折叠、流程怎么编号。多行 docstring 的正文相对开闭引号再缩进 4 格；单行 docstring 写在一行内。方法里步骤多时用 `# N.` 或 `# N~M.`。不直观的方法调用旁边加一行短说明。

- **何时用**：编写或补全 Python 注释，或审查注释是否能折叠、能不能看出流程。
- **文档**：[SKILL.md](python-comments/SKILL.md)、[examples.md](python-comments/examples.md)。

### leetcode-1-download-content

从 LeetCode 中国站抓原题正文和示例图，生成离线 Markdown，并维护 `leetCode题目.md` 里的「题目列表」。题号 4 位补零，正文落到 `LeetCode/LeetCode{NNNN}/`，图片进 `imgs/`。

- **何时用**：给出题号或 titleSlug，要求下载原题，或只要求更新题目索引。
- **文档**：[SKILL.md](leetcode-1-download-content/SKILL.md)、[reference.md](leetcode-1-download-content/reference.md)、[examples.md](leetcode-1-download-content/examples.md)。
- **脚本**：[download_leetcode_problem.py](leetcode-1-download-content/scripts/download_leetcode_problem.py)、[update_leetcode_index.py](leetcode-1-download-content/scripts/update_leetcode_index.py)。
- **配合**：题解由 [leetcode-2-analizy-solution](#leetcode-2-analizy-solution) 写。建议先抓原题。

### leetcode-2-analizy-solution

根据题解截图或题解网页，识别正文和数学公式，整理成中文题解 Markdown。文件名是 `题解-LeetCode{题号}-{算法标签}.md`，含原题链接、算法总览链接、思路和代码。公式用 `$...$` / `$$...$$`。同一题多种写法可以各写一篇，并互相链接。

- **何时用**：要求写题解、解析题解截图或网址，或整理 BFS / DFS / DP 等解法笔记。
- **文档**：[SKILL.md](leetcode-2-analizy-solution/SKILL.md)、[reference.md](leetcode-2-analizy-solution/reference.md)、[examples.md](leetcode-2-analizy-solution/examples.md)。
- **配合**：文首要链接同目录原题时，先由 [leetcode-1-download-content](#leetcode-1-download-content) 抓取，或确认原题文件已经在。
