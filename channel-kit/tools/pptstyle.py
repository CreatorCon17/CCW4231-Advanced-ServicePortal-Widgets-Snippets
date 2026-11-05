"""PPT-style (light) Shorts toolkit for ServiceNow Simplified: white bg, navy/green/amber, Calibri (Carlito)."""
import math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import snlib as S   # audio (voice 9), SRT/transcript writers, logo loader

W, H, FPS = 1080, 1920, 30
NAVY, GREEN, AMBER = (30, 39, 97), (78, 158, 95), (245, 197, 24)
LIGHT, GREYT, INK, WHITE, BG = (229, 231, 235), (107, 114, 128), (17, 24, 39), (255, 255, 255), (250, 250, 252)
RED = (200, 45, 60)
CB = "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"
CR = "/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf"
CI = "/usr/share/fonts/truetype/crosextra/Carlito-Italic.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
def font(s, kind="b"):
    return ImageFont.truetype({"b": CB, "r": CR, "i": CI, "m": MONO}[kind], int(s))
ease = S.ease
SYM_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SYM_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def tfont(text, size, kind="b"):
    """Carlito has no ✓/✗ glyphs; fall back to DejaVu for strings that contain them."""
    if any(c in text for c in "✓✗"):
        return ImageFont.truetype(SYM_R if kind in ("r", "i") else SYM_B, int(size * 0.9))
    return font(size, kind)

def text_c(d, y, s, size, fill, kind="b"):
    f = font(size, kind); w = d.textlength(s, font=f)
    if w > W - 100:
        f = font(size * (W - 100) / w, kind); w = d.textlength(s, font=f)
    d.text(((W - w) / 2, y), s, font=f, fill=fill)

def background():
    img = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(img)
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=(238, 239, 243))
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=(238, 239, 243))
    d.rectangle([W - 128, 50, W - 98, 80], fill=AMBER)           # deck corner marks
    d.rectangle([W - 84, 50, W - 54, 80], fill=GREEN)
    d.rectangle([40, H - 90, 70, H - 60], fill=NAVY)
    lg = S.logo(300)
    img.alpha_composite(lg, (40, 40))
    return img

def chip(d, x, y, text, color, size=34, fg=WHITE):
    f = tfont(text, size); w = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + w + 40, y + size + 22], 10, fill=color)
    d.text((x + 20, y + 9), text, font=f, fill=fg)
    return w + 40

def header(img, kicker, title, p, kicker_color=NAVY, title_color=INK, sub=None):
    d = ImageDraw.Draw(img)
    a = ease(p * 4)
    y = 190 - 30 * (1 - a)
    f = font(34); w = d.textlength(kicker, font=f)
    chip(d, (W - w - 40) / 2, y, kicker, kicker_color)
    text_c(d, y + 80, title, 76, title_color)
    if sub:
        text_c(d, y + 170, sub, 42, GREYT, "i")
    d.rectangle([W / 2 - 110, y + (230 if sub else 175), W / 2 + 10, y + (238 if sub else 183)], fill=GREEN)
    d.rectangle([W / 2 + 18, y + (230 if sub else 175), W / 2 + 110, y + (238 if sub else 183)], fill=AMBER)

def card(img, box, r=22, fill=WHITE, border=LIGHT, shadow=True):
    x0, y0, x1, y1 = box
    if shadow:
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([x0 + 4, y0 + 10, x1 + 4, y1 + 10], r, fill=(30, 39, 97, 40))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    ImageDraw.Draw(img).rounded_rectangle(box, r, fill=fill, outline=border, width=3)

def bar(img, box, text, r=22):
    x0, y0, x1, _ = box
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x1, y0 + 84], r, fill=NAVY)
    d.rectangle([x0, y0 + 50, x1, y0 + 84], fill=NAVY)
    d.text((x0 + 36, y0 + 20), text, font=font(42), fill=WHITE)

def field(d, x, y, w, label, value, value_kind="r", value_color=INK, h=84, label_size=32, value_size=38, border=LIGHT):
    d.text((x, y), label, font=font(label_size, "r"), fill=GREYT)
    d.rounded_rectangle([x, y + 44, x + w, y + 44 + h], 12, fill=WHITE, outline=border, width=3)
    if value:
        d.text((x + 22, y + 44 + (h - value_size) / 2 - 4), value, font=font(value_size, value_kind), fill=value_color)

def ring(img, box, t, color=AMBER, pad=8):
    x0, y0, x1, y1 = box
    pulse = pad + 3 * math.sin(t * 7)
    b = [x0 - pulse, y0 - pulse, x1 + pulse, y1 + pulse]
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle(b, 16, outline=color + (200,), width=12)
    img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(5)))
    ImageDraw.Draw(img).rounded_rectangle(b, 16, outline=color, width=6)

