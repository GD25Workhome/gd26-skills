#!/usr/bin/env python3
"""createMdFile: recommend a path + frontmatter date for a markdown artifact.

Takes a slug, resolves config, and emits a recommended absolute path
under <output_dir>[/<subdir>]/YYMMDD-NN-<slug>.md where NN is a
global-per-day counter in the same directory (01, 02, 03, ...),
plus a `date` string for frontmatter. Does NOT touch the filesystem —
no mkdir, no file creation. The calling agent uses its own Write tool
to create the file (and add the body) at the recommended path.

Skill's contract is "where to put the md file", nothing more.
File creation is the caller's responsibility.

Config resolution: project-level > user-level > built-in defaults.
If project-level config is missing and user-level exists, auto-copy
user-level to project-level so subsequent runs are project-served.

Output (stdout):
    FILEPATH=<recommended absolute path>
    FRONTMATTER_DATE=YYMMDD
"""
import argparse
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("__PYYAML_MISSING__\nRun: pip install pyyaml", file=sys.stderr)
    sys.exit(3)


SKILL_DIR = Path.home() / '.claude' / 'skills' / 'save-md-artifact'
USER_CONFIG_PATH = SKILL_DIR / 'config.yaml'
EXAMPLE_PATH = SKILL_DIR / 'config.example.yaml'

# Built-in defaults (lowest priority)
DEFAULTS = {
    'output_dir': 'ai-docs',
    'subdir': '',
    'slug_max_length': 200,
    'slug_fallback': 'untitled',
}


def project_root() -> Path:
    try:
        out = subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'], text=True
        ).strip()
        return Path(out)
    except Exception:
        return Path.cwd()


def load_yaml(path: Path) -> dict:
    if not path or not path.is_file():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding='utf-8')) or {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def resolve_config(root: Path) -> dict:
    """Merge defaults < user-level < project-level. Auto-copy user→project."""
    cfg = dict(DEFAULTS)
    proj_cfg = root / '.claude' / 'save-md-artifact.yaml'

    # Layer 1: user-level
    user_data = load_yaml(USER_CONFIG_PATH)
    for k in DEFAULTS:
        if k in user_data:
            cfg[k] = user_data[k]

    # Layer 2: project-level (highest; auto-create from user if missing)
    if proj_cfg.is_file():
        proj_data = load_yaml(proj_cfg)
        for k in DEFAULTS:
            if k in proj_data:
                cfg[k] = proj_data[k]
    else:
        try:
            proj_cfg.parent.mkdir(parents=True, exist_ok=True)
            src = USER_CONFIG_PATH if USER_CONFIG_PATH.is_file() else (
                EXAMPLE_PATH if EXAMPLE_PATH.is_file() else None
            )
            if src:
                shutil.copy2(src, proj_cfg)
        except Exception:
            pass  # non-fatal; merged cfg still applies

    return cfg


def sanitize_slug(raw: str, max_length: int, fallback: str) -> str:
    """Sanitize slug: replace whitespace with hyphens, strip path/control chars."""
    if not raw:
        return fallback
    s = re.sub(r'\s+', '-', raw.strip())
    # Strip path separators + filesystem-unsafe chars + control chars
    s = re.sub(r'[\\/:*?"<>|\x00-\x1f]+', '', s)
    # Collapse repeated hyphens
    s = re.sub(r'-+', '-', s).strip('-')
    if not s:
        return fallback
    if len(s) > max_length:
        s = s[:max_length].rstrip('-')
    return s


def next_counter(output_dir: Path, date_short: str) -> int:
    """Next global counter for `date_short` in `output_dir`.

    Counter is shared across all slugs in the same directory on the
    same day: every new file increments by 1, regardless of slug.
    Returns 1 if no files exist for that date.
    """
    counters = []
    for f in output_dir.glob(f"{date_short}-*.md"):
        m = re.match(rf'^{date_short}-(\d{{2}})-', f.name)
        if m:
            counters.append(int(m.group(1)))
    return max(counters, default=0) + 1


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--slug', required=True,
                        help='Semantic short name (e.g. "修复-bug"). 中文 OK.')
    parser.add_argument('--project-root', default=None,
                        help='Override git root (for testing).')
    args = parser.parse_args()

    root = Path(args.project_root) if args.project_root else project_root()
    cfg = resolve_config(root)

    safe_slug = sanitize_slug(args.slug, cfg['slug_max_length'], cfg['slug_fallback'])
    now = datetime.now()
    # Filename date: YYMMDD (6 digits). Frontmatter date uses the
    # same format — short and aligned with the filename.
    date_short = now.strftime('%y%m%d')
    fm_date = date_short

    output_dir = root / cfg['output_dir']
    if cfg.get('subdir'):
        sub = Path(cfg['subdir'])
        if sub.is_absolute() or '..' in sub.parts:
            print(f'__PATH_TRAVERSAL__\nSUBDIR={cfg["subdir"]}', file=sys.stderr)
            sys.exit(2)
        output_dir = output_dir / sub

    # Counter is per (date, directory) — global across all slugs that day.
    counter = next_counter(output_dir, date_short)

    # Recommend path; do NOT create the directory or file. The caller
    # decides whether to mkdir and Write the file.
    target = output_dir / f"{date_short}-{counter:02d}-{safe_slug}.md"

    print(f"FILEPATH={target}")
    print(f"FRONTMATTER_DATE={fm_date}")


if __name__ == '__main__':
    sys.exit(main())
