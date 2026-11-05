"""After the voice-9 re-render: update durations, chapters and voice notes in the upload sheets, and rebuild the zips."""
import os, re, shutil, subprocess, zipfile

S = os.path.dirname(os.path.abspath(__file__))

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())

def mmss(x):
    return f"{int(x // 60)}:{int(x % 60):02d}"

# --- ZZ_YY shorts sheet: voice note + durations
zz = {"short1_zz_yy_attached_but_missing": "SHORT 1", "short2_find_hidden_attachments": "SHORT 2", "short3_business_rule_fix": "SHORT 3",
      "short4_dont_fix_by_hand": "SHORT 4", "short5_cleanup_script_trap": "SHORT 5", "short6_interview_question": "SHORT 6"}
p = os.path.join(S, "shorts_youtube_upload.md")
s = open(p).read().replace("speaker 531", "speaker 522, \"voice 9\"")
for base, tag in zz.items():
    n = tag.split()[1]
    d = round(dur(os.path.join(S, f"short{n}", base + ".mp4")))
    s = re.sub(rf'(## {tag}: "[^"]+" )\(\d+ s\)', rf"\g<1>({d} s)", s)
open(p, "w").write(s)

# --- best-practice shorts sheet (voice note)
p = os.path.join(S, "ServiceNow_BestPractices_Shorts_upload.md")
s = open(p).read()
s = s.replace("**Voice licence:** Piper TTS, LibriTTS (CC BY 4.0).", "**Voice:** voice 9 (Piper TTS, LibriTTS speaker 522, CC BY 4.0).")
lens = [dur(os.path.join(S, "bp", f"bp{k}", f)) for k in range(1, 7) for f in os.listdir(os.path.join(S, "bp", f"bp{k}")) if f.endswith(".mp4")]
s = re.sub(r"34–39 s", f"{round(min(lens))}–{round(max(lens))} s", s)
open(p, "w").write(s)

# --- long video sheet: chapters + duration
L = os.path.join(S, "long")
chapters = open(os.path.join(L, "chapters.txt")).read().strip()
total = dur(os.path.join(L, "ServiceNow_30_Best_Practices.mp4"))
p = os.path.join(L, "ServiceNow_30_Best_Practices_upload.md")
s = open(p).read()
s = re.sub(r"(⏱ Chapters\n)(.*?)(\n\n▶ Quick)", lambda m: m.group(1) + chapters + m.group(3), s, flags=re.S)
s = s.replace("7:31", mmss(total))
s = s.replace("This one is 7:31.", f"This one is {mmss(total)}.")
open(p, "w").write(s)

# --- rebuild packages
def pack(folder, files, zipname):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)
    for f in files:
        shutil.copy(f, folder)
    z = os.path.join(S, zipname)
    if os.path.exists(z):
        os.remove(z)
    with zipfile.ZipFile(z, "w", zipfile.ZIP_STORED) as zf:
        for f in sorted(os.listdir(folder)):
            zf.write(os.path.join(folder, f), f)
    print(zipname, f"{os.path.getsize(z) / 1e6:.0f} MB")

zz_files = []
for n in range(1, 7):
    d = os.path.join(S, f"short{n}")
    zz_files += [os.path.join(d, f) for f in os.listdir(d)
                 if f.startswith(f"short{n}_") and f.endswith(("mp4", "_captions.srt", "_transcript.txt", "_cover.jpg")) and "tmp" not in f]
zz_files += [os.path.join(S, "shorts_youtube_upload.md"), os.path.join(S, "zz_yy-shorts-series.md")]
pack(os.path.join(S, "ServiceNowSimplified_Shorts"), zz_files, "ServiceNowSimplified_Shorts.zip")

bp_files = []
for k in range(1, 7):
    d = os.path.join(S, "bp", f"bp{k}")
    bp_files += [os.path.join(d, f) for f in os.listdir(d) if f.startswith(f"bp{k}_") and "tmp" not in f]
bp_files.append(os.path.join(S, "ServiceNow_BestPractices_Shorts_upload.md"))
pack(os.path.join(S, "BestPractices_Shorts"), bp_files, "ServiceNow_BestPractices_Shorts.zip")

lv_files = [os.path.join(L, f) for f in ("ServiceNow_30_Best_Practices.mp4", "ServiceNow_30_Best_Practices_captions.srt",
            "ServiceNow_30_Best_Practices_transcript.md", "ServiceNow_30_Best_Practices_upload.md", "thumbnail_30_best_practices.jpg")]
pack(os.path.join(S, "LongVideo_30_Best_Practices"), lv_files, "LongVideo_30_Best_Practices.zip")
print("long:", mmss(total)); print(chapters)
