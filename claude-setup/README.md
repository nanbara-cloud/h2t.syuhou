# Claude Code サイト制作セット

PCの Claude Code で、どのプロジェクトからでも次の3つのスキルを使えるようにするセットです。

| スキル | 中身 | 入る場所 |
|---|---|---|
| **ui-ux-pro-max** | 配色・フォント・デザインスタイルを業種に合わせて選ぶ | `~/.claude/skills/ui-ux-pro-max/` |
| **motion-design**（LottieFiles製） | アニメーションのタイミングや動き方の決め方 | `~/.claude/skills/motion-design/` |
| **lp-maker**（このセット独自） | 上の2つを使ってLPを1ページ作る社内手順 | `~/.claude/skills/lp-maker/` |

`~` はユーザーのホームフォルダのことです。Windows では `C:\Users\<ユーザー名>` になります。

3つとも無料です。有料プランの契約、課金、APIキーの登録は一切ありません。

---

## 1. 事前に必要なもの

| ソフト | 用途 | 入っているかの確認 |
|---|---|---|
| Claude Code | 本体 | `claude --version` |
| Node.js（LTS版） | スキルを入れるのに使う | `node --version` |
| Python 3 | ui-ux-pro-max の検索に使う | Windows：`python --version`<br>Mac：`python3 --version` |
| Git（任意） | このリポジトリを取ってくるのに使う | `git --version` |

入っていないものは公式サイトから入れてください（どれも無料です）。

- Node.js：https://nodejs.org （LTS と書かれた方）
- Python：https://www.python.org/downloads/ （Windows は Microsoft Store の「Python 3」でも可）。インストール画面で「Add python.exe to PATH」にチェックを入れてください。
- Git：https://git-scm.com/downloads

---

## 2. PCを立ち上げたらやること

### 手順A：このリポジトリをPCに取ってくる

**Git を使う場合**（ターミナル／PowerShell で実行）

```bash
git clone https://github.com/nanbara-cloud/h2t.syuhou.git
cd h2t.syuhou
git checkout claude/epic-gates-05i06y
cd claude-setup
```

（後でこのブランチが main に取り込まれたら、`git checkout` の行は不要です）

**Git を使わない場合**
1. GitHub で `nanbara-cloud/h2t.syuhou` を開き、ブランチを `claude/epic-gates-05i06y` に切り替える。
2. 緑の「Code」ボタンから「Download ZIP」を選び、ダウンロードしたZIPを展開する。
3. 展開したフォルダの中の `claude-setup` を開く。

### 手順B：セットアップを実行する（1回だけ）

**Windows**：`claude-setup` フォルダで PowerShell を開いて（フォルダ内で Shift＋右クリック →「PowerShell ウィンドウをここで開く」）、次を実行します。

```powershell
powershell -ExecutionPolicy Bypass -File .\setup-windows.ps1
```

**Mac**：ターミナルで `claude-setup` フォルダに移動して、次を実行します。

```bash
bash setup-mac.sh
```

最後に次のように3行とも `OK` と出れば成功です。

```
OK  ~/.claude/skills/ui-ux-pro-max/SKILL.md
OK  ~/.claude/skills/motion-design/SKILL.md
OK  ~/.claude/skills/lp-maker/SKILL.md
完了しました。Claude Code を再起動してください。
```

### 手順C：Claude Code を再起動して確かめる

Claude Code を開き直して、入力欄に `/` と打ちます。候補に `ui-ux-pro-max`、`motion-design`、`lp-maker` が出れば使えます。

---

## 3. 使い方

### LPを作るとき（いちばんよく使う形）

`templates/lp-request.md` の中身をコピーし、【】の中を書き換えて Claude Code に貼り付けます。lp-maker スキルが動き、次の順で作業します。

1. ui-ux-pro-max で、配色・フォント・スタイルを先に決める（理由も添えて報告）
2. motion-design の考え方で、控えめなスクロール表示を入れる
3. スマホ優先・メイリオ基本・無料素材だけで、HTML1ファイルにする
4. ブラウザで崩れを確認し、直してから報告する

