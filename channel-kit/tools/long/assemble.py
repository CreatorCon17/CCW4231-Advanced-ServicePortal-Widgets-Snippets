"""Join rendered parts into the final long video + combined SRT + transcript + chapter list."""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lv

parts = lv.PARTS
names = {"intro": "Intro"} | {c["key"]: c["name"] for c in lv.CHAPTERS} | {"outro": "Recap & wrap-up"}

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())

lst = os.path.join(HERE, "parts", "list.txt")
with open(lst, "w") as f:
    for p in parts:
        f.write(f"file '{os.path.join(HERE, 'parts', p, 'part.mp4')}'\n")
final = os.path.join(HERE, "ServiceNow_30_Best_Practices.mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final], check=True)

def ts_parse(s):
    h, m, rest = s.split(":"); sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000
def ts_fmt(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
def chap_fmt(x):
    m, s = divmod(int(x), 60)
    return f"{m}:{s:02d}"

offset, n, srt, transcript, chapters = 0.0, 1, [], [], []
for p in parts:
    chapters.append(f"{chap_fmt(offset)} {names[p]}")
    blocks = open(os.path.join(HERE, "parts", p, "part.srt")).read().strip().split("\n\n")
    transcript.append(f"## {names[p]}")
    for b in blocks:
        lines = b.split("\n")
        a, c = lines[1].split(" --> ")
        text = " ".join(lines[2:])
        srt.append(f"{n}\n{ts_fmt(ts_parse(a) + offset)} --> {ts_fmt(ts_parse(c) + offset)}\n{text}\n")
        transcript.append(text)
        n += 1
    transcript.append("")
    offset += dur(os.path.join(HERE, "parts", p, "part.mp4"))
open(os.path.join(HERE, "ServiceNow_30_Best_Practices_captions.srt"), "w").write("\n".join(srt))
open(os.path.join(HERE, "ServiceNow_30_Best_Practices_transcript.md"), "w").write("# ServiceNow: 30 Best Practices (transcript)\n\n" + "\n".join(transcript))
open(os.path.join(HERE, "chapters.txt"), "w").write("\n".join(chapters) + "\n")
print(final, f"{offset/60:.2f} min")
print("\n".join(chapters))
