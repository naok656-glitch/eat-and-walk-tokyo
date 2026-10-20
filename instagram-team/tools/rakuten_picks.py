#!/usr/bin/env python3
"""楽天市場の商品検索APIで「選び方」ごとのおすすめを探し、docs/index.html(まとめページ)を作る。

使い方:
  python3 rakuten_picks.py           picks.json の各テーマを検索して docs/index.html を書き出す
  python3 rakuten_picks.py --sample  APIを呼ばず、見本データでページの見た目だけ確認する

必要な環境変数(クラウド環境「インスタ活用」に設定済み。新しいセッションでのみ読み込まれる):
  RAKUTEN_APP_ID, RAKUTEN_ACCESS_KEY, RAKUTEN_AFFILIATE_ID
"""
import html
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PICKS = os.path.join(HERE, "..", "picks", "picks.json")
OUT = os.path.join(ROOT, "docs", "index.html")
API = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260701"
SITE = "https://naok656-glitch.github.io"
JST = timezone(timedelta(hours=9))


def search(keyword, rule):
    params = {
        "applicationId": os.environ["RAKUTEN_APP_ID"],
        "accessKey": os.environ["RAKUTEN_ACCESS_KEY"],
        "affiliateId": os.environ["RAKUTEN_AFFILIATE_ID"],
        "keyword": keyword,
        "hits": 30,
        "sort": "-reviewCount",
        "availability": 1,
        "format": "json",
    }
    req = urllib.request.Request(f"{API}?{urllib.parse.urlencode(params)}",
                                 headers={"Referer": SITE + "/", "Origin": SITE})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    items = [i.get("Item", i) for i in data.get("Items", [])]
    ok = [i for i in items
          if int(i.get("reviewCount") or 0) >= rule["min_reviews"]
          and float(i.get("reviewAverage") or 0) >= rule["min_rating"]
          and i.get("affiliateUrl")]
    return ok[: rule["per_theme"]]


def image_of(item):
    imgs = item.get("mediumImageUrls") or []
    if not imgs:
        return ""
    first = imgs[0]
    return first.get("imageUrl", "") if isinstance(first, dict) else str(first)


def card(item):
    e = html.escape
    name = e(item.get("itemName", ""))
    price = int(item.get("itemPrice") or 0)
    img = image_of(item)
    return f"""<article class="item">
  {f'<img src="{e(img)}" alt="" loading="lazy" width="128" height="128">' if img else ''}
  <div class="body">
    <h3>{name}</h3>
    <p class="meta">{price:,}円(税込・取得時点) / レビュー {e(str(item.get("reviewAverage", "")))}({int(item.get("reviewCount") or 0):,}件) / {e(item.get("shopName", ""))}</p>
    <a class="btn" href="{e(item["affiliateUrl"])}" rel="sponsored nofollow noopener" target="_blank">楽天市場で見る</a>
  </div>
</article>"""


def render(config, results, fetched_at):
    e = html.escape
    sections = []
    for t in config["themes"]:
        cards = "\n".join(card(i) for i in results.get(t["id"], []))
        if not cards:
            cards = '<p class="empty">条件に合う商品が見つかりませんでした(次回の更新で再検索します)。</p>'
        sections.append(f"""<section id="{e(t["id"])}">
  <h2>{e(t["title"])}</h2>
  <p class="lead">{e(t["note"])}</p>
  {cards}
</section>""")
    nav = " ".join(f'<a href="#{e(t["id"])}">{e(t["title"])}</a>' for t in config["themes"])
    rule = config["rule"]
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(config["page_title"])}</title>
<style>
:root {{ --bg:#FBF7F0; --card:#fff; --ink:#2B2B2B; --muted:#6B6459; --accent:#2F7D7A; --soft:#DCEDEB; --line:#E6DED1; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#1C1F1E; --card:#262A29; --ink:#EDE8DF; --muted:#A8A196; --accent:#6FC2BD; --soft:#2A3D3B; --line:#3A3F3D; }} }}
body {{ margin:0; background:var(--bg); color:var(--ink); font-family:"Noto Sans JP",system-ui,sans-serif; line-height:1.7; }}
.wrap {{ max-width:680px; margin:0 auto; padding:24px 16px 48px; }}
.pr {{ display:inline-block; font-size:.8rem; font-weight:700; background:var(--accent); color:var(--bg); padding:2px 10px; border-radius:999px; }}
h1 {{ font-size:1.5rem; margin:8px 0 4px; }}
.disclosure {{ font-size:.85rem; color:var(--muted); }}
nav {{ display:flex; flex-wrap:wrap; gap:8px; margin:16px 0 8px; }}
nav a {{ background:var(--soft); color:var(--accent); padding:6px 12px; border-radius:999px; text-decoration:none; font-weight:700; font-size:.9rem; }}
h2 {{ font-size:1.2rem; margin:32px 0 4px; }}
.lead {{ color:var(--muted); margin:0 0 12px; }}
.item {{ display:flex; gap:12px; background:var(--card); border:1px solid var(--line); border-radius:16px; padding:12px; margin-bottom:12px; }}
.item img {{ width:96px; height:96px; object-fit:contain; border-radius:8px; background:#fff; flex:none; }}
.body {{ min-width:0; }}
h3 {{ font-size:.95rem; margin:0 0 4px; overflow-wrap:anywhere; display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical; overflow:hidden; }}
.meta {{ font-size:.8rem; color:var(--muted); margin:0 0 8px; }}
.btn {{ display:inline-block; background:var(--accent); color:var(--bg); padding:6px 14px; border-radius:10px; text-decoration:none; font-weight:700; font-size:.9rem; }}
footer {{ margin-top:32px; font-size:.8rem; color:var(--muted); }}
</style>
</head>
<body><div class="wrap">
<span class="pr">PR</span>
<h1>{e(config["page_title"])}</h1>
<p class="disclosure">このページは楽天アフィリエイトを利用しています。リンクから購入されると、運営者に紹介料が入ることがあります。商品は「レビュー{rule["min_reviews"]}件以上・評価{rule["min_rating"]}以上」の条件で自動で選んでいます。運営者が実際に使ったものではありません。</p>
<nav>{nav}</nav>
{"".join(sections)}
<footer>価格・在庫・レビューは {fetched_at} 時点の楽天市場の情報です。最新の内容は各商品ページで確認してください。<br>くらしの買い物ノート(Instagram @kurashi_kaimono)</footer>
</div></body></html>
"""


def main():
    with open(PICKS, encoding="utf-8") as f:
        config = json.load(f)
    results = {}
    if "--sample" in sys.argv:
        sample = {"itemName": "見本の商品名(実在しません)", "itemPrice": 9999, "reviewAverage": 4.5, "reviewCount": 1234,
                  "shopName": "見本ショップ", "affiliateUrl": "https://example.com/", "mediumImageUrls": []}
        results = {t["id"]: [sample] for t in config["themes"]}
    else:
        for t in config["themes"]:
            results[t["id"]] = search(t["keyword"], config["rule"])
            print(f"{t['id']}: {len(results[t['id']])}件")
            time.sleep(1.5)  # 楽天APIの1秒あたりの上限に配慮
    fetched_at = datetime.now(JST).strftime("%Y年%m月%d日")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(render(config, results, fetched_at))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
