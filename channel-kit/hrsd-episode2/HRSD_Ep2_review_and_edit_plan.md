# HRSD Episode 2: review, fixes & edit plan

## 1. What's in this kit

| File | What it is | Where it goes in your edit |
|---|---|---|
| `HRSD_Episode2_Hybrid_v2.pptx` | Your deck with 3 text fixes (below). Nothing else changed. | Replace the original |
| `slide1_narrated.mp4` | Title card, ~5 s | Right after the cold open (0:25) |
| `PPT_walkthrough_slides2-5.mp4` | Slides 2–5 narrated from your script, with amber highlights that follow the narration | The PPT section (2:00–3:30) |
| `slide2…5_narrated.mp4` | The same four, as separate clips | If you want to cut between them and face-cam |
| `slide6_narrated.mp4` | Mock HRIS table schema | Start of Build 1 (3:30), *before* you create the fields |
| `slide7_narrated.mp4` | "What we're NOT doing today" | Outro, where you list honest flags (14:00) |
| `slide8_narrated.mp4` | Next episode card | Last ~15–20 s, which leaves room for YouTube end-screen elements |
| `bumper_build1/2/3.mp4`, `bumper_demo1/2.mp4` (+ `.png`) | 2.6 s section title cards in your deck style | Before each build / demo |
| `lowerthird_employee/manager/hr_team.png` | Transparent "LOGGED IN AS" overlays | Every time you switch user (your own production note says to) |
| `slide*.srt` | Subtitles for each narrated clip | Merge into the episode's captions |

**About the narration:** the clips use **voice 9** (free AI voice, LibriTTS speaker 522, CC BY 4.0). Add the credit line
"Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)" to the description.
This series is personal ("I'm KB", face-cam, client stories), so consider recording these lines in your own voice or with ElevenLabs later.
The exact lines are in the `slide*.srt` files.

---

## 2. Fixes I already made in the deck (`_v2.pptx`)

| Slide | Before | After | Why |
|---|---|---|---|
| 5 | "Four build steps + two demo moments" | "**Three** build steps + two demo moments" | The slide lists 3 BUILD + 2 DEMO, and your script says "three builds, two demos" |
| 5 | Step 3: "Approval email, portal approval… Both approve and reject paths." | "Manager approves from My Approvals, then the case transitions. (Approval email arrives in Ep 4.)" | Your script says notifications are Episode 4, and Demo 1 only shows the approve path |
| 8 | "Subscribe — new episode will be soon" | "Subscribe — new episode coming soon" | Grammar |

---

## 3. Script issues to fix before you record (ranked)

1. **Client name (check this first).** The scope is "[client] HR Mock" / `x_[client]_…`, and the script says it's "based on an actual client project".
   If *the client* is the real client, showing their name in a public video can breach your NDA or contract. A neutral scope
   (e.g. `x_snsimp_hr_mock`) removes the risk. Only you know whether it matters, but decide **before** you record, because the name is on slide 6 and in every table name on screen.

2. **Scope mismatch.** The table is created in the *[client] HR Mock* scope, but the flow is created with Application = *Advanced Solutions*.
   A flow in one scope writing to a table in another needs cross-scope access (table Application Access settings and/or cross-scope privileges).
   That bites hard in **Episode 3**, when the flow writes to this table. Either build both in the same scope, or say on camera why they differ.

3. **Scoped table name.** In a scoped app, the platform adds the scope prefix to the name you type. Typing `leave_record` only gives
   `x_[client]_hris_mock_leave_record` if your scope prefix is exactly `x_[client]_hris_mock`. Check that the name on screen matches slide 6.

4. **Requester with no manager.** "Requested For → Manager" is empty for some users. Test what *Ask For Approval* does with no approver
   on your release, then add a guard, e.g. *If Manager is empty → assign to Leave Management Team with a work note*.
   That's 20–30 s on camera, and it's the first thing real viewers will hit.

5. **"No notifications yet" may not be true.** Out of the box, approval records can trigger approval-request notifications.
   On a PDI the email usually isn't *sent*, but it may appear in the outbox. Check `sys_email` after Demo 1 and adjust the line
   ("emails are Episode 4") if needed.

6. **Reject path is built but never shown.** Build 3 adds the Else branch, but no demo exercises it. Either show a 20-second reject
   (case → Closed Incomplete), or say "test the reject path yourself; it's the same flow".

7. **Field names on the HR Case.** The script says "Resolution Code" and "Close notes". Confirm the exact labels on `sn_hr_core_case`
   in your release before recording, so the Update Record step on screen matches what you say.

8. **Cold open says "Four moving parts"**, but slide 3 says five steps. Say "five steps" for consistency.

---

## 4. Edit plan (timeline)

```
0:00  Cold open montage (your screen recording) — keep under 25 s
0:25  slide1_narrated.mp4  (title)
0:30  Series intro (face-cam)
1:15  Recap (face-cam)
2:00  PPT_walkthrough_slides2-5.mp4
3:30  bumper_build1 → slide6_narrated → build on PDI
5:30  bumper_build2 → Flow Designer (150% zoom)
8:00  bumper_demo1 → lowerthird_employee → … → lowerthird_manager → …
10:00 bumper_build3 → Flow Designer
11:30 bumper_demo2 → lowerthird_employee / manager / hr_team as you switch
13:00 Bridge to Episode 3 (face-cam)
14:00 slide7_narrated (honest flags) → outro → slide8_narrated (end screen)
```

**Chapters for the description** (update the times after editing):
```
0:00 What we're building
0:30 Series intro
1:15 Where we are
2:00 The flow & build order
3:30 Build 1: Mock HRIS table
5:30 Build 2: Manager approval (Flow Designer)
8:00 Demo 1: Manager approves
10:00 Build 3: Auto-assign on approval
11:30 Demo 2: HR team updates HRIS & closes
13:00 Why Episode 3 matters
14:00 Wrap-up & next episode
```

---

## 5. Suggestions

- **Thumbnail:** slide 3's five-step flow, cropped tight, with "MANAGER APPROVAL" in big text and your face (if you use face-cam).
  Episode number small, top corner. Series thumbnails should look alike so the playlist reads as one set.
- **Shorts to cut from this episode** (each stands alone):
  1. *"Approver = requester's manager in 1 data pill"*: the Flow Designer pill path (Trigger → HR Case → Requested For → Manager).
  2. *"HRSD vs HRIS: who owns leave?"*: slide 4, 30 s. A strong opinion is good for comments.
  3. *"What happens if the requester has no manager?"*: the edge case from §3.4.
- **Pacing:** your notes already say this, and they're right. Speed-ramp every save spinner and impersonation click. The lower-thirds replace the need to show the impersonation menu.
- **Comment question:** your "where does leave data live?" question is good. Pin it as the first comment too.
