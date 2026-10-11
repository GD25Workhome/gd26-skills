---
type: project_topic
status: active
summary: "结束 frontmatter 的 --- 前必须空一行，否则 CommonMark 会把它当成二级标题。"
tags: [project-cairn, frontmatter, markdown]
contains: [decision, lesson]
created: 2026-10-11
updated: 2026-10-11
related: []
authoring_mode: ai_generated

---
# frontmatter 分隔线

## 当前结论

知识专题和毕业笔记的 YAML frontmatter，最后一个字段与结束 `---` 之间留一空行。模板 `skills/project-cairn/assets/templates/topic.md`，以及 `scripts/obsidian-graduate.sh`、`scripts/lark-wiki-graduate.sh` 按这个形状生成。

2026-10-11 核对了本机已安装副本。`~/.cursor/skills/project-cairn` 与 `~/.claude/skills/project-cairn` 的 `assets/templates/topic.md` 在结束 `---` 前已有空行，未再改。两处的 `scripts/obsidian-graduate.sh`、`scripts/lark-wiki-graduate.sh` 当时仍紧贴，已补上同一空行。Notion 毕业脚本写的是数据库属性，不拼这段 Markdown，未改。

## 教训

CommonMark 把「一行文字，下一行 `---`」解析成 setext 二级标题。结束分隔线若紧贴 `authoring_mode` 这一行，预览会吃掉 `---`，整段 frontmatter 显示成正文。空行打断这个匹配；YAML 本身允许该空行。
