---
name: lp-maker
description: 店舗・サービスのLP（ランディングページ）を1ページのHTMLで作る手順。ui-ux-pro-max で配色・フォント・スタイルを先に決め、motion-design で控えめなスクロール表示を入れ、スマホ優先・メイリオ基本・無料素材のみで作り、ブラウザで崩れを確認してから報告する。「LPを作って」「ランディングページ」「店舗のサイトを1ページで」などの依頼で使う。
---

# LP作成スキル（lp-maker）

店舗やサービスのLPを、HTML1ファイルで作るための社内手順です。
依頼文は `templates/lp-request.md` の形で受け取る想定です。

## 0. 依頼内容の確認

依頼文から次の4つを読み取ります。

| 項目 | 例 |
|---|---|
| 業種・店舗 | 新橋の焼き鳥店 |
| 目的 | 予約を増やす |
| 載せる内容 | メニュー、席、アクセス、予約ボタン |
| 参考 | 参考サイトのURL、または MotionSites でコピーした指示文 |

- 【例：…】のまま届いた欄は、例の内容で作り、報告でそのことを伝える。
- 参考がある場合は、構成と雰囲気だけを寄せる。**文章と画像はそのまま流用しない。**
- 店名・住所・電話番号・価格など事実が分からないものは、仮の値（〇〇、03-0000-0000 など）にして、報告で「差し替えが必要」と一覧にする。

## 1. デザインを先に決める（ui-ux-pro-max）

必ず `ui-ux-pro-max` スキルを使って、コードを書く前に決める。

```bash
python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<業種を英語で> <雰囲気>" --design-system -p "<店名>" --motion 2 --density 3 --variance 4
python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<業種> <雰囲気>" --domain color -n 4
python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "japanese <雰囲気>" --domain typography -n 3
python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "japanese serif mincho" --domain google-fonts -n 5
```

（Windows では `python3` を `python` に読み替える）

決めること：

- **配色**：背景・文字・補助文字・アクセント・予約ボタンの5色を CSS 変数（`:root`）で定義する。
- **フォント**：本文は **メイリオ** を基本にする。
  `font-family:"メイリオ",Meiryo,"Hiragino Kaku Gothic ProN","Hiragino Sans","Noto Sans JP",sans-serif;`
  見出しだけ、業種に合う無料の Google Fonts（例：Shippori Mincho B1、Zen Old Mincho）を使ってよい。
- **スタイル**：業種と客層に合う1つを選ぶ。

**AIっぽい、ありきたりなデザインを避ける：**
- スキルの最初の候補をそのまま使わない。根拠（例：「食欲を誘う赤＋暖色の金」）だけを残し、業種と土地の色に置き換える。
  - 例：焼き鳥店なら、炭の黒・生成り・たれの金茶・提灯の紅殻。
- 避けるもの：紫〜青のグラデーション、ピンク地に赤、Inter や Roboto だけの見出し、絵文字のアイコン、どの業種にも使える汎用コピー。
- 文字と背景のコントラストは 4.5:1 以上にする。決めたら次のように計算して確かめる。

```python
def L(h):
    h=h.lstrip('#');c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]
    return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def cr(a,b):
    a,b=L(a),L(b);return (max(a,b)+0.05)/(min(a,b)+0.05)
print(cr("#F3EBDD","#1A1613"))  # 文字色, 背景色
```

報告では、配色・フォント・スタイルのそれぞれに **選んだ理由を一言** 添える。

## 2. 構成

目的が「予約を増やす」「問い合わせを増やす」なら、次の構成を基本にする。

1. ヒーロー：場所が分かる短いラベル／キャッチコピー／予約ボタン（主）と内容を見るボタン（副）／営業時間などの要点
2. こだわり（3点）
3. メニュー・料金（価格は税込表記。コースがあれば予約ボタンを添える）
4. 席・設備
5. アクセス：表形式（住所・最寄駅・営業時間・定休日・支払い方法）と、Googleマップを開くリンク
6. 予約：ネット予約（主）と電話（副）、予約の流れ3ステップ
7. フッター

- **スマホでは画面下に予約バーを常に表示する**（電話／予約）。本文の最後が隠れないよう、`body` の下に余白を取る。
- 主ボタン（予約）は1種類の色だけにして、ほかのボタンは枠線だけにする。
- 押せるところは高さ44px以上にする。
- 予約できるかどうか分からないのに「空いています」のように言い切る文言は使わない。

## 3. 動き（motion-design）

必ず `motion-design` スキルの考え方で入れる。**控えめ、読みやすさ優先。**

- スクロールで表示：透明から不透明へ＋下から16pxだけ移動。0.5〜0.6秒、減速カーブ `cubic-bezier(.2,.6,.2,1)`。
- 並んだ項目は0.08秒ずつずらす（ずらす合計は0.4秒以内）。
- 一度表示したら消さない（スクロールで戻っても隠さない）。
- ライブラリは使わず `IntersectionObserver` で書く。
- 端末の「視差効果を減らす」設定（`prefers-reduced-motion: reduce`）では動きをなくす。
- JavaScriptが止まっていても全文が読めるようにする。非表示にするのは `<head>` で `html` に `js` クラスが付いたときだけにする（ちらつき防止）。
- 動き続けるものはヒーローの背景など1か所だけ。ゆっくり（5秒程度）明滅させる程度にとどめる。

