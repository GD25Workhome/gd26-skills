# gd26-skills

日常开发工作的 skills 的存储。

## 结构

- 在目录 `skills/` 下建立各种 skills 的信息。
- 在目录 `scripts/` 下编写本机同步的脚本，负责将项目下指定的 skills 复制到指定目录下（若目标目录已存在同名 skill，则先备份旧目录再拷贝）。

## 已收录的 skills

### 主要 skills

- 项目日常开发
  - 项目知识沉淀
    - 技能介绍：
      1. **project-cairn** 把 AI 协作中的进展、决策与教训沉淀进项目（`AGENTS.md` + `cairn/`），可复用经验经确认后再「毕业」到 Obsidian / Notion / 飞书知识库。文档优先，无独立 CLI；日常维护靠项目内 `AGENTS.md` 规则驱动。
      2. 新项目先 **初始化**；之后照常协作即可自动记 LOG / 专题。审计、升级、毕业、分支关闭复盘等按需口头触发。写入外部知识库须人工确认。
      3. 工作笔记命名可配合本仓库的 **save-md-artifact** / **ai-docs-md-naming**（`YYMMDD-NN-<slug>.md`）。
    - 技能命令（对 agent 说自然语言即可，无终端 slash 命令）：

      | 意图    | 示例说法                       |
      | ----- | -------------------------- |
      | 初始化   | 在本项目中初始化 Project Cairn     |
      | 日常沉淀  | （正常协作即可）/ 把刚才的结论记进 cairn   |
      | 审计    | 审计本项目的 Cairn，查漂移和缺漏        |
      | 升级    | 把本项目的 Cairn 升级到当前 skill 规范 |
      | 毕业    | 准备毕业候选 / 把这条经验毕业到知识库       |
      | 消费知识库 | 先查知识库再做 / 引用这条笔记到 Cited    |
      | 分支收尾  | 这条探索分支要关了，做分支关闭复盘          |

    - **project-cairn**
      - **说明**：标准化 AI 协作项目的知识沉淀与跨项目复用（init / maintenance / audit / upgrade / graduation / consume / branch-closure）。
      - **主文档**：[SKILL.md](skills/project-cairn/SKILL.md)、[README.md](skills/project-cairn/README.md)、[references/](skills/project-cairn/references/)
      - **同步**：可用 `scripts/sync-skills-to-cursor*.sh` 装到 `~/.cursor/skills/project-cairn`。
  - 文件名格式化
    - 技能介绍：
      1. **save-md-artifact** 在要把内容存成 Markdown 时，只负责**算出唯一文件名与落盘路径**（不替你写正文、不直接创建文件）；脚本输出 `FILEPATH` / `FRONTMATTER_DATE`，由主 agent 再用 Write 落盘。
      2. 典型文件名形如 `YYMMDD-NN-<中文slug>.md`；slug 用中文概括内容。可单独使用，也可被上游技能按约定调用。
      3. **可被前一个技能依赖**：**project-cairn** 在写 `cairn/` 之外的非骨架工作笔记时，约定经本技能生成 `YYMMDD-NN-` 前缀路径（软依赖：不装也能跑 Cairn 核心流程，但工作笔记命名审计会要求合规）。本仓库另有规则型 **ai-docs-md-naming**，侧重 `ai_docs/` 命名纪律，职责不同。
    - 技能命令（示例）：

      | 意图      | 示例说法                                      |
      | ------- | ----------------------------------------- |
      | 推荐路径    | 帮我给这篇内容起一个 md 文件名和存放路径                    |
      | 指定 slug | 用 save-md-artifact，slug 为「独立-skill-新建简化板」 |

    - **save-md-artifact**
      - **说明**：推荐 md 文件名与路径；通过 `scripts/createMdFile.py --slug '…'` 计算路径，主 agent 负责 Write。
      - **主文档**：[SKILL.md](skills/save-md-artifact/SKILL.md)
      - **脚本**：[createMdFile.py](skills/save-md-artifact/scripts/createMdFile.py)
      - **配合关系**：可被 **[project-cairn](skills/project-cairn/SKILL.md)** 依赖（工作笔记命名）；与 **[ai-docs-md-naming](skills/ai-docs-md-naming/SKILL.md)** 互补而非互相替代。注意：SKILL 内示例路径写的是 `~/.claude/skills/...`，在 Cursor 下需装到对应 skills 目录或改调用路径。
  - 开发日记
    - 技能介绍：
      1. **agent-diary** 读取配置目录里按日期存放的开发日报，整理成时间段、事项、投入、完成与未完成，并按项目类型写成公司日志、个人日志、其它；判断不了的放进待确认。默认汇总一段时间内的跨项目、跨会话记录，只有明确限制范围时才收窄。相同内容去重，冲突先问。只整理日报。
      2. 用户级 `~/.agentdiary/config.yaml` 与编程工具无关，Cursor 与 Claude Code 共用一份，只放日记目录、时区、文件名，以及缺日报时的两个开关。项目名单写在日记目录的 `agentdiary.md`，跟着日记走：一节一个项目，写类型、部门，路径和别名可选（如「袜业库」之于「大唐袜业」），不知道仓库路径的项目可以只按名称记一条。当前工作区不在名单里时，先推测类型、名称、部门，连同路径问过用户再追加。日记里出现、不知道仓库路径的项目不自动记入。还没有用户级配置时，先问日记目录并确认时区与文件名，本轮不整理。
      3. 只在用户点名，或明确要求总结 / 整理开发日记、工作日志时触发（也可以直接敲 `/agent-diary`）。默认先在对话里给出结果；用户要求写回时，把总结合并追加进对应日期的「工作记录」，流水和总结保持原样。当天日报不存在时默认先问是否新建。
    - 技能命令（示例）：

      | 意图     | 示例说法                          |
      | ------ | ----------------------------- |
      | 总结今天   | 用 agent-diary 总结今天的工作日志       |
      | 指定日期   | 用 agent-diary 整理 261009 的开发日记 |
      | 一段时间   | 用 agent-diary 整理最近 3 天的开发日记   |
      | 只看当前项目 | 用 agent-diary，只要当前项目          |
      | 直接调用   | `/agent-diary`                |
      | 写回     | 把刚才的工作记录写回日记                  |

    - **agent-diary**
      - **说明**：开发日记整理。单日（今天 / 昨天 / `YYMMDD` 等）和日期区间都支持。用户级配置在 `~/.agentdiary/config.yaml`；项目名单在 `<diary_dir>/agentdiary.md`。配置不放在项目根。
      - **主文档**：[SKILL.md](skills/agent-diary/SKILL.md)、[examples.md](skills/agent-diary/examples.md)、[config.example.yaml](skills/agent-diary/config.example.yaml)、[agentdiary.example.md](skills/agent-diary/agentdiary.example.md)
      - **同步**：Cursor 用 `scripts/sync-skills-to-cursor*.sh` 装到 `~/.cursor/skills/agent-diary`；Claude Code 将目录复制到 `~/.claude/skills/agent-diary`。
