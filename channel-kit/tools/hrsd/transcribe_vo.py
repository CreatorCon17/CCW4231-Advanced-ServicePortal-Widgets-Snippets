"""Split the user's recording at pauses and transcribe each speech chunk (offline Whisper via sherpa-onnx)."""
import json, os, re, subprocess, sys, wave
import numpy as np
import sherpa_onnx

HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(os.path.dirname(HERE), "asr", "sherpa-onnx-whisper-base.en")
SRC = os.path.join(HERE, "myvo", "ep2_slide.m4a")
WAV16 = os.path.join(HERE, "myvo", "full16k.wav")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", SRC, "-ac", "1", "-ar", "16000", WAV16], check=True)

# pauses
log = subprocess.run(["ffmpeg", "-i", WAV16, "-af", "silencedetect=noise=-35dB:d=0.45", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
with wave.open(WAV16) as w:
    sr = w.getframerate()
    audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
total = len(audio) / sr
# speech chunks = gaps between silences
chunks, t = [], 0.0
for s, e in zip(starts, ends + [total] * (len(starts) - len(ends))):
    if s - t > 0.25:
        chunks.append((t, s))
    t = e
if total - t > 0.25:
    chunks.append((t, total))

rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=os.path.join(M, "base.en-encoder.int8.onnx"), decoder=os.path.join(M, "base.en-decoder.int8.onnx"),
    tokens=os.path.join(M, "base.en-tokens.txt"), language="en", task="transcribe", num_threads=4)
out = []
for a, b in chunks:
    seg = audio[max(0, int((a - 0.1) * sr)):int((b + 0.1) * sr)]
    st = rec.create_stream(); st.accept_waveform(sr, seg); rec.decode_stream(st)
    out.append(dict(start=round(a, 2), end=round(b, 2), text=st.result.text.strip()))
    print(f"{a:7.2f}-{b:7.2f}  {st.result.text.strip()}")
json.dump(out, open(os.path.join(HERE, "myvo", "chunks.json"), "w"), indent=1)
