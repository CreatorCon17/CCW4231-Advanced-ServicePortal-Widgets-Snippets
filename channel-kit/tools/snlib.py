"""Shared toolkit for ServiceNow Simplified Shorts: VO (Piper), music, captions, branding, render."""
import math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
PIPER = os.environ.get("SNS_PIPER") or os.path.join(ROOT, "venv", "bin", "piper")
VOICE = os.environ.get("SNS_VOICE") or os.path.join(ROOT, "voice", "libritts", "en-us-libritts-high.onnx")  # LibriTTS, CC BY 4.0
SPEAKER = "522"  # voice 9 (chosen by ear), LibriTTS CC BY 4.0
# logo: channel-kit/brand/logo.png (override with SNS_LOGO env var)
LOGO_PATH = os.environ.get("SNS_LOGO") or os.path.join(os.path.dirname(ROOT), "brand", "logo.png")

W, H, FPS, GAP = 1080, 1920, 30, 0.3
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
def font(s, kind="b"):
    return ImageFont.truetype({"b": FB, "r": FR, "m": FM}[kind], int(s))

ACCENT = (98, 216, 155)
AMBER = (255, 196, 61)
RED = (255, 72, 88)
WHITE = (245, 246, 250)
GREY = (150, 158, 178)
INK = (32, 38, 52)
CARD = (250, 251, 253)
LINE = (220, 224, 232)
NAVY = (52, 64, 84)

def ease(p):
    p = max(0.0, min(1.0, p)); return p * p * (3 - 2 * p)

def text_c(d, y, s, size, fill, kind="b", stroke=6):
    f = font(size, kind)
    w = d.textlength(s, font=f)
    if w > W - 70:                       # auto-fit long lines
        f = font(size * (W - 70) / w, kind)
        w = d.textlength(s, font=f)
    d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))

def header(img, title, sub, color, p, kind="b"):
    d = ImageDraw.Draw(img)
    a = ease(p * 4)
    y = 250 - 40 * (1 - a)
    text_c(d, y, title, 80, color, kind=kind)
    if sub:
        text_c(d, y + 104, sub, 44, WHITE, stroke=4)

def shadow_card(img, box, r=28, fill=CARD):
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x0 + 8, y0 + 16, x1 + 8, y1 + 16], r, fill=(0, 0, 0, 150))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    ImageDraw.Draw(img).rounded_rectangle(box, r, fill=fill)

def title_bar(img, box, text, r=28):
    x0, y0, x1, _ = box
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x1, y0 + 90], r, fill=NAVY)
    d.rectangle([x0, y0 + 60, x1, y0 + 90], fill=NAVY)
    d.text((x0 + 40, y0 + 22), text, font=font(40), fill=WHITE)

def ring(img, box, color, t, alpha=1.0):
    pulse = 6 + 4 * math.sin(t * 8)
    x0, y0, x1, y1 = box
    b = [x0 - pulse, y0 - pulse, x1 + pulse, y1 + pulse]
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle(b, 22, outline=color + (int(255 * alpha),), width=8)
    img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(3)))
    ImageDraw.Draw(img).rounded_rectangle(b, 22, outline=color + (int(255 * alpha),), width=5)

def file_icon(d, x, y, s=1.0, color=(90, 140, 255)):
    w, h = 54 * s, 68 * s
    d.polygon([(x, y), (x + w * 0.65, y), (x + w, y + h * 0.28), (x + w, y + h), (x, y + h)], fill=color)
    d.polygon([(x + w * 0.65, y), (x + w, y + h * 0.28), (x + w * 0.65, y + h * 0.28)], fill=(200, 215, 255))
    for k in range(3):
        d.line([(x + w * 0.18, y + h * (0.5 + k * 0.14)), (x + w * 0.82, y + h * (0.5 + k * 0.14))], fill=WHITE, width=max(2, int(4 * s)))

def cursor(d, x, y, click=0.0):
    if click > 0:
        r = 20 + 50 * click
        d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 255, 255), width=4)
    d.polygon([(x, y), (x, y + 52), (x + 14, y + 40), (x + 26, y + 64), (x + 36, y + 58), (x + 24, y + 36), (x + 42, y + 34)],
              fill=WHITE, outline=(0, 0, 0))

