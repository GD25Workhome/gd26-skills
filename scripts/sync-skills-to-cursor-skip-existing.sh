#!/usr/bin/env bash
#
# 将本仓库 skills/ 下的技能目录同步到 ~/.cursor/skills/
# 若目标已存在同名技能，直接跳过（不备份、不覆盖、不交互询问）。
#
# 用法：
#   ./scripts/sync-skills-to-cursor-skip-existing.sh
#   或：bash scripts/sync-skills-to-cursor-skip-existing.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SOURCE_SKILLS="${REPO_ROOT}/skills"
DEST_SKILLS="${HOME}/.cursor/skills"

main() {
  if [[ ! -d "${SOURCE_SKILLS}" ]]; then
    echo "错误：找不到技能源目录：${SOURCE_SKILLS}" >&2
    exit 1
  fi

  mkdir -p "${DEST_SKILLS}"

  local synced=0
  local skipped=0

  local path name dest
  for path in "${SOURCE_SKILLS}"/*; do
    [[ -e "${path}" ]] || continue
    [[ -d "${path}" ]] || continue

    name="$(basename "${path}")"
    [[ "${name}" == .* ]] && continue

    dest="${DEST_SKILLS}/${name}"

    if [[ -e "${dest}" ]]; then
      echo "已跳过（目标已存在）：${name}"
      ((skipped++)) || true
      continue
    fi

    echo "正在复制：${name} -> ${dest}"
    cp -R "${path}" "${dest}"
    ((synced++)) || true
  done

  echo ""
  echo "完成。已同步 ${synced} 个技能到 ${DEST_SKILLS}"
  if (( skipped > 0 )); then
    echo "已跳过 ${skipped} 个（目标目录已有同名技能）。"
  fi
}

main "$@"
