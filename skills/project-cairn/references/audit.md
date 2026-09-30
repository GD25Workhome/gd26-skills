# audit

对项目知识层的手动或 agent 请求检查。Audit 是日常工作中漏记记录的安全网。

## 检查项

- 过长的 LOG 条目，或含本应放在知识专题文档中的结论。
- 缺少有用 frontmatter 的知识专题文档。
- 对反复出现的决策或已解决问题缺少专题。
- 专题与旧 LOG 条目之间的矛盾（专题优先；标出过时的 LOG 条目）。
- 混入 `cairn/`、应移回代码树的工程资产。
- `Cited.md` 中的断链或过时指针。
- 尚未审阅的毕业候选。
- 暂缓对接 provider 的项目（`.cairn/config.yaml` 中 `graduation.provider: none`）持有已确认的毕业候选——标出连接知识库仍待办（`graduation.md` → Deferred provider）。暂缓本身是合法状态，不是缺陷；仅在确有候选在等待时才标出。
- 标记为 `graduation_status: candidate` 但尚未毕业或确认的项目专题。
- 标记为 `graduation_status: deferred` 或 `graduation_status: not_applicable`、但正文上下文不足以解释该判断的项目专题。
- 知识库笔记缺少 `graduated_from` 来源。
- 新毕业在项目侧或知识库侧缺少非空的 `graduated_by` 列表。
- 被触碰的团队专题，其可安全识别的实质人类贡献者未出现在 `contributors` 中。
- 空的 Origin quote 标题，或缺少发言人/核定角色、日期与语境归属的直接引述。
- 潜在风险的引述内容。仅作为提示供人工审阅；永不自动给出安全裁决。
- 不要仅因缺少 `contributors` 或 `graduated_by` 而标出未触碰的遗留笔记：它们仍有效，仅在被触碰或重新毕业时回填。
- 已毕业但缺少推荐回指（`graduated_to` / `graduated_at`）的项目专题。
- frontmatter `updated` 日期新于 `graduated_at` 的项目专题——对应知识库笔记可能已过时；建议重新毕业（见 `graduation.md` → Re-graduation），不要自动触发。
- 已关闭或放弃的探索分支，其有价值的 `cairn/` 知识从未被抢救（应触发分支关闭复盘，或 LOG / 专题 / 毕业候选跟进）。
- 相对当前技能规范的实例漂移：从 `.cairn/config.yaml` 读取 `skill_spec_date`，对每一条新于此日期的 `references/upgrade.md` 变更日志条目运行 Detect 步骤（缺字段 = 跑完整变更日志）。用各条目的修复指引与安全级别报告漂移项；修复属于 `upgrade.md` 的升级流程，不是 audit 的职责。
- 工作笔记文件名合规：`cairn/` 外、不在固定名列表上的任何 md，须遵守 `AGENTS.md` → 工作笔记命名规则——slug 语言与 `.cairn/config.yaml` 中的 `cairn.language` 一致；文件名带 `save-md-artifact` 产出的 `YYMMDD-NN-` 前缀；无手动 `0-` / `1-` 前缀、裸 `note.md` 或仅阶段名；阶段/期次编号在 frontmatter `stage`，不在文件名。对每处违规标出当前实际名称与建议重命名目标。

## 行为

建议修复。未经用户确认，不要静默改写大段内容。

本次 audit 运行本身应得一条 `cairn/LOG.md` 条目——简短摘要检查了什么、发现了什么，外加指向发现结果的指针，像其他条目一样加在顶部。追加此记录不是「改写内容」；禁止改写规则保护已有材料，不保护 audit 发生这一事实的日志。
