# Upload sheet: HRSD Episode 1 Short "Auto-fill the Manager field"

**File:** `hrsd_ep1_short_autopopulate.mp4` (1080×1920, 43 s, voice 9, −14 LUFS) · `…_captions.srt` · `…_cover.jpg`
**Source:** HR Leave Request series, Episode 1.1 (HR Service & Record Producer), the auto-populate part at ~18:28–20:30.

## Title (pick one)
1. ✅ `Auto-Fill the Manager Field in ServiceNow (No Client Script)`
2. `Stop Writing Client Scripts for This (ServiceNow Auto-Populate)`
3. `ServiceNow Record Producer Trick: Auto-Populate Manager & Location`

## Description
```
Auto-fill Manager and Location on a ServiceNow record producer, with zero client scripts:
1) Requested for → Default value: javascript:gs.getUserID()
2) Manager variable → Auto-populate tab → Dependent question: Requested for → Dot-walk path: Manager
3) Same for Location
Catch: it only follows fields on the record you point it at. Employee type lives on the HR profile, not sys_user.

From Episode 1 of the HR Leave Request series (HRSD). Full build: tap the related video above ⬆️

#servicenow #hrsd #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

## Tags
```
servicenow, service now, servicenow hrsd, record producer, auto populate servicenow, catalog variables, servicenow client script, servicenow tutorial, servicenow developer, servicenow tips, hr service delivery
```

## Settings
| Setting | Value |
|---|---|
| **Related video** | **Episode 1.1** (HR Service & Record Producer). This is the only clickable link from a Short |
| Audience | Not made for kids |
| Category | Education |
| Captions | Upload `hrsd_ep1_short_autopopulate_captions.srt` (English, with timing) |
| Altered/synthetic content | No (illustrated UI; AI voice doesn't imitate a real person) |
| Playlist | HR Leave Request Series (HRSD) |
| Cover | The hook frame ("Auto-fill the Manager field / No client script") |

## Pinned comment
```
Do you still use onChange client scripts for this, or have you switched to Auto-populate? 👇
```

## Before publishing
- [ ] Confirm the **Auto-populate** tab exists on catalog variables in your release (it's a newer feature; check your PDI). If the label differs, tell me and I'll update the on-screen text.
- [ ] Names on screen (Alex Carter, Sam Patel, London) are illustrative. No client or employer names anywhere ✅
