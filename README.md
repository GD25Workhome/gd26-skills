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
    2. scan-code-analizy-output、scan-output-field-logic、scan-output-field-logic-drilldown三个技能适合在对代码深度解读时配合在一起使用。建议使用方式为：先用scan-code-analizy-output列举代码做了哪些事情；然后使用scan-output-field-logic技能分析代码的数据变更细节，并标记复杂字段；最后使用scan-output-field-logic-drilldown分析复杂字段的逻辑，进行深度下钻，输出逻辑细节。这三个技能本质上是对analizy-code的分析流程的细化，用更聚焦的提示词，发掘大型接口的内部逻辑
  - **analizy-code**（analyze-code）
    - **说明**：从用户给出的代码入口下钻分析，按固定章节输出中文技术解读（入口与入参、出参与依赖、流程与 Mermaid 图、实体与关系、用例、横切与待确认）；默认将完整解读落盘到 `ai_docs/`，文件名遵循 **ai-docs-md-naming**。
    - **主文档**：[SKILL.md](skills/analizy-code/SKILL.md)、[examples.md](skills/analizy-code/examples.md)
    - **配合关系**：**analizy-code** 在默认落盘且用户未指定路径/文件名时，须按 **[ai-docs-md-naming](skills/ai-docs-md-naming/SKILL.md)** 的规则命名。

  - **scan-code-analizy-output**
    - **说明**：扫码代码的所有输出。
    - **主文档**：[SKILL.md](skills/scan-code-analizy-output/SKILL.md)

  - **scan-output-field-logic**
    - **说明**：面向分析结果中的字段与输出项，快速梳理字段含义、来源与基础流转逻辑。
    - **主文档**：[SKILL.md](skills/scan-output-field-logic/SKILL.md)

  - **scan-output-field-logic-drilldown**
    - **说明**：在字段逻辑扫描基础上继续下钻，定位关键字段的详细计算链路与依赖关系。
    - **主文档**：[SKILL.md](skills/scan-output-field-logic-drilldown/SKILL.md)、[examples.md](skills/scan-output-field-logic-drilldown/examples.md)

### 其它 skills

- **ai-docs-md-naming**
  - **说明**：在用户未指定文件名、需将 Markdown 写入仓库（默认 `ai_docs/`）时，按 `YYMMDDNN-描述.md` 生成唯一文件名：须先列出目标目录、仅统计当天前缀文件、取最大 `NN` 再加一；禁止凭记忆猜序号。
  - **主文档**：[SKILL.md](skills/ai-docs-md-naming/SKILL.md)




## 脚本 `scripts`
- sync-skills-to-cursor.sh：将skill下所有的技能同步到`~/.cursor/skills/`中，可以选择是否备份旧的技能