"""08: キャラ立ち絵(透過PNG, 口パク差分)から3秒・30fpsの透過webm(VP9 alpha)を作る。
使い方: python3 -I tools/gen_08_motion.py <キャラフォルダ> <口差分PNGをカンマ区切り(開→閉)> """
import sys, math, subprocess, shutil, tempfile
from pathlib import Path
from PIL import Image
folder = Path(sys.argv[1]); mouths = [Image.open(folder / m).convert("RGBA") for m in sys.argv[2].split(",")]
name = folder.name; FPS, N = 30, 90; CW, CH = 560, 700
def frame(i, kind):
    t = i / FPS; k = int((t * 8)) % len(mouths); base = mouths[k] if kind.startswith("talk") else mouths[min(1, len(mouths) - 1)]
    sc, dx, dy, rot = 1.0, 0, 0, 0
    if kind == "talk_idle": dy = -4 * math.sin(t * 2 * math.pi * 1.5)
    elif kind == "talk_bounce": dy = -30 * abs(math.sin(t * 2 * math.pi * 2))
    elif kind == "talk_shake": dx = 14 * math.sin(t * 2 * math.pi * 6); rot = 4 * math.sin(t * 2 * math.pi * 6)
    elif kind == "jump": dy = -140 * max(0, math.sin(t * 2 * math.pi / 1.5)) ; sc = 1 + 0.05 * (dy < -10)
    elif kind == "nod": rot = 6 * math.sin(t * 2 * math.pi * 1.2); dy = 8 * abs(math.sin(t * 2 * math.pi * 1.2))
    elif kind == "slide_in_left": p = min(1, t / 0.7); e = 1 - (1 - p) ** 3; dx = -500 * (1 - e)
    elif kind == "slide_in_right": p = min(1, t / 0.7); e = 1 - (1 - p) ** 3; dx = 500 * (1 - e)
    elif kind == "zoom_pop": p = min(1, t / 0.4); sc = 0.2 + 0.8 * (1 - (1 - p) ** 3) + 0.08 * math.sin(p * math.pi)
    im = base.resize((int(base.width * sc), int(base.height * sc)), Image.LANCZOS)
    if rot: im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    c.alpha_composite(im, (int((CW - im.width) / 2 + dx), int(CH - im.height - 20 + dy))) if True else None
    return c
for kind in ["talk_idle", "talk_bounce", "talk_shake", "jump", "nod", "slide_in_left", "slide_in_right", "zoom_pop"]:
    tmp = Path(tempfile.mkdtemp())
    for i in range(N): frame(i, kind).save(tmp / f"f{i:03d}.png")
    out = folder / f"{name}_{kind}.webm"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(tmp / "f%03d.png"), "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "34", "-auto-alt-ref", "0", str(out)], check=True)
    shutil.rmtree(tmp); print(out.name, out.stat().st_size // 1024, "KB")
