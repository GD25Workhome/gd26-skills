# graduation

经人工确认，将已验证的项目知识提升到外部知识库。单向：项目 → 知识库。Skill 不得静默毕业知识。

## 候选标准

毕业候选必须满足：

- 已在项目中验证，而非仅凭猜测。
- 可在当前项目之外复用。
- 已从本地实现细节中抽象出来。
- 本身不是工程资产（资产永不毕业；仅关于它们的知识可毕业）。
- 可安全迁入目标知识库。
- 可通过 `graduated_from` 追溯。

## 暂缓对接 provider（首次毕业时再连接）

`.cairn/config.yaml` 中 `graduation.provider: none` 表示项目在 init 时有意推迟连接知识库（见 `init.md` → Deferred graduation provider）。候选检测与人工确认（流程步骤 1–3）照常工作——仅 provider 写入被阻塞。当已确认的候选准备好毕业时：

1. 现在收集 provider 决策——init 决策 #3–#4，分级默认值照常生效（用户级 `~/.config/cairn/config.yaml` 可一键复用）。
2. 运行所选 provider 的预检（`init.md` → Tool-backed provider preflight），直到其报告 `ok`。
3. 将结果冻结进 `.cairn/config.yaml`，用标准的单 provider 或多 provider 形态替换 `provider: none` 标记。
4. 更新 `AGENTS.md`：将暂缓渲染（「初始化配置」三行、知识库消费反射要点、知识沉淀规则要点）按 `init.md` 恢复为标准已连接形态。
5. 继续下方正常流程；把「已连接 provider X」折入本次毕业自己的 `cairn/LOG.md` 条目（若随后中止毕业，也可为连接单独记一条）。

若用户仍拒绝连接 provider，则停止——没有 provider 无法继续毕业。候选保持已记录状态（可选 `graduation_status: candidate`），audit 会持续标出。

## 流程

1. 提出候选（Skill 可检测；audit 是兜底）。
2. 用户在任何写入或准备之前确认。
3. 若某项目专题已显式做过判断，可选择在项目专题笔记上记录 `graduation_status`：`candidate`、`deferred` 或 `not_applicable`。不要默认给每个专题都加此字段。
4. 人工确认之后、provider 写入之前：
   1. 按 `frontmatter.md` 解析确认人身份，并作为 `graduated_by` 同时传给项目侧与知识库侧。
   2. 从多个来源毕业时，合并并去重所有源专题的 `contributors`。
   3. 对照目标受众，重新检查任何原话引述。将安全的引述带入知识库笔记的 **Background**；若发现风险，则两侧一致脱敏，或两侧都省略。
   4. 无引述是合法状态，永远不要为此创建占位小节。
5. 准备带有必填 frontmatter 的知识库笔记（`graduated_from` 与非空的 `graduated_by` 强制；见 `frontmatter.md`），并在项目专题笔记上记录 `graduated_by`。也可选择在该处记录 `graduated_to` / `graduated_at`。选择 `tags` 时，先查 provider 已有的标签清单（Obsidian：`obsidian tags counts`），优先复用已有标签而非自造近义标签——消费时按标签查询的召回依赖这一纪律（见 `provider-interface.md` → Read side）。
6. 将本次毕业本身记为一条 `cairn/LOG.md` 条目——摘要加上指向知识库笔记的指针——与 audit 运行记录自身的方式相同（见 `audit.md` → Behavior）。

## 笔记正文结构

知识库笔记正文必须以 **Background**、然后 **Conclusion** 开头，顺序固定。其后小节不固定——按知识本身需要塑形：

1. **Background**（必填，第一）——知识产生的情境：在解决什么问题、如何被发现或遭遇、为何需要。读者需要起源才能判断该笔记是否适用于自己的场景。
2. **Conclusion**（必填，第二）——核心主张或解法本身。
3. **后续小节**（按需，跟随知识）——主张需要支撑时写证据（推理、已验证案例、对比、反例）；知识偏操作时写实践指南（步骤、安全模式、决策检验）；在有用处写适用范围、边界或不适用情形。

不要把正文以结论开头。快速扫读由 frontmatter 的 `summary`（一行结论）承担，因此正文不必再以结论起笔。常见标题的中文名称固定在 `zh-glossary.md`。

