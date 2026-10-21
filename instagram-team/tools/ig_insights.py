#!/usr/bin/env python3
"""Instagramの成績を集計して、reports/YYYYMMDD.md に書き出す(週次レポート)。

使い方: python3 ig_insights.py
認証は ig_publish.py と同じ(クラウド環境のシークレットが graph.instagram.com に自動で付ける)。
"""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

API = "https://graph.instagram.com/v23.0"
METRICS = ["views", "reach", "saved", "shares", "likes", "comments", "ig_reels_avg_watch_time"]
HERE = os.path.dirname(os.path.abspath(__file__))
JST = timezone(timedelta(hours=9))


def get(path, **params):
    with urllib.request.urlopen(f"{API}/{path}?{urllib.parse.urlencode(params)}", timeout=30) as r:
        return json.load(r)


def metric(media_id, name):
    try:
        return get(f"{media_id}/insights", metric=name)["data"][0]["values"][0]["value"]
    except Exception:
        return None  # 取れない指標は空欄にする(推測で埋めない)


def main():
    account = get("me", fields="username,followers_count,media_count")
    media = get("me/media", fields="id,caption,timestamp,permalink,media_product_type", limit=50).get("data", [])
    rows = []
    for m in media:
        v = {k: metric(m["id"], k) for k in METRICS}
        title = (m.get("caption") or "").splitlines()[0][:30]
        posted = datetime.fromisoformat(m["timestamp"].replace("+0000", "+00:00")).astimezone(JST).strftime("%m/%d")
        views, saved = v["views"] or 0, v["saved"] or 0
        rows.append((posted, title, v, f"{saved / views * 100:.1f}%" if views else "-"))
    today = datetime.now(JST)
    lines = [f"# Instagram週次レポート({today:%Y-%m-%d})", "",
             f"アカウント: @{account.get('username')} / フォロワー {account.get('followers_count')} / 投稿 {account.get('media_count')}", "",
             "| 投稿日 | 冒頭 | 再生 | リーチ | 保存 | 保存率 | シェア | いいね | コメント | 平均視聴(秒) |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for posted, title, v, rate in rows:
        avg = f"{v['ig_reels_avg_watch_time'] / 1000:.1f}" if v["ig_reels_avg_watch_time"] is not None else "-"
        lines.append(f"| {posted} | {title} | {v['views']} | {v['reach']} | {v['saved']} | {rate} | {v['shares']} | {v['likes']} | {v['comments']} | {avg} |")
    lines += ["", "数値はInstagram APIから取得した値。空欄(None)は取得できなかった指標。投稿数が少ないうちは傾向を断定しない。"]
    out_dir = os.path.join(HERE, "..", "reports")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{today:%Y%m%d}.md")
    for path in (out, os.path.join(out_dir, "latest.md")):  # latest.md は週次戦略会議が読む
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
