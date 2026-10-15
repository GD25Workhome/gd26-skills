# 简单介绍

[CodeGraph](https://github.com/colbymchenry/codegraph)（`@colbymchenry/codegraph`，MIT）是给编程代理用的**本地代码知识图谱**。它不是 Cursor Agent Skill（没有 `SKILL.md`），而是一套 CLI，再通过 MCP 接到 Cursor、Claude Code、Codex、Gemini、OpenCode、Antigravity、Kiro、GitHub Copilot、Hermes Agent。

代理平时靠 grep、glob、逐文件阅读来摸清调用关系和依赖。CodeGraph 事先把符号、调用边、依赖建成图，存在项目里的 `.codegraph/codegraph.db`（SQLite）。问结构问题时，一次 `codegraph_explore` 就能带回：相关符号的原文（按文件分组、带行号）、它们之间的调用路径（含回调、接口到实现这类 grep 跟不住的动态分发）、以及改动的影响范围。数据不出本机，不需要 API key。

文件一改，图会跟着更新。MCP 服务用系统文件事件监听，默认安静约 2 秒后增量同步；会话刚连上时也会按文件大小、修改时间和内容哈希补一次，避免 `git pull` 或别的编辑器改过的文件还停在旧图上。同步窗口里若结果还引用未入库的文件，响应里会带提示，让代理直接读那个文件。

语言按扩展名自动识别，常见的有 TypeScript / JavaScript、Python、Go、Rust、Java、C / C++、C#、PHP、Ruby、Swift、Kotlin、Scala、Dart，以及 Vue、Svelte、Astro 等。也识别一批 Web 框架的路由（Django、Flask、FastAPI、Express、NestJS、Spring、Next.js、Vue Router 等），把 URL 接到处理函数上。默认跳过 `node_modules`、`dist`、`.gitignore` 里的路径，以及大于 1 MB 的文件。

官方文档：[https://colbymchenry.github.io/codegraph/](https://colbymchenry.github.io/codegraph/)

# 使用方式



## 如何安装

分三步。装 CLI 和接入代理是本机一次；建图是每个仓库各做一次。`codegraph install` **不会**索引代码。

### 1. 安装 CLI

macOS / Linux（自带运行时，不要求本机先有 Node）：

```bash
curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh
```

已有 Node 时也可以：

```bash
npm i -g @colbymchenry/codegraph
```

安装脚本不会改当前 shell 的 PATH。装完后**新开一个终端**，确认 `codegraph version` 能跑。

### 2. 接到代理

```bash
codegraph install
```

交互里选择要配置的代理（Cursor 会被自动检测到），以及配置写到用户级还是只写当前项目。这一步写入 MCP 配置（启动命令是 `codegraph serve --mcp`），并在代理说明文件里加一小段用法。Cursor 需要**重载窗口或重启**后，MCP 才会出现。

非交互示例：

```bash
codegraph install --yes --target=cursor
codegraph install --yes --init    # 接好代理后，顺手为当前目录建图
```



### 3. 为每个项目建图

在仓库根目录：

```bash
codegraph init
```

会创建 `.codegraph/` 并完成首次索引。之后保存文件即自动更新，不必再跑 `codegraph sync`。本仓库 `gd26-skills` 已在 2026-10-15 执行过 `codegraph init`（12 个文件，113 个节点，216 条边）。

### 升级与卸下

```bash
codegraph upgrade          # 按当初的安装方式原地升级；--check 只查看
codegraph uninstall        # 从各代理去掉配置，并卸掉 CLI
codegraph uninstall --keep-cli
codegraph uninit           # 只删当前项目的 .codegraph/
codegraph telemetry off    # 关闭匿名用量统计
```



## 如何使用

图建好之后，在 Cursor 里直接问结构问题即可。代理应调用 MCP 工具 `codegraph_explore`，把返回的源码当作已经读过，不必再用 grep 复核。默认只暴露这一个工具；`codegraph_node`、`codegraph_search`、`codegraph_callers` 等仍然可用，但要设环境变量 `CODEGRAPH_MCP_TOOLS` 才会出现在 MCP 列表里，平时用对应的 CLI 即可。

适合这样问：

- 这段代码在做什么、某个函数怎么工作
- 请求从入口怎样走到数据库 / 某个函数怎样调用到另一个
- 改这个符号会影响到哪些调用方

当前 Cursor 会话若是从**没有** `.codegraph/` 的目录启动的，工具仍然可用：给已建图的项目传 `projectPath`。没有索引的路径会提示改用内置的 Read / Grep，不会硬失败。是否建图由人决定，代理不会自己跑 `codegraph init`。

自己在终端里查，和 MCP 是同一套结果：

```bash
codegraph explore "登录请求怎样写到数据库"
codegraph node UserService          # 单个符号的源码和调用方；也可传文件路径
codegraph query UserService         # 按名字搜符号
codegraph callers saveUser
codegraph callees saveUser
codegraph impact saveUser           # 改这个符号的影响半径
codegraph affected src/auth.ts      # 变更会碰到哪些测试
codegraph status                    # 节点数、待同步文件
codegraph sync                      # 监听关掉或要在脚本里先对齐时再手动跑
codegraph index --force             # 全量重建
```

可选的项目根配置是 `codegraph.json`（没有这个文件就是零配置）：

```json
{
  "exclude": ["static/"],
  "include": ["Tools/"],
  "deprioritize": ["scripts/"],
  "extensions": { ".tpl": "php" }
}
```

- `exclude`：已提交进 git、但 `.gitignore` 去不掉的目录（如随仓库提交的主题、SDK）。
- `include`：故意被 gitignore、但仍要进图的源码。
- `deprioritize`：仍可搜到，只是不要压过正式代码（通用名字的脚本目录）。
- `extensions`：把非标准后缀映射到已支持的语言；改完后执行 `codegraph index`。

常见问题：提示未初始化就在该仓库跑 `codegraph init`；MCP 连不上就确认 `codegraph status` 正常，再重跑 `codegraph install` 并重启 Cursor；符号缺失时等一两秒让自动同步完成，或手动 `codegraph sync`，并确认文件没有被 gitignore 或默认排除。