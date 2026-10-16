---
type: project_topic
status: active
summary: "CodeGraph（本地代码图谱 CLI + MCP）在本机与 gd26-skills 的接入状态、安装会写什么，以及核对它行为时的坑。"
tags: [codegraph, mcp, claude-code, cursor]
contains: [decision, lesson]
created: 2026-10-15
updated: 2026-10-15
related: []
authoring_mode: ai_generated

---

# CodeGraph

## 当前结论

CodeGraph（`@colbymchenry/codegraph`，MIT）不是 `skills/` 里的 Agent Skill，而是本地优先的代码知识图谱：CLI + MCP server，把符号与调用边存进项目里的 `.codegraph/codegraph.db`（SQLite / WAL）。项目定位见 [codegraph 简介与用法](../otherSkill/codeGraph/00-codeGraph.md)（该笔记按已发布的 1.6.2 逐项核对过，是这块知识的主文档；本页只留跨会话要记的状态与坑）。

本机与仓库状态（2026-10-15）：

| 项 | 状态 |
| --- | --- |
| CLI | `codegraph` 1.6.2，`/opt/homebrew/bin/codegraph`（npm 全局包 `@colbymchenry/codegraph@1.6.2`） |
| Claude Code | 已接入 —— `~/.claude.json` 的 `mcpServers.codegraph`、`~/.claude/settings.json` 的 `mcp__codegraph__*` 权限与 `UserPromptSubmit` hook、`~/.claude/CLAUDE.md` 的标记块 |
| Cursor | 早已接入 —— `~/.cursor/mcp.json`（带 `--path ${workspaceFolder}`） |
| gd26-skills | 已 `codegraph init`（17 文件 / 113 节点 / 216 边，2026-10-15 复核） |

`codegraph install` 对 Claude Code 会多做两件容易被忽略的事：写 `mcp__codegraph__*` 自动放行权限，并装 `UserPromptSubmit` hook（`codegraph prompt-hook`，每次提问注入相关符号提示）。`--no-permissions` 只关权限、不管 hook；关 hook 用 `CODEGRAPH_NO_PROMPT_HOOK=1`，而 `codegraph upgrade` 会把它重新打开。

MCP 默认只列出 `codegraph_explore` 一个工具，另外 7 个（`node`/`search`/`callers`/`callees`/`impact`/`files`/`status`）要设 `CODEGRAPH_MCP_TOOLS` 才出现。

## 决策记录

1. 2026-10-15：Claude Code 侧按用户级（global）接入，用 `codegraph install -t claude -l global -y`，与已有的 Cursor 接入并存。不写项目级配置，这样每个仓库都能用同一份接线。
2. 2026-10-15：建图（`codegraph init`）仍由人按仓库决定，不由代理自动跑。
3. 2026-10-15：知识主文档留在工作笔记 `otherSkill/codeGraph/00-codeGraph.md`，`cairn/` 只留状态与坑，避免两处各写一份清单。

## 教训

判断 CodeGraph 的行为，要按**已发布的 release tag / 已装包**核对，不能只读仓库里的文档。这次实测发现三处文档落后于代码：

- 官方站点 `reference/mcp-server.md` 仍写「没有索引时不列出任何工具」，实际该门禁已移除（无索引时工具照常列出，查询走引导、不报错）。
- 官方站点 `reference/integrations.md` 的代理清单漏了 GitHub Copilot。
- CodeGraph 仓库自己的 `AGENTS.md` 写「installer 不再往说明文件写指令块」，实际文件里仍有完整正文（为 Task 子代理和非 MCP 环境加回）。

可复用的核对手段：`git show v<已装版本>:<文件>`，或直接看 npm 全局包里那份 dist / 实跑 `codegraph --help`。

## 开放问题

`codegraph ui`（浏览器视图）尚未随版本发布（需 `CODEGRAPH_UI=1` 才放行）。发布后值得回头评估是否纳入常用流程。