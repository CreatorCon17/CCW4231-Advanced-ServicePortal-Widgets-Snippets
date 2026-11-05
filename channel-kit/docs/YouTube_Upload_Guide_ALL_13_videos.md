# YouTube Upload Guide — ServiceNow Simplified (13 videos)

Copy-paste ready. One section per video: **Title · Description · Tags · Settings · Pinned comment**.

---

## 0. How YouTube actually decides (so you know what matters)

| What | How much it matters | What we do |
|---|---|---|
| **Title + thumbnail/first frame** | High: decides if people click | Keyword first, curiosity second, under ~60 chars visible |
| **First 2–3 seconds (Shorts)** | Very high: decides "swiped away" vs watched | Already built into every video (hook text + voice) |
| **Watch time / % viewed / rewatches** | Very high | Shorts are 28–42 s; keep them, don't pad |
| **Comments, likes, shares, subscribes** | Medium | Every video ends with a question; pin a comment that asks one |
| **Description (first ~2 lines)** | Medium for search | Main keyword in line 1 |
| **Hashtags** | Low–medium | **3 per video** (first 3 show above the title). Never more than 15, or all are ignored |
| **Tags** | **Low**: YouTube says tags mainly help with misspellings | 8–12 short tags, including "service now" spelling |
| **Links in Shorts description/comments** | **Not clickable** since 2023 | Use the **Related video** field on every Short |
| **Captions (.srt)** | Helps accessibility + search | Upload the `_captions.srt` for every video |
| **Playlists / series** | Helps session watch time | 3 playlists (below) |

**Same settings for all 13:**
- Audience: **No, it's not made for kids**
- Category: **Education** · Language: **English** · Caption language: **English**
- Altered or synthetic content: **No**. These are illustrated graphics, and the AI voice doesn't imitate a real person.
  (Ticking "Yes" is harmless if you prefer.)
- License: Standard YouTube License · Allow embedding: On · Comments: On
- **Keep the voice credit line** at the end of every description: `Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)`. It's required by the licence.

**Playlists to create:**
1. `ZZ_YY Hidden Attachments — ServiceNow Explained` → ZZ_YY Shorts 1–6 + your existing long video
2. `ServiceNow Best Practices` → Long video + Best-Practice Shorts 1–6
3. `HR Leave Request Series (HRSD)` → Episode 1.1, 1.2, 2… (when you upload Episode 2)

---

## 1. Posting schedule (2 weeks, 1 upload per day)

Upload the **long video first**: the 6 Best-Practice Shorts point to it via Related video, so it needs to exist.
Check **YouTube Studio → Analytics → Audience → "When your viewers are on YouTube"** and schedule at the start of your darkest hour.

| Day | Upload | Related video (Shorts) |
|---|---|---|
| 1 | **LONG: 30 ServiceNow Best Practices** | — |
| 2 | ZZ_YY Short 1 — Attached but missing | Your ZZ_YY video (`RwLf7Vw4QGQ`) |
| 3 | BP Short 1 — Server-side scripting | Long video |
| 4 | ZZ_YY Short 2 — Find them all | ZZ_YY video |
| 5 | BP Short 2 — Client scripts | Long video |
| 6 | ZZ_YY Short 6 — Interview question | ZZ_YY video |
| 7 | BP Short 3 — Business rules | Long video |
| 8 | ZZ_YY Short 4 — Delete 5 letters | ZZ_YY video |
| 9 | BP Short 4 — Debugging | Long video |
| 10 | ZZ_YY Short 3 — Business Rule fix | ZZ_YY video |
| 11 | BP Short 5 — Logs & queues | Long video |
| 12 | ZZ_YY Short 5 — Cleanup script trap | ZZ_YY video |
| 13 | BP Short 6 — Update sets & XML | Long video |

> BP Shorts end with "Next: …", so keep them in order 1→6. Alternating series stops your feed from feeling repetitive.

---

## 2. LONG VIDEO — 30 ServiceNow Best Practices (8:02)

**File:** `ServiceNow_30_Best_Practices.mp4` · Thumbnail: `thumbnail_30_best_practices.jpg` · Captions: `ServiceNow_30_Best_Practices_captions.srt`

