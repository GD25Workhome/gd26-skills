# provider-interface

每个毕业 provider 适配器脚本（预检 + 毕业）必须满足的行为契约，外加消费时使用的读侧查询能力契约。在新增第 4 个 provider 或改动现有 provider 之前先读本文——`graduation/` 下各 provider 参考展示的是三个现有 provider 如何满足本契约，而非另一套规则。日常毕业执行不需要本文件；所选 provider 参考携带每条原则在该 provider 上的具体后果。

## 预检脚本

- 只读。永远不执行任何写入。
- 向 stdout 打印 JSON 裁决，至少包含 `status`（字符串）与 `next`（字符串，可执行的人工指引）键。额外的 provider 专属诊断字段（`cli_installed`、`db_readable`、`has_wiki_scope` 等）是预期的，且不要求跨 provider 同名。
- 当且仅当 `status == "ok"` 时退出码为 0。其他所有 status 退出 1。
- `status == "ok"` 是调用方可以安全进入毕业脚本的信号——无需再重检其他项。
- 基于 schema 的 provider 必须同时校验必填属性名与其类型。缺名与已有类型不兼容是不同失败：Notion 对前者报告 `db_props_missing`，对后者报告 `db_prop_type_mismatch` 外加 `{property,expected,actual}` 条目。

## `create_note`（毕业脚本的核心操作）

- 必须支持 `--dry-run`。在 dry-run 模式下，脚本必须做 **无 provider 侧写入、无变更性 API 调用**——仍可做只读调用（如解析目标）与仅本地文件系统暂存工作（如 `mktemp` 出的 payload 文件，退出时清理），因为二者都不触碰 provider 的真实状态。它必须把本会做的事打印到 stderr，并向 stdout 打印一个 JSON 对象，该对象是 **真实成功形态的超集**（真实输出的每个键都有，值为占位；允许额外信息键）——不要求键对键完全一致。
- 写入前必须解析/验证写入目标（**读依赖先于写**——三个 provider 均已验证：Lark 在创建节点前读取目标空间；Notion 预检在 create 前确认 DB 已共享/可读；Obsidian 在写入文件前解析 vault 的真实文件系统路径）。Provider 适配器不得假定有写权限就意味着目标有效。
- **每个适配器必须提供由标志驱动的 frontmatter 构建；调用方永远不应需要把 frontmatter 手写嵌入 `--content`。** `--content`（若接受）仅为正文。这是适配器*能力*上的硬要求——标志必须存在，且在使用时必须就是构建 frontmatter 的方式。这不是要求每个调用点都传这些标志。
  - 实现方式 **并非** 跨 provider 统一：
    - **原生结构化字段**（Notion）：frontmatter 标志映射到真实数据库属性（Select/Multi-select/Text/Date），与页面正文物理分离。
    - **嵌入文本块**（Obsidian、Lark）：frontmatter 标志组装成 YAML 格式文本块，作为字面内容写在笔记/文档顶部。这不是 Notion 属性那种「原生」。对 Obsidian，它与平台自身的磁盘格式完全一致。对 Lark，这是结构化意图的人类可读文本表达；已确认经飞书 markdown 转换后 **不会** 以可解析 YAML 存活——`---` 标记本身会作为字面文本存活，但嵌套列表条目（`graduated_from` 的 `- project: ... / path: ...`）在往返中丢失缩进，于是 YAML 解析器要么报错，要么静默把 `path` 误当成列表条目的顶层兄弟键而非其字段。把 Lark frontmatter 块当作给人/Agent 读者看的文档，而非机器可再解析的结构——实测见 `cairn/LOG.md` 2026-07-02。
  - `--graduated-from` 不是跨 provider 的标准化标志：Obsidian 与 Lark 将其作为可重复的 `"<project>|<path>"` 结构化条目（匹配生产环境 `graduated_from` frontmatter——见 `frontmatter.md`）；Notion 现有的 `--graduated-from` 取单个纯文本值写入一个 `rich_text` 属性。同名标志，三种语义——不要假定可互换。
  - 每个适配器必须提供可重复的 `--contributor NAME` 与 `--graduated-by NAME` 能力。每次出现向对应列表追加一个人类可读名称；即使只有一个名称也保持列表形态，并对重复身份去重且不改变首次出现顺序。身份解析属于毕业工作流，不属于底层适配器。
  - 省略这些标志时，底层适配器必须保持向后兼容。但毕业工作流每次新毕业与重新毕业都必须至少传入一个 `--graduated-by NAME`；缺席仅对遗留/直接底层调用受支持，不适用于新的工作流产出。
