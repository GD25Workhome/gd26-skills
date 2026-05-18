#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
维护 LeetCode/leetCode题目.md 中「## 题目列表」章节。

索引文件格式参见 gd26-algorithm/LeetCode/leetCode题目.md。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

INDEX_FILENAME = "leetCode题目.md"
SECTION_LIST = "## 题目列表"
MAIN_LINE_RE = re.compile(r"^- \[(\d+)\.\s+(.+?)\]\(([^)]+)\)\s*$")
SUB_LINE_RE = re.compile(r"^  - (.+)$")
HEADING_RE = re.compile(r"^## .+")
TITLE_LINE_RE = re.compile(r"^#\s*(\d+)\.\s+(.+?)\s*$")
PROBLEM_DIR_RE = re.compile(r"^LeetCode(\d{4})$")
PROBLEM_FILE_RE = re.compile(r"^LeetCode(\d{4})-(.+)\.md$")


@dataclass
class IndexEntry:
    """题目列表中的一条主题目及其可选备注子项。"""

    question_id: int
    title: str
    link: str
    notes: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        """链接文字：「102. 二叉树的层序遍历」。"""
        return f"{self.question_id}. {self.title}"

    def format_main_line(self) -> str:
        return f"- [{self.label}]({self.link})"

    def format_block(self) -> str:
        lines = [self.format_main_line()]
        for note in self.notes:
            lines.append(f"  - {note}")
        return "\n".join(lines)


def index_path(leetcode_dir: Path) -> Path:
    return leetcode_dir / INDEX_FILENAME


def normalize_link(link: str) -> str:
    """统一链接路径，去掉 ./ 前缀。"""
    link = link.strip()
    if link.startswith("./"):
        return link[2:]
    return link


def build_link(padded_id: str, filename: str) -> str:
    return f"LeetCode{padded_id}/LeetCode{padded_id}-{filename}"


def parse_title_from_md(md_path: Path) -> tuple[int, str] | None:
    """从原题 Markdown 首行标题解析题号与题名。"""
    try:
        first = md_path.read_text(encoding="utf-8").splitlines()[0]
    except (OSError, IndexError):
        return None
    match = TITLE_LINE_RE.match(first.strip())
    if match:
        return int(match.group(1)), match.group(2).strip()
    return None


def scan_problem_entries(leetcode_dir: Path) -> dict[int, IndexEntry]:
    """
    扫描 LeetCode 目录下所有原题 Markdown（排除题解-*），生成索引条目。
    """
    entries: dict[int, IndexEntry] = {}
    if not leetcode_dir.is_dir():
        return entries

    for folder in sorted(leetcode_dir.iterdir()):
        if not folder.is_dir():
            continue
        dir_match = PROBLEM_DIR_RE.match(folder.name)
        if not dir_match:
            continue
        padded = dir_match.group(1)

        for md_path in sorted(folder.glob("LeetCode*.md")):
            if md_path.name.startswith("题解-"):
                continue
            file_match = PROBLEM_FILE_RE.match(md_path.name)
            if not file_match:
                continue

            qid = int(file_match.group(1))
            file_title = file_match.group(2)

            parsed = parse_title_from_md(md_path)
            if parsed:
                qid, title = parsed
            else:
                title = file_title

            rel_link = f"{folder.name}/{md_path.name}"
            entries[qid] = IndexEntry(
                question_id=qid,
                title=title,
                link=normalize_link(rel_link),
            )
            break  # 每目录只取一个原题文件

    return entries


def split_index_sections(content: str) -> tuple[str, list[str], str]:
    """
    将索引文件拆为：题目列表之前、题目列表行、题目列表之后。
    题目列表行含 ## 题目列表 标题行本身。
    """
    lines = content.splitlines()
    start: int | None = None
    end: int | None = None

    for i, line in enumerate(lines):
        if line.strip() == SECTION_LIST:
            start = i
            continue
        if start is not None and i > start and HEADING_RE.match(line):
            end = i
            break

    if start is None:
        return content, [], ""

    if end is None:
        end = len(lines)

    before = "\n".join(lines[:start])
    list_body = lines[start:end]
    after = "\n".join(lines[end:])
    return before, list_body, after