- 代码分析
  - 代码分析技能介绍：
    1. analizy-code 为通用代码扫描接口，大接口受限于模型上下文限制，可能会输出不全
    2. **scan-1-code-analizy-output**、**scan-2-output-field-logic**、**scan-3-output-field-logic-drilldown** 三个技能适合在对代码深度解读时按顺序配合使用。建议顺序：先用 **scan-1-code-analizy-output** 列举代码做了哪些事情；再用 **scan-2-output-field-logic** 分析数据变更细节并标记复杂字段；最后用 **scan-3-output-field-logic-drilldown** 对复杂字段深度下钻。这三个技能本质上是对 **analizy-code** 分析流程的细化，用更聚焦的提示词发掘大型接口的内部逻辑。
  - **analizy-code**（analyze-code）
    - **说明**：从用户给出的代码入口下钻分析，按固定章节输出中文技术解读（入口与入参、出参与依赖、流程与 Mermaid 图、实体与关系、用例、横切与待确认）；默认将完整解读落盘到 `ai_docs/`，文件名遵循 **ai-docs-md-naming**。
    - **主文档**：[SKILL.md](skills/analizy-code/SKILL.md)、[examples.md](skills/analizy-code/examples.md)
    - **配合关系**：**analizy-code** 在默认落盘且用户未指定路径/文件名时，须按 **[ai-docs-md-naming](skills/ai-docs-md-naming/SKILL.md)** 的规则命名。
  - **scan-1-code-analizy-output**
    - **说明**：扫码代码的所有输出（深度分析流程第 1 步）。
    - **主文档**：[SKILL.md](skills/scan-1-code-analizy-output/SKILL.md)
    - **配合关系**：建议作为 **scan-2-output-field-logic**、**scan-3-output-field-logic-drilldown** 的前置基线。
  - **scan-2-output-field-logic**
    - **说明**：面向分析结果中的字段与输出项，梳理字段含义、来源与基础计算逻辑（深度分析流程第 2 步）。
    - **主文档**：[SKILL.md](skills/scan-2-output-field-logic/SKILL.md)
    - **配合关系**：建议在 **scan-1-code-analizy-output** 之后使用；复杂字段（L3/L4）可交由 **scan-3-output-field-logic-drilldown** 继续下钻。
  - **scan-3-output-field-logic-drilldown**
    - **说明**：在字段逻辑扫描基础上继续下钻，定位关键字段的详细计算链路与依赖关系（深度分析流程第 3 步）。
    - **主文档**：[SKILL.md](skills/scan-3-output-field-logic-drilldown/SKILL.md)、[examples.md](skills/scan-3-output-field-logic-drilldown/examples.md)
    - **配合关系**：须有 **scan-1** / **scan-2** 或等价基线文档后再使用；不适用首次泛泛读代码的场景。