**Title (use #1; #2/#3 for A/B testing via "Test & Compare" if your channel has it):**
1. `30 ServiceNow Best Practices Every Developer Should Know`
2. `Stop Writing Slow ServiceNow Code: 30 Best Practices`
3. `ServiceNow Best Practices in 8 Minutes (Scripts, Business Rules, Debugging)`

**Description:**
```
30 ServiceNow best practices for developers and admins: server-side scripting, client scripts, business rules, debugging, logs & queues, and update sets / XML. Each one shows what to avoid and what to do instead.

⏱ Chapters
0:00 Intro
0:24 Server-side scripting
2:10 Client scripts
3:31 Business rules
4:40 Debugging
5:45 Logs & queues
6:42 Update sets & XML
7:30 Recap & wrap-up

What you'll learn:
✅ GlideAggregate vs getRowCount, encoded queries, setLimit
✅ getValue vs getDisplayValue (and why it matters)
✅ g_scratchpad & async GlideAjax instead of getReference
✅ Why current.update() in a Business Rule is a bad idea
✅ gs.info vs gs.log, Debug Business Rule, Slow Queries
✅ What update sets DON'T capture, and XML export limits

▶ Quick refreshers: ServiceNow Best Practices Shorts → <PLAYLIST LINK>
▶ ZZ_YY hidden attachments explained → https://www.youtube.com/watch?v=RwLf7Vw4QGQ

Based on ServiceNow's published developer best practices. Code on screen is illustrative. Test in a sub-production instance first.

#servicenow #servicenowdeveloper #servicenowbestpractices

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Tags:**
```
servicenow, service now, servicenow best practices, servicenow developer, servicenow tutorial, glide record, glideaggregate, business rule servicenow, client script servicenow, servicenow debugging, update set, servicenow interview questions
```

**Extras:**
- **End screen** (last 20 s): Subscribe + "Playlist: ServiceNow Best Practices" + "Best for viewer"
- **Cards:** at 0:24 → Best Practices Shorts playlist · at 3:31 → your ZZ_YY video
- Monetization: 8:02 → mid-roll ads available. Place one at a chapter boundary (e.g. 3:31), not mid-sentence.

**Pinned comment:**
```
Which of these 30 do you see broken most in code reviews? 👇 (Chapters are in the description.)
```

---

## 3. ZZ_YY SHORTS (6)

**Related video for all 6:** `https://www.youtube.com/watch?v=RwLf7Vw4QGQ`
**Tags for all 6:**
```
servicenow, service now, zz_yy, sys_attachment, servicenow attachment, attachment not showing servicenow, servicenow business rule, servicenow admin, servicenow developer, servicenow tips
```

### ZZ_YY Short 1 — Attached but missing (36 s)
**Title:** `ServiceNow Attachment Missing? It's ZZ_YY (Not a Bug)`
**Description:**
```
Attachment uploaded… but the incident shows nothing? That's ZZ_YY. Files from variables and image fields get a ZZ_YY prefix in sys_attachment, which hides them from the attachment list. Platform design, not a bug.
Full explanation + fix: tap the related video above ⬆️

#servicenow #servicenowadmin #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```
**Pinned comment:** `Have you hit ZZ_YY on a real project? Which table? 👇`

### ZZ_YY Short 2 — Find them all (31 s)
**Title:** `Find Every Hidden Attachment in ServiceNow (10 Seconds)`
**Description:**
```
Find every hidden (ZZ_YY) attachment in your ServiceNow instance:
1) sys_attachment.list  2) Table name starts with ZZ_YY  3) Group by Table name

#servicenow #servicenowtips #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```
**Pinned comment:** `How many ZZ_YY files did you find? Drop the number 👇`

### ZZ_YY Short 3 — Business Rule fix (32 s)
**Title:** `Fix Hidden ServiceNow Attachments Automatically (Business Rule)`
**Description:**
```
Stop fixing ZZ_YY attachments by hand. An async Business Rule on insert moves them back into the attachment list. Use while, not if, so every file gets fixed.
Script is in the pinned comment.

#servicenow #businessrule #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```
**Pinned comment (the script):**
```
Business Rule · incident · async · Insert · Advanced
var att = new GlideRecord('sys_attachment');
var table = current.getTableName();
att.addQuery('table_name', 'ZZ_YY' + table);
att.addQuery('table_sys_id', current.sys_id);
att.query();
while (att.next()) {
  att.setValue('table_name', table);
  att.update();
}
Test in a sub-prod instance first.
```

### ZZ_YY Short 4 — Delete 5 letters (33 s)
**Title:** `Delete 5 Letters and the Attachment Comes Back? (ServiceNow)`
**Description:**
```
Removing ZZ_YY from sys_attachment.table_name brings the file back into the attachment list, and the image field still works. ZZ_YY only controls visibility. But fixing records by hand doesn't scale, so automate it.

#servicenow #servicenowadmin #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```
**Pinned comment:** `Manual fix or Business Rule: which does your team use? 👇`

### ZZ_YY Short 5 — Cleanup script trap (28 s)
**Title:** `This ServiceNow Cleanup Script Can Delete Real Files`
**Description:**
```
Orphan-attachment cleanup jobs look up each attachment's table. But there's no table called ZZ_YYincident, so files still in use can look orphaned. Strip the ZZ_YY prefix first, and always dry-run (log, don't delete).

#servicenow #servicenowdeveloper #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```
**Pinned comment:** `The code is a pattern to show the trap, not a ready-made job. Have you seen this happen? 👇`

### ZZ_YY Short 6 — Interview question (28 s)
**Title:** `ServiceNow Interview Question: What Does ZZ_YY Mean?`
**Description:**
```
ServiceNow interview question: what does ZZ_YY mean?
It's a prefix on sys_attachment.table_name. The file belongs to a variable or image field, so it's hidden from the attachment list. By design, not a bug.

#servicenow #servicenowinterview #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```
**Pinned comment:** `Did you get it before the answer? Comment YES or NO 👇`

---

## 4. BEST-PRACTICE SHORTS (6)

**Related video for all 6:** your **long video** (upload it first, then paste its link)
**Tags for all 6:**
```
servicenow, service now, servicenow best practices, servicenow developer, servicenow tips, servicenow tutorial, servicenow interview questions, servicenow scripting
```

### BP Short 1 — Server-side scripting (37 s)
**Title:** `4 ServiceNow Scripting Habits Senior Devs Never Skip`
**Description:**
```
4 server-side scripting habits: GlideAggregate instead of getRowCount, setLimit(1), no hard-coded sys_ids (use a system property), and getValue() instead of dot-walking to sys_id.
Part 1/6 of ServiceNow Best Practices.

#servicenow #servicenowdeveloper #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```
**Pinned comment:** `Which one do you see broken most in code reviews? 👇`

### BP Short 2 — Client scripts (42 s)
**Title:** `Slow ServiceNow Forms? Fix These 4 Client Script Mistakes`
**Description:**
```
UI Policy before Client Script · exit onChange early · g_scratchpad or async GlideAjax (not getReference) · pass the display value to setValue.
Part 2/6 of ServiceNow Best Practices.

#servicenow #clientscript #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```
**Pinned comment:** `What's the slowest form you've had to fix? 👇`

### BP Short 3 — Business rules (37 s)
**Title:** `4 ServiceNow Business Rule Mistakes (current.update!)`
**Description:**
```
No current.update() in Business Rules · always add a condition · async instead of after when it can wait · Script Includes instead of global Business Rules.
Part 3/6 of ServiceNow Best Practices.

#servicenow #businessrule #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```
**Pinned comment:** `Ever seen a recursive Business Rule in production? 👇`

### BP Short 4 — Debugging (41 s)
**Title:** `Still Using gs.log()? Debug ServiceNow the Right Way`
**Description:**
```
gs.info / gs.debug work in scoped and global apps · switch logging with a system property · Debug Business Rule symbols ==> <== === · clean up before production.
Part 4/6 of ServiceNow Best Practices.

#servicenow #debugging #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```
**Pinned comment:** `What's your go-to ServiceNow debugging trick? 👇`

### BP Short 5 — Logs & queues (39 s)
**Title:** `Your ServiceNow Logs Are Warning You (Here's Where to Look)`
**Description:**
```
System Log > All · node log messages to search for (slow evaluate, recursive business rule…) · System Diagnostics > Slow Queries · noisy events in the Event Log.
Part 5/6 of ServiceNow Best Practices.

#servicenow #servicenowadmin #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```
**Pinned comment:** `How often do you actually check the system log? Be honest 👇`

### BP Short 6 — Update sets & XML (38 s)
**Title:** `Worked in Dev, Broke in Test? ServiceNow Update Set Tips`
**Description:**
```
Keep a migration document · some data isn't captured in update sets (move it as XML) · XML import skips business rules and the cache · an XML export contains only that record.
Part 6/6 of ServiceNow Best Practices.

#servicenow #updateset #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```
**Pinned comment:** `What's the worst update set surprise you've had? 👇`

---

## 5. Checklist per upload (30 seconds each)

- [ ] Title pasted · Description pasted (voice credit line kept) · Tags pasted
- [ ] Captions: upload the `_captions.srt` (English, "With timing")
- [ ] Shorts: **Related video** set · cover frame picked (the hook frame)
- [ ] Long video: custom thumbnail · chapters show in the progress bar · end screen + cards
- [ ] Added to the right playlist
- [ ] Scheduled for your audience's peak time
- [ ] After publishing: pin the comment, and **reply to every comment in the first hour**. Early engagement helps distribution.

## 6. What to watch after 48 hours (YouTube Studio)

| Metric | Shorts: healthy | If low, try |
|---|---|---|
| **Viewed vs swiped away** | > 60–70% viewed | Change the title / first frame on the next Short; the hook is the issue |
| **Average % viewed** | > 70% (rewatches can push it above 100%) | Cut the slowest scene in the next one |
| Long video: **CTR** | 4–10% is typical | Test title #2 / #3, brighten the thumbnail |
| Long video: **avg view duration** | > 40% | Check where the retention graph drops, and fix that pattern next time |

These numbers are common creator benchmarks, not YouTube guarantees. Compare against your own channel average.
