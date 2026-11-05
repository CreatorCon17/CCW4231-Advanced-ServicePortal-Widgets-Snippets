# ServiceNow Simplified: Best Practices Shorts (6-part series)

All videos: 1080×1920 · 37–42 s · male AI voice · logo badge + end card · ~−15 LUFS.

**Voice:** voice 9 (Piper TTS, LibriTTS speaker 522, CC BY 4.0). Keep the credit line in every description.

**Settings for all:** Not made for kids · Category: Education · Subtitles: upload the `_captions.srt` (English, with timing) · Altered/synthetic content: No (illustrated graphics; voice doesn't imitate a real person).

**Playlist:** create "ServiceNow Best Practices (Shorts)" and add all 6 in order. The end cards say "Next: …", so post in order, one per day.

**Tags (all):** `servicenow, servicenow best practices, servicenow developer, servicenow admin, servicenow tips, servicenow interview questions, servicenow simplified, glide record, business rule, client script`

---

## 1/6 · Server-Side Scripting
**File:** `bp1_server_side_scripting.mp4` (+ `_captions.srt`, `_transcript.txt`, `_cover.jpg`)

**Title:** `4 ServiceNow server-side scripting habits (GlideAggregate, setLimit, getValue) #servicenow`

**Description**
```
Four server-side scripting habits every ServiceNow developer should have.

• Counting records? Use GlideAggregate. getRowCount() pulls every record first, and gets slower as the table grows.
• Need just one record? Add setLimit(1) and let the database stop early.
• Never hard-code sys_ids. Store them in a system property and read it with gs.getProperty().
• Need a reference field's sys_id? Use getValue(). Don't dot-walk to sys_id.

Part 1/6 of the ServiceNow Best Practices series. Save it for your next code review.

#servicenow #servicenowdeveloper #javascript #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Pinned comment:** `Which of these do you see broken most in code reviews? 👇`

---

## 2/6 · Client Scripts
**File:** `bp2_client_scripts.mp4` (+ `_captions.srt`, `_transcript.txt`, `_cover.jpg`)

**Title:** `Slow ServiceNow forms? 4 client script best practices #servicenow`

**Description**
```
Is your form slow to load? These four client script habits fix most of it.

• Making fields mandatory, visible or read-only? Use a UI Policy, not a Client Script.
• In onChange scripts, exit early when the form is loading or the new value is empty.
• Need server data? Use g_scratchpad (display BR) or async GlideAjax. Client GlideRecord and getReference() are no longer recommended.
• Setting a reference field? Pass the display value too, or the form makes an extra trip to the server.

Part 2/6 of the ServiceNow Best Practices series. Save it for your next code review.

#servicenow #servicenowdeveloper #clientscript #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Pinned comment:** `Which of these do you see broken most in code reviews? 👇`

---

## 3/6 · Business Rules
**File:** `bp3_business_rules.mp4` (+ `_captions.srt`, `_transcript.txt`, `_cover.jpg`)

**Title:** `4 ServiceNow Business Rule mistakes (current.update, global BRs) #servicenow`

**Description**
```
Four business rule mistakes that slow down your instance.

• Don't call current.update() in a Business Rule. It runs the rules again and can loop. In a before rule, just set the value. It saves automatically.
• Always add a condition. Without one, the rule runs on every single save.
• If the user doesn't need the result right away, use async instead of after. They get control back faster.
• Don't write global Business Rules. They load everywhere. Put reusable code in a Script Include. It loads only when called.

Part 3/6 of the ServiceNow Best Practices series. Save it for your next code review.

#servicenow #businessrule #servicenowdeveloper #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Pinned comment:** `Which of these do you see broken most in code reviews? 👇`

---

## 4/6 · Debugging
**File:** `bp4_debugging.mp4` (+ `_captions.srt`, `_transcript.txt`, `_cover.jpg`)

**Title:** `Stop using gs.log(): ServiceNow debugging best practices #servicenow`

**Description**
```
Still debugging with gs dot log? Here's a better way.

• gs.log() and gs.print() don't work in scoped apps. Use gs.info() or gs.debug(). They work in both.
• Wrap debug messages in a system property check. Turn logging on or off without touching code.
• Debug Business Rule shows every rule that ran: started, finished, or skipped, with the condition that failed.
• Before production, remove leftover log and alert statements, and switch debugging off.

Part 4/6 of the ServiceNow Best Practices series. Save it for your next code review.

#servicenow #debugging #servicenowdeveloper #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Pinned comment:** `Which of these do you see broken most in code reviews? 👇`

---

## 5/6 · Logs & Queues
**File:** `bp5_logs_and_queues.mp4` (+ `_captions.srt`, `_transcript.txt`, `_cover.jpg`)

**Title:** `Your ServiceNow logs are warning you: where to look #servicenow`

**Description**
```
Your logs are warning you. Here's where to look.

• Check System Logs > System Log > All regularly. Every error: fix it, or document it as a known issue.
• Search your node logs for these messages. Each one points to a script or query that needs fixing.
• Open System Diagnostics > Slow Queries. Sort by Total Execution Time, and use Example to find the script behind it.
• In the Event Log, sort by Processing duration and group by Name. An event nothing responds to is just noise.

Part 5/6 of the ServiceNow Best Practices series. Save it for your next code review.

#servicenow #servicenowadmin #performance #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Pinned comment:** `Which of these do you see broken most in code reviews? 👇`

---

## 6/6 · Update Sets & Xml
**File:** `bp6_update_sets_xml.mp4` (+ `_captions.srt`, `_transcript.txt`, `_cover.jpg`)

**Title:** `Update set worked in dev, broke in test? ServiceNow migration tips #servicenow`

**Description**
```
Your update set worked in dev, but broke in test? Here's why.

• Keep a migration document: the order to apply update sets, plus plugins, properties and servers to set up.
• Some data isn't captured in update sets, like approval lookup records. Move it as XML, and note it in the update set description.
• Importing XML doesn't run Business Rules and doesn't update the instance cache. Plan for that.
• An XML export has only that record. Export a user, and their groups and roles don't come with it.

Part 6/6 of the ServiceNow Best Practices series. Save it for your next code review.

#servicenow #updateset #servicenowadmin #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Pinned comment:** `Which of these do you see broken most in code reviews? 👇`