- 数据爬取
  - LeetCode 刷题文档技能介绍：
    1. **leetcode-1-download-content** 从 leetcode.cn 抓取原题正文与示例图，生成 `LeetCode/LeetCode{4位题号}/` 下的原题 Markdown，并维护 `leetCode题目.md` 中「题目列表」索引。
    2. **leetcode-2-analizy-solution** 根据题解截图或题解网页，识别正文与数学公式，梳理为 `题解-LeetCode{题号}-{算法标签}.md`（含思路、LaTeX 公式与 Java 代码）。
    3. 建议顺序：先抓原题，再写题解；题解文首链接同目录原题文件，并可链到 `算法总结文字/` 下 BFS、DFS、DP 总览。
  - **leetcode-1-download-content**
    - **说明**：抓取 LeetCode 中国站原题（题干、示例、提示、图片），题号 4 位补零，落盘 `LeetCode{NNNN}-{中文题名}.md`；图片存 `imgs/`；默认同步 `leetCode题目.md` 题目列表（保留备注与其它章节）。
    - **主文档**：[SKILL.md](skills/leetcode-1-download-content/SKILL.md)、[reference.md](skills/leetcode-1-download-content/reference.md)、[examples.md](skills/leetcode-1-download-content/examples.md)
    - **脚本**：[download_leetcode_problem.py](skills/leetcode-1-download-content/scripts/download_leetcode_problem.py)、[update_leetcode_index.py](skills/leetcode-1-download-content/scripts/update_leetcode_index.py)
  - **leetcode-2-analizy-solution**
    - **说明**：解析题解截图或网页，再叙述为中文题解 Markdown；文件名 `题解-LeetCode{NNNN}-{广度优先|深度优先|动态规划|…}.md`；数学式用 `$...$` / `$$...$$`；同一题多种写法可各写一篇并互链「姊妹题解」。
    - **主文档**：[SKILL.md](skills/leetcode-2-analizy-solution/SKILL.md)、[reference.md](skills/leetcode-2-analizy-solution/reference.md)、[examples.md](skills/leetcode-2-analizy-solution/examples.md)
    - **配合关系**：依赖同目录原题 md 时，须先由 **leetcode-1-download-content** 抓取或确认原题已存在。

### 其它 skills

- **python-comments**
  - **说明**：在通用 Python 注释规范（简体中文 docstring、类型提示）之上，要求**多行** docstring 正文相对 `"""` 再缩进 4 格、**单行** docstring 写在一行内以便折叠；流程较多时用 `# N.` / `# N~M.` 步骤注释；不直观的方法调用处添加一行简短说明。
  - **主文档**：[SKILL.md](skills/python-comments/SKILL.md)、[examples.md](skills/python-comments/examples.md)
- **ai-docs-md-naming**
  - **说明**：在用户未指定文件名、需将 Markdown 写入仓库（默认 `ai_docs/`）时，按 `YYMMDDNN-描述.md` 生成唯一文件名：须先列出目标目录、仅统计当天前缀文件、取最大 `NN` 再加一；禁止凭记忆猜序号。
  - **主文档**：[SKILL.md](skills/ai-docs-md-naming/SKILL.md)

## 脚本 `scripts`

- **sync-skills-to-cursor.sh**：将 `skills/` 下所有技能同步到 `~/.cursor/skills/`；目标已有同名技能时可选择备份或覆盖。
- **sync-skills-to-cursor-skip-existing.sh**：同上，但目标已有同名技能时 **直接跳过**，无交互、不备份、不覆盖。适合只安装本机尚未有的新技能。

