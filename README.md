# gd26-skills

日常开发工作的 skills 的存储。

## 结构

- 在目录 `skills/` 下建立各种 skills 的信息。
- 在目录 `scripts/` 下编写本机同步的脚本，负责将项目下指定的 skills 复制到指定目录下（若目标目录已存在同名 skill，则先备份旧目录再拷贝）。

## 已收录的 skills

### 主要 skills
- 代码分析
  - **analizy-code**（analyze-code）
    - **说明**：从用户给出的代码入口下钻分析，按固定章节输出中文技术解读（入口与入参、出参与依赖、流程与 Mermaid 图、实体与关系、用例、横切与待确认）；默认将完整解读落盘到 `ai_docs/`，文件名遵循 **ai-docs-md-naming**。
    - **主文档**：[SKILL.md](skills/analizy-code/SKILL.md)、[examples.md](skills/analizy-code/examples.md)
    - **配合关系**：**analizy-code** 在默认落盘且用户未指定路径/文件名时，须按 **[ai-docs-md-naming](skills/ai-docs-md-naming/SKILL.md)** 的规则命名。

  - **scan-code-analizy-output**
    - **说明**：对 `analizy-code` 产出的分析文档做快速扫描，提炼关键结构与重点信息，便于后续二次处理。
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