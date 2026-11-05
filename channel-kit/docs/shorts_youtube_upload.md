# ServiceNow Simplified: Shorts upload sheet (Shorts 1–6, ZZ_YY series)

**All videos:** 1080×1920, H.264/AAC, ~−15 LUFS, male AI voice, ServiceNow Simplified logo (corner badge + end card).

**Voice licence:** Piper TTS, LibriTTS voice (speaker 522, "voice 9"), licensed **CC BY 4.0**. Commercial use is OK,
**but attribution is required**. The credit line is already in every description below. Keep it.

---

## SHORT 1: "Attached… but missing" (36 s)
**Files:** `short1_zz_yy_attached_but_missing.mp4` · `…_captions.srt` · `…_transcript.txt` · `…_cover.jpg`

**Title:** `ServiceNow attachment missing? It's ZZ_YY (not a bug) #servicenow`

**Description**
```
The screenshot is attached… but the incident shows nothing? 🤔

When a file is uploaded through a variable or an image field, ServiceNow stores it in
sys_attachment with a ZZ_YY prefix on the table name (e.g. ZZ_YYincident).
That prefix hides it from the attachment list. It's platform design, not a bug.

▶ Full video + Business Rule fix: https://www.youtube.com/watch?v=RwLf7Vw4QGQ

#servicenow #servicenowdeveloper #servicenowadmin #sys_attachment #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Pinned comment**
```
Full fix (Business Rule) here 👉 https://www.youtube.com/watch?v=RwLf7Vw4QGQ
Have you hit ZZ_YY in your instance? Tell me which table 👇
```

---

## SHORT 2: "Find every hidden attachment in 10 seconds" (31 s)
**Files:** `short2_find_hidden_attachments.mp4` · `…_captions.srt` · `…_transcript.txt` · `…_cover.jpg`

**Title:** `Find every hidden attachment in ServiceNow (10 seconds) #servicenow`

**Description**
```
Find every attachment hidden from the attachment list, in 10 seconds:

1. Filter navigator → sys_attachment.list
2. Condition: Table name | starts with | ZZ_YY → Run
3. Group by Table name to see which tables are affected

Bookmark: sys_attachment_list.do?sysparm_query=table_nameSTARTSWITHZZ_YY

▶ Why it happens + Business Rule fix: https://www.youtube.com/watch?v=RwLf7Vw4QGQ

#servicenow #servicenowadmin #servicenowdeveloper #sys_attachment #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Pinned comment**
```
How many ZZ_YY files did you find? Drop the number 👇
Full explanation + fix: https://www.youtube.com/watch?v=RwLf7Vw4QGQ
```

---

## SHORT 3: "Fix hidden attachments automatically" (32 s)
**Files:** `short3_business_rule_fix.mp4` · `…_captions.srt` · `…_transcript.txt` · `…_cover.jpg`

**Title:** `Fix ZZ_YY hidden attachments automatically (Business Rule) #servicenow`

**Description**
```
Stop fixing hidden attachments by hand. An async Business Rule on incident (Insert)
moves ZZ_YY attachments back into the attachment list automatically.

Tip: use while, not if, so records with multiple files get every file fixed.

▶ Full walkthrough: https://www.youtube.com/watch?v=RwLf7Vw4QGQ

#servicenow #servicenowdeveloper #businessrule #sys_attachment #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Pinned comment (with the script)**
```
Script from the video 👇 (Business Rule · incident · async · Insert · Advanced)
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

---

## SHORT 4: "Delete 5 letters = fixed?" (33 s)
**Files:** `short4_dont_fix_by_hand.mp4` · `…_captions.srt` · `…_transcript.txt` · `…_cover.jpg`

**Title:** `Remove ZZ_YY and the attachment comes back… but don't do it by hand #servicenow`

**Description**
```
Removing the ZZ_YY prefix from sys_attachment.table_name makes the file appear in the
attachment list, and the image field keeps working. ZZ_YY only controls visibility.
But doing it by hand doesn't scale. Automate it with an async Business Rule.

▶ Full video: https://www.youtube.com/watch?v=RwLf7Vw4QGQ

#servicenow #servicenowadmin #sys_attachment #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Pinned comment**
```
Manual fix or Business Rule: which does your team use? 👇
```

---

## SHORT 5: "Your cleanup script might delete real files" (28 s)
**Files:** `short5_cleanup_script_trap.mp4` · `…_captions.srt` · `…_transcript.txt` · `…_cover.jpg`

**Title:** `This ServiceNow cleanup script can delete REAL attachments (ZZ_YY trap) #servicenow`

**Description**
```
Orphan-attachment cleanup scripts look up each attachment's table. But there is no table
called ZZ_YYincident, so in-use files can look orphaned. Strip the ZZ_YY prefix first,
and always do a dry run (log, don't delete).

▶ Why ZZ_YY exists: https://www.youtube.com/watch?v=RwLf7Vw4QGQ

#servicenow #servicenowdeveloper #sys_attachment #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Pinned comment**
```
The code in this Short is a pattern to show the trap, not a ready-made cleanup job.
Filter your query and test in sub-prod first. Have you seen this happen? 👇
```

---

## SHORT 6: "Interview question: what is ZZ_YY?" (28 s)
**Files:** `short6_interview_question.mp4` · `…_captions.srt` · `…_transcript.txt` · `…_cover.jpg`

**Title:** `ServiceNow interview question: what does ZZ_YY mean? #servicenow`

**Description**
```
ServiceNow interview question: what does ZZ_YY mean?

1. A prefix on sys_attachment.table_name
2. The file belongs to a variable or image field
3. Hidden from the attachment list, by design (not a bug)
4. Need it visible? An async Business Rule sets the table name back

▶ Full explainer: https://www.youtube.com/watch?v=RwLf7Vw4QGQ

#servicenow #servicenowinterview #servicenowinterviewquestions #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Pinned comment**
```
Did you get it right before the answer? Comment YES or NO 👇
```

---

## Posting schedule (one per day)
| Day | Short | Why |
|---|---|---|
| 1 | Short 1: Attached… but missing | Introduces the problem |
| 2 | Short 2: Find them all | Quick win |
| 3 | Short 6: Interview Q | Different audience (job seekers) |
| 4 | Short 4: Delete 5 letters | Shows the manual fix + why not by hand |
| 5 | Short 3: Business Rule fix | The payoff: the automated fix |
| 6 | Short 5: Cleanup trap | Strongest warning hook, for admins |

---

## Tags (same for all)
```
servicenow, servicenow tutorial, servicenow attachment, ZZ_YY, sys_attachment, servicenow business rule, servicenow admin, servicenow developer, servicenow tips, attachment not showing servicenow, servicenow interview questions, servicenow simplified
```

## Settings (same for all)
| Setting | Value |
|---|---|
| Audience | No, it's not made for kids |
| Category | Education |
| Related video | The long video (`RwLf7Vw4QGQ`) |
| Subtitles | Upload the `_captions.srt` → English → "With timing" |
| Altered or synthetic content | **No**: illustrated UI and graphics, and the synthetic voice doesn't imitate a real person. Ticking "Yes" carries no penalty if you prefer. |
| Schedule | See the posting schedule above |

## Before publishing
- [ ] Watch each one on your phone with sound on. Check how the voice says "Z Z, Y Y" and that captions aren't under the Shorts buttons.
- [ ] Screens are illustrations; INC numbers, file names and the counts in Short 2 are examples.
- [ ] Short 3: run the business rule on your PDI with **two** attachment variables and confirm both files appear.
- [ ] Short 2: confirm on your instance that typing `sys_attachment.list` in the navigator opens the list (it should on current releases).
