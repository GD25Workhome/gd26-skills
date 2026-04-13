#!/usr/bin/env bash
#
# 将本仓库 skills/ 下的技能目录同步到 ~/.cursor/skills/
# 若目标已存在同名技能，可选择在 ~/.cursor/skills-back/ 下按「名称-年月日时分秒」备份后再覆盖。
#
# 用法：
#   ./scripts/sync-skills-to-cursor.sh
#   或：bash scripts/sync-skills-to-cursor.sh
#

set -euo pipefail

# 本脚本所在目录的上一级 = 仓库根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SOURCE_SKILLS="${REPO_ROOT}/skills"
DEST_SKILLS="${HOME}/.cursor/skills"
BACKUP_ROOT="${HOME}/.cursor/skills-back"

# 生成备份后缀：年月日时分秒（例如 20260413143022）
timestamp_suffix() {
  date +%Y%m%d%H%M%S
}

# 询问是/否，默认否
ask_yes_no() {
  local prompt="$1"
  local reply
  read -r -p "${prompt} [y/N] " reply || true
  case "${reply:-}" in
    [yY]|[yY][eE][sS]) return 0 ;;
    *) return 1 ;;
  esac
}

# 询问是/否，默认为是
ask_yes_no_default_yes() {
  local prompt="$1"
  local reply
  read -r -p "${prompt} [Y/n] " reply || true
  case "${reply:-Y}" in
    [nN]|[nN][oO]) return 1 ;;
    *) return 0 ;;
  esac
}

main() {
  if [[ ! -d "${SOURCE_SKILLS}" ]]; then
    echo "错误：找不到技能源目录：${SOURCE_SKILLS}" >&2
    exit 1
  fi

  mkdir -p "${DEST_SKILLS}" "${BACKUP_ROOT}"

  local count=0
  local skipped=0

  # 遍历 skills 下的一级子目录（每个目录视为一个技能）
  local name
  for path in "${SOURCE_SKILLS}"/*; do
    [[ -e "${path}" ]] || continue
    [[ -d "${path}" ]] || continue
    name="$(basename "${path}")"
    # 跳过隐藏目录
    [[ "${name}" == .* ]] && continue

    local dest="${DEST_SKILLS}/${name}"

    if [[ -e "${dest}" ]]; then
      echo ""
      echo "检测到目标已存在同名技能：${name}"
      echo "  源：${path}"
      echo "  目标：${dest}"

      if ask_yes_no_default_yes "是否将现有技能备份到 ${BACKUP_ROOT}/ 下？"; then
        local ts
        ts="$(timestamp_suffix)"
        local backup_path="${BACKUP_ROOT}/${name}-${ts}"
        echo "正在备份：${dest} -> ${backup_path}"
        mv "${dest}" "${backup_path}"
      else
        if ask_yes_no "不备份。是否直接覆盖目标目录（将删除现有 ${name}）？"; then
          echo "正在删除目标目录：${dest}"
          rm -rf "${dest}"
        else
          echo "已跳过：${name}"
          ((skipped++)) || true
          continue
        fi
      fi
    fi

    echo "正在复制：${name} -> ${dest}"
    cp -R "${path}" "${dest}"
    ((count++)) || true
  done

  echo ""
  echo "完成。已同步 ${count} 个技能到 ${DEST_SKILLS}"
  if (( skipped > 0 )); then
    echo "已跳过 ${skipped} 个（存在冲突且未覆盖）。"
  fi
}

main "$@"
