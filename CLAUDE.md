# CLAUDE.md

This repo has two parts:
- `Lab_1` … `Lab_6`: Service Portal widget code snippets (CreatorCon CCW4231 workshop).
- `channel-kit/`: everything for KB's YouTube channel **ServiceNow Simplified** (Shorts, long videos, HRSD series).
  **Read `channel-kit/README.md` before making any new Short, video, script or upload sheet.**

## Channel defaults (apply to every new Short / video unless KB says otherwise)

- **Visual style = KB's PPT style** (see `channel-kit/brand/ppt_style_reference_*.png` and `channel-kit/hrsd-episode2/HRSD_Episode2_Hybrid_v2.pptx`):
  white / light background, navy `#1E2761`, green `#4E9E5F`, amber `#F5C518` (highlight/warning), light grey `#E5E7EB`,
  font Calibri (render with Carlito, which is metric-compatible), logo `channel-kit/brand/logo.png`, two small amber+green squares top-right.
  Earlier Shorts used a dark theme. New ones should follow the PPT style.
- **Voice:** KB's own voice for the HRSD series (face-cam, personal). For faceless Shorts/long videos: **"voice 9"** =
  Piper TTS, LibriTTS speaker **522** (CC BY 4.0). Always add `Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)` to descriptions.
  Don't use the Piper "Ryan" voice: it's non-commercial only. ElevenLabs may replace voice 9 later.
- **Formats:** Shorts 1080×1920, 25–45 s, hook in first 2 s, captions burned in, logo badge + end card.
  Long videos 1920×1080, chapters, ≥ 8:00 if mid-roll ads matter. Loudness ≈ −14 to −16 LUFS.
- **Branding rule (hard):** the only name/brand shown anywhere (video, slides, file names, descriptions, scripts) is
  **ServiceNow Simplified**. Never show a client or employer name. Before delivering, scan text files, PPT text and the
  rendered slide images for client names.
- **Accuracy first:** verify ServiceNow claims (docs/community) before putting them on screen; never show unverified numbers
  or real client names (the HRSD scope was renamed to **"HRIS Leave"** for this reason). Say "illustrative" for mock UI.
- **YouTube:** links in Shorts descriptions/comments are not clickable, so use the Related video field. 3 hashtags, 8–12 tags.
  Short requests: `channel-kit/docs/Short_Request_Template.md`. Upload sheet format: see `channel-kit/docs/YouTube_Upload_Guide_ALL_13_videos.md`.

## Current series status

| Series | Status |
|---|---|
| ZZ_YY Shorts 1–6 | Done (voice 9). Related video: https://www.youtube.com/watch?v=RwLf7Vw4QGQ |
| Best Practices Shorts 1–6 + long video "30 ServiceNow Best Practices" (8:02) | Done (voice 9) |
| HRSD Ep 1.1 Short: auto-populate Manager/Location (PPT style, voice 9, 43 s) | Done (`channel-kit/tools/shorts/ep1_autopopulate.py`) |
| HRSD Ep 1.2 Shorts A (employee type via GlideAjax, 43 s) + B (leave duration/balance + console debug, 40 s) | Done (`channel-kit/tools/shorts/ep12_shorts.py`) |
| HRSD Ep 2 Shorts A (no-manager guard, 35 s), B (manager pill + rejection rule, 37 s), C (HRSD requests / HRIS records, 39 s) | Done (`channel-kit/tools/shorts/ep2_shorts.py`); Related video = Ep 2 once published |
| Concept Shorts 1–3 (attachments & inheritance, browser folders, output became input; 71–75 s) | Done (`channel-kit/tools/shorts/concept_shorts.py`); publish order 2 → 1 → 3 |
| HRSD HR Leave Request series, 5 episodes | Ep 1.1, 1.2 done. **Ep 2: KB re-recording with `HRSD_Episode2_Recording_Script_FINAL.md` (script + slide VO in one file) + deck v3** (`channel-kit/hrsd-episode2/`; needs his 9 slide VO files). Ep 3 = REST integration A → B, Basic Auth then OAuth 2.0 (outline: `channel-kit/hrsd-episode3/`), Ep 4 = notifications & SLAs, Ep 5 = portal/Employee Center |

## HRSD demo architecture
Two ServiceNow instances: **Instance A = HRSD** (forms, flow, HR Case) and **Instance B = "Mock HRIS"** (stand-in for the client's
Workday/SAP; scoped app HRIS Leave + HRIS Leave table). Ep 2 = manual entry on B, no auth yet. Ep 3 = Scripted REST API on B,
Connection & Credential alias on A with Basic Auth, then OAuth 2.0. Details: `channel-kit/README.md`.
