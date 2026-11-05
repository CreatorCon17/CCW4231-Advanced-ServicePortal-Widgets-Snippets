#!/bin/bash
# Re-render every video with voice 9 (LibriTTS speaker 522, set as default in snlib.py).
S="$(cd "$(dirname "$0")" && pwd)"
PY="$S/venv/bin/python"
LOG="$S/rerender_progress.txt"
: > "$LOG"
# wait for the HRSD render to finish (don't compete for CPU)
while ps aux | grep -q "[h]rsd_video.py"; do sleep 10; done
echo "start $(date +%T)" >> "$LOG"

boost() {  # +3 dB with limiter, same as the original Shorts
  f="$1"; ffmpeg -y -loglevel error -i "$f" -c:v copy -af "volume=3dB,alimiter=limit=0.85:level=false" \
    -c:a aac -b:a 192k -movflags +faststart "$f.tmp.mp4" && mv "$f.tmp.mp4" "$f"
}

# clear cached voice lines
rm -f "$S"/short{1,2,3,4,5,6}/build/vo_*.wav "$S"/bp/bp*/build/vo_*.wav "$S"/long/parts/*/build/vo_*.wav

# ZZ_YY Shorts (batches of 3)
( cd "$S" && $PY short1/short1_v2.py >/dev/null 2>&1 ) & ( cd "$S" && $PY short2/short2.py >/dev/null 2>&1 ) & ( cd "$S" && $PY short3/short3.py >/dev/null 2>&1 ) & wait
( cd "$S" && $PY short4/short4.py >/dev/null 2>&1 ) & ( cd "$S" && $PY short5/short5.py >/dev/null 2>&1 ) & ( cd "$S" && $PY short6/short6.py >/dev/null 2>&1 ) & wait
for f in "$S"/short1/short1_zz_yy_attached_but_missing.mp4 "$S"/short2/short2_find_hidden_attachments.mp4 "$S"/short3/short3_business_rule_fix.mp4 \
         "$S"/short4/short4_dont_fix_by_hand.mp4 "$S"/short5/short5_cleanup_script_trap.mp4 "$S"/short6/short6_interview_question.mp4; do boost "$f"; done
echo "zz_yy shorts done $(date +%T)" >> "$LOG"

# Best-practice Shorts
( cd "$S/bp" && $PY bp_shorts.py 1 >/dev/null 2>&1 ) & ( cd "$S/bp" && $PY bp_shorts.py 2 >/dev/null 2>&1 ) & ( cd "$S/bp" && $PY bp_shorts.py 3 >/dev/null 2>&1 ) & wait
( cd "$S/bp" && $PY bp_shorts.py 4 >/dev/null 2>&1 ) & ( cd "$S/bp" && $PY bp_shorts.py 5 >/dev/null 2>&1 ) & ( cd "$S/bp" && $PY bp_shorts.py 6 >/dev/null 2>&1 ) & wait
for k in 1 2 3 4 5 6; do boost "$(ls "$S"/bp/bp$k/bp${k}_*.mp4 | grep -v tmp | head -1)"; done
echo "bp shorts done $(date +%T)" >> "$LOG"

# Long video
cd "$S/long"
for p in ch1 ch2 ch3 ch4; do ( $PY lv.py $p >/dev/null 2>&1 ) & done; wait
for p in ch5 ch6 intro outro; do ( $PY lv.py $p >/dev/null 2>&1 ) & done; wait
$PY assemble.py > assemble_out.txt 2>&1
echo "long done $(date +%T)" >> "$LOG"

# refresh docs + packages
$PY "$S/refresh_docs.py" >> "$LOG" 2>&1
echo ALLDONE >> "$LOG"