def parse_list_body(list_body: list[str]) -> list[IndexEntry]:
    """解析「题目列表」章节内的条目（含备注子项）。"""
    entries: list[IndexEntry] = []
    current: IndexEntry | None = None

    for line in list_body:
        if line.strip() == SECTION_LIST:
            continue
        main = MAIN_LINE_RE.match(line)
        if main:
            if current is not None:
                entries.append(current)
            current = IndexEntry(
                question_id=int(main.group(1)),
                title=main.group(2).strip(),
                link=normalize_link(main.group(3)),
            )
            continue
        sub = SUB_LINE_RE.match(line)
        if sub and current is not None:
            current.notes.append(sub.group(1))
            continue

    if current is not None:
        entries.append(current)
    return entries


def merge_entries(
    existing: list[IndexEntry],
    scanned: dict[int, IndexEntry],
    *,
    sort_by_id: bool = False,
) -> list[IndexEntry]:
    """
    合并已有索引与磁盘扫描结果：
    - 保留原有顺序与备注；
    - 更新链接与标题；
    - 追加磁盘上新发现、索引中缺失的题。
    """
    result: list[IndexEntry] = []
    seen: set[int] = set()

    for old in existing:
        if old.question_id not in scanned:
            result.append(old)
            seen.add(old.question_id)
            continue
        fresh = scanned[old.question_id]
        merged = IndexEntry(
            question_id=fresh.question_id,
            title=fresh.title,
            link=fresh.link,
            notes=list(old.notes),
        )
        result.append(merged)
        seen.add(old.question_id)

    for qid, entry in scanned.items():
        if qid not in seen:
            result.append(entry)
            seen.add(qid)

    if sort_by_id:
        result.sort(key=lambda e: e.question_id)
    return result


def format_list_section(entries: list[IndexEntry]) -> str:
    """生成完整的「## 题目列表」章节文本。"""
    blocks = [entry.format_block() for entry in entries]
    body = "\n".join(blocks)
    if body:
        return f"{SECTION_LIST}\n\n{body}"
    return f"{SECTION_LIST}\n\n"


def compose_index(before: str, entries: list[IndexEntry], after: str) -> str:
    """拼装完整索引文件内容（章节之间保留空行）。"""
    list_section = format_list_section(entries)
    parts: list[str] = []

    before_stripped = before.rstrip()
    if before_stripped:
        parts.append(before_stripped)
        parts.append("")

    parts.append(list_section.rstrip())

    after_stripped = after.lstrip()
    if after_stripped:
        parts.append("")
        parts.append(after_stripped)

    return "\n".join(parts).rstrip() + "\n"


def default_index_header() -> str:
    return "# LeetCode 题目索引\n"


def update_index(
    leetcode_dir: Path,
    *,
    sort_by_id: bool = False,
    dry_run: bool = False,
) -> Path:
    """
    根据磁盘上的原题 Markdown 更新 leetCode题目.md。
    保留「题目列表」之外的章节及每条下的备注子项。
    """
    leetcode_dir = leetcode_dir.resolve()
    scanned = scan_problem_entries(leetcode_dir)
    idx_file = index_path(leetcode_dir)

    if idx_file.exists():
        content = idx_file.read_text(encoding="utf-8")
        before, list_body, after = split_index_sections(content)
        existing = parse_list_body(list_body)
        if before.strip() == "":
            before = default_index_header()
    else:
        before = default_index_header()
        existing = []
        after = ""

    merged = merge_entries(existing, scanned, sort_by_id=sort_by_id)
    new_content = compose_index(before, merged, after)

    if not dry_run:
        leetcode_dir.mkdir(parents=True, exist_ok=True)
        idx_file.write_text(new_content, encoding="utf-8")

    return idx_file


def upsert_entry_after_write(
    leetcode_dir: Path,
    md_path: Path,
    *,
    sort_by_id: bool = False,
) -> Path:
    """
    抓取单题后快速更新索引：以全量扫描合并，确保链接与标题与刚写入文件一致。
    """
    return update_index(leetcode_dir, sort_by_id=sort_by_id)
