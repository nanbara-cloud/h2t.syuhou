#!/usr/bin/env python3
"""週報 ss_report_v4.html の kintone 由来データ（KPI・パイプライン・受注・問い合わせ）を作り直す。

kintone の営業マスタ（アプリ238）を API で読み、HTML 内の次の定数を置き換える:
  STATIC_KPI / STATIC_PIPE / STATIC_JUCHU / STATIC_ROUTE_DATA と、ヘッダーの最終更新日時。

認証: リクエストヘッダー X-Cybozu-API-Token。クラウド環境ではプロキシが本物のトークンを
差し込むので、環境変数 KINTONE_API_TOKEN が無ければダミー値で送る。

使い方:
  python3 scripts/kintone_update.py ss_report_v4.html            # 書き換える
  python3 scripts/kintone_update.py ss_report_v4.html --dry-run  # 差分の件数だけ表示
  python3 scripts/kintone_update.py ss_report_v4.html --records records.json  # 取得済みデータを使う
"""
import argparse, datetime, json, os, re, sys, urllib.parse, urllib.request

BASE = 'https://h2-inc.cybozu.com/k/v1/'
APP_SALES = 238
TOKEN = os.environ.get('KINTONE_API_TOKEN', 'proxy-injected')
JST = datetime.timezone(datetime.timedelta(hours=9))

FIELDS = ['$id', '案件ステータス', '商談者', 'アポ獲得者_プルダウン', '法人名', '見込みランク', '月額単価',
          '商談日時', '商談予定日時', '回答予定日時', 'アポ経路', 'アポ獲得日時', '課金開始日',
          '締結譲渡完了日', '契約期間', 'IS_レコード種別', '更新日時', '屋号']

PIPE_STATUSES = ('時期改め', 'トス', '見込み', '再提案NG', 'ツール提案', 'アポ')
PIPE_FROM = '2023-04-01'   # アポ獲得日がこの日以降の案件だけパイプラインに出す
JUCHU_FROM = '2026-04-01'  # 課金開始日がこの日以降を受注一覧に出す（今期）


def _req(method, path, body=None, params=None):
    url = BASE + path + ('?' + urllib.parse.urlencode(params) if params else '')
    headers = {'X-Cybozu-API-Token': TOKEN}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers['Content-Type'] = 'application/json'
    r = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(r, timeout=120) as f:
        return json.load(f)


def fetch_sales():
    cur = _req('POST', 'records/cursor.json', {'app': APP_SALES, 'fields': FIELDS, 'size': 500})
    rows = []
    while True:
        d = _req('GET', 'records/cursor.json', params={'id': cur['id']})
        for rec in d['records']:
            rows.append({k: v['value'] for k, v in rec.items()})
        if not d['next']:
            return rows


# ---------- helpers ----------
def jst(x):
    if not x:
        return None
    return datetime.datetime.fromisoformat(x.replace('Z', '+00:00')).astimezone(JST)

def ymd(x):
    d = jst(x); return d.strftime('%Y/%m/%d') if d else ''

def ym(x):
    d = jst(x); return d.strftime('%Y-%m') if d else ''

def num(x):
    try: return int(float(x))
    except (TypeError, ValueError): return 0

def sp(x):   # '南原　龍司' -> '南原 龍司'
    return (x or '').replace('　', ' ').strip()

def ns(x):   # '南原　龍司' -> '南原龍司'
    return (x or '').replace('　', '').replace(' ', '').strip()

def rank(x):
    return (x or '').split('（')[0]

def term(r):
    t = r.get('契約期間') or ''
    return int(t) if str(t).isdigit() else 12


# ---------- builders ----------
def is_hp(r):
    return rank(r['見込みランク']) == 'HP受注'


def in_juchu(r):
    """課金開始日が今期以降、または見込みランクが「HP受注」なら受注。"""
    if is_hp(r):
        return True
    return bool(r['課金開始日']) and ymd(r['課金開始日']) >= JUCHU_FROM.replace('-', '/')


def build_juchu(S):
    """課金開始日が入っていれば受注（ステータスは問わない）。見込みランク「HP受注」も受注に含め hp=True を付ける。"""
    rows = [r for r in S if in_juchu(r)]
    rows.sort(key=lambda r: int(r['$id']), reverse=True)
    return [{'person': sp(r['商談者']), 'name': (r['法人名'] or '').strip(), 'price': num(r['月額単価']),
             'kakin_d': ymd(r['課金開始日']), 'keiyaku_d': ymd(r['締結譲渡完了日']),
             'route': r['アポ経路'] or '', 'term': term(r), 'hp': is_hp(r)} for r in rows]


def build_pipe(S):
    """進行中の案件。課金開始日が入ったもの（=受注）は除く。"""
    rows = [r for r in S if r['案件ステータス'] in PIPE_STATUSES and r['アポ獲得日時']
            and ymd(r['アポ獲得日時']) >= PIPE_FROM.replace('-', '/') and not in_juchu(r)]
    rows.sort(key=lambda r: (r['アポ獲得日時'], int(r['$id'])), reverse=True)
    return [{'person': sp(r['商談者']), 'apo_person': sp(r['アポ獲得者_プルダウン']), 'status': r['案件ステータス'],
             'name': (r['法人名'] or '').strip(), 'rank': rank(r['見込みランク']), 'price': num(r['月額単価']),
             'shodan_d': ymd(r['商談日時']), 'ans_d': ymd(r['回答予定日時']), 'route': r['アポ経路'] or ''} for r in rows]


