"""HRSD Episode 2: narrated slide clips (with highlights), lower-thirds and section bumpers.
Usage: python hrsd_video.py [speaker_id]"""
import math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PIPER = os.path.join(ROOT, "venv", "bin", "piper")
MODEL = os.path.join(ROOT, "voice", "libritts", "en-us-libritts-high.onnx")
SPEAKER = sys.argv[1] if len(sys.argv) > 1 else "522"
SLIDES = os.path.join(HERE, "v2")
OUT = os.path.join(HERE, "out")
BUILD = os.path.join(HERE, "build", f"spk{SPEAKER}")
os.makedirs(OUT, exist_ok=True); os.makedirs(BUILD, exist_ok=True)
W, H, FPS = 1920, 1080, 30
NAVY, GREEN, AMBER, LIGHT = (30, 39, 97), (78, 158, 95), (245, 197, 24), (229, 231, 235)
CB = "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"
CR = "/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf"
font = lambda s, b=True: ImageFont.truetype(CB if b else CR, int(s))

ALL = (86, 260, 1836, 960)
# slide -> [(narration, highlight box or None)]
CLIPS = {
 1: [("Episode two. Manager approval, and the HR handoff.", None)],
 2: [("Five episodes in total. Episode one is done. It ended up split into part one point one, and one point two, because it ran long.", (78, 236, 1836, 470)),
     ("Today is episode two. Manager approval, and the HR handoff.", (78, 472, 1836, 598)),
     ("After this, episode three builds the real HRIS integration. Episode four adds notifications and SLAs. And episode five polishes the portal.", (78, 592, 1484, 952))],
 3: [("This is the end-to-end flow, in five steps.", (78, 272, 1836, 951)),
     ("The employee submits. The case routes to their manager. And the manager approves, or rejects.", (78, 272, 1836, 677)),
     ("The case gets assigned to the Leave Management team. Then the team updates the external HRIS, and closes the case.", (78, 683, 1836, 951)),
     ("Step five is marked amber, because it's the manual step. The HR team types it into Workday or SAP by hand. We leave it manual on purpose today, so you can see exactly where episode three's integration slots in.", (78, 820, 1836, 1020))],
 4: [("One principle before we build. HRSD and your HRIS do different jobs.", (78, 258, 1836, 418)),
     ("HRSD owns the request, the approval decision, and the audit trail.", (78, 452, 943, 972)),
     ("The HRIS, Workday, SAP, or whatever your client runs, owns the real leave balance, and payroll.", (978, 452, 1843, 972)),
     ("A lot of projects try to make HRSD the system of record for leave. Don't. Payroll, finance, and auditors will all fight you. HRSD requests. The HRIS records.", (78, 452, 1843, 972))],
 5: [("Here's today's build order. Three builds, and two demos.", (78, 164, 900, 237)),
     ("First, we build the mock HRIS table. Then, the manager approval in Flow Designer.", (78, 266, 1844, 553)),
     ("Then we demo the manager side.", (78, 553, 1844, 690)),
     ("Next, we build the auto-assignment to the Leave Management team.", (78, 690, 1844, 826)),
     ("And finally, we demo the team updating the mock HRIS, and closing the case.", (78, 826, 1844, 963))],
 6: [("This mock table stands in for Workday or SAP. Episode three's integration writes to this exact table, so what we build now gets reused.", (78, 234, 1836, 336)),
     ("Employee ID, leave type, and the start and end dates.", (78, 348, 1836, 638)),
     ("Days taken, in calendar days for now. An approval reference, holding the HR case number, so we can trace back to HRSD. And recorded at.", (78, 638, 1836, 854)),
     ("Today, the HR team adds a row here by hand. In episode three, Flow Designer does it automatically on approval.", (78, 911, 1822, 984))],
 7: [("Some things we're deliberately not covering today. Each one has its own episode.", None),
     ("Multi-level approvals, and notifications and SLAs, come in episode four.", (78, 265, 1836, 605)),
     ("The real HRIS integration is episode three. And Employee Center polish is episode five.", (78, 611, 1836, 951))],
 8: [("Next episode: external HRIS integration. We automate the manual step you just watched the team do.", None),
     ("Subscribe, so you don't miss it.", None)],
}
GAP, TAIL, HEAD = 0.45, 0.9, 0.5

