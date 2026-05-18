---
name: leetcode-1-download-content
description: >-
  从 LeetCode 中国站（leetcode.cn）抓取原题正文与示例图，生成离线 Markdown，
  并维护 LeetCode/leetCode题目.md 中「题目列表」索引（保留备注子项与其它章节）。
  题号 4 位补零，文件名为 LeetCode题号-中文题名.md，图片落 imgs/。
  在用户要求抓取/下载 LeetCode 原题、更新题目目录索引、或维护 leetCode题目.md 时启用。
---

# LeetCode 原题抓取（download-content）

## 何时启用

- 用户给出 **题号**（如 `102`、`310`）或 **titleSlug**，要求抓取/下载/保存 **原题** Markdown。
- 用户提到 `LeetCode` 目录、`imgs`、原题归档，且任务目标是 **题目描述**（不是题解）。
- 用户要求 **更新/同步/维护** `leetCode题目.md` 或「题目列表」索引（可单独执行，不必同时抓题）。

**不覆盖**：题解撰写、代码实现——另有技能处理。

## 目标产物（必须遵守）

| 项 | 规则 |
|----|------|
| 根路径 | 当前 **项目根目录** 下的 `LeetCode/`（用户指定其它根目录时从其指定） |
| 题目目录 | `LeetCode/LeetCode{NNNN}/`，`NNNN` 为 **4 位补零** 题号（`102` → `0102`） |
| Markdown 文件 | `LeetCode{NNNN}-{中文题名}.md`，与目录同级 |
| 图片目录 | `LeetCode/LeetCode{NNNN}/imgs/`，Markdown 内用相对路径 `imgs/xxx.jpg` |
| 内容语言 | 优先 `translatedContent`（中文）；无译文再退回英文 `content` |
| 忠实度 | 保留原题 **题目描述、示例（含图）、数据范围/提示**；不删减官方约束；可略去 HTML 噪声（`&nbsp;` 等） |

### Markdown 结构模板

与仓库范例对齐（参见 [examples.md](examples.md)）：

```markdown
# {题号}. {中文标题}

**难度：** {简单|中等|困难}

## 题目描述

{题干段落，保留行内 code/加粗}

## 示例

### 示例 1

![示例 1 示意图](imgs/xxx.jpg)
- **输入：** `...`
- **输出：** `...`
- **解释：** ...（若有）

### 示例 2
...

## 提示（数据范围）

- {约束条目}
```

**难度映射**：`Easy`→简单，`Medium`→中等，`Hard`→困难。

## 子能力：维护题目索引

索引文件路径：**`LeetCode/leetCode题目.md`**（相对于项目根）。只维护其中的 **`## 题目列表`**；`## BFS相关扩展` 等其它章节 **原样保留**。

### 题目列表条目格式

```markdown
- [{题号}. {中文标题}](LeetCode{4位题号}/LeetCode{4位题号}-{中文标题}.md)
  - {可选备注，2 空格缩进}
```

范例（含备注子项）：

```markdown
- [542. 01矩阵](./LeetCode0542/LeetCode0542-01矩阵.md)
  - 常规解法为BFS，不难实现；
  - 但还有动态规划的解法，理解需要门槛
```

### 维护规则（必须遵守）

| 规则 | 说明 |
|------|------|
| 扫描范围 | 各 `LeetCode/LeetCode{NNNN}/` 下 `LeetCode{NNNN}-*.md`，**排除** `题解-` 开头文件 |
| 标题来源 | 优先原题 Markdown 首行 `# 102. 标题`；否则用文件名中的标题 |
| 链接 | 相对 `leetCode题目.md`，推荐 `LeetCode0102/LeetCode0102-xxx.md`（脚本会去掉 `./`） |
| 顺序 | **默认**保持索引中已有顺序；**新题**追加在列表末尾 |
| 备注 | 同一题号下已有 `  - ` 备注 **不得删除** |
| 重排 | 仅当用户要求或传入 `--sort` / `--sort-index` 时按题号升序重排 |
| 其它章节 | `## 题目列表` 之后的内容（待解题、TODO 等）**禁止改写** |

