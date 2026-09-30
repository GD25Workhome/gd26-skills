# frontmatter

定义项目侧与知识库侧的 frontmatter。

## 项目知识专题文档 — 推荐字段

- `type`
- `status`
- `summary`
- `tags`
- `contains`
- `created`
- `updated`
- `contributors`（有条件出现；存在可识别的人类贡献者时添加）
- `graduated_by`（毕业时添加，不预先盖章）
- `graduated_to`（毕业时添加，不预先盖章）
- `graduated_at`（毕业时添加，不预先盖章）
- `graduation_status`（可选；仅在做过毕业就绪判断后添加）
- `related`
- `authoring_mode`

## 知识库笔记 — 必填字段

- `type`
- `summary`
- `contains`
- `tags`
- `graduated_from`
- `graduated_by`（每次新毕业必填）
- `authoring_mode`

存在可识别的人类贡献者时有条件出现：

- `contributors`

每次新毕业，知识库侧都要求有 `graduated_from` 与非空的 `graduated_by`。项目侧 `graduated_to` 推荐但非强制。适用范围、版本/时间上下文、最近验证时间、来源回链若未提升到 frontmatter，应出现在笔记正文中。遗留笔记在 audit 策略下仍有效：团队专题被触碰时回填 `contributors`，重新毕业时回填 `graduated_by`。

### `graduated_from` 形态

`graduated_from` 是 **`{project, path}` 条目列表**，不是标量——已对照毕业进 Obsidian 知识库的笔记验证，其中多篇有超过一条（从多个源专题/文件蒸馏而来）：

```yaml
graduated_from:
  - project: "Project Cairn"
    path: "/absolute/or/vault-relative/source/path.md"
  - project: "Project Cairn"
    path: "/another/source/file.md"
```

每个写入结构化 frontmatter 的 provider（相对把 frontmatter 留给调用方手写嵌入，例如 Lark）都应使用此形态，而非单个字符串。`scripts/obsidian-graduate.sh` 由可重复的 `--graduated-from "<project>|<path>"` 标志构建它。

对 `path`，优先使用 **源项目相对** 路径（如 `cairn/<topic>.md`）：`project` 字段已说明是哪个项目，相对路径在换机与仓库搬迁后仍存活。绝对路径出现在较旧的生产笔记中，仍可接受；新毕业应写项目相对路径。

### 人类出处形态

两个字段都是人类可读名称列表，即使只有一人时也是。优先使用实际暴露的平台显示名，但不要求全局稳定身份：

```yaml
contributors:
  - Alice
graduated_by:
  - Alice
```

- `contributors` 记录实质参与形成该知识的人。不要用于每个与会者、Markdown 打字员、所有权，或 AI 写作模式。
- `graduated_by` 记录显式确认毕业的人类，而非执行写入的 Agent、适配器或 API 客户端。
- 不要预先为空字段盖章。存在可识别人类贡献者时添加 `contributors`；仅在发生毕业时添加 `graduated_by`。
- 重新毕业时，将当前确认人并入 `graduated_by`，不重复已有身份。`cairn/LOG.md` 仍是带日期的事件账本。
- 在需要出处字段时惰性解析名称：显式用户输入 -> 实际暴露的平台显示名 -> 无歧义的惯用称呼 -> 即时提问。不要挪到 `cairn init`，也不要静默使用 OS、路径、Git、仓库所有者或记忆推导的名称。

## 枚举值

- `type`（与 OKF 对齐的概念对象种类）：
  - 当前产出：`project_topic`（项目侧），`knowledge_note`（知识库侧）。
  - 前瞻性，不由 init/maintenance 自动创建：`reference`、`playbook`、`decision_record`、`log_index`。
- `status`：`active`、`superseded`、`archived`、`needs_review`。
- `contains`（受控，多值）：任意 `decision`、`experience`、`lesson`、`procedure`、`reference`、`open_question`。
- `graduation_status`（可选）：`candidate`、`deferred`、`not_applicable`。

## 字段语义

- `type` 回答「这是哪种知识对象？」——单一概念对象种类。
- `contains` 回答「里面有哪些知识成分？」——多值内容构成。单篇知识专题文档可同时持有经验与教训，因此永远不要用 `type: experience/lesson`；用 `contains` 表示混合内容。
- `tags` 回答「应按哪些主题、领域、项目或技术被找到？」——开放、多值的检索标签；它们不驱动规则决策。
- `graduation_status` 在已做出显式毕业就绪判断时记录之。不要预先盖章 `not_reviewed`；缺席表示尚未记录毕业判断。专题显得可复用且可确认时用 `candidate`；可能在更多验证或抽象后变得可复用时用 `deferred`；已审阅且不应作为笔记毕业时用 `not_applicable`。理由重要时写在正文中。
- `authoring_mode`：`ai_generated` | `human_written` | `ai_assisted`。记录笔记如何写成，以便在知识库中区分 AI 生成、人类撰写与人机协作笔记。它不编码信任、审阅状态或所有权。它与两个人类出处字段 `contributors` 和 `graduated_by` 正交。Project Cairn 自动生成的知识专题文档默认为 `ai_generated`。
