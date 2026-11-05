# ServiceNow Simplified: channel kit

Everything needed to continue making Shorts and videos in the same style, voice and workflow.
(Rendered videos and voice models are **not** stored here, because they're too big. They're regenerated with the tools below.)

## Folder map

| Folder | What's in it |
|---|---|
| `brand/` | `logo.png` (269×77, transparent, so put it on a white badge on dark backgrounds), PPT style reference images |
| `hrsd-episode2/` | Deck **`HRSD_Episode2_Hybrid_v3.pptx`** (9 slides, current) + v2, **`HRSD_Episode2_Recording_Script_FINAL.md`** (current: full script + slide VO in one file), Script v3, Script v2, original v1 script, review & edit plan, slide voice-over recording script, `overlays/` (Instance A / Instance B badges) |
| `hrsd-episode3/` | Episode 3 outline: REST integration Instance A → Instance B, Basic Auth then OAuth 2.0 |
| `docs/` | YouTube upload guide (all 13 videos), ZZ_YY Shorts series plan, upload sheets, long-video transcript |
| `tools/` | Python generators (see below) |

## Brand: the PPT style (default for new content)

| Element | Value |
|---|---|
| Background | White / very light grey (`#FAFAFC`) |
| Primary | Navy `#1E2761` (titles, header bars, number badges) |
| Secondary | Green `#4E9E5F` ("DONE", "DEMO", positive) |
| Highlight | Amber `#F5C518` (warnings, "manual step", focus rings) |
| Neutral | Light grey `#E5E7EB`, text grey `#6B7280` |
| Font | Calibri (use Carlito on Linux: `/usr/share/fonts/truetype/crosextra/Carlito-*.ttf`) |
| Marks | Two small squares top-right (amber + green), small navy square bottom-left, small logo bottom-left |
| Motion | Gentle push-in (≈2.5%), amber rounded highlight box + dim the rest, white fades between slides |

Ready-made assets in this style (from Episode 2): BUILD/DEMO title cards and "LOGGED IN AS" lower-thirds.
Regenerate with `tools/hrsd/hrsd_video.py` (`ONLY=overlays`).

> **New Shorts: use `tools/pptstyle.py`** (light PPT style: white bg, navy/green/amber, Carlito, logo top-left,
> navy caption band with amber current word; Carlito lacks ✓/✗, so `tfont()` falls back to DejaVu). Example:
> `tools/shorts/ep1_autopopulate.py` (HRSD Ep 1.1 auto-populate Short).
>
> Older note: `tools/snlib.py` (Shorts/long-video toolkit) still renders the **dark** theme used for the ZZ_YY and
> Best-Practices series. To follow the PPT style for new Shorts, swap its background and colour constants for the values above.

## Voice

- **Voice 9** = Piper TTS + LibriTTS high model, **speaker 522** (CC BY 4.0, credit required). Set in `tools/snlib.py` (`SPEAKER`).
- Voice 1 (speaker 531) was the earlier voice. All delivered videos were re-rendered with voice 9 and verified.
- HRSD series: KB records his own voice. Workflow: one line per highlight, ~1 s pause between lines →
  `tools/hrsd/transcribe_vo.py` (offline Whisper via sherpa-onnx) finds the lines → `tools/hrsd/my_vo_render.py`
  re-times the highlights, cuts retakes (`CUTS`), cleans the audio, and renders the slide clips.

## Setup in a fresh session

```bash
python3 -m venv venv && ./venv/bin/pip install numpy pillow piper-tts python-pptx sherpa-onnx
mkdir -p voice/libritts && curl -L -o /tmp/l.tgz https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-en-us-libritts-high.tar.gz && tar xzf /tmp/l.tgz -C voice/libritts
# speech recognition (only for aligning KB's own recordings):
mkdir -p asr && curl -L https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-base.en.tar.bz2 | tar xj -C asr
# system tools used: ffmpeg, soffice (LibreOffice), pdftoppm
```
The tools expect `venv/`, `voice/`, `asr/` next to them (the scratchpad layout used when they were written), or set
`SNS_PIPER`, `SNS_VOICE`, `SNS_LOGO`. Paths inside the per-video scripts may need adjusting. Treat them as templates.

## Tools

| Script | Makes |
|---|---|
| `tools/snlib.py` | Shared Shorts toolkit: TTS, music bed, captions, logo badge, code cards, render pipeline |
| `tools/shorts/short1_v2.py … short6.py` | ZZ_YY Shorts 1–6 |
| `tools/shorts/bp_shorts.py <1-6>` | Best-Practices Shorts (data-driven: tips = code/bullets/path) |
| `tools/long/lv.py <part>` + `assemble.py` + `thumb.py` | 16:9 long video in parts, joined with chapters/SRT; thumbnail |
| `tools/hrsd/hrsd_video.py` | Narrated, highlighted slide clips from the deck + bumpers + lower-thirds |
| `tools/hrsd/my_vo_render.py`, `transcribe_vo.py` | Same clips with KB's own recorded voice |
| `tools/rerender_voice9.sh`, `refresh_docs.py` | Batch re-render + refresh upload sheets/zips |
| `tools/pick_voice.py` | Pitch scan used to shortlist male voices |

## Lessons learned (don't repeat)

- Never `pkill -f <pattern>` from a shell whose own command line contains the pattern: it kills itself.
- Piper TTS isn't deterministic; verify the voice by spectral fingerprint, not by sample comparison.
- Mock UI must not invent menu items or numbers; label illustrative data on screen.
- Files over 30 MB can't be sent in chat; split zips.

## HRSD demo architecture (two ServiceNow instances)
- **Instance A — HRSD:** record producer, approval flow, HR Case, audit trail (Episodes 1, 2, 4, 5).
- **Instance B — Mock HRIS:** a second ServiceNow instance standing in for the client's Workday / SAP. Scoped app
  **HRIS Leave** + **HRIS Leave table** (system of record). Always call it "Mock HRIS" on screen.
- Episode 2: the HR team enters the row on B **by hand**. No auth set up yet (by design).
- Episode 3: Scripted REST API + integration user on B; Connection & Credential alias on A, first **Basic Auth**, then **OAuth 2.0**.
- Show `hrsd-episode2/overlays/overlay_instance_*.png` top-right whenever the video switches instance.
