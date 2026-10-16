#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 LeetCode 中国站（leetcode.cn）抓取题目正文与图片，生成约定格式的 Markdown。

用法:
  python download_leetcode_problem.py 102
  python download_leetcode_problem.py minimum-height-trees --output-dir /path/to/project
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.request
from html import unescape
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from leetcode_index import upsert_entry_after_write

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "缺少依赖 beautifulsoup4，请先安装：pip install 'beautifulsoup4>=4.12.0,<5.0.0'"
    ) from exc

GRAPHQL_URL = "https://leetcode.cn/graphql/"
PROBLEMS_ALL_URL = "https://leetcode.cn/api/problems/all/"

DIFFICULTY_ZH = {
    "Easy": "简单",
    "Medium": "中等",
    "Hard": "困难",
}

GRAPHQL_QUERY = """
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
"""


def _http_json(url: str, payload: dict[str, Any] | None = None) -> Any:
    """发送 GET/POST 请求并解析 JSON。"""
    headers = {
        "User-Agent": "gd26-skills-leetcode-download/1.0",
        "Content-Type": "application/json",
    }
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST" if payload else "GET")
    context = ssl.create_default_context()
    try:
        with urllib.request.urlopen(request, context=context, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {err.code} {url}: {body[:500]}") from err


def pad_question_id(raw_id: str) -> str:
    """题号左侧补零至 4 位，用于目录与文件名前缀。"""
    digits = re.sub(r"\D", "", raw_id)
    if not digits:
        raise ValueError(f"无法解析题号: {raw_id}")
    return digits.zfill(4)


def resolve_title_slug(identifier: str) -> tuple[str, str]:
    """
    将题号或 slug 解析为 (frontend_id, title_slug)。
    identifier 为纯数字时走题目列表 API；否则视为 slug。
    """
    identifier = identifier.strip()
    if identifier.isdigit():
        payload = _http_json(PROBLEMS_ALL_URL)
        target = identifier.lstrip("0") or "0"
        for item in payload.get("stat_status_pairs", []):
            stat = item.get("stat", {})
            qid = str(stat.get("frontend_question_id", ""))
            if qid == target or qid == identifier:
                return qid, stat["question__title_slug"]
        raise RuntimeError(f"未在 leetcode.cn 题目列表中找到题号 {identifier}")
    return identifier, identifier


def fetch_question(title_slug: str) -> dict[str, Any]:
    """通过 GraphQL 获取题目详情。"""
    body = _http_json(
        GRAPHQL_URL,
        {"query": GRAPHQL_QUERY, "variables": {"titleSlug": title_slug}},
    )
    if body.get("errors"):
        raise RuntimeError(f"GraphQL 错误: {body['errors']}")
    question = body.get("data", {}).get("question")
    if not question:
        raise RuntimeError(f"未找到题目 slug={title_slug}")
    return question


def _inline_to_md(node: Tag | NavigableString) -> str:
    """将行内节点转为 Markdown（code/strong/em 等）。"""
    if isinstance(node, NavigableString):
        return unescape(str(node))
    if not isinstance(node, Tag):
        return ""
    name = node.name.lower()
    inner = "".join(_inline_to_md(child) for child in node.children)
    if name == "code":
        return f"`{inner.strip()}`"
    if name in {"strong", "b"}:
        return f"**{inner.strip()}**"
    if name in {"em", "i"}:
        return f"*{inner.strip()}*"
    if name == "br":
        return "\n"
    if name == "sub":
        return inner
    if name == "sup":
        return inner
    if name == "a":
        href = node.get("href", "")
        text = inner.strip() or href
        return f"[{text}]({href})" if href else text
    return inner


def _paragraph_to_md(p: Tag) -> str:
    text = "".join(_inline_to_md(child) for child in p.children).strip()
    return re.sub(r"\s+", " ", text)


def _plain_heading(text: str) -> str:
    """去掉 Markdown 加粗标记，便于识别「示例 N」「提示」等标题行。"""
    return re.sub(r"\*+", "", text).strip()


def _collect_until_next_strong(tag: Tag) -> str:
    """读取 strong 标签之后、下一个 strong 之前的文本。"""
    parts: list[str] = []
    for sibling in tag.next_siblings:
        if isinstance(sibling, NavigableString):
            parts.append(str(sibling))
        elif isinstance(sibling, Tag) and sibling.name.lower() in {"strong", "b"}:
            break
        elif isinstance(sibling, Tag):
            parts.append(sibling.get_text())
    return unescape("".join(parts)).strip()


def _pre_to_bullets(pre: Tag) -> list[str]:
    """将 <pre> 中的输入/输出转为 Markdown 列表项（支持行内 <strong> 标签）。"""
    lines: list[str] = []
    strong_tags = pre.find_all(["strong", "b"])
    if strong_tags:
        for tag in strong_tags:
            label = tag.get_text().strip().rstrip("：").rstrip(":")
            value = _collect_until_next_strong(tag)
            if label in {"输入", "Input"}:
                lines.append(f"- **输入：** `{value}`")
            elif label in {"输出", "Output"}:
                lines.append(f"- **输出：** `{value}`")
            elif label in {"解释", "Explanation"}:
                lines.append(f"- **解释：** {value}")
        return lines

    for line in pre.get_text("\n").splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("输入：") or line.startswith("输入:"):
            val = line.split("：", 1)[-1].split(":", 1)[-1].strip()
            lines.append(f"- **输入：** `{val}`")
        elif line.startswith("输出：") or line.startswith("输出:"):
            val = line.split("：", 1)[-1].split(":", 1)[-1].strip()
            lines.append(f"- **输出：** `{val}`")
        elif line.startswith("解释：") or line.startswith("解释:"):
            val = line.split("：", 1)[-1].split(":", 1)[-1].strip()
            lines.append(f"- **解释：** {val}")
        else:
            lines.append(f"- {line}")
    return lines


def _constraints_to_md(ul: Tag) -> list[str]:
    items: list[str] = []
    for li in ul.find_all("li", recursive=False):
        text = "".join(_inline_to_md(child) for child in li.children).strip()
        if text:
            items.append(f"- {text}")
    return items


def _download_image(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "gd26-skills-leetcode-download/1.0"})
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, context=context, timeout=60) as response:
        dest.write_bytes(response.read())


