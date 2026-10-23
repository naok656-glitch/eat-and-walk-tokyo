"""09_telop_fukidashi_effect: 80枚をPillowでコード生成（透過PNG 1280x720）。
ルール: 短文字(最大8字)・黄色文字+黒フチ・文字だらけ禁止。
"""
import math, random, csv, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "assets_library/09_telop_fukidashi_effect")
OUT.mkdir(parents=True, exist_ok=True)
FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"  # IPA Font License (再配布可)
W, H = 1280, 720
YELLOW, BLACK, WHITE, RED = (255, 230, 0, 255), (0, 0, 0, 255), (255, 255, 255, 255), (230, 30, 30, 255)
rows = []

def font(sz): return ImageFont.truetype(FONT, sz)

def canvas(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))

def fit(draw, text, maxw, start=220):
    s = start
    while s > 40:
        b = draw.textbbox((0, 0), text, font=font(s), stroke_width=s // 8)
        if b[2] - b[0] <= maxw: return s
        s -= 6
    return s

def telop(text, fill=YELLOW, stroke=BLACK, pos=(W // 2, H // 2), maxw=1100, rot=0, start=220):
    im = canvas(); d = ImageDraw.Draw(im)
    s = fit(d, text, maxw, start)
    d.text(pos, text, font=font(s), fill=fill, stroke_width=max(6, s // 8), stroke_fill=stroke, anchor="mm")
    return im.rotate(rot, resample=Image.BICUBIC, center=(W // 2, H // 2)) if rot else im

def bubble(kind, text, fill=WHITE, tc=BLACK):
    im = canvas(); d = ImageDraw.Draw(im)
    box = (140, 120, 1140, 520)
    if kind == "round":
        d.ellipse(box, fill=fill, outline=BLACK, width=10)
        d.polygon([(420, 480), (330, 640), (560, 510)], fill=fill, outline=BLACK)
        d.ellipse((400, 470, 540, 515), fill=fill)
    elif kind == "rect":
        d.rounded_rectangle(box, 60, fill=fill, outline=BLACK, width=10)
        d.polygon([(800, 505), (900, 650), (900, 505)], fill=fill, outline=BLACK)
        d.rectangle((806, 500, 894, 512), fill=fill)
    elif kind == "shout":
        cx, cy, pts = 640, 320, []
        for i in range(32):
            a = math.pi * 2 * i / 32; r = 500 if i % 2 == 0 else 380
            pts.append((cx + r * math.cos(a) * 1.05, cy + r * math.sin(a) * 0.62))
        d.polygon(pts, fill=fill, outline=BLACK, width=10)
    elif kind == "cloud":
        for x, y in [(300, 250), (480, 170), (700, 170), (900, 250), (900, 400), (700, 470), (480, 470), (300, 400)]:
            d.ellipse((x - 130, y - 110, x + 130, y + 110), fill=fill, outline=BLACK, width=10)
        d.rectangle((300, 200, 900, 450), fill=fill)
        for x, y, r in [(380, 560, 40), (320, 630, 24), (280, 680, 14)]:
            d.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=BLACK, width=8)
    elif kind == "box":
        d.rectangle(box, fill=fill, outline=BLACK, width=12)
        d.rectangle((160, 140, 1120, 500), outline=BLACK, width=4)
    s = fit(d, text, 800, 190)
    d.text((640, 320), text, font=font(s), fill=tc, stroke_width=0, anchor="mm")
    return im

def star(d, cx, cy, r, n=5, fill=YELLOW, outline=BLACK):
    pts = []
    for i in range(n * 2):
        a = -math.pi / 2 + math.pi * i / n; rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill, outline=outline, width=6)

def arrow(direction, col=RED):
    im = canvas(); d = ImageDraw.Draw(im)
    base = [(-300, -70), (60, -70), (60, -170), (320, 0), (60, 170), (60, 70), (-300, 70)]
    ang = {"right": 0, "down": 90, "left": 180, "up": 270, "diag_dr": 45, "diag_ur": 315}[direction]
    c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = [(640 + x * c - y * s_, 360 + x * s_ + y * c) for x, y in base]
    d.polygon(pts, fill=col, outline=BLACK, width=10)
    return im

def effect(kind):
    im = canvas(); d = ImageDraw.Draw(im); rnd = random.Random(hash(kind) & 0xffff)
    if kind == "radial_lines":
        for i in range(60):
            a = math.pi * 2 * i / 60; d.line([(640 + 220 * math.cos(a), 360 + 220 * math.sin(a)), (640 + 900 * math.cos(a), 360 + 900 * math.sin(a))], fill=BLACK, width=6)
    elif kind == "focus_lines":
        for i in range(90):
            a = math.pi * 2 * i / 90; w = rnd.randint(3, 14)
            d.line([(640 + 700 * math.cos(a), 360 + 700 * math.sin(a)), (640 + 1100 * math.cos(a), 360 + 1100 * math.sin(a))], fill=(0, 0, 0, 230), width=w)
    elif kind == "stars":
        for _ in range(9): star(d, rnd.randint(100, 1180), rnd.randint(80, 640), rnd.randint(40, 90))
    elif kind == "sparkle":
        for _ in range(14):
            x, y, r = rnd.randint(80, 1200), rnd.randint(60, 660), rnd.randint(20, 60)
            d.polygon([(x, y - r), (x + r / 4, y - r / 4), (x + r, y), (x + r / 4, y + r / 4), (x, y + r), (x - r / 4, y + r / 4), (x - r, y), (x - r / 4, y - r / 4)], fill=WHITE, outline=(255, 210, 0, 255), width=3)
    elif kind == "sweat":
        for x, y in [(900, 200), (980, 300), (850, 320)]:
            d.polygon([(x, y - 70), (x + 40, y + 20), (x, y + 60), (x - 40, y + 20)], fill=(120, 200, 255, 255), outline=BLACK, width=6)
    elif kind == "anger":
        d.line([(500, 250), (640, 250), (640, 130)], fill=RED, width=22); d.line([(780, 250), (640, 250), (640, 370)], fill=RED, width=22)
        d.line([(500, 250), (640, 250), (640, 370)], fill=RED, width=22); d.line([(780, 250), (640, 250), (640, 130)], fill=RED, width=22)
    elif kind == "heart":
        d.ellipse((470, 220, 650, 400), fill=RED, outline=BLACK, width=8); d.ellipse((630, 220, 810, 400), fill=RED, outline=BLACK, width=8)
        d.polygon([(480, 340), (800, 340), (640, 560)], fill=RED, outline=BLACK, width=8); d.rectangle((500, 300, 780, 350), fill=RED)
    elif kind == "exclaim":
        d.polygon([(590, 120), (690, 120), (670, 440), (610, 440)], fill=RED, outline=BLACK, width=10); d.ellipse((590, 480, 690, 580), fill=RED, outline=BLACK, width=10)
    elif kind == "question":
        d.arc((520, 120, 760, 340), 160, 440, fill=RED, width=44); d.line([(640, 330), (640, 430)], fill=RED, width=44); d.ellipse((605, 490, 675, 560), fill=RED)
    elif kind == "bang":
        for i in range(16):
            a = math.pi * 2 * i / 16; r = 330 if i % 2 == 0 else 150
            pass
        pts = [(640 + (330 if i % 2 == 0 else 160) * math.cos(math.pi * 2 * i / 24), 360 + (330 if i % 2 == 0 else 160) * math.sin(math.pi * 2 * i / 24)) for i in range(24)]
        d.polygon(pts, fill=YELLOW, outline=BLACK, width=10)
    elif kind == "dots":
        for i in range(3): d.ellipse((460 + i * 130, 330, 540 + i * 130, 410), fill=BLACK)
    elif kind == "check":
        d.line([(430, 370), (580, 520), (860, 200)], fill=(40, 190, 70, 255), width=60, joint="curve")
    elif kind == "cross":
        d.line([(440, 160), (840, 560)], fill=RED, width=64); d.line([(840, 160), (440, 560)], fill=RED, width=64)
    elif kind == "circle_mark":
        d.ellipse((380, 100, 900, 620), outline=RED, width=40)
    elif kind == "underline":
        d.line([(200, 600), (1080, 590)], fill=RED, width=26)
    elif kind == "zigzag":
        d.line([(160, 420), (320, 220), (480, 420), (640, 220), (800, 420), (960, 220), (1120, 420)], fill=RED, width=22, joint="curve")
    elif kind == "confetti":
        for _ in range(120):
            x, y = rnd.randint(0, W), rnd.randint(0, H); c = rnd.choice([RED, YELLOW, (60, 140, 255, 255), (40, 190, 70, 255)])
            d.rectangle((x, y, x + rnd.randint(10, 24), y + rnd.randint(6, 14)), fill=c)
    elif kind == "flash":
        d.ellipse((140, -60, 1140, 780), fill=(255, 255, 255, 170)); im = im.filter(ImageFilter.GaussianBlur(40))
    elif kind == "vignette":
        for i in range(60): d.rectangle((i * 6, i * 3.4, W - i * 6, H - i * 3.4), outline=(0, 0, 0, max(0, 200 - i * 4)), width=7)
    elif kind == "money_fall":
        for _ in range(14):
            x, y = rnd.randint(60, 1160), rnd.randint(40, 600); d.ellipse((x, y, x + 90, y + 90), fill=(255, 200, 0, 255), outline=BLACK, width=6); d.text((x + 45, y + 45), "円", font=font(54), fill=BLACK, anchor="mm")
    elif kind == "speed_h":
        for _ in range(26):
            y = rnd.randint(0, H); x = rnd.randint(0, 600); d.line([(x, y), (x + rnd.randint(300, 650), y)], fill=(255, 255, 255, 210), width=rnd.randint(3, 9))
    elif kind == "fire":
        for x, h in [(420, 280), (540, 400), (640, 480), (740, 400), (860, 280)]:
            d.polygon([(x - 90, 640), (x, 640 - h), (x + 90, 640)], fill=(255, 120, 0, 255), outline=BLACK, width=6)
            d.polygon([(x - 45, 640), (x, 640 - h * 0.6), (x + 45, 640)], fill=YELLOW)
    elif kind == "corner_ribbon":
        d.polygon([(0, 0), (420, 0), (0, 420)], fill=RED, outline=BLACK, width=8)
    elif kind == "shock_lines":
        for i in range(18):
            a = math.pi * 2 * i / 18; d.line([(640 + 330 * math.cos(a), 360 + 330 * math.sin(a)), (640 + 520 * math.cos(a), 360 + 520 * math.sin(a))], fill=BLACK, width=14)
    elif kind == "gloom":
        for x in range(160, 1100, 70): d.line([(x, 80), (x, 200 + (x % 140))], fill=(60, 60, 120, 255), width=22)
    elif kind == "ring_wave":
        for r in (120, 220, 320): d.ellipse((640 - r, 360 - r, 640 + r, 360 + r), outline=(255, 255, 255, 230), width=12)
    return im

def save(name, im, cat, text="", note=""):
    fn = f"{name}.png"; im.save(OUT / fn, optimize=True)
    rows.append([f"09_telop_fukidashi_effect/{fn}", cat, text, note])

# --- A) テロップ 32 (黄色+黒フチ 24 / 赤・白バリエ 8) ---
telops = ["衝撃","えっ!?","注意","実話","速報","緊急","必見","無料","大問題","危険","違法?","逮捕!","ヤバい","激安","絶品","最強","驚愕","本当?","結論","理由","なぜ?","嘘でしょ","まさか","ここ重要","要確認","3つ","1位","NG","正解","話題"]
for i, t in enumerate(telops[:24], 1): save(f"telop_yellow_{i:02d}", telop(t), "telop_yellow", t, "黄色+黒フチ")
for i, t in enumerate(telops[24:30] + ["悲報", "朗報"], 1):
    c = [RED, WHITE][i % 2]; save(f"telop_color_{i:02d}", telop(t, fill=c), "telop_color", t, "赤/白+黒フチ")
# --- B) 吹き出し 24 ---
bt = [("round","えっ?"),("round","なるほど"),("round","マジ!?"),("rect","ふむ…"),("rect","つまり?"),("rect","そう!"),("shout","大変!"),("shout","ヤバい!"),("shout","危ない!"),("cloud","うーん"),("cloud","どうしよ"),("cloud","お腹すいた"),("box","ナレ"),("box","解説"),("box","豆知識"),("round","ありがと"),("rect","ダメ!"),("shout","きた!"),("cloud","まさか…"),("round","ほう"),("rect","ええっ"),("shout","逃げろ!"),("cloud","ふー"),("round","よし!")]
for i, (k, t) in enumerate(bt, 1): save(f"fukidashi_{k}_{i:02d}", bubble(k, t), f"fukidashi_{k}", t, "白地+黒文字")
# --- C) 矢印 8 ---
for i, dname in enumerate(["right","left","up","down","diag_dr","diag_ur","right","down"], 1): save(f"arrow_{i:02d}_{dname}", arrow(dname, RED if i < 5 else YELLOW), "arrow", "", "赤/黄矢印")
# --- D) 効果 16 ---
effs = ["radial_lines","focus_lines","stars","sparkle","sweat","anger","heart","exclaim","question","bang","dots","check","cross","circle_mark","underline","zigzag","confetti","flash","vignette","money_fall","speed_h","fire","corner_ribbon","shock_lines","gloom","ring_wave"]
for i, e in enumerate(effs[: 80 - len(rows)], 1): save(f"effect_{i:02d}_{e}", effect(e), "effect", "", e)
assert len(rows) == 80, len(rows)
with open(OUT / "_manifest_09.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows([["file", "category", "text", "note"]] + rows)
print("generated", len(rows))
