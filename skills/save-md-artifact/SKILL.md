---
name: save-md-artifact
description: 当用户要把内容存到 md 文件时触发。此技能只推荐 md 文件名和存放路径，不创建文件。
allowed-tools:
  - Bash(python3 ~/.claude/skills/save-md-artifact/scripts/createMdFile.py --slug *)
  - Write
---

# Save Markdown Artifact

slug 用**中文**概括内容（例：`独立-skill-新建简化板-面试向`、`简单笑话`）。

```bash
python3 ~/.claude/skills/save-md-artifact/scripts/createMdFile.py --slug '<slug>'
```

stdout：`FILEPATH=<路径>`、`FRONTMATTER_DATE=<YYMMDD>`。

主 agent 用 Write 创建 `<FILEPATH>`，content = `---\ndate: <FRONTMATTER_DATE>\n---\n\n<正文>`。
