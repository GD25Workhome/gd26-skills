# upgrade

将已初始化的项目实例拉齐到当前技能规范，或度量其漂移程度。`cairn init` 把当日规范冻结进项目（AGENTS.md 措辞、配置形态、LOG 约定）；技能持续演进，冻结副本不会自动更新。本参考既是检测清单，也是弥合差距的执行手册。

**Current spec date: 2026-09-04**

## 「升级」的两层——分开看

1. **技能副本**（安装在 agent 技能目录下的文件）。此处不在范围：技能仅为文档、无自更新，用户按当初安装方式刷新（重跑安装命令 / git pull）。
2. **项目实例**（项目的 `AGENTS.md`、`.cairn/config.yaml`、`cairn/LOG.md` 约定，以及已毕业的知识库笔记）。本参考升级的是这一层。

这是**拉取模型**：上游变更从不主动通知任何人。漂移被容忍，直到 audit 或显式升级请求将其曝光。实例旧于其技能副本是危险状态（agent 按新参考对旧实例文件行动）；实例与旧技能副本一致则内部自洽，在副本刷新前无害。

## 执行升级

1. 从项目的 `.cairn/config.yaml` 读取 `skill_spec_date`。
   - **缺字段** → 视为早于所有条目：跑下方完整变更日志。
2. 按**新于该日期**的变更日志条目，从旧到新逐条处理。对每条：运行 **Detect**；若已漂移，按其安全级别应用 **Fix**——`auto` 可直接修复（展示 diff），`confirm` 提出方案并等待用户。
3. 全部条目处理完毕后，将 `.cairn/config.yaml` 中的 `skill_spec_date` 盖章为上方当前规范日期（若无字段则添加）。
4. 将升级记为一条 `cairn/LOG.md` 条目——检查了什么、修了什么、拒绝了什么——与 audit 运行记自身相同。

`cairn audit` 将步骤 1–2 作为漂移检查运行并报告发现、不修复（见 `audit.md`）；用户请求的升级跑全部四步。

## 维护本变更日志（技能作者纪律）

每项规范变更落地前须回答一个问题：**它是否影响已初始化实例或已毕业笔记？** 若是，在同一提交中于此添加条目，并将当前规范日期 bump 为变更日期。使现有实例仍有效的技能内部编辑（措辞、路由、新 provider 适配）不进条目。漏记意味着该漂移无处可检——本纪律是整套机制的单点故障。

条目格式——四个固定字段：

- **Affects**：影响哪一实例面（`AGENTS.md` / `config` / `LOG` / `knowledge-base notes` / `user environment`）。
- **Detect**：一条具体、可执行的检查。
- **Fix**：修复动作。
- **Safety**：`auto`（机械，展示 diff 后应用）或 `confirm`（改变含义、目标，或项目外任何事物——先问）。

## 变更日志（从旧到新）

### 2026-07-01 — LOG 条目逆时序，最新在顶

- **Affects**：`cairn/LOG.md`（+ 其导言行）。
- **Detect**：自上而下比较条目日期；升序（最旧在前）或新条目追加在底部 = 已漂移。同时检查导言行是否声明最新在顶。
- **Fix**：将条目重排为最新优先并修正导言行。用条目内日期作为排序依据；同日多条时，仅当有日内顺序证据（例如一条引用另一条）才保留相对顺序，否则保持文件内该日原有顺序。
- **Safety**：日期明确时为 `auto`；排序证据薄弱时为 `confirm`。

### 2026-07-03 — provider 的 `target`/`index` 为容器相对路径（无 vault/根前缀）

- **Affects**：`config`（`graduation.target` / `graduation.index`，单 provider 键或 `providers:` 列表条目）。
- **Detect**：对文件系统型 provider（Obsidian），`target`/`index` 为绝对路径或以 vault 自身名称开头（双重嵌套，如 vault `MyVault` 上的 `MyVault/30_kb/...`）= 已漂移。
- **Fix**：改写为 vault 相对（如 `30_kb/INDEX.md`）。潜伏至首次毕业才暴露，届时写入错误位置——在任何毕业前修复。
- **Safety**：`confirm`（改变未来毕业写入位置）。

### 2026-07-03 — 消费反射使用语义测试，而非触发词

- **Affects**：`AGENTS.md`（「Knowledge base consumption reflex」要点）。
- **Detect**：该要点缺少毕业对称语义测试——「before work whose reusable kernel (any conclusion it **produces or depends on**) would be **graduation-worthy**, check the index first」——例如仍列触发关键词，或无条件地说「always check」。
- **Fix**：用当前模板措辞（`assets/templates/AGENTS.md`）替换该要点，按项目的 `language` 翻译，保留项目自身的 `{{KNOWLEDGE_INDEX}}` 替换。
- **Safety**：`auto`（机械换为模板文本；展示 diff）。

### 2026-07-03 — 存在用户级分级默认值（`~/.config/cairn/config.yaml`）

- **Affects**：`user environment`（项目实例内部无影响）。
- **Detect**：`~/.config/cairn/config.yaml` 不存在，但用户至少有一个已初始化项目。
- **Fix**：提议从本项目已解析配置创建该文件（形态：`assets/templates/user-config.yaml`），以便后续 init 一键复用默认值。拒绝亦可；本条目是提议，不是修复。
- **Safety**：`confirm`（写入项目外）。

### 2026-07-03 — `graduated_from` 路径为项目相对

- **Affects**：`knowledge-base notes`（已配置 provider 中已毕业的笔记）。
- **Detect**：任一 `graduated_from` 条目的 `path` 为绝对路径（前导 `/` 或机器专属前缀）= 已漂移。
- **Fix**：将 `path` 值改写为项目相对。若该笔记已有待办重新毕业则并入其中；否则直接修复。
- **Safety**：`confirm`（编辑知识库内容）。