def tts(key, text):
    p = os.path.join(BUILD, f"{key}.wav")
    if not os.path.exists(p):
        subprocess.run([PIPER, "-m", MODEL, "-s", SPEAKER, "-f", p], input=text.encode(), check=True, capture_output=True)
    with wave.open(p) as w:
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return a, sr

def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"

def render_clip(n, custom=None, suffix="_narrated", srt_dir=None):
    """custom = (wav_path, segs, total) to use a recorded voice instead of TTS."""
    slide = Image.open(os.path.join(SLIDES, f"s-{n}.png")).convert("RGB").resize((W, H), Image.LANCZOS)
    if custom:
        wav, segs, total = custom
        return _render_video(n, slide, wav, segs, total, suffix, srt_dir)
    segs, t, parts, sr = [], HEAD, [], 22050
    for i, (text, box) in enumerate(CLIPS[n]):
        a, sr = tts(f"s{n}_{i}", text)
        segs.append(dict(start=t, dur=len(a) / sr, box=box, text=text))
        parts.append((t, a))
        t += len(a) / sr + GAP
    total = t - GAP + TAIL
    vo = np.zeros(int(total * sr) + 1, np.float32)
    for st, a in parts:
        i0 = int(st * sr); vo[i0:i0 + len(a)] += a
    wav = os.path.join(BUILD, f"clip{n}.wav")
    with wave.open(wav, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(vo, -1, 1) * 32767).astype(np.int16).tobytes())
    return _render_video(n, slide, wav, segs, total, suffix, srt_dir)