# ---------- branding ----------
_LOGO = Image.open(LOGO_PATH).convert("RGBA")
_cache = {}
def logo(width):
    if width not in _cache:
        _cache[width] = _LOGO.resize((width, round(_LOGO.height * width / _LOGO.width)), Image.LANCZOS)
    return _cache[width]

def logo_badge(img, x, y, width, pad=16, alpha=1.0):
    lg = logo(width)
    bw, bh = lg.width + 2 * pad, lg.height + 2 * pad
    badge = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    ImageDraw.Draw(badge).rounded_rectangle([0, 0, bw - 1, bh - 1], 18, fill=(255, 255, 255, 240))
    badge.alpha_composite(lg, (pad, pad))
    if alpha < 1:
        badge.putalpha(Image.eval(badge.getchannel("A"), lambda v: int(v * alpha)))
    img.alpha_composite(badge, (int(x), int(y)))
    return bw, bh

# ---------- background ----------
def _bg():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = yy / H
    bg = np.stack([10 + 8 * g, 18 + 10 * g, 30 + 16 * (1 - g)], -1)
    vig = 1 - 0.5 * (((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2)
    img = Image.fromarray((bg * np.clip(vig, 0.3, 1)[..., None]).astype(np.uint8), "RGB").convert("RGBA")
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, W, 60):
        gd.line([(x, 0), (x, H)], fill=(255, 255, 255, 10))
    for y in range(0, H, 60):
        gd.line([(0, y), (W, y)], fill=(255, 255, 255, 10))
    img.alpha_composite(grid)
    return img

# ---------- audio ----------
def _write_wav(path, data, rate):
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes((np.clip(data, -1, 1) * 32767).astype(np.int16).tobytes())

def build_audio(lines, out, length_scale=0.92):
    segs, t, sr = [], 0.3, 22050
    for i, (scene, vo_text, cap) in enumerate(lines):
        path = os.path.join(out, f"vo_{i:02d}.wav")
        if not os.path.exists(path):
            subprocess.run([PIPER, "-m", VOICE, "-s", SPEAKER, "-f", path, "--length-scale", str(length_scale)],
                           input=vo_text.encode(), check=True, capture_output=True)
        with wave.open(path) as w:
            dur, sr = w.getnframes() / w.getframerate(), w.getframerate()
        segs.append(dict(scene=scene, cap=cap, path=path, start=t, dur=dur))
        t += dur + GAP
    total = t + 0.7
    vo = np.zeros(int(total * sr), dtype=np.float32)
    for s in segs:
        with wave.open(s["path"]) as w:
            a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        i0 = int(s["start"] * sr)
        vo[i0:i0 + len(a)] += a
    msr = 44100
    tt = np.arange(int(total * msr)) / msr
    music = np.zeros_like(tt)
    chords = [(130.81, 164.81, 196.0), (110.0, 130.81, 164.81), (87.31, 110.0, 130.81), (98.0, 123.47, 146.83)]
    for k in range(int(total // 4) + 2):
        a, b = k * 4.0, k * 4.0 + 4.6
        m = (tt >= a) & (tt < b)
        if not m.any():
            continue
        env = np.clip(np.minimum((tt[m] - a) / 1.0, (b - tt[m]) / 1.0), 0, 1)
        for f in chords[k % 4]:
            music[m] += env * np.sin(2 * np.pi * f * tt[m])
    pluck = np.sin(2 * np.pi * 523.25 * tt) * np.exp(-((tt % 0.5) * 14))
    music = music / np.abs(music).max() * 0.14 + pluck * 0.035
    music *= np.clip(np.minimum(tt / 0.8, (total - tt) / 1.2), 0, 1)
    _write_wav(os.path.join(out, "vo.wav"), vo, sr)
    _write_wav(os.path.join(out, "music.wav"), music, msr)
    return segs, total

def write_transcript(segs, path):
    with open(path, 'w') as f:
        f.write('\n'.join(s['cap'] for s in segs) + '\n')

def write_srt(segs, path):
    def ts(x):
        h, r = divmod(x, 3600); m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"
    with open(path, "w") as f:
        for i, s in enumerate(segs, 1):
            f.write(f"{i}\n{ts(s['start'])} --> {ts(s['start'] + s['dur'])}\n{s['cap']}\n\n")

# ---------- frame composition ----------
KEEP_CASE = ("ZZ_YY", "sys_", "table_name", ".list", "sysparm")

def captions(img, segs, t):
    for s in segs:
        if s["start"] <= t < s["start"] + s["dur"]:
            words = s["cap"].split()
            wts = np.array([len(w) + 3 for w in words], float)
            cum = np.cumsum(wts) / wts.sum() * s["dur"]
            wi = min(int(np.searchsorted(cum, t - s["start"])), len(words) - 1)
            c0 = (wi // 3) * 3
            d = ImageDraw.Draw(img)
            parts = [(w if (any(k in w for k in KEEP_CASE) or any(ch in w for ch in '_(') or '.' in w.rstrip('.,?!:')) else w.upper(), AMBER if c0 + j == wi else WHITE)
                     for j, w in enumerate(words[c0:c0 + 3])]
            size = 66
            f = font(size)
            total = sum(d.textlength(w + " ", font=f) for w, _ in parts)
            if total > W - 60:
                f = font(size * (W - 60) / total)
                total = sum(d.textlength(w + " ", font=f) for w, _ in parts)
            x = (W - total) / 2
            for w, col in parts:
                d.text((x, 1440), w, font=f, fill=col, stroke_width=8, stroke_fill=(0, 0, 0))
                x += d.textlength(w + " ", font=f)
            return

def render(lines, scenes, here, basename, end_scene="end"):
    out = os.path.join(here, "build")
    os.makedirs(out, exist_ok=True)
    segs, total = build_audio(lines, out)
    print(f"total {total:.1f}s", file=sys.stderr)
    write_srt(segs, os.path.join(here, f"{basename}_captions.srt"))
    write_transcript(segs, os.path.join(here, f"{basename}_transcript.txt"))
    BG = _bg()

    def scene_at(t):
        cur = segs[0]
        for s in segs:
            if t >= s["start"] - 0.15:
                cur = s
        lt = t - (cur["start"] - 0.15)
        return cur, lt, lt / (cur["dur"] + GAP)

    def frame(fi):
        t = fi / FPS
        img = BG.copy()
        s, lt, p = scene_at(t)
        scenes[s["scene"]](img, lt, min(1.0, max(0.0, p)))
        captions(img, segs, t)
        if s["scene"] != end_scene:          # corner badge (end card shows the big logo)
            logo_badge(img, 36, 46, 230, pad=12, alpha=0.95)
        if lt < 0.1:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(70 * (1 - lt / 0.1)))))
        return img.convert("RGB")

    if "preview" in sys.argv:
        for s in segs:
            frame(int((s["start"] + s["dur"] * 0.85) * FPS)).save(os.path.join(out, f"prev_{s['scene']}.png"))
        return None
    frame(int((segs[0]["start"] + segs[0]["dur"] * 0.9) * FPS)).save(os.path.join(here, f"{basename}_cover.jpg"), quality=92)
    silent = os.path.join(out, "silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                           "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    for fi in range(int(total * FPS)):
        ff.stdin.write(frame(fi).tobytes())
    ff.stdin.close(); ff.wait()
    final = os.path.join(here, f"{basename}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", os.path.join(out, "vo.wav"),
                    "-i", os.path.join(out, "music.wav"), "-filter_complex",
                    "[1:a]aresample=44100,volume=1.6,asplit=2[v][vs];[2:a]volume=0.9[m];"
                    "[m][vs]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=300[duck];"
                    "[v][duck]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", final], check=True)
    return final

def end_card(img, t, p, line1, line2, box_title, box_sub, box_cta):
    d = ImageDraw.Draw(img)
    lw = 560
    lh = logo(lw).height + 48
    logo_badge(img, (W - lw - 48) / 2, 200 - 30 * (1 - ease(p * 4)), lw, pad=24)
    text_c(d, 480, line1, 88, WHITE, stroke=8)
    text_c(d, 590, line2, 88, AMBER, stroke=8)
    shadow_card(img, (110, 760, 970, 1090), fill=(18, 26, 42))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([110, 760, 970, 1090], 28, outline=ACCENT, width=5)
    d.text((160, 800), box_title, font=font(54), fill=ACCENT)
    d.text((160, 890), box_sub, font=font(38, "r"), fill=GREY)
    d.text((160, 975), box_cta, font=font(44), fill=WHITE)
    bob = 12 * math.sin(t * 5)
    text_c(d, 1190 + bob, "FOLLOW for more", 56, WHITE, stroke=5)
    text_c(d, 1260 + bob, "ServiceNow tips", 56, ACCENT, stroke=5)

# ---------- code + record helpers ----------
import re as _re
_TOK = _re.compile(r"('[^']*'|/\^[^/]+/|\b(?:var|new|while|if|function|return)\b|//.*$)")
CODE_COL = dict(str=(152, 224, 160), kw=(206, 150, 255), cm=(120, 130, 150), rx=(255, 170, 120), df=(225, 230, 240))

def code_card(img, box, lines, t=0.0, hl=(), reveal=1.0, size=34, title="Business Rule script"):
    x0, y0, x1, y1 = box
    shadow_card(img, box, fill=(16, 20, 32))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x1, y0 + 70], 28, fill=(34, 40, 58))
    d.rectangle([x0, y0 + 40, x1, y0 + 70], fill=(34, 40, 58))
    for k, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([x0 + 30 + k * 36, y0 + 24, x0 + 52 + k * 36, y0 + 46], fill=c)
    d.text((x0 + 150, y0 + 18), title, font=font(30, "r"), fill=GREY)
    f = font(size, "m")
    lh = int(size * 1.55)
    n = max(0, min(len(lines), int(math.ceil(len(lines) * reveal))))
    for i, line in enumerate(lines[:n]):
        y = y0 + 100 + i * lh
        if i in hl:
            band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(band).rounded_rectangle([x0 + 14, y - 8, x1 - 14, y + lh - 12], 10,
                                                   fill=AMBER + (int(60 + 25 * math.sin(t * 6)),))
            img.alpha_composite(band)
            d = ImageDraw.Draw(img)
        dim = bool(hl) and i not in hl
        d.text((x0 + 26, y), f"{i + 1:>2}", font=font(size * 0.8, "m"), fill=(80, 90, 110))
        x = x0 + 26 + d.textlength("00  ", font=f)
        for part in _TOK.split(line):
            if not part:
                continue
            if part.startswith("//"):
                c = CODE_COL["cm"]
            elif part.startswith("'"):
                c = CODE_COL["str"]
            elif part.startswith("/^"):
                c = CODE_COL["rx"]
            elif part in ("var", "new", "while", "if", "function", "return"):
                c = CODE_COL["kw"]
            else:
                c = CODE_COL["df"]
            if dim:
                c = tuple(int(v * 0.45 + 16 * 0.55) for v in c)
            d.text((x, y), part, font=f, fill=c)
            x += d.textlength(part, font=f)