店名・住所・電話番号・予約URLなどを書いておけば、それが入ります。空欄なら仮の値で作り、差し替えが必要な箇所を一覧で教えてくれます。

### スキルを1つだけ使うとき

| やりたいこと | 頼み方の例 |
|---|---|
| デザインの方向を決めたい | `/ui-ux-pro-max 歯医者のサイトに合う配色とフォントを提案して` |
| 既存ページを見直したい | `このページのUIを ui-ux-pro-max で見直して、直すところを挙げて` |
| アニメーションを付けたい | `/motion-design 予約ボタンを押したときの動きを付けて` |
| 動きが変なのを直したい | `このアニメーションが安っぽい。motion-design の考え方で直して` |

`/スキル名` を付けなくても、内容が合えば Claude Code が自動で使います。

### 参考：このセットで作った見本

`lp/yakitori-shimbashi.html`（新橋の焼き鳥店の見本LP）。ブラウザにドラッグすると開けます。

---

## 4. 更新するとき

```bash
npm install -g ui-ux-pro-max-cli@latest
uipro update --global
npx skills add LottieFiles/motion-design-skill -g -a claude-code -y
```

lp-maker の手順を変えたいときは、このリポジトリの `claude-setup/skills/lp-maker/SKILL.md` を書き換えて、もう一度セットアップを実行します。

## 5. 削除するとき

```bash
uipro uninstall --global
```

`motion-design` と `lp-maker` は、`~/.claude/skills/` の中の同じ名前のフォルダを削除すれば消えます。

---

## 6. うまくいかないとき

| 症状 | 原因 | 対処 |
|---|---|---|
| `node` / `npm` が見つからない | Node.js が入っていない、または入れた後にターミナルを開き直していない | Node.js を入れて、ターミナルを開き直す |
| Windows で「このシステムではスクリプトの実行が無効」 | PowerShell の実行ポリシー | 上の `-ExecutionPolicy Bypass` 付きのコマンドで実行する |
| `uipro` が見つからない | npm のグローバルフォルダが PATH に入っていない | ターミナルを開き直す。だめなら `npx -y ui-ux-pro-max-cli init --ai claude --global` で実行する |
| Mac で `npm install -g` が権限エラー（EACCES） | グローバルフォルダの権限 | `sudo` は使わず、`npx -y ui-ux-pro-max-cli init --ai claude --global` で実行する |
| ui-ux-pro-max の検索で `python3` がない | Python が入っていない | Python 3 を入れる。Windows では `python` という名前で動く |
| `/` で候補にスキルが出ない | Claude Code を再起動していない | Claude Code を一度閉じて開き直す |
| 会社のネットワークでダウンロードが止まる | プロキシやフィルタ | 社内のIT担当に `registry.npmjs.org` と `github.com` への接続を確認する |

自動で入らない場合は、手でこの3つを打てば同じ状態になります（lp-maker だけは手でコピーします）。

```bash
npm install -g ui-ux-pro-max-cli
uipro init --ai claude --global
npx skills add LottieFiles/motion-design-skill -g -a claude-code -y
```

その後、`claude-setup/skills/lp-maker` フォルダを `~/.claude/skills/` の中にコピーしてください。

---

## 7. 入れていないもの（任意・有料連携の可能性あり）

- **LottieFiles Creator MCP**：アニメーションを MP4・GIF・Lottie ファイルに書き出す追加機能です。LottieFiles アカウントとの連携が必要なので、このセットには入れていません。使いたい場合だけ、内容と料金を確認してから次のコマンドで入れてください。
  `claude mcp add --transport http --scope user creator-mcp https://creator.mcp.lottiefiles.com/mcp`
- **ui-ux-pro-max と一緒に入る関連スキル**（banner-design、brand、design、design-system、slides、ui-styling）：このうち design のロゴ・アイコン生成などは Gemini の APIキーが必要です。キーを登録しない限り、その機能だけ動きません（ほかは使えます）。