```html
<!-- head 内 -->
<script>
if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window){document.documentElement.classList.add('js');}
</script>
```

```css
.js .reveal{opacity:0;transform:translateY(16px);
  transition:opacity .56s cubic-bezier(.2,.6,.2,1),transform .56s cubic-bezier(.2,.6,.2,1);
  transition-delay:calc(var(--i,0) * 80ms)}
.js .reveal.is-in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.js .reveal{opacity:1;transform:none;transition:none}}
```

```html
<!-- body の最後 -->
<script>
(function(){
  if (!document.documentElement.classList.contains('js')) return;
  var io = new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('is-in'); io.unobserve(e.target); } });
  }, { rootMargin:'0px 0px -8% 0px', threshold:0.1 });
  document.querySelectorAll('.reveal').forEach(function(el){ io.observe(el); });
})();
</script>
```

## 4. 作り方のルール

- **HTML1ファイル**。CSSとJSは中に書く。
- **スマホ優先**：基本のCSSはスマホ向けに書き、`@media (min-width:768px)` でPC向けを足す。
- 本文は16px以上、行間1.7〜1.8。
- 横にはみ出させない（横スクロールが出ないこと）。
- 見出しが変な位置で改行しないよう、言葉の切れ目を `<span style="display:inline-block">` で囲む。本文には `text-wrap:pretty` を付ける。
- **無料の素材・ライブラリだけ**：
  - 画像：自作のSVGイラスト、または実店舗の写真（ユーザー提供）。ストック写真を使う場合は、無料で商用利用できるもの（Unsplash など）に限り、出典を報告する。
  - アイコン：Lucide（MIT）のSVGを直接埋め込む。絵文字は使わない。
  - フォント：Google Fonts（OFL）。
  - 地図：APIキーの要らない Googleマップへのリンク（`https://www.google.com/maps/search/?api=1&query=...`）。
- 有料プラン、APIキー、課金が必要なものは使わない。
- 電話は `tel:` リンクにする。ネット予約先のURLが分からないときは、仮でページ内の `#reserve` に飛ばし、HTMLのコメントに「差し替えてください」と書く。
- アクセシビリティ：`lang="ja"`、本文へ移動するスキップリンク、`:focus-visible` の枠、飾りのSVGには `aria-hidden="true"`、意味のある図には `role="img"` と `aria-label` を付ける。

保存場所は、作業中のフォルダの `lp/<店や業種の英字名>.html` を基本にする。

## 5. ブラウザで確認して直す（必須）

完成したら、必ずブラウザで開いて崩れを確認し、**直してから** 報告する。

Playwright が使える場合は、次のスクリプトでスマホ（375px・320px）とPC（1280px）を確認する。

```js
// check-lp.js  使い方: node check-lp.js lp/xxx.html
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file://' + path.resolve(process.argv[2]);
  const b = await chromium.launch();
  for (const [name, vp] of [['sp375',{width:375,height:740}],['sp320',{width:320,height:640}],['pc',{width:1280,height:800}]]) {
    const p = await b.newPage({ viewport: vp });
    const errs=[]; p.on('pageerror',e=>errs.push(e.message));
    await p.goto(file, { waitUntil: 'networkidle' });
    const h = await p.evaluate(()=>document.body.scrollHeight);
    for (let y=0;y<h;y+=300){ await p.evaluate(y=>window.scrollTo(0,y),y); await p.waitForTimeout(60); }
    await p.waitForTimeout(800); await p.evaluate(()=>window.scrollTo(0,0));
    const r = await p.evaluate(()=>({
      横はみ出し: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      表示されない要素: [...document.querySelectorAll('.reveal')].filter(e=>!e.classList.contains('is-in')).length,
    }));
    console.log(name, r, errs);
    await p.screenshot({ path: `check-${name}.png`, fullPage: true });
    await p.close();
  }
  await b.close();
})();
```

確認すること：
- 横スクロールが出ないこと、すべての要素が表示されること、エラーが出ないこと。
- スクリーンショットを見て、見出しの変な改行、ずれ、重なり、文字が読みにくい箇所がないこと。
- PCで横に並べたカードの見出しの高さが揃っていること。揃っていなければ、カードに `align-content:start` を付ける。
- スマホの予約バーが本文の最後を隠していないこと。

Playwright が使えない場合は、ユーザーにブラウザで開いてもらい、スマホ幅（開発者ツールの 375px）とPC幅で見てもらう。

## 6. 報告の形

1. 作ったファイルの場所
2. デザイン（配色・フォント・スタイル、それぞれ理由を一言）
3. 入れた動き
4. ページの構成
5. ブラウザ確認の結果と、直したところ
6. 使った素材・ライブラリ（すべて無料であること）
7. 公開前に差し替えが必要なところ（仮の店名・住所・電話・価格・予約URL・写真など）
