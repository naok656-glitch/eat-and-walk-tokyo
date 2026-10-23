"""index.csv を実ファイルから再生成。manifest(09/stock)があればそれのメタ情報を使う。"""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
meta = {}
for m in ROOT.glob("**/_manifest*.csv"):
    for r in csv.DictReader(open(m, encoding="utf-8")):
        meta[r["file"]] = r
rows = []
for p in sorted(ROOT.glob("0*/*")):
    if p.suffix.lower() not in {".jpg",".png",".webm"}: continue
    rel = p.relative_to(ROOT).as_posix(); m = meta.get(rel, {})
    rows.append([rel, p.parent.name, m.get("type") or m.get("category") or p.suffix[1:], m.get("text") or m.get("query",""), m.get("author","自作(Pillowコード生成)" if rel.startswith("09") else ""), m.get("license","自作/IPAフォント(再配布可)" if rel.startswith("09") else ""), m.get("source_url",""), "3s" ])
with open(ROOT / "index.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["file","folder","type","keyword_or_text","author","license","source_url","use_duration"]); w.writerows(rows)
tgt = {"01_money":20,"02_car":20,"03_house":20,"04_job":20,"05_izakaya_food":40,"06_police_legal":40,"07_city_news":40,"08_bb_characters":80,"09_telop_fukidashi_effect":80}
from collections import Counter
c = Counter(r[1] for r in rows)
print(len(rows), "files"); [print(f"{k:28s}{c.get(k,0):3d}/{v}") for k,v in tgt.items()]
