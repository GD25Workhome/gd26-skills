# 技术参考

## 路径与命名

```
LeetCode/
└── LeetCode{NNNN}/
    ├── LeetCode{NNNN}-{中文题名}.md      # 原题（leetcode-1）
    ├── 题解-LeetCode{NNNN}-{算法标签}.md  # 本技能产出
    └── imgs/                              # 原题图；题解示意图可选放此或 imgs/solution/
```

| 函数 | 示例 |
|------|------|
| `pad_id(102)` | `0102` |
| `pad_id(1162)` | `1162` |
| 题解文件名 | `题解-LeetCode0102-广度优先.md` |

## 文首「总览」链接

相对于 `LeetCode/LeetCode{NNNN}/题解-*.md`：

| 算法标签 | 链接 |
|----------|------|
| 广度优先 | `../../算法总结文字/BFS/BFS算法总结.md` |
| 深度优先 | `../../算法总结文字/DFS/DFS算法总结.md` |
| 动态规划 | `../../算法总结文字/DP/DP思想总结.md` |

## 数学公式（Markdown 渲染）

| 类型 | 写法 | 示例 |
|------|------|------|
| 行内 | `$...$` | 队列长度 $s_i$，复杂度 $O(mn)$ |
| 块级 | `$$...$$` 独立成行 | 状态转移方程 |
| 多行对齐 | `aligned` 环境 | 见 542 题解中的 `cases` / `min` |

截图常见符号对应：

| 截图 | LaTeX |
|------|-------|
| si, s_i | `$s_i$` |
| min(h) | `$\min(h)$` |
| O(mn) | `$O(mn)$` |
| 分数/根号 | `\frac{}{}`、`\sqrt{}` |

避免使用仅 HTML 的 `<sub>`；统一 LaTeX。

## 代码块

- 语言标识：`java`
- 类名常用 `Solution`，与 LeetCode 一致
- 长代码可省略无关 `import`，但保持方法完整可读

## 网页题解抓取要点（leetcode.cn）

典型 URL：

```
https://leetcode.cn/problems/{slug}/solutions/...
https://leetcode.cn/problems/{slug}/description/
```

处理顺序建议：

1. 定位正文容器（题解文章主体，非侧边栏）。
2. 提取标题、段落、列表、代码 `<pre>`。
3. 将 MathJax/KaTeX 节点转为 LaTeX（若无 API，按渲染结果手排）。
4. 图片 `src` 下载到本题 `imgs/`，文件名保持可读。
5. 记录 canonical 链接于文末（可选），如 1162 范例中的官方社区题解 URL。

## 截图识别要点

1. 先 **通读全图** 再分节写入，避免段落顺序错乱。
2. 代码块单独抽出，不要与正文混排。
3. 红字/高亮往往是 **关键结论**，写入「思路和算法」段首或加粗。
4. 多图按阅读顺序合并为一份题解，不要一图一节空标题。

## 本地代码引用（gd26-algorithm 惯例）

若仓库存在 `java_test`：

```text
java_test/src/main/java/com/lance/leetcode/test{NNNN}/CodeForLeetCode{NNNN}_{Tag}.java
```

文首「姊妹写法」或文末「本地实现见」可指向该路径（相对项目根）。

## 错误处理

| 情况 | 处理 |
|------|------|
| 无原题 md | 提示先用 leetcode-1 抓题，或请用户确认题号/标题 |
| 截图模糊 | 标「待确认」，列出无法辨认的公式/句子 |
| 同标签题解已存在 | 询问覆盖或换标签（如「动态规划-优化」） |
| 无法判断算法 | 询问用户文件名中的 `{算法标签}` |
