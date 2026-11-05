"""Rebuild the HRSD slide clips with KB's own recorded voice; highlights re-timed to his line starts."""
import os, subprocess, sys, wave
sys.argv = [sys.argv[0]]  # keep hrsd_video's default arg handling
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hrsd_video as HV

SRC = os.path.join(HERE, "myvo", "ep2_slide.m4a")
OUTDIR = os.path.join(HERE, "out_myvoice")
os.makedirs(OUTDIR, exist_ok=True)

# (start, end) of each spoken line in the recording, in seconds (from pause detection + transcription)
LINES = {
 1: [(1.34, 5.08)],
 2: [(7.21, 18.11), (19.96, 25.00), (26.27, 37.83)],
 3: [(41.22, 44.14), (45.07, 53.27), (54.54, 62.77), (63.63, 83.75)],
 4: [(85.27, 92.09), (94.43, 99.63), (114.45, 123.17), (124.46, 139.43)],   # 100.0–114.2 = first take, cut
 5: [(140.69, 144.73), (145.27, 153.07), (154.54, 157.07), (159.60, 164.48), (166.05, 172.28)],
 6: [(175.86, 188.45), (190.20, 195.90), (198.58, 213.40), (216.79, 226.57)],
 7: [(229.47, 234.77), (235.52, 240.06), (240.52, 247.31)],
 8: [(249.29, 258.14), (260.92, 262.77)],
}
CUTS = {4: [(100.03, 114.15)]}   # retake removed
LEAD, TAIL = 0.6, 0.8
CLEAN = "highpass=f=80,afftdn=nf=-28,acompressor=threshold=-20dB:ratio=2.5:attack=10:release=200,aresample=48000"

def render(n):
    a0 = LINES[n][0][0] - LEAD
    a1 = LINES[n][-1][1] + TAIL
    keep = [(a0, a1)]
    for c0, c1 in CUTS.get(n, []):
        new = []
        for k0, k1 in keep:
            if c1 <= k0 or c0 >= k1:
                new.append((k0, k1))
            else:
                if c0 > k0: new.append((k0, c0))
                if c1 < k1: new.append((c1, k1))
        keep = new

    def remap(t):  # original time -> clip time
        out = 0.0
        for k0, k1 in keep:
            if t >= k1:
                out += k1 - k0
            elif t >= k0:
                return out + (t - k0)
        return out

    wav = os.path.join(HV.BUILD, f"myvo_s{n}.wav")
    parts = "".join(f"[0:a]atrim={k0:.3f}:{k1:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={k1-k0-0.03:.3f}:d=0.03[p{i}];"
                    for i, (k0, k1) in enumerate(keep))
    cat = "".join(f"[p{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1,{CLEAN}[a]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", SRC, "-filter_complex", parts + cat, "-map", "[a]",
                    "-ac", "1", wav], check=True)
    with wave.open(wav) as w:
        total = w.getnframes() / w.getframerate()
    segs = []
    for (s, e), (text, box) in zip(LINES[n], HV.CLIPS[n]):
        segs.append(dict(start=remap(s), dur=remap(e) - remap(s), box=box, text=text))
    out, _ = HV.render_clip(n, custom=(wav, segs, total), suffix="_myvoice", srt_dir=OUTDIR)
    print(n, f"{total:.1f}s", out, file=sys.stderr)
    return out

if __name__ == "__main__":
    import concurrent.futures as cf
    with cf.ProcessPoolExecutor(4) as ex:
        res = dict(zip(LINES, ex.map(render, LINES)))
    lst = os.path.join(HV.BUILD, "walk_myvo.txt")
    open(lst, "w").write("".join(f"file '{res[n]}'\n" for n in (2, 3, 4, 5)))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    os.path.join(OUTDIR, "PPT_walkthrough_slides2-5_myvoice.mp4")], check=True)
    print("done", file=sys.stderr)