- 输出 JSON 至少须包含一个位置/标识符字段与一个链接/URL 字段。确切字段名按 provider 适当命名，不标准化（Notion 为 `{id,url}`，Obsidian 为 `{path,obsidian_url}`，Lark 为 `{node_token,obj_token,url}`）。
- 写入后必须尝试回读验证。验证不匹配或失败降级为 stderr 上的 `warn:`——永远不得回滚或使整体操作失败，因为对象/文件已经创建。

## `update_note`（重新毕业进已有目标）

- 每个 provider 适配器必须暴露显式 update 模式，对准原 `create_note` 返回的精确位置/标识符。省略 update 标识符时，create 模式保持向后兼容。
- Update 模式替换已有笔记正文，并在同一对象上写入所提供的当前属性/frontmatter。不得创建第二个 provider 对象，也不得再追加一份正文副本。
- 毕业工作流——而非底层适配器——读取既往出处并解析新的去重 `graduated_by` 并集。适配器忠实地写入完整的所供列表；既不得发明身份，也不得对照 provider 状态静默合并。
- Provider 标识符是显式的：Obsidian 使用同一 vault 相对笔记路径（`--force` 授权覆盖）；Lark 需要已有的 `node_token`、`obj_token` 与 URL；Notion 需要已有的 page ID。成功 JSON 返回这些相同标识符。
- 替换机制是 provider 原生的：Obsidian 原子替换同一文件；Lark 使用已安装 CLI 的 `docs +update --command overwrite`；Notion PATCH 页面属性，归档当前每个顶层子块，再追加替换子块。替换可能移除仅存在于 provider 的正文内容，因此重新毕业仍须人工确认。
- `create_note` 的回读与 `--dry-run` 义务同样适用于 update 模式。

## `update_index`（按 provider 可选）

- 并非每个 provider 都需要此步骤。当 provider 的容器结构本身已充当索引（Notion：数据库自身的视图/属性）时，没有单独的索引步骤，契约也不要求发明一个。
- 当 provider 支持索引追加步骤时，**必须幂等**：追加前检查索引中是否已有该笔记的条目，若有则跳过追加。用有界、无歧义的定界符匹配（例如 markdown 链接开形式 `[$TITLE](` 或 WikiLink `[[$TITLE]]`）——裸子串检查会产生假阳性（标题为「Lark CLI 踩坑合集」的条目会子串匹配新毕业标题「Lark CLI」），从而跳过追加，使新创建的对象成为孤儿、无法从索引到达——这比本条款要防止的重复行更糟。
- 幂等的索引追加不会把 create 模式变成 upsert。重复的 create 调用仍可能再造一个底层对象；重新毕业必须选择显式 `update_note` 模式并带上已存的原标识符。

## 跨 provider 传输与 API 面原则

从三个 provider 的真实运行中学到；`graduation/` 下各 provider 参考携带 provider 专属后果。

- **`create_note` 并不总是纯写。** 某些 provider 必须在创建前*解析目标*（空间/文件夹/节点），而解析需要读权限。Wiki provider 的「创建节点」隐式读取空间，因此仅有写授权不够。显式建模读依赖；不要假定仅有写范围就能创建。
- **Provider 的 CLI 便利可能比其 API 更严。** 当高层快捷方式附加会拒绝本可有效调用的前置条件（如字面 scope 预检）时，毕业写入优先使用 provider 的原始/原生 API。
- **Provider 的官方 CLI 不自动等于最可靠的传输。** 会拉取远程 spec 解析端点、或忽略 `HTTPS_PROXY` 的 CLI，可能在代理/CI 环境失败，而直接 REST 打同一 API 却可行。在真实环境验证传输；准备好回退到直接 REST（curl），并对不稳定出口（如随机 SSL EOF）做按请求重试。

## 读侧：`query`（文档化能力，非适配器脚本）

消费流程（`consume.md` → Retrieval）需要进入知识库的读路径。与写侧不同，读侧 **不提供适配器脚本**：查询是按任务由消费 Agent 临时组合的，把它们冻进脚本只会固定漏斗形态，而消除不了真正复杂度。本契约标准化的是能力类别、偏好顺序与回退规则。

### 能力类别