当一段安全的短直接摘录能实质性还原场景时，将其放在 **Background** 内，采用如下可移植 Markdown 形态：

```markdown
### Origin quote

> "Exact excerpt."
>
> — identity, YYYY-MM-DD, short context
```

保留直接措辞，并应用 `maintenance.md` 中的脱敏/场景摘要规则。该小节可选；没有合适引述时，永远不要添加空标题或占位。

## 重新毕业（更新已毕业专题）

项目专题笔记一旦毕业后并非冻结——它仍是项目内本地的当前真相，可随项目推进就地持续更新。「单向」指知识库笔记不会因项目侧编辑而被静默覆盖，而非项目侧来源不能再变。

当已有 `graduated_to` 的专题出现实质性新进展（真实更新，而非错别字修正）时，提议重新毕业：以适配器的显式 update 模式再次走同一毕业流程，对准同一知识库笔记（同一 provider 适配器与已存标识符），将 `graduated_at` 更新为新日期，并将当前确认人并入两侧的 `graduated_by`，不重复已有身份。在调用底层适配器之前完成该并集解析；适配器写入所提供的当前真相，不推断既往身份。在 `cairn/LOG.md` 中保留事件/时间/目标与确认人关联；frontmatter 仍是去重后的身份列表，而非事件历史。这是单向 `graduate` 动作的正常重复，不是新的同步机制——用户仍须在任何写入前确认，与首次毕业相同。在重新毕业发生之前，知识库笔记仍是跨项目当前真相，但可能落后于项目最新本地状态；`cairn audit` 会标出这一点（见 `audit.md`）。

## Provider 适配器约束

每个适配器脚本必须满足 `references/provider-interface.md`。跨 provider 传输与 API 面原则在该处；下方各 provider 参考补充该 provider 的具体后果。

写入机制因 provider 而异；把它们放在各 provider 的 `.cairn/config.yaml` 条目中，不要硬编码进流程。

Provider 机制按 provider 各有一份参考。任何写入前，先读该参考，运行其 Step 0 预检，仅在 `status: ok` 时继续。

| Provider type | Required provider reference | Required Step 0 preflight | Write adapter |
|---|---|---|---|
| `obsidian` | [`graduation/obsidian.md`](graduation/obsidian.md) | `scripts/obsidian-preflight.sh` | `scripts/obsidian-graduate.sh` |
| `lark-wiki` | [`graduation/lark-wiki.md`](graduation/lark-wiki.md) | `scripts/lark-preflight.sh` | `scripts/lark-wiki-graduate.sh` |
| `notion` | [`graduation/notion.md`](graduation/notion.md) | `scripts/notion-preflight.sh` | `scripts/notion-graduate.sh` |

写入适配器列固定各 provider 的主单笔记入口；provider 参考枚举该 provider 的完整脚本集。若配置的 provider 为 `none`，留在上方「暂缓对接 provider」流程，直到选定其一。若 provider 值不受支持、其参考缺失或未读、或具名预检尚未返回 `ok`，则在任何 provider 侧写入前停止并报告错误。缺少预检结果是阻塞状态，不等于允许凭记忆重建 provider 机制；dry-run 不能替代真实写入前的这一关卡。

### Lark / Feishu wiki 适配器（实操示例）

已移至 [`graduation/lark-wiki.md`](graduation/lark-wiki.md)。

### Notion 适配器（实操示例）

已移至 [`graduation/notion.md`](graduation/notion.md)。

### Obsidian 适配器（实操示例）

已移至 [`graduation/obsidian.md`](graduation/obsidian.md)。

## 知识库链接

当目标 provider 支持 wiki 风格链接时，仅在上下文有用时添加链接。不要仅为了把笔记连起来而加通用「Related」列表。

- 当某句或某段依赖、解释、对比或操作化另一知识笔记时，添加 wiki 链接。
- 把链接放在该局部上下文内，并用周围文字说清连接理由。
- 不要仅因两篇笔记共享标签、来自同一项目、或同批毕业而链接。

毕业后，知识库笔记是该专题的跨项目当前真相，不会再从项目回写。项目专题笔记仍是本项目本地上下文中的当前真相（以及知识如何抵达的历史记录）；两层不互相竞争。