### 何时自动更新索引

- 使用 `download_leetcode_problem.py` 抓题成功后 **默认**更新索引。
- 仅维护目录、不抓题时，单独运行 `update_leetcode_index.py`。

```bash
python3 skills/leetcode-1-download-content/scripts/update_leetcode_index.py \
  --output-dir PROJECT_ROOT
```

可选：`--sort` 按题号排序；`--dry-run` 预览不写文件。抓题时可用 `--no-index` 跳过、`--sort-index` 排序。

## 推荐工作流

### 1. 确认题号与输出根目录

- 题号：用户给的数字或 slug；数字题号走列表 API 解析 slug。
- 输出根：默认 **当前工作区项目根**（含 `LeetCode/` 或即将创建该目录的仓库，如 `gd26-algorithm`）。

### 2. 优先执行脚本（稳定、可重复）

在技能目录下安装依赖并运行（将 `PROJECT_ROOT` 换成实际项目根）：

```bash
python3 -m pip install -r skills/leetcode-1-download-content/scripts/requirements.txt

python3 skills/leetcode-1-download-content/scripts/download_leetcode_problem.py \
  102 \
  --output-dir PROJECT_ROOT
```

参数说明：

- 第一个参数：题号（`102`）或 slug（`binary-tree-level-order-traversal`）。
- `--output-dir`：写入 `PROJECT_ROOT/LeetCode/...` 的目录。
- `--overwrite`：覆盖已存在的同名 Markdown（**不**自动删 imgs 内旧图）。
- `--no-index`：不更新 `leetCode题目.md`。
- `--sort-index`：更新索引时按题号升序重排。

脚本数据源：`leetcode.cn` GraphQL + 题目列表 API；自动下载 `<img src>` 到 `imgs/`；**默认**同步题目列表索引。

### 2b. 仅维护索引（不抓题）

```bash
python3 skills/leetcode-1-download-content/scripts/update_leetcode_index.py \
  --output-dir PROJECT_ROOT
```

适用于：手工新增原题 md 后补索引、批量校正链接/标题、合并磁盘与索引差异。

### 3. 对照范例做人工校对（必要时）

脚本输出应已接近范例。生成后 **打开 Markdown 与官方页面对照**，按需微调：

- 漏掉的独立文本行（如「树的高度是指……」）补入 **题目描述**。
- 示例图 alt 文案、示例下的补充说明（树结构简述等）可按 [examples.md](examples.md) 风格 **增补**，但勿改写官方输入/输出/约束数值。
- 上标/下标（如 `2 * 10^4`）按官网显示修正。

### 4. 无脚本时的备用抓取

仅在无法运行 Python 时使用：

1. `POST https://leetcode.cn/graphql/`，查询 `question(titleSlug: $slug) { translatedTitle translatedContent difficulty questionFrontendId }`。
2. 题号 → slug：`GET https://leetcode.cn/api/problems/all/`，按 `frontend_question_id` 匹配。
3. 解析 HTML：题干 / `示例 N` / `提示` / `<ul>` 约束；**每个** `<img src>` 下载到 `imgs/`，扩展名取自 URL。
4. 按上文目录与命名写入文件。

## 完成检查清单

复制并逐项确认：

```
- [ ] 路径：LeetCode/LeetCode{4位题号}/LeetCode{4位题号}-{中文题}.md
- [ ] 题号标题行：# {题号}. {中文标题}
- [ ] 含难度、题目描述、示例、提示（数据范围）
- [ ] 原题图片均在 imgs/，Markdown 为相对路径 imgs/...
- [ ] 输入/输出与官网一致（含反引号包裹的代码片段）
- [ ] 未把题解、思路、代码实现写入本文件
- [ ] leetCode题目.md 的「题目列表」已含本题链接（除非使用 --no-index）
- [ ] 原有备注子项与其它 ## 章节未被误删
```

## 参考

- 范例目录（只读对照）：`gd26-algorithm/LeetCode/` 下 `LeetCode0102`、`LeetCode0310` 等。
- 范例说明：[examples.md](examples.md)
- 接口与脚本细节：[reference.md](reference.md)