Provider 的读侧描述必须说明它支持这四类查询中的哪些，以及用什么：

1. **Structured** — 按 frontmatter/属性过滤（`type`、`contains`、`tags`、`graduated_from` 等）。
2. **Tag** — 枚举标签清单或列出带某标签的笔记。
3. **Fulltext** — 内容搜索，理想情况下限定在知识库容器内。
4. **Graph** — 从命中沿链接/反向链接到相邻笔记。

Provider 不要求四类全支持；`consume.md` 的漏斗使用已有能力并跳过没有的。

### 规则

- **优先使用 provider 原生查询接口，而非原始文件系统 `grep`。** 原生接口查询 provider 的语义索引——frontmatter 与行内标签统一在一次标签查询下，别名解析进反向链接，已保存视图被求值——这些都不是对笔记文件做字面文本 grep 能复现的。原始 grep/直接读取是*回退*，不是默认。
- **回退必须保持显式且可用。** 当原生接口不可用或命中已知不可靠（CLI 缺失、应用未运行、假成功退出码）时，降级为直接文件系统/API 读取，而不是中止消费流程。
- **查询未命中不等于证明不存在。** 无论哪一层，漏斗都以扫描相关（子）INDEX 作为召回安全网收尾——见 `consume.md` → Retrieval。
- **写侧对应：标签纪律。** 标签查询召回依赖毕业时选择的标签。发明新标签前，先查 provider 的标签清单，优先复用而非近义自造（见 `graduation.md` → Flow 中对应步骤）。

### 各 provider 映射

- **Obsidian** — 通过 `obsidian` CLI 覆盖全部四类（CLI 1.12 上原语已确认存在；尚未大规模实操）：结构化 `properties` / `property:read` / `base:query`（Bases 已保存视图，`format=json`）；标签 `tag name=<tag> verbose` / `tags counts`；全文 `search` / `search:context`（`path=` 限定知识文件夹，`format=json`）；图谱 `backlinks` / `links`。审计式扫掠的策展附加：`orphans` / `deadends` / `unresolved`。可靠性注意与写侧已文档化的相同（`rc=0` 假成功、异步 vault 切换、需要应用在运行）→ 回退是在已解析 vault 路径下直接读文件系统。
- **Notion** — 数据库*就是*索引，因此结构化查询是原生的：`POST /v1/databases/{id}/query` 带属性过滤器（传输规则与写侧相同：直接 REST + 重试，固定 `Notion-Version`）。标签只是 Multi-select 属性过滤，不是单独机制。全文 `POST /v1/search` 是工作区级且粗粒度——把结果过滤回 KB 数据库。图谱弱（仅页面提及）。
- **Lark wiki** — 已验证的读路径是树遍历（`wiki nodes list`）加 INDEX 文档拉取（`docs +fetch`）；套件级搜索 API 存在但对流程 **未验证**——在真实环境测过之前不要依赖。

## 横切

- 错误处理：硬失败调用 `die()` 风格辅助（消息到 stderr，`exit 1`）。软/可恢复问题（如回读不匹配、缺少可选依赖）向 stderr 打印 `warn: ...` 并继续。
- macOS Bash 3.2 兼容是每个 bash 适配器的硬要求：不用 `mapfile`/`readarray`，不用关联数组，不假定存在 `timeout`/`gtimeout`。**在 `set -u` 下迭代可能为空的数组需要 `"${ARR[@]:-}"`，而非裸 `"${ARR[@]}"`**——在真实 bash 3.2.57 上已确认：数组零元素时裸形式会抛 `unbound variable`，即使已声明。非 bash 适配器（如 `notion-graduate-batch.py`）按构造豁免 bash 专属规则。
- **适配器脚本之间无共享代码。** 每个脚本都是完整、独立、可自上而下通读的单元——没有 `lib.sh`。重试/预检模式跨 provider 看起来相似，但检查的是真正不同的条件（Lark：OAuth scope 状态机；Notion：网络/SSL 不稳；Obsidian：异步 vault 加载竞态）；共享辅助要么过于通用省不下真正复杂度，要么把 provider 专属分支泄漏回「共享」文件。Project Cairn 对这些脚本的受众（Agent 读共享毕业核心加一份所选 provider 参考，再端到端调用一个脚本）从单文件自包含中获益多于 DRY。仅当加入第 4 个 provider 且真正稳定的公共辅助显现时再重新审视。
