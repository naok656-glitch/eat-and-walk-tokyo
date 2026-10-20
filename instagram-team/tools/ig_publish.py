#!/usr/bin/env python3
"""Instagram API(Instagramログイン版)でリールを投稿する。

使い方:
  python3 ig_publish.py check            トークンとアカウントを確認(投稿しない)
  python3 ig_publish.py due [--dry-run]  schedule.json のうち、承認済みで予約時刻を過ぎた未投稿のものを投稿
                                         (mode が "manual" のものは本人がアプリで予約したものとして飛ばす)

認証:
  クラウド環境の「シークレット」(Bearer、許可ウェブサイト graph.instagram.com)に入れたトークンを、
  通信の途中で Authorization ヘッダーとして自動で付ける。スクリプトはトークンを持たない。
  環境変数 IG_ACCESS_TOKEN がある場合だけ、それを access_token として送る(予備の方法)。
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

API = "https://graph.instagram.com/v23.0"  # バージョンは公式ドキュメントで要確認
HERE = os.path.dirname(os.path.abspath(__file__))
SCHEDULE = os.path.join(HERE, "..", "reels", "schedule.json")
JST = timezone(timedelta(hours=9))


def call(method, path, **params):
    if os.environ.get("IG_ACCESS_TOKEN"):
        params["access_token"] = os.environ["IG_ACCESS_TOKEN"]
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{path}"
    if method == "GET":
        req = urllib.request.Request(f"{url}?{data.decode()}")
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        # エラー本文にトークンは含まれないが、念のためURLは表示しない
        raise SystemExit(f"API error {e.code}: {e.read().decode()[:500]}")


def check():
    me = call("GET", "me", fields="user_id,username,account_type")
    print(f"username={me.get('username')} account_type={me.get('account_type')} user_id={me.get('user_id')}")
    limit = call("GET", f"{me['user_id']}/content_publishing_limit", fields="quota_usage,config")
    print(f"publishing_limit={json.dumps(limit.get('data'), ensure_ascii=False)}")


def publish_reel(user_id, video_url, caption):
    container = call("POST", f"{user_id}/media", media_type="REELS", video_url=video_url, caption=caption, share_to_feed="true")
    cid = container["id"]
    for wait in [10, 15, 20, 30, 30, 60, 60, 120, 120, 180]:
        time.sleep(wait)
        status = call("GET", cid, fields="status_code,status")
        if status.get("status_code") == "FINISHED":
            break
        if status.get("status_code") in ("ERROR", "EXPIRED"):
            raise SystemExit(f"container {cid} failed: {status}")
    else:
        raise SystemExit(f"container {cid} not finished in time")
    media = call("POST", f"{user_id}/media_publish", creation_id=cid)
    return media["id"]


def due(dry_run):
    with open(SCHEDULE, encoding="utf-8") as f:
        sched = json.load(f)
    now = datetime.now(JST)
    targets = [p for p in sched["posts"]
               if p.get("approved") and not p.get("published_media_id") and p.get("mode") != "manual"
               and datetime.fromisoformat(p["at"]) <= now]
    if not targets:
        print("投稿対象なし")
        return
    user_id = None if dry_run else call("GET", "me", fields="user_id")["user_id"]
    for p in targets:
        with open(os.path.join(HERE, "..", "reels", p["dir"], "caption.txt"), encoding="utf-8") as f:
            caption = f.read().strip()
        video_url = sched["video_base_url"] + f"{p['dir']}/reel.mp4"
        if dry_run:
            print(f"[dry-run] {p['at']} {p['dir']} {video_url} caption={len(caption)}文字")
            continue
        media_id = publish_reel(user_id, video_url, caption)
        p["published_media_id"] = media_id
        p["published_at"] = datetime.now(JST).isoformat(timespec="minutes")
        print(f"投稿完了 {p['dir']} media_id={media_id}")
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
