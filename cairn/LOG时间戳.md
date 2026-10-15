---
type: project_topic
status: active
summary: "cairn/LOG.md 条目标题时间戳使用本地时间 YYYY-MM-DD HH:mm，精确到分钟。"
tags: [project-cairn, log]
contains: [decision]
created: "2026-10-13"
updated: "2026-10-13"
related: []
authoring_mode: ai_generated

---
# LOG 条目标题时间戳

## 当前结论

- `cairn/LOG.md` 新增条目的二级标题时间戳为本地时钟 **`YYYY-MM-DD HH:mm`**（24 小时制，精确到分钟）。
- 不带秒、不带时区后缀；形如 `## 2026-10-13 14:05 · <摘要>`。
- 规范日期之前的日精度（`YYYY-MM-DD`）历史条目可保留；排序时视为该日时刻未知，保持其相对顺序。
- 专题 frontmatter 的 `created`/`updated`、Cited 表日期列仍可按日；本约定只约束 LOG 条目标题。

## 决策记录

- 2026-10-13：用户确认原先只到天的格式不够用，升级 skill 与本实例约定到分钟。技能侧入口：`skills/project-cairn/references/maintenance.md`；实例漂移条目：`references/upgrade.md` → 2026-10-13。