def _render_video(n, slide, wav, segs, total, suffix, srt_dir):
    with open(os.path.join(srt_dir or OUT, f"slide{n}.srt"), "w") as f:
        for k, s in enumerate(segs, 1):
            f.write(f"{k}\n{ts(s['start'])} --> {ts(s['start'] + s['dur'])}\n{s['text']}\n\n")

    def box_at(tt):
        cur = None
        for s in segs:
            if tt >= s["start"] - 0.25:
                cur = s
        return cur

    silent = os.path.join(BUILD, f"clip{n}{suffix}.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", silent],
                          stdin=subprocess.PIPE)
    nf = int(total * FPS)
    prev_box = None
    for fi in range(nf):
        tt = fi / FPS
        z = 1.0 + 0.025 * (tt / total)                      # slow push-in
        zw, zh = int(W / z), int(H / z)
        x0, y0 = (W - zw) // 2, (H - zh) // 2
        img = slide.crop((x0, y0, x0 + zw, y0 + zh)).resize((W, H), Image.BILINEAR).convert("RGBA")
        s = box_at(tt)
        if s and s["box"]:
            e = ease((tt - (s["start"] - 0.25)) / 0.4)
            bx = [(v - c) * z + c for v, c in zip(s["box"], (W / 2, H / 2, W / 2, H / 2))]
            dim = Image.new("RGBA", (W, H), (15, 20, 50, int(95 * e)))
            ImageDraw.Draw(dim).rounded_rectangle(bx, 18, fill=(0, 0, 0, 0))
            img.alpha_composite(dim)
            glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(glow).rounded_rectangle(bx, 18, outline=AMBER + (int(200 * e),), width=10)
            img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(6)))
            ImageDraw.Draw(img).rounded_rectangle(bx, 18, outline=AMBER + (int(255 * e),), width=5)
        fade = min(1.0, tt / 0.35, (total - tt) / 0.35)
        if fade < 1:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(255 * (1 - max(0, fade))))))
        ff.stdin.write(img.convert("RGB").tobytes())
    ff.stdin.close(); ff.wait()
    out = os.path.join(srt_dir or OUT, f"slide{n}{suffix}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-c:v", "copy",
                    "-af", "aresample=48000,loudnorm=I=-16:TP=-1.5", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-shortest", out], check=True)
    return out, total

# ---------------- overlays ----------------
def lower_third(name, role, color, fname):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x, y = 70, 880
    t1, t2 = "LOGGED IN AS", name
    w = max(d.textlength(t2, font=font(52)), 420) + 90
    d.rounded_rectangle([x + 6, y + 8, x + w + 6, y + 140 + 8], 18, fill=(0, 0, 0, 90))
    d.rounded_rectangle([x, y, x + w, y + 140], 18, fill=(255, 255, 255, 245))
    d.rounded_rectangle([x, y, x + 16, y + 140], 8, fill=color + (255,))
    d.text((x + 44, y + 18), t1, font=font(26), fill=(107, 114, 128))
    d.text((x + 44, y + 52), t2, font=font(52), fill=NAVY)
    lx = x + 44 + d.textlength(t1, font=font(26)) + 18
    rw = d.textlength(role, font=font(24)) + 32
    d.rounded_rectangle([lx, y + 14, lx + rw, y + 48], 17, fill=color + (255,))
    d.text((lx + 16, y + 17), role, font=font(24), fill=(255, 255, 255) if color != AMBER else NAVY)
    img.save(os.path.join(OUT, fname))

def bumper(kind, num, title, fname):
    color = NAVY if kind == "BUILD" else GREEN
    frames = int(2.6 * FPS)
    mp4 = os.path.join(OUT, fname)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest",
                           "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", mp4], stdin=subprocess.PIPE)
    for fi in range(frames):
        tt = fi / FPS
        e = ease(tt / 0.5)
        out = 1 - ease((tt - 2.1) / 0.5)
        img = Image.new("RGB", (W, H), (255, 255, 255))
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, W, H], fill=(250, 250, 252))
        bar_w = int(W * e)
        d.rectangle([0, 380, bar_w, 700], fill=color)
        d.rectangle([0, 700, int(W * e * 0.35), 716], fill=GREEN if kind == "BUILD" else AMBER)
        if e > 0.6:
            a = int(255 * min(1, (e - 0.6) / 0.4) * out)
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            ld.rounded_rectangle([140, 440, 420, 520], 14, fill=(255, 255, 255, a))
            ld.text((172, 450), f"{kind} {num}", font=font(52), fill=color + (a,))
            ld.text((140, 545), title, font=font(96), fill=(255, 255, 255, a))
            img = img.convert("RGBA"); img.alpha_composite(layer); img = img.convert("RGB")
        if out < 1:
            img = Image.blend(Image.new("RGB", (W, H), (255, 255, 255)), img, max(0, out))
        ff.stdin.write(img.tobytes())
    ff.stdin.close(); ff.wait()
    # also a still PNG
    still = Image.new("RGB", (W, H), (250, 250, 252)); d = ImageDraw.Draw(still)
    d.rectangle([0, 380, W, 700], fill=color); d.rectangle([0, 700, int(W * 0.35), 716], fill=GREEN if kind == "BUILD" else AMBER)
    d.rounded_rectangle([140, 440, 420, 520], 14, fill=(255, 255, 255)); d.text((172, 450), f"{kind} {num}", font=font(52), fill=color)
    d.text((140, 545), title, font=font(96), fill=(255, 255, 255))
    still.save(mp4.replace(".mp4", ".png"))

if __name__ == "__main__":
    only = os.environ.get("ONLY")
    if only != "clips":
        lower_third("Dougie Macarthur", "EMPLOYEE", GREEN, "lowerthird_employee.png")
        lower_third("Narvdasaver Dubey", "MANAGER", NAVY, "lowerthird_manager.png")
        lower_third("Leave Management Team member", "HR TEAM", AMBER, "lowerthird_hr_team.png")
        bumper("BUILD", 1, "Mock HRIS table", "bumper_build1.mp4")
        bumper("BUILD", 2, "Manager approval (Flow Designer)", "bumper_build2.mp4")
        bumper("DEMO", 1, "Manager approves", "bumper_demo1.mp4")
        bumper("BUILD", 3, "Auto-assign on approval", "bumper_build3.mp4")
        bumper("DEMO", 2, "Team updates HRIS & closes", "bumper_demo2.mp4")
    if only != "overlays":
        res = {}
        for n in CLIPS:
            res[n] = render_clip(n)
            print(n, f"{res[n][1]:.1f}s", file=sys.stderr)
        lst = os.path.join(BUILD, "walk.txt")
        open(lst, "w").write("".join(f"file '{res[n][0]}'\n" for n in (2, 3, 4, 5)))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                        os.path.join(OUT, "PPT_walkthrough_slides2-5.mp4")], check=True)
