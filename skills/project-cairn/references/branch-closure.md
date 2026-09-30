# branch-closure

在探索分支被合并、放弃或回滚时，用于抢救知识的复盘。由阅读项目 `AGENTS.md` 规则触发；没有自动 hook。Git 决定代码线的命运；本次复盘决定分支经验是否值得保留。

## 何时

在合并、放弃或回滚一条探索分支之前，且其 `cairn/` 笔记或过程产物（如 `docs/superpowers/` 下）发生过变更时。

## 对每项变更分类

把分支上的每一项变更恰好放进一个桶：

- **discard** — 死胡同或已被取代的探索噪声。不要带入 `main`。
- **merge-to-project** — 仍成立的已验证负面结果、决策或教训。沉淀进 `main` 的 `cairn/<topic>.md`（就地更新或新建），并加一条简短的 `cairn/LOG.md` 指针。
- **graduate** — 可超出本项目复用的知识。标为毕业候选（专题笔记上 `graduation_status: candidate`）。不要在此写入知识库；那走人工确认的 `graduation.md` 流程。永远不要静默毕业。
- **archive-reference** — 值得保留的过程产物（规格/计划）。记录指向其路径的指针；不要把正文复制进 `cairn/`。

## 原则

`main` 只接收沉淀后的当前真相，永不接收分支的完整探索历史。分支被回滚并不意味着其知识应消失。不要仅因分支被丢弃就删除已有的 `main` 结论（单向，如同毕业）。

## 产出

记录分类（在真实项目中，写一篇短复盘笔记或一条 `cairn/LOG.md` 条目）。应用 merge-to-project 沉淀与 graduate 标记，把 discard 项挡在 `main` 之外，并记录 archive 指针。
