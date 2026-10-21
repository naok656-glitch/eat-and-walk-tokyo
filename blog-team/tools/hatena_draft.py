#!/usr/bin/env python3
"""はてなブログ(くらしの買い物ノート)に記事を保存する。標準は「下書き」、--publish を付けたときだけ公開する。

使い方:
  python3 hatena_draft.py list                     最新の記事一覧(タイトル・下書きかどうか)
  python3 hatena_draft.py post <article.html> --title "タイトル" [--category カテゴリ ...] [--publish]
                                                   本文HTMLを下書き(--publish なら公開)で保存し、URLを表示

必要な環境変数: HATENA_API_KEY(クラウド環境「インスタ活用」に設定済み。新しいセッションでのみ読み込まれる)
ネットワーク: blog.hatena.ne.jp の許可が必要
"""
import argparse
import base64
import os
import re
import sys
import urllib.request
from xml.sax.saxutils import escape

HATENA_ID = "naoki656"
BLOG_ID = "oyakudachi11111.hatenablog.com"
ENDPOINT = f"https://blog.hatena.ne.jp/{HATENA_ID}/{BLOG_ID}/atom/entry"


def request(method, url, body=None):
    auth = base64.b64encode(f"{HATENA_ID}:{os.environ['HATENA_API_KEY']}".encode()).decode()
    req = urllib.request.Request(url, data=body, method=method,
                                 headers={"Authorization": "Basic " + auth, "Content-Type": "application/xml; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode()


def list_entries():
    xml = request("GET", ENDPOINT)
    for entry in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        title = re.search(r"<title>(.*?)</title>", entry, re.S)
        draft = "<app:draft>yes</app:draft>" in entry
        url = re.search(r'<link rel="alternate" type="text/html" href="([^"]+)"', entry)
        print(("[下書き] " if draft else "[公開]   ") + (title.group(1) if title else "") + ("" if draft or not url else "  " + url.group(1)))


def post(path, title, categories, publish=False):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    cats = "".join(f'<category term="{escape(c)}" />' for c in categories)
    body = f"""<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://www.w3.org/2005/Atom" xmlns:app="http://www.w3.org/2007/app">
  <title>{escape(title)}</title>
  <content type="text/html">{escape(content)}</content>
  {cats}
  <app:control><app:draft>{'no' if publish else 'yes'}</app:draft></app:control>
</entry>""".encode("utf-8")
    xml = request("POST", ENDPOINT, body)
    expected = "<app:draft>no</app:draft>" if publish else "<app:draft>yes</app:draft>"
    if expected not in xml:
        sys.exit("意図した状態(公開/下書き)で保存されたことを確認できませんでした。はてなブログの記事の管理画面を確認してください")
    url = re.search(r'<link rel="alternate" type="text/html" href="([^"]+)"', xml)
    print(("公開しました: " if publish else "下書きを保存しました: ") + title)
    if url:
        print("記事URL:", url.group(1))
    if not publish:
        print("確認・公開はこちら: https://blog.hatena.ne.jp/naoki656/oyakudachi11111.hatenablog.com/entries?status=draft")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["list", "post"])
    ap.add_argument("path", nargs="?")
    ap.add_argument("--title")
    ap.add_argument("--category", action="append", default=[])
    ap.add_argument("--publish", action="store_true")
    a = ap.parse_args()
    if a.cmd == "list":
        list_entries()
    else:
        if not (a.path and a.title):
            sys.exit("post には本文ファイルと --title が必要です")
        post(a.path, a.title, a.category, a.publish)
