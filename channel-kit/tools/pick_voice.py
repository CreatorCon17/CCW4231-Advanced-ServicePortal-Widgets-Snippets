"""Synthesize a test line for many LibriTTS speakers and estimate median pitch (F0) to find male voices."""
import os, subprocess, wave, sys
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
PIPER = os.path.join(ROOT, "venv", "bin", "piper")
MODEL = os.path.join(ROOT, "voice", "libritts", "en-us-libritts-high.onnx")
OUT = os.path.join(ROOT, "voice", "samples")
os.makedirs(OUT, exist_ok=True)
TEXT = "The screenshot is attached. But the incident shows nothing. This is not a bug, it's platform design."

def f0_stats(path):
    with wave.open(path) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    fl, hop = int(0.04 * sr), int(0.01 * sr)
    f0s = []
    for i in range(0, len(x) - fl, hop):
        fr = x[i:i + fl] * np.hanning(fl)
        if np.sqrt((fr ** 2).mean()) < 0.02:
            continue
        ac = np.correlate(fr, fr, "full")[fl - 1:]
        lo, hi = int(sr / 300), int(sr / 70)
        lag = lo + np.argmax(ac[lo:hi])
        if ac[lag] / ac[0] > 0.45:
            f0s.append(sr / lag)
    f0s = np.array(f0s)
    return (np.median(f0s), np.std(f0s), len(x) / sr) if len(f0s) > 20 else (0, 0, 0)

rows = []
for sid in range(0, 904, 9):
    p = os.path.join(OUT, f"s{sid:03d}.wav")
    if not os.path.exists(p):
        subprocess.run([PIPER, "-m", MODEL, "-s", str(sid), "-f", p], input=TEXT.encode(), capture_output=True, check=True)
    med, sd, dur = f0_stats(p)
    rows.append((sid, med, sd, dur))
for r in sorted(rows, key=lambda r: r[1]):
    if 0 < r[1] < 150:
        print(f"speaker {r[0]:3d}  F0 {r[1]:6.1f} Hz  sd {r[2]:5.1f}  dur {r[3]:.2f}s")
