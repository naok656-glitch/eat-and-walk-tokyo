"""01-07 の素材取得。実写=Pixabay/Pexels API、イラスト=Pollinations(irasutoya style)。
使い方: python3 tools/fetch_stock.py   (リポジトリ直下の .env に PIXABAY_API_KEY / PEXELS_API_KEY)
3種混ぜ: 各フォルダ 実写50% / イラスト50% を目安(3秒ごとに種類が変わる)。
商用NG対策: Pixabay=Pixabay License, Pexels=Pexels License(商用可)のみ。取得元URL・作者・ライセンスを index に記録。
人物の顔が主役の写真・ロゴ・ブランド・実在報道写真は検索語から外す。
"""
import csv, os, sys, time, urllib.parse
from pathlib import Path
import requests
from PIL import Image
from io import BytesIO

ROOT = Path(__file__).resolve().parents[1]
def load_env():
    for p in (ROOT.parent / ".env", ROOT / ".env"):
        if p.exists():
            for l in p.read_text().splitlines():
                if "=" in l and not l.startswith("#"):
                    k, v = l.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"\''))
load_env()
PIX, PEX = os.getenv("PIXABAY_API_KEY"), os.getenv("PEXELS_API_KEY")

PLAN = {  # folder: (枚数, [(検索語 英, イラスト用プロンプト)])
 "01_money": (20, ["coins","banknotes yen","wallet","piggy bank","calculator","savings"]),
 "02_car": (20, ["car","driving","parking","road","traffic","gas station"]),
 "03_house": (20, ["house","apartment","living room","kitchen","key","real estate"]),
 "04_job": (20, ["office work","laptop work","interview","meeting","commute train","factory worker"]),
 "05_izakaya_food": (40, ["izakaya","yakitori","sushi","ramen","beer glass","tempura","japanese food","tokyo street food"]),
 "06_police_legal": (40, ["police car","gavel","law book","handcuffs","court","document stamp","traffic sign","caution tape"]),
 "07_city_news": (40, ["tokyo skyline","shibuya crossing","train station","newspaper","city night","tokyo tower","crowd walking","rain city"]),
}
def photo_pixabay(q, n):
    r = requests.get("https://pixabay.com/api/", params={"key": PIX, "q": q, "image_type": "photo", "per_page": max(n,3), "safe": "true", "orientation": "horizontal"}, timeout=30).json()
    for h in r.get("hits", [])[:n]:
        yield h["largeImageURL"], f"pixabay:{h['id']}", h["user"], "Pixabay License(商用可)", h["pageURL"]
def photo_pexels(q, n):
    r = requests.get("https://api.pexels.com/v1/search", params={"query": q, "per_page": n, "orientation": "landscape"}, headers={"Authorization": PEX}, timeout=30).json()
    for h in r.get("photos", []):
        yield h["src"]["large2x"], f"pexels:{h['id']}", h["photographer"], "Pexels License(商用可)", h["url"]
def illust(q, seed):
    p = f"irasutoya style, flat cute japanese clip art illustration of {q}, simple, white background, no text, no logo"
    return "https://image.pollinations.ai/prompt/" + urllib.parse.quote(p) + f"?width=1280&height=720&nologo=true&seed={seed}", f"pollinations:seed{seed}", "AI generated", "Pollinations生成(商用可・出力は自己責任確認)", "https://pollinations.ai"

def main():
    rows = []
    for folder, (total, qs) in PLAN.items():
        out = ROOT / folder; out.mkdir(exist_ok=True); i = 0
        half = total // 2
        per = max(1, -(-half // len(qs)))
        for q in qs:
            srcs = []
            if PIX: srcs += list(photo_pixabay(q, per))
            if PEX: srcs += list(photo_pexels(q, per))
            srcs = srcs[:per]
            for s in range(per): srcs.append(illust(q, 1000 + len(rows) + s))
            for url, sid, author, lic, page in srcs:
                if i >= total: break
                try:
                    b = requests.get(url, timeout=90).content; im = Image.open(BytesIO(b)).convert("RGB"); im.thumbnail((1920, 1080))
                    i += 1; kind = "illust" if sid.startswith("pollinations") else "photo"
                    fn = f"{folder[:2]}_{kind}_{i:03d}.jpg"; im.save(out / fn, quality=88)
                    rows.append([f"{folder}/{fn}", folder, kind, q, sid, author, lic, page])
                except Exception as e:
                    print("skip", url, e, file=sys.stderr)
                time.sleep(0.3)
        print(folder, i, "/", total)
    with open(ROOT / "_manifest_stock.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([["file","folder","type","query","source_id","author","license","source_url"]] + rows)
if __name__ == "__main__":
    if not (PIX or PEX): sys.exit("PIXABAY_API_KEY / PEXELS_API_KEY が見つかりません (.env)")
    main()
