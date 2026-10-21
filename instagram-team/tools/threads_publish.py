#!/usr/bin/env python3
"""Threads API でテキスト投稿(リンク添付つき)をする。Instagram の ig_publish.py と同じ考え方。

使い方:
  python3 threads_publish.py check            接続確認(投稿しない)
  python3 threads_publish.py due [--dry-run]  threads/schedule.json のうち、承認済み・時刻を過ぎた・未投稿の分を投稿

認証:
  クラウド環境のネットワークシークレット(Bearer、許可ウェブサイト graph.threads.net)が
  Authorization ヘッダーを自動で付ける。スクリプトはトークンを持たない。
  環境変数 THREADS_ACCESS_TOKEN がある場合だけ、それを access_token として送る(予備)。

二重投稿の防止:
  記録(schedule.json)を保存できない環境でも、直近の投稿に同じ書き出しの投稿があれば投稿しない。
  予定から3日以上過ぎた未記録分は投稿しない。
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

API = "https://graph.threads.net/v1.0"
HERE = os.path.dirname(os.path.abspath(__file__))
SCHEDULE = os.path.join(HERE, "..", "threads", "schedule.json")
JST = timezone(timedelta(hours=9))
MAX_CHARS = 500  # Threads の本文上限(公式ドキュメントで要確認)


def call(method, path, **params):
    if os.environ.get("THREADS_ACCESS_TOKEN"):
        params["access_token"] = os.environ["THREADS_ACCESS_TOKEN"]
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{path}"
    req = urllib.request.Request(f"{url}?{data.decode()}") if method == "GET" else urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"API error {e.code}: {e.read().decode()[:500]}")


def check():
    me = call("GET", "me", fields="id,username")
    print(f"username={me.get('username')} id={me.get('id')}")


def already_posted(text):
    head = text.strip()[:60]
    for m in call("GET", "me/threads", fields="id,text", limit=50).get("data", []):
        if (m.get("text") or "").strip()[:60] == head:
            return m["id"]
    return None


def publish(text, link=None):
    params = {"media_type": "TEXT", "text": text}
    if link:
        params["link_attachment"] = link
    cid = call("POST", "me/threads", **params)["id"]
    time.sleep(5)  # 公式の推奨は公開前に少し待つこと
    return call("POST", "me/threads_publish", creation_id=cid)["id"]


def due(dry_run):
    with open(SCHEDULE, encoding="utf-8") as f:
        sched = json.load(f)
    now = datetime.now(JST)
    targets = [p for p in sched["posts"]
               if p.get("approved") and not p.get("published_id") and datetime.fromisoformat(p["at"]) <= now]
    for p in [p for p in targets if now - datetime.fromisoformat(p["at"]) > timedelta(days=3)]:
        print(f"要確認: {p['id']} は予定から3日以上過ぎても記録がないため投稿しない")
        targets.remove(p)
    if not targets:
        print("投稿対象なし")
        return
    for p in targets:
        text = p["text"].strip()
        if len(text) > MAX_CHARS:
            print(f"飛ばす {p['id']}: {len(text)}文字で上限超え")
            continue
        if dry_run:
            print(f"[dry-run] {p['at']} {p['id']} {len(text)}文字 link={p.get('link')}")
            continue
        existing = already_posted(text)
        pid = existing or publish(text, p.get("link"))
        p["published_id"] = pid
        p["published_at"] = datetime.now(JST).isoformat(timespec="minutes")
        print(("投稿済みのため記録だけ更新 " if existing else "投稿完了 ") + f"{p['id']} id={pid}")
        with open(SCHEDULE, "w", encoding="utf-8") as f:
            json.dump(sched, f, ensure_ascii=False, indent=2)
            f.write("\n")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "check":
        check()
    elif cmd == "due":
        due("--dry-run" in sys.argv)
    else:
        print(__doc__)
