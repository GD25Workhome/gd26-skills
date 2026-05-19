# gd26-skills

日常开发工作的 skills 的存储。

## 结构

- 在目录 `skills/` 下建立各种 skills 的信息。
- 在目录 `scripts/` 下编写本机同步的脚本，负责将项目下指定的 skills 复制到指定目录下（若目标目录已存在同名 skill，则先备份旧目录再拷贝）。

## 已收录的 skills

### 主要 skills
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

- **ai-docs-md-naming**
  - **说明**：在用户未指定文件名、需将 Markdown 写入仓库（默认 `ai_docs/`）时，按 `YYMMDDNN-描述.md` 生成唯一文件名：须先列出目标目录、仅统计当天前缀文件、取最大 `NN` 再加一；禁止凭记忆猜序号。
  - **主文档**：[SKILL.md](skills/ai-docs-md-naming/SKILL.md)




## 脚本 `scripts`
- sync-skills-to-cursor.sh：将skill下所有的技能同步到`~/.cursor/skills/`中，可以选择是否备份旧的技能