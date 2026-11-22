# Claude Code サイト制作セット（Windows 用）
# 使い方: このフォルダで PowerShell を開き、次を実行
#   powershell -ExecutionPolicy Bypass -File .\setup-windows.ps1
# 入るもの（すべて無料）:
#   %USERPROFILE%\.claude\skills\ui-ux-pro-max   … UI UX Pro Max（公式CLI）
#   %USERPROFILE%\.claude\skills\motion-design   … LottieFiles motion-design（公式 skills CLI）
#   %USERPROFILE%\.claude\skills\lp-maker        … LP作成手順（このリポジトリ同梱）
#   %USERPROFILE%\.claude\CLAUDE.md              … サイト制作の決まりごとを追記（記憶）
$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Skills = Join-Path $env:USERPROFILE ".claude\skills"

Write-Host "== 必要なソフトの確認 =="
foreach ($c in @("node", "npm", "npx")) {
  if (-not (Get-Command $c -ErrorAction SilentlyContinue)) {
    Write-Host "!! $c がありません。https://nodejs.org から Node.js（LTS）を入れてから再実行してください。"
    exit 1
  }
}
node --version
if (Get-Command python -ErrorAction SilentlyContinue) { python --version }
else { Write-Host "!! python がありません（ui-ux-pro-max の検索に必要）。Microsoft Store か https://www.python.org から入れてください。続行します。" }

Write-Host "== 1/3 UI UX Pro Max =="
npm install -g ui-ux-pro-max-cli
if ($LASTEXITCODE -ne 0) { throw "npm install に失敗しました" }
uipro init --ai claude --global
if ($LASTEXITCODE -ne 0) { throw "uipro init に失敗しました" }

Write-Host "== 2/3 motion-design =="
npx -y skills add LottieFiles/motion-design-skill -g -a claude-code -y
if ($LASTEXITCODE -ne 0) { throw "skills add に失敗しました" }

Write-Host "== 3/3 lp-maker =="
$Lp = Join-Path $Skills "lp-maker"
New-Item -ItemType Directory -Force -Path $Lp | Out-Null
Copy-Item -Recurse -Force (Join-Path $Here "skills\lp-maker\*") $Lp
Copy-Item -Force (Join-Path $Here "templates\lp-request.md") (Join-Path $Lp "lp-request.md")

Write-Host "== 記憶（.claude\CLAUDE.md）=="
$Mem = Join-Path $env:USERPROFILE ".claude\CLAUDE.md"
$Add = Get-Content -Raw -Encoding UTF8 (Join-Path $Here "memory\global-memory.md")
$Cur = ""
if (Test-Path $Mem) { $Cur = Get-Content -Raw -Encoding UTF8 $Mem }
if ($null -eq $Cur) { $Cur = "" }
# 古い記憶を新しい内容に置き換える（ほかの記述はそのまま）
$Cur = [regex]::Replace($Cur, '(?s)\r?\n?<!-- h2t-site-kit:start -->.*?<!-- h2t-site-kit:end -->\r?\n?', '')
$Utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($Mem, ($Cur.TrimEnd() + "`n`n" + $Add), $Utf8)
Write-Host "OK  $Mem に追記しました"

Write-Host "== 確認 =="
$ok = $true
foreach ($s in @("ui-ux-pro-max", "motion-design", "lp-maker")) {
  $f = Join-Path $Skills "$s\SKILL.md"
  if (Test-Path $f) { Write-Host "OK  $f" } else { Write-Host "NG  $s"; $ok = $false }
}
if ($ok) { Write-Host "完了しました。Claude Code を再起動してください。" }
else { Write-Host "入らなかったものがあります。README.md の「うまくいかないとき」を見てください。"; exit 1 }