def inc_card(img, t, attachments=(), box=(90, 560, 990, 1300), number="INC0010021", ring_att=None, extra=None):
    x0, y0, x1, y1 = box
    shadow_card(img, box)
    title_bar(img, box, f"Incident  {number}")
    d = ImageDraw.Draw(img)
    rows = [("Short description", "Unable to log in to Outlook"), ("Urgency", "3 - Medium")]
    for i, (k, v) in enumerate(rows):
        yy = y0 + 125 + i * 75
        d.text((x0 + 40, yy), k, font=font(30, "r"), fill=GREY)
        d.text((x0 + 380, yy), v, font=font(32, "r"), fill=INK)
    ay = y0 + 300
    d.text((x0 + 40, ay), f"Attachments ({len(attachments)})", font=font(36), fill=INK)
    abox = (x0 + 40, ay + 55, x1 - 40, ay + 175)
    d.rounded_rectangle(abox, 16, outline=LINE, width=4)
    if attachments:
        for k, name in enumerate(attachments[:1]):
            file_icon(d, abox[0] + 30, abox[1] + 25, 1.0)
            d.text((abox[0] + 110, abox[1] + 38), name, font=font(36), fill=INK)
    else:
        d.text((abox[0] + 40, abox[1] + 40), "No attachments", font=font(36, "r"), fill=GREY)
    if ring_att:
        ring(img, abox, ring_att, t)
    if extra:
        extra(img, d, (x0, ay + 210, x1, y1))
    return abox