MAIN = ('南原龍司', '田中莉奈', '中岡世里菜', '高橋広輝')
WINDOW_FROM = '2023-04-01'  # KPI はアポ獲得日がこの日以降のレコードで集計
ROUTE_FROM = '2024-04-01'   # 問い合わせ・SWW 一覧はアポ獲得日がこの日以降


def in_window(r, since):
    return bool(r['アポ獲得日時']) and ymd(r['アポ獲得日時']) >= since.replace('-', '/')


def build_kpi(S):
    """月×担当（商談者）ごとのアポ・商談・契約・売上・見込み・課金開始の件数。"""
    W = [r for r in S if in_window(r, WINDOW_FROM)]
    out = {}

    def add(m, p, k, v=1):
        if not m or p not in MAIN:
            return
        d = out.setdefault(m, {}).setdefault(p, {'apo': 0, 'shodan': 0, 'keiyaku': 0, 'uriage': 0,
                                                 'price_sum': 0, 'mikomi': 0, 'kakin': 0})
        d[k] += v

    for r in W:
        p = ns(r['商談者'])
        agency = r['案件ステータス'] == '代理店系'
        if not agency:
            add(ym(r['アポ獲得日時']), p, 'apo')
            add(ym(r['商談日時']), p, 'shodan')
        if r['締結譲渡完了日']:
            m = ym(r['締結譲渡完了日'])
            add(m, p, 'keiyaku'); add(m, p, 'uriage', num(r['月額単価']) * term(r)); add(m, p, 'price_sum', num(r['月額単価']))
        if r['課金開始日']:
            add(ym(r['課金開始日']), p, 'kakin')
        if r['案件ステータス'] == '見込み' and not in_juchu(r):
            add(ym(r['商談日時']), p, 'mikomi')
    return {m: out[m] for m in sorted(out)}


def build_route(S):
    """問い合わせ・SWW（展示会）経由の案件一覧。"""
    rows = [r for r in S if r['アポ経路'] in ('問い合わせ', 'SWW') and in_window(r, ROUTE_FROM)
            and ns(r['商談者']) in MAIN and r['案件ステータス'] != '代理店系']
    rows.sort(key=lambda r: (r['アポ獲得日時'], int(r['$id'])), reverse=True)
    return [{'person': ns(r['商談者']), 'route': r['アポ経路'], 'status': r['案件ステータス'],
             'name': (r.get('屋号') or '').strip() or (r['法人名'] or '').strip(), 'rank': rank(r['見込みランク']),
             'price': num(r['月額単価']), 'shodan_d': ymd(r['商談日時']), 'shodan_yotei': ymd(r['商談予定日時']),
             'ans_d': ymd(r['回答予定日時'])} for r in rows]


def replace_const(html, name, value):
    pat = re.compile(r'(const ' + name + r' = )(.*?)(;\n)', re.S)
    if not pat.search(html):
        raise SystemExit(f'{name} が見つかりません')
    return pat.sub(lambda m: m.group(1) + json.dumps(value, ensure_ascii=False) + m.group(3), html, count=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html')
    ap.add_argument('--records', help='取得済みの営業マスタJSON（テスト用）')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    S = json.load(open(a.records, encoding='utf-8')) if a.records else fetch_sales()
    if len(S) < 1000:
        raise SystemExit(f'営業マスタの件数が少なすぎます（{len(S)}件）。取得に失敗した可能性があるため中止します')
    data = {'STATIC_KPI': build_kpi(S), 'STATIC_PIPE': build_pipe(S),
            'STATIC_JUCHU': build_juchu(S), 'STATIC_ROUTE_DATA': build_route(S)}
    html = open(a.html, encoding='utf-8').read()
    new = html
    for k, v in data.items():
        new = replace_const(new, k, v)
    now = datetime.datetime.now(JST)
    new = re.sub(r"document\.getElementById\('updAt'\)\.textContent='[^']*';",
                 "document.getElementById('updAt').textContent='🗓 最終更新: %d年%d月%d日 %s（自動更新）';"
                 % (now.year, now.month, now.day, now.strftime('%H:%M')), new, count=1)
    summary = {k: len(v) for k, v in data.items()}
    mik = [p for p in data['STATIC_PIPE'] if p['status'] == '見込み']
    summary['見込み'] = len(mik)
    summary['見込み月額合計'] = sum(p['price'] for p in mik)
    summary['HP受注'] = sum(1 for j in data['STATIC_JUCHU'] if j.get('hp'))
    print(json.dumps(summary, ensure_ascii=False))
    if a.dry_run:
        return
    with open(a.html, 'w', encoding='utf-8') as f:
        f.write(new)


if __name__ == '__main__':
    main()
