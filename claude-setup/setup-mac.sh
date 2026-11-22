#!/usr/bin/env bash
# Claude Code サイト制作セット（Mac / Linux 用）
# 使い方: このフォルダで  bash setup-mac.sh
# 入るもの（すべて無料）:
#   ~/.claude/skills/ui-ux-pro-max   … UI UX Pro Max（公式CLI）
#   ~/.claude/skills/motion-design   … LottieFiles motion-design（公式 skills CLI）
#   ~/.claude/skills/lp-maker        … LP作成手順（このリポジトリ同梱）
#   ~/.claude/CLAUDE.md              … サイト制作の決まりごとを追記（記憶）
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

echo "== 必要なソフトの確認 =="
for c in node npm npx; do
  command -v "$c" >/dev/null || { echo "!! $c がありません。https://nodejs.org から Node.js（LTS）を入れてから再実行してください。"; exit 1; }
done
if command -v python3 >/dev/null; then python3 --version; else echo "!! python3 がありません（ui-ux-pro-max の検索に必要）。https://www.python.org から入れてください。続行します。"; fi
node --version

echo "== 1/3 UI UX Pro Max =="
npm install -g ui-ux-pro-max-cli
uipro init --ai claude --global

echo "== 2/3 motion-design =="
npx -y skills add LottieFiles/motion-design-skill -g -a claude-code -y

echo "== 3/3 lp-maker =="
mkdir -p "$HOME/.claude/skills/lp-maker"
cp -R "$HERE/skills/lp-maker/." "$HOME/.claude/skills/lp-maker/"
cp "$HERE/templates/lp-request.md" "$HOME/.claude/skills/lp-maker/lp-request.md"

echo "== 記憶（~/.claude/CLAUDE.md）=="
MEM="$HOME/.claude/CLAUDE.md"
touch "$MEM"
if grep -q "h2t-site-kit:start" "$MEM"; then
  # 古い記憶を新しい内容に置き換える（ほかの記述はそのまま）
  awk '/<!-- h2t-site-kit:start -->/{skip=1} !skip{print} /<!-- h2t-site-kit:end -->/{skip=0}' "$MEM" > "$MEM.tmp" && mv "$MEM.tmp" "$MEM"
fi
printf '\n' >> "$MEM"; cat "$HERE/memory/global-memory.md" >> "$MEM"
echo "OK  $MEM に追記しました"

echo "== 確認 =="
ok=1
for s in ui-ux-pro-max motion-design lp-maker; do
  if [ -f "$HOME/.claude/skills/$s/SKILL.md" ]; then echo "OK  ~/.claude/skills/$s/SKILL.md"; else echo "NG  $s"; ok=0; fi
done
[ "$ok" = 1 ] && echo "完了しました。Claude Code を再起動してください。" || { echo "入らなかったものがあります。README.md の「うまくいかないとき」を見てください。"; exit 1; }