### 2026-07-15 — `.cairn/config.yaml` 引入 `skill_spec_date` 字段

- **Affects**：`config`。
- **Detect**：字段缺失。
- **Fix**：跑上方完整变更日志（缺字段 = 早于一切），然后用当前规范日期盖章该字段。本条目是字段存在前初始化的每个实例的冷启动路径。
- **Safety**：`auto`（盖章本身；上方各修复保持各自级别）。

### 2026-07-16 — 人类出处与可选原话引述

- **Affects**：`project topic notes`、`knowledge-base notes`、已存毕业标识符，以及 Notion provider 数据库 schema。
- **Detect**：在 2026-07-16 或之后创建或实质更新的专题有可安全识别的人类贡献者但无 `contributors`；在 2026-07-16 或之后的毕业任一侧缺少非空 `graduated_by`；或 Notion 预检报告缺少/类型错误的 `contributors` / `graduated_by` Multi-select 属性。未触碰的遗留笔记缺字段不算漂移。另标出空的、无归属的，或因未解决披露风险而毕业后仅一侧有意保留的原话引述节。对曾重新毕业的专题，在其 provider 容器中搜索同标题重复对象或重复正文；若存在重复，或项目未保留 update 模式所需的原 provider 标识符，则先前仅创建流程已漂移。
- **Fix**：在身份可确认时添加并去重两个身份列表；下次毕业前添加或纠正两个 Notion Multi-select 属性；遗留笔记仅在被触碰或重新毕业时回填。经人工确认后，在项目与知识库两侧移除、显式脱敏，或以带标签的场景摘要替换风险原文。为未来显式 update 模式保留一个规范 provider 对象及其标识符；仅在人工审阅后提议归档/删除意外重复。已有规范笔记就地更新：Obsidian 同路径 + `--force`，飞书已存节点/文档标识符，Notion 已存 page ID。
- **Safety**：在项目内添加已确认身份并去重列表值为 `auto`；更改 provider schema、外部知识库笔记、归属、引述或脱敏为 `confirm`。

### 2026-08-05 — 完成回复须经 Cairn 检查点

- **Affects**：`AGENTS.md` 完成行为。
- **Detect**：项目 `AGENTS.md` 缺少要求在任何完成性声明前做 Cairn 检查点的规则——包括但不限于工作已完成或已实现、已定稿、已更新、已同步、已验证或测试通过；问题已修复或已解决；交付物已可用；声明工作已结束；以及语义等价措辞——或缺少只读例外与条件性 LOG/专题/ROADMAP 行为。
- **Fix**：加入当前 `assets/templates/AGENTS.md` 的「完工回复闸门」，按项目语言翻译（模板默认中文；非中文再译）；保持实例已解析的项目/provider 值不变。
- **Safety**：`confirm`（改变 agent 可结束回复的时机，并可能导致写入项目知识文件）。

### 2026-08-07 — `git_policy` 按项目决策，并通过 `.gitignore` 强制执行

- **Affects**：`user environment`（`~/.config/cairn/config.yaml`）、`config`，以及项目的 `.gitignore`。
- **Detect**：两项独立检查。① `~/.config/cairn/config.yaml` 在 `defaults` 下有 `git_policy`（或 `reference_git_policy`）= 已漂移：该字段曾是分级默认值，保存后初始化的任何项目可能继承了从未被询问的答案。② 项目 `.cairn/config.yaml` 写着 `git_policy: ignore` 或 `private_sync`，但项目 `.gitignore` 无覆盖 `knowledge_dir` 的规则 = 已漂移：声明的策略无效，`git add .` 仍会提交知识目录。（对 `reference_git_policy` 与 `<knowledge_dir>/Reference/` 做同样检查。）
- **Fix**：① 从用户级 `defaults` 块删除 `git_policy` / `reference_git_policy` 键；其余文件不动。② 就本仓库实际需求问用户一次——不要假定已记录值曾是真实回答——然后补上缺失的 `.gitignore` 规则，或将 `.cairn/config.yaml` 中的 `git_policy` 改为与现实一致。静默继承取值的实例没有其他纠正点。
- **Safety**：`confirm`（触及项目外文件，并改变未来提交内容）。

### 2026-09-04 — `git_policy: ignore` 覆盖整个 Cairn 足迹，并使用中性注释

- **Affects**：项目的 `.gitignore`（并因此影响仓库远程已携带的内容）。
- **Detect**：对 `.cairn/config.yaml` 写着 `git_policy: ignore` 或 `private_sync` 的项目，运行 `git ls-files -- .cairn AGENTS.md CLAUDE.md '<knowledge_dir>'`。任一路径被列出 = 已漂移：策略说 Cairn 不进本仓库，这些却已提交——若远程公开，则已发布。另计漂移：忽略块注释点名 `cairn init`、策略或 Cairn 本身。
- **Fix**：将忽略块扩展为覆盖 `<knowledge_dir>/`、`.cairn/`，以及 Cairn 撰写的 `AGENTS.md` / `CLAUDE.md`，并将块注释替换为中性的 `# Local working files, not part of the project`。忽略规则对 git 已跟踪路径无效：用 `git rm --cached <path>` 作为补救列出这些路径，由用户决定——取消跟踪须其批准；若仓库已推送，须直说从 HEAD 删除不会从历史或任何已镜像处删除。
- **Safety**：`confirm`（改变未来提交内容，并可能意味着接受或改写已发布历史）。
