#!/bin/zsh

set -euo pipefail

REPO_DIR="/Users/pirateli/Documents/WB共创营/wb-workshop"
SOURCE_XLSX="/Users/pirateli/Desktop/workbuddy/workbuddy共创营/Skill收集评测表.xlsx"
PYTHON_BIN="/Users/pirateli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
SYNC_SCRIPT="$REPO_DIR/scripts/sync_skills_from_excel.py"
DATA_FILE="$REPO_DIR/data/skills-data.js"
PAGE_FILE="$REPO_DIR/WB共创营行业Skill资源库.html"

echo "开始更新行业 Skill 资源库..."

if [[ ! -f "$SOURCE_XLSX" ]]; then
  echo ""
  echo "未找到底表："
  echo "$SOURCE_XLSX"
  echo ""
  echo "请先把最新的 Skill收集评测表.xlsx 放到这个位置。"
  read -k 1 "?按任意键退出"
  exit 1
fi

cd "$REPO_DIR"

"$PYTHON_BIN" "$SYNC_SCRIPT" "$SOURCE_XLSX" "$DATA_FILE"

git add "$DATA_FILE" "$PAGE_FILE" "$SYNC_SCRIPT"

if git diff --cached --quiet; then
  echo ""
  echo "底表内容没有变化，页面无需更新。"
  read -k 1 "?按任意键关闭窗口"
  exit 0
fi

COMMIT_MSG="Update skill library $(date '+%Y-%m-%d %H:%M')"
git commit -m "$COMMIT_MSG"

if git push origin main; then
  echo ""
  echo "更新完成，已推送到 GitHub。"
else
  echo ""
  echo "本地更新和提交已经完成，但推送失败。"
  echo "你可以稍后在这个仓库里重新执行一次 git push origin main。"
fi

echo ""
read -k 1 "?按任意键关闭窗口"
