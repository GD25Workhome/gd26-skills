---
type: project_topic
status: active
summary: "mattpocock/skills 的 grill 四项装在本机 ~/.agents/skills/，用来在动手前把业务规则问清。"
tags: [skills, grill, cursor]
contains: [decision, lesson]
created: 2026-10-11
updated: 2026-10-11
related: []
authoring_mode: ai_generated

---

# grill 技能

## 当前结论

2026-10-11 从 [mattpocock/skills](https://github.com/mattpocock/skills) 把四项技能装到本机用户目录，供 Cursor 在各个项目里使用。没有写入 `gd26-skills` 仓库，也没有装安装器附带的 `find-skills`。

安装命令：

```bash
npx skills@latest add mattpocock/skills -a cursor -g -s grill-me grilling grill-with-docs domain-modeling
```

文件在 `~/.agents/skills/` 下的 `grill-me`、`grilling`、`grill-with-docs`、`domain-modeling`。`~/.cursor/skills/` 里没有这四项目录。Cursor 把 `~/.agents/skills/` 和 `~/.cursor/skills/` 都当作本机用户技能目录。

这四项用来在写代码前把规则问清。使用时把追问收在业务规则、边界、输入输出和例子上。

## 决策记录

1. 2026-10-11：装用户级，不装进 `gd26-skills`。`-a cursor` 只表示目标是 Cursor；不加 `-g` 会写进当前仓库。
2. 2026-10-11：只装 `grill-me`、`grilling`、`grill-with-docs`、`domain-modeling`。`find-skills` 属于安装器仓库 `vercel-labs/skills`，不参与这套追问，选择不装。以后若要装：`npx skills add vercel-labs/skills@find-skills`。
3. 2026-10-11：追问范围收在业务规则、边界、输入输出和例子。实现细节不放进这一轮。

## 用法

新开一个 Agent 对话再用。`grill-me` 和 `grill-with-docs` 标了 `disable-model-invocation: true`，只有输入对应的 `/` 命令才会带上。

| 怎么说 | 技能 | 发生什么 |
| --- | --- | --- |
| `/grill-me` | `grill-me` → `grilling` | 一轮一轮提问，不写文件，确认理解一致前不动手 |
| `/grill-with-docs` | `grill-with-docs` → `grilling` + `domain-modeling` | 同样追问，并把定下来的术语和少数决策写进当前仓库 |
| 讨论术语、改 `GLOSSARY.md` 或 ADR 时由 Agent 自己接 | `domain-modeling` | 收紧用词，对照代码，随手改词汇表 |
| 说 grill、或要求把方案问透时由 Agent 自己接 | `grilling` | 执行下面的提问步骤 |

`grill-me` 和 `grill-with-docs` 的正文各只有一行，分别要求去执行 `grilling`，以及同时执行 `grilling` 和 `domain-modeling`。Cursor 没有 Claude Code 那种 Skill 工具。点名这两个入口后，按同目录里已安装的 `grilling`、`domain-modeling` 的 `SKILL.md` 做。

### `/grill-me`

适合规则还在对话里、还没对着某个仓库落文档。开场可以加上范围，例如：「只问业务规则、边界、输入输出和例子。」

`grilling` 的问法：

- 把待定事项看成一棵决策树。每一轮只问当前已经能问的问题，依赖还没回答的问题留到后面。
- 每题编号，并给出推荐答案。问法写成点头就等于接受推荐答案。
- 事实由 Agent 自己查，不拿能查到的事反问人。决定等人来做，答完再出下一轮。
- 没有未问的分支、并且人确认双方理解一致之后，才算结束。在此之前不写代码。

### `/grill-with-docs`

适合对着现有代码问，并且希望下次不用把同一套词再说一遍。提问步骤与 `/grill-me` 相同，另外按 `domain-modeling` 写文档。

写到**当前工作仓库**，不是写到 `gd26-skills`，除非追问就是在这个仓库里进行：

- 术语定下来就立刻写入仓库根目录的 `GLOSSARY.md`。多数仓库只有一份。根目录已有 `GLOSSARY-MAP.md` 时，按它指向的各上下文分别写。
- 词汇表只收这个上下文特有的词：一词一两句，写它是什么，并列出不要用的近义词。不写实现，也不把它当成规格说明。
- 用词和现有词汇表或代码不一致时，当场指出来，由人决定以哪边为准。
- `docs/adr/000N-简述.md` 只在三件同时成立时才写：以后难改、以后的人会奇怪为什么这样、而且确实在几个办法里选了一个。多数决定不写 ADR。没有第一条术语或第一条 ADR 之前，不先建空文件。

## 教训

`-a cursor` 容易看成「装到 Cursor 用户目录」。它只选择 Agent。在仓库里执行且不加 `-g` 时，技能会进该仓库。这次加了 `-g`，文件落在 `~/.agents/skills/`，不在 `~/.cursor/skills/`。

## 开放问题

尚未在新的 Agent 对话里确认输入 `/grill-me` 时，Cursor 能列出并带上这项技能。