def _image_filename(url: str, index: int) -> str:
    path_name = Path(urlparse(url).path).name
    if path_name and "." in path_name:
        return path_name
    return f"image{index}.jpg"


def html_to_markdown_sections(
    html: str,
    imgs_dir: Path,
    *,
    download_images: bool = True,
) -> tuple[str, list[str], list[str]]:
    """
    将题目 HTML 拆为：题目描述、示例块列表、提示列表。
    同时下载图片到 imgs_dir，返回的示例文本中已替换为相对路径。
    """
    soup = BeautifulSoup(html, "html.parser")
    description_parts: list[str] = []
    examples: list[str] = []
    constraints: list[str] = []

    current_example_title: str | None = None
    current_example_lines: list[str] = []
    image_index = 0
    orphan_inline_parts: list[str] = []

    def flush_orphan_inline() -> None:
        nonlocal orphan_inline_parts
        if not orphan_inline_parts or current_example_title is not None:
            orphan_inline_parts = []
            return
        text = re.sub(r"\s+", " ", "".join(orphan_inline_parts)).strip()
        if text:
            description_parts.append(text)
        orphan_inline_parts = []

    def flush_example() -> None:
        nonlocal current_example_title, current_example_lines
        if current_example_title:
            block = [f"### {current_example_title}", ""]
            block.extend(current_example_lines)
            block.append("")
            examples.append("\n".join(block).rstrip())
        current_example_title = None
        current_example_lines = []

    for element in soup.children:
        if isinstance(element, NavigableString):
            text = unescape(str(element))
            if text.strip() and current_example_title is None:
                orphan_inline_parts.append(text)
            continue
        if not isinstance(element, Tag):
            continue
        name = element.name.lower()

        if name in {"strong", "b", "em", "i", "code", "sub", "sup", "a"} and current_example_title is None:
            orphan_inline_parts.append(_inline_to_md(element))
            continue

        flush_orphan_inline()

        if name == "p":
            text = _paragraph_to_md(element)
            if not text or text == "\xa0":
                continue
            plain = _plain_heading(text)
            example_match = re.match(r"^(示例\s*\d+|Example\s*\d+)\s*[:：]?\s*$", plain, re.I)
            if example_match:
                flush_example()
                num = re.search(r"\d+", example_match.group(1))
                n = num.group(0) if num else "1"
                current_example_title = f"示例 {n}"
                continue
            if re.match(r"^提示\s*[:：]?$", plain) or re.match(r"^Constraints\s*[:：]?$", plain, re.I):
                flush_example()
                continue
            if current_example_title is None:
                description_parts.append(text)
            else:
                current_example_lines.append(text)

        elif name == "img" and current_example_title is not None:
            src = element.get("src", "").strip()
            if not src:
                continue
            image_index += 1
            filename = _image_filename(src, image_index)
            rel = f"imgs/{filename}"
            alt = (element.get("alt") or "").strip() or f"{current_example_title} 示意图"
            if download_images:
                _download_image(src, imgs_dir / filename)
            current_example_lines.append(f"![{alt}]({rel})")

        elif name == "pre":
            if current_example_title is None:
                description_parts.append("```\n" + element.get_text().strip() + "\n```")
            else:
                bullets = _pre_to_bullets(element)
                if bullets:
                    current_example_lines.extend(bullets)

        elif name == "ul":
            if current_example_title is not None:
                flush_example()
            constraints.extend(_constraints_to_md(element))

        elif name == "img" and current_example_title is None:
            # 题干中的图片（较少见）
            src = element.get("src", "").strip()
            if src:
                image_index += 1
                filename = _image_filename(src, image_index)
                rel = f"imgs/{filename}"
                if download_images:
                    _download_image(src, imgs_dir / filename)
                description_parts.append(f"![示意图]({rel})")

    flush_orphan_inline()
    flush_example()
    description = "\n\n".join(description_parts).strip()
    return description, examples, constraints


