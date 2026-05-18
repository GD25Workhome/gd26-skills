# 技术参考

## GraphQL（leetcode.cn）

```http
POST https://leetcode.cn/graphql/
Content-Type: application/json
```

```graphql
query questionDetail($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    titleSlug
    translatedTitle
    translatedContent
    content
    difficulty
  }
}
```

- 中文正文：`translatedContent`（HTML）
- 无译文时：使用 `content`

## 题号 → titleSlug

```http
GET https://leetcode.cn/api/problems/all/
```

在 `stat_status_pairs[].stat` 中匹配 `frontend_question_id`，读取 `question__title_slug`。

## 图片

- 来源：题干/示例 HTML 中的 `<img src="https://...">`
- 保存：`LeetCode/LeetCode{NNNN}/imgs/{原文件名或 imageN.ext}`
- Markdown：`![说明](imgs/文件名)`，使用 **相对路径**

## 题目索引（leetCode题目.md）

| 项 | 说明 |
|----|------|
| 路径 | `LeetCode/leetCode题目.md` |
| 维护范围 | 仅 `## 题目列表` |
| 保留 | 每条下的 `  - ` 备注；`## 题目列表` 之后的所有章节 |
| 条目格式 | `- [{题号}. {标题}](LeetCode{NNNN}/LeetCode{NNNN}-{标题}.md)` |

实现逻辑见 `scripts/leetcode_index.py`（解析 / 扫描磁盘 / 合并）。

## 脚本

| 文件 | 作用 |
|------|------|
| `scripts/download_leetcode_problem.py` | 拉取题目、下载图片、写 Markdown；**默认**更新索引 |
| `scripts/update_leetcode_index.py` | 仅维护 `leetCode题目.md` 题目列表 |
| `scripts/leetcode_index.py` | 索引解析与合并库 |
| `scripts/requirements.txt` | `beautifulsoup4` |

```bash
# 仅同步索引
python3 scripts/update_leetcode_index.py --output-dir PROJECT_ROOT
python3 scripts/update_leetcode_index.py --output-dir PROJECT_ROOT --sort
```

依赖安装（在正确 Python/conda 环境中执行）：

```bash
pip install -r scripts/requirements.txt
```

## 登录与限制

- 公开题目 **无需登录** 即可通过上述接口获取。
- 若遇频率限制或空正文，间隔重试；仍失败则提示用户检查网络或稍后再试。
- 会员专享题若接口无正文，如实告知用户，勿编造题干。
