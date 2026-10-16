#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
维护 LeetCode/leetCode题目.md 的「题目列表」索引。

用法:
  python update_leetcode_index.py --output-dir /path/to/project
  python update_leetcode_index.py --output-dir /path/to/project --sort
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from leetcode_index import update_index


def main() -> int:
    parser = argparse.ArgumentParser(description="维护 LeetCode/leetCode题目.md 题目列表索引")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        help="项目根目录（索引位于 <output-dir>/LeetCode/leetCode题目.md）",
    )
    parser.add_argument(
        "--sort",
        action="store_true",
        help="按题号数字升序重排题目列表（默认保持已有顺序，新题追加在末尾）",
    )
    parser.add_argument("--dry-run", action="store_true", help="仅打印将写入的路径，不修改文件")
    args = parser.parse_args()

    leetcode_dir = args.output_dir.resolve() / "LeetCode"
    try:
        path = update_index(leetcode_dir, sort_by_id=args.sort, dry_run=args.dry_run)
    except Exception as exc:  # noqa: BLE001
        print(f"错误: {exc}", file=sys.stderr)
        return 1

    action = "将更新" if args.dry_run else "已更新"
    print(f"{action}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