def build_markdown(question: dict[str, Any], html: str, imgs_dir: Path) -> str:
    """组装与仓库范例一致的 Markdown 正文。"""
    qid = str(question["questionFrontendId"])
    title = question.get("translatedTitle") or question.get("title") or ""
    difficulty = DIFFICULTY_ZH.get(question.get("difficulty", ""), question.get("difficulty", ""))

    description, examples, constraints = html_to_markdown_sections(html, imgs_dir)

    lines = [
        f"# {qid}. {title}",
        "",
        f"**难度：** {difficulty}",
        "",
        "## 题目描述",
        "",
        description,
        "",
        "## 示例",
        "",
    ]
    if examples:
        lines.append("\n\n".join(examples))
    else:
        lines.append("（原题未提供示例）")
        lines.append("")

    lines.extend(["", "## 提示（数据范围）", ""])
    if constraints:
        lines.extend(constraints)
    else:
        lines.append("（原题未提供数据范围）")
    lines.append("")
    return "\n".join(lines)


def write_problem(
    identifier: str,
    output_dir: Path,
    *,
    overwrite: bool = False,
    update_index: bool = True,
    sort_index: bool = False,
) -> Path:
    """抓取并写入题目 Markdown，返回生成的文件路径。"""
    frontend_id, title_slug = resolve_title_slug(identifier)
    question = fetch_question(title_slug)

    padded = pad_question_id(str(question.get("questionFrontendId") or frontend_id))
    title = question.get("translatedTitle") or question.get("title") or title_slug
    safe_title = re.sub(r'[\\/:*?"<>|]', "", title).strip()

    folder = output_dir / "LeetCode" / f"LeetCode{padded}"
    md_name = f"LeetCode{padded}-{safe_title}.md"
    md_path = folder / md_name
    imgs_dir = folder / "imgs"

    if md_path.exists() and not overwrite:
        raise FileExistsError(f"文件已存在（使用 --overwrite 覆盖）: {md_path}")

    html = question.get("translatedContent") or question.get("content") or ""
    if not html.strip():
        raise RuntimeError("题目正文为空")

    folder.mkdir(parents=True, exist_ok=True)
    markdown = build_markdown(question, html, imgs_dir)
    md_path.write_text(markdown, encoding="utf-8")

    if update_index:
        leetcode_root = output_dir / "LeetCode"
        upsert_entry_after_write(leetcode_root, md_path, sort_by_id=sort_index)

    return md_path


def main() -> int:
    parser = argparse.ArgumentParser(description="从 leetcode.cn 下载题目并生成 Markdown")
    parser.add_argument(
        "identifier",
        help="题号（如 102、310）或 titleSlug（如 binary-tree-level-order-traversal）",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        help="项目根目录（将写入 <output-dir>/LeetCode/LeetCodeXXXX/）",
    )
    parser.add_argument("--overwrite", action="store_true", help="覆盖已存在的 Markdown")
    parser.add_argument("--no-index", action="store_true", help="不更新 LeetCode/leetCode题目.md 索引")
    parser.add_argument(
        "--sort-index",
        action="store_true",
        help="更新索引时按题号升序重排题目列表",
    )
    args = parser.parse_args()

    try:
        path = write_problem(
            args.identifier,
            args.output_dir.resolve(),
            overwrite=args.overwrite,
            update_index=not args.no_index,
            sort_index=args.sort_index,
        )
    except Exception as exc:  # noqa: BLE001 — CLI 统一报错
        print(f"错误: {exc}", file=sys.stderr)
        return 1

    print(f"已生成: {path}")
    if not args.no_index:
        idx = args.output_dir.resolve() / "LeetCode" / "leetCode题目.md"
        print(f"已更新索引: {idx}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