def cursor(d, x, y, click=0.0):
    if click > 0:
        r = 18 + 44 * click
        d.ellipse([x - r, y - r, x + r, y + r], outline=NAVY, width=4)
    d.polygon([(x, y), (x, y + 52), (x + 14, y + 40), (x + 26, y + 64), (x + 36, y + 58), (x + 24, y + 36), (x + 42, y + 34)],
              fill=WHITE, outline=INK)

KEEP = ("gs.", "javascript", "sys_user", "g_form", "()", "_", "parseInt", "GlideAjax", "onChange")
def captions(img, segs, t):
    for s in segs:
        if s["start"] <= t < s["start"] + s["dur"]:
            words = s["cap"].split()
            wts = np.array([len(w) + 3 for w in words], float)
            cum = np.cumsum(wts) / wts.sum() * s["dur"]
            wi = min(int(np.searchsorted(cum, t - s["start"])), len(words) - 1)
            c0 = (wi // 3) * 3
            d = ImageDraw.Draw(img)
            parts = [(w if any(k in w for k in KEEP) else w.upper(), c0 + j == wi) for j, w in enumerate(words[c0:c0 + 3])]
            f = font(70)
            sp = d.textlength(" ", font=f)
            total = sum(d.textlength(w, font=f) for w, _ in parts) + sp * (len(parts) - 1)
            if total > W - 140:
                f = font(70 * (W - 140) / total); sp = d.textlength(" ", font=f)
                total = sum(d.textlength(w, font=f) for w, _ in parts) + sp * (len(parts) - 1)
            x = (W - total) / 2; y = 1450
            d.rounded_rectangle([x - 34, y - 18, x + total + 34, y + 96], 24, fill=NAVY)
            for w, cur in parts:
                ww = d.textlength(w, font=f)
                if cur:
                    d.rounded_rectangle([x - 8, y - 4, x + ww + 8, y + 82], 12, fill=AMBER)
                d.text((x, y), w, font=f, fill=NAVY if cur else WHITE)
                x += ww + sp
            return

def end_card(img, t, p, line1, line2, sub1, sub2):
    d = ImageDraw.Draw(img)
    lw = 640
    lg = S.logo(lw)
    a = ease(p * 4)
    img.alpha_composite(lg, (int((W - lw) / 2), int(330 - 30 * (1 - a))))
    text_c(d, 600, line1, 84, NAVY)
    text_c(d, 700, line2, 84, GREEN)
    card(img, (110, 860, 970, 1150))
    d = ImageDraw.Draw(img)
    d.rectangle([110, 860, 126, 1150], fill=AMBER)
    d.text((170, 900), sub1, font=font(52), fill=NAVY)
    d.text((170, 985), sub2, font=font(40, "r"), fill=GREYT)
    bob = 8 * math.sin(t * 5)
    chip(d, 330, 1250 + bob, "FOLLOW for more", GREEN, size=48)

def render(lines, scenes, here, basename, end_scene="end"):
    out = os.path.join(here, "build"); os.makedirs(out, exist_ok=True)
    segs, total = S.build_audio(lines, out)
    S.write_srt(segs, os.path.join(here, f"{basename}_captions.srt"))
    S.write_transcript(segs, os.path.join(here, f"{basename}_transcript.txt"))
    BG_ = background()
    def scene_at(t):
        cur = segs[0]
        for s in segs:
            if t >= s["start"] - 0.15:
                cur = s
        lt = t - (cur["start"] - 0.15)
        return cur, lt, lt / (cur["dur"] + S.GAP)
    def frame(fi):
        t = fi / FPS
        img = BG_.copy()
        s, lt, p = scene_at(t)
        scenes[s["scene"]](img, lt, min(1.0, max(0.0, p)))
        captions(img, segs, t)
        if lt < 0.1:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(120 * (1 - lt / 0.1)))))
        return img.convert("RGB")
    if "preview" in sys.argv:
        for s in segs:
            frame(int((s["start"] + s["dur"] * 0.85) * FPS)).save(os.path.join(out, f"prev_{s['scene']}.png"))
        return None
    frame(int((segs[0]["start"] + segs[0]["dur"] * 0.9) * FPS)).save(os.path.join(here, f"{basename}_cover.jpg"), quality=92)
    silent = os.path.join(out, "silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", silent],
                          stdin=subprocess.PIPE)
    for fi in range(int(total * FPS)):
        ff.stdin.write(frame(fi).tobytes())
    ff.stdin.close(); ff.wait()
    final = os.path.join(here, f"{basename}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", os.path.join(out, "vo.wav"),
                    "-i", os.path.join(out, "music.wav"), "-filter_complex",
                    "[1:a]aresample=44100,volume=1.6,asplit=2[v][vs];[2:a]volume=0.8[m];"
                    "[m][vs]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=300[duck];"
                    "[v][duck]amix=inputs=2:normalize=0,volume=2.2,alimiter=limit=0.85:level=false[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", final], check=True)
    return final
