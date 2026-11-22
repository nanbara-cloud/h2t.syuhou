# h2t.syuhou リポジトリのメモ

## このリポジトリにあるもの
- `schedule.html`、`ss_report_v4.html`：既存のページ。kintone から自動更新されるものがあるので、頼まれない限り触らない。
- `lp/`：Claude Code で作ったLP。見本は `lp/yakitori-shimbashi.html`。
- `claude-setup/`：PCに入れるサイト制作セット。
  - スキル：ui-ux-pro-max、motion-design、lp-maker
  - 説明書：`claude-setup/README.md`
  - セットアップ：`setup-windows.ps1`、`setup-mac.sh`
  - 依頼文のひな形：`templates/lp-request.md`
  - PC全体用の記憶：`memory/global-memory.md`（セットアップを実行すると `~/.claude/CLAUDE.md` に追記される）

## サイト制作の依頼が来たら
`claude-setup/memory/global-memory.md` の決まりごとに従う。要点：
- lp-maker の手順で進める。ui-ux-pro-max でデザインを先に決め、選んだ理由を添える。動きは motion-design の考え方で、控えめにする。
- 本文はメイリオ、スマホ優先、HTML1ファイル、無料素材のみ。AIっぽい配色や文字は避ける。
- 有料プラン・課金・APIキーが要る手順は実行せず、止めて報告する。
- 完成後はブラウザで崩れを確認し、直してから日本語で報告する。

スキルが `~/.claude/skills/` に無い環境（クラウドのセッションなど）では、作業前に入れる。

```bash
npm install -g ui-ux-pro-max-cli && uipro init --ai claude --global
npx -y skills add LottieFiles/motion-design-skill -g -a claude-code -y
mkdir -p ~/.claude/skills/lp-maker && cp -R claude-setup/skills/lp-maker/. ~/.claude/skills/lp-maker/
```

## ユーザーのPCについて
- このユーザーのPCに入れる作業は、PCで `claude-setup` のセットアップを実行するか、PC側の Claude Code に頼んでもらう。
- クラウドのセッションからPCを使うには、Claude デスクトップアプリの「設定 → Claude Code → Remote Control」でフォルダを共有してもらい、接続を申請する。承認はユーザーが行う。
