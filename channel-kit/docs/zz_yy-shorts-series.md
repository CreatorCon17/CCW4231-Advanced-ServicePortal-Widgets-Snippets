# Shorts Series — "ZZ_YY Hidden Attachments in ServiceNow"

Source video: *How to Fix ZZ_YY Hidden Attachments in ServiceNow (sys_attachment Explained)*
https://www.youtube.com/watch?v=RwLf7Vw4QGQ

---

## 0. What this is based on (read first)

- **I could not watch the video.** YouTube is blocked from the environment this was written in. I only know its
  **title** (confirmed by web search). The analysis below covers the **topic** and the format the title implies
  (problem → explanation → fix). It isn't based on the actual hooks, pacing or visuals you used.
- The technical content is from my knowledge of the platform. **Verify every script on your PDI before recording**
  (checklist in §5). Don't put anything on screen that you haven't run yourself.

---

## 1. Analysis

### What the long video covers (from the title)
| Element | What it is |
|---|---|
| **Problem** | An attachment exists, but it doesn't show in the record's attachment list (paperclip) |
| **Cause** | Its `sys_attachment.table_name` is prefixed with `ZZ_YY` (e.g. `ZZ_YYsc_req_item` instead of `sc_req_item`) |
| **Where it comes from** | Files uploaded through a **field or variable** rather than the paperclip: Image fields (e.g. user photo), File Attachment fields, and **Attachment-type catalog variables** |
| **Fix** | Find them in `sys_attachment`, then copy them (or, carefully, re-point them) to the real table |

### Why this topic works for Shorts
- **A mystery hook is built in:** "the file is there but invisible". That's curiosity plus frustration, which viewers relate to.
- **One weird keyword:** `ZZ_YY` looks strange, so people stop scrolling to find out what it is.
- **It splits naturally into small, standalone payoffs:** what it is, how to find it, how to fix it, and a trap.
  That makes it ideal for a series of 5–6 Shorts that all point back to the long video.

### Hook patterns to use (one per Short)
1. **Mystery:** "The file is attached… but nobody can see it."
2. **Speed:** "Find every hidden attachment in 10 seconds."
3. **Fix:** "Copy catalog attachments to the task in one line."
4. **Warning:** "Don't just rename ZZ_YY. Here's why."
5. **Danger:** "Your cleanup script might be deleting real files."
6. **Interview:** "Interview question: what does ZZ_YY mean?"

### Retention rules applied to every script
- **Hook in the first 2 s**, on screen as text *and* spoken.
- **One idea per Short.** If it needs a second idea, it becomes a second Short.
- **Show, don't describe:** the screen recording proves each claim (list view, script, result).
- **Captions always on**, max 3–4 words at a time, with keywords highlighted.
- **End with a loop or a payoff**, plus a pointer to the full video ("Full fix in the long video").
- **Length: 25–45 s.** Shorter is better when the payoff is clear.

---

## 2. Format for every Short (vertical 1080×1920)

```
┌──────────────────────┐
│  HOOK TEXT (top)     │  ← big, 2–5 words, stays 2–3 s
│                      │
│  SCREEN RECORDING    │  ← PDI, zoomed 150–200% so text is readable on a phone
│  (crop the relevant  │
│   part, not the      │
│   whole browser)     │
│                      │
│  CAPTIONS            │  ← middle-lower, above the YouTube UI
│  (keep bottom ~300px │
│   clear)             │
└──────────────────────┘
```

**Converting your horizontal recording to vertical:** don't letterbox the full 16:9 screen (the text gets tiny).
Crop to the relevant area and zoom. In CapCut: Canvas 9:16 → scale the clip to ~180% → keyframe the
position to follow your cursor. In DaVinci: timeline 1080×1920 → Zoom + Position keyframes.

---

## 3. THE SCRIPTS

### SHORT 1 — "The Invisible Attachment" (~35 s) ⭐ post first

| Time | On screen | Voiceover |
|---|---|---|
| 0–2 s | Hook text: **"ATTACHED… BUT INVISIBLE?"** over a RITM with an empty paperclip | "The file is attached… but nobody can see it." |
| 2–8 s | Catalog item in the Portal: user uploads a file in an **Attachment variable** → submit | "A user uploads a file through a catalog attachment variable. They submit." |
| 8–14 s | Open the RITM → attachment list is **empty** (circle it red) | "You open the request item, and there's no attachment. Nothing." |
| 14–24 s | `sys_attachment` list → the record → zoom in on `table_name = ZZ_YYsc_req_item` | "But it is in sys_attachment. Look at the table name: ZZ_YY sc_req_item. That prefix hides it from the attachment list." |
| 24–32 s | Text: **"ZZ_YY = uploaded via a field or variable"** | "ZZ_YY means the file belongs to a field or variable, not to the record's paperclip." |
| 32–35 s | Text: **"FIX → full video ↑"** | "Here's how to fix it. Full video's linked above." |

---

### SHORT 2 — "Find Them All in 10 Seconds" (~25 s)

| Time | On screen | Voiceover |
|---|---|---|
| 0–2 s | Hook: **"FIND EVERY HIDDEN FILE"** | "Find every hidden attachment in your instance, in ten seconds." |
| 2–6 s | Navigator: type `sys_attachment.list` → Enter | "Type sys_attachment dot list." |
| 6–14 s | Filter: **Table name — starts with — ZZ_YY** → Run | "Filter: table name, starts with, ZZ_YY. Run." |
| 14–20 s | Group by Table name → counts per table | "Group by table name, and now you can see exactly which tables have hidden files." |
| 20–25 s | Text: **"Save this filter"** + bookmark icon | "Save it. You'll need it again." |

**Bonus on-screen text (optional):**
`sys_attachment_list.do?sysparm_query=table_nameSTARTSWITHZZ_YY`

---

### SHORT 3 — "Copy Catalog Attachments to the Task" (~40 s)

| Time | On screen | Voiceover |
|---|---|---|
| 0–2 s | Hook: **"FULFILLERS CAN'T SEE THE FILE?"** | "Your fulfillers can't see the file the user uploaded?" |
| 2–8 s | SC Task form with an empty attachment list | "Because it was uploaded in a variable, it's stored as ZZ_YY, and it never reaches the task." |
| 8–26 s | Business Rule form (Table: **sc_task**, After, Insert), then the code below, typed or highlighted line by line | "Create an after-insert business rule on sc_task. One line: copy from ZZ_YY sc_req_item on the parent RITM, into this task." |
| 26–36 s | Submit a new request → open the task → the **file is visible** ✅ | "Submit a new request. Open the task, and there's the file." |
| 36–40 s | Text: **"1 line. Done."** | "One line. Done. Follow for more ServiceNow fixes." |

```javascript
// Business Rule — Table: sc_task | When: after | Insert: true
(function executeRule(current, previous) {
    new GlideSysAttachment().copy(
        'ZZ_YYsc_req_item', current.getValue('request_item'),  // source: hidden RITM files
        'sc_task',          current.getUniqueValue()           // target: this task
    );
})(current, previous);
```

> ⚠️ **Verify before recording:** on some releases or setups the attachment variable's file may still be on
> `ZZ_YYsc_cart_item` at the point your rule runs. Check the actual `table_name` on your PDI and use that.
> Also: if the rule runs twice, you get duplicates. Insert-only avoids that.

---

### SHORT 4 — "Don't Fix It by Hand" (~30 s)  *(updated to match your long video's demo)*

| Time | On screen | Voiceover |
|---|---|---|
| 0–2 s | Hook: **"DELETE 5 LETTERS = FIXED?"** over the `table_name` field | "Delete five letters and the attachment comes back?" |
| 2–12 s | Edit `ZZ_YYincident` → `incident` on the sys_attachment record → refresh the incident → the file appears ✅ | "Yes. Remove ZZ_YY, refresh, and the file shows in the attachment list. The image field still works too." |
| 12–20 s | Text: **"But… every record? By hand?"** + a pile of incidents | "But doing that by hand for every record? Only admins can, and nobody will keep it up." |
| 20–28 s | Business Rule form: incident, async, insert | "Put the same logic in an async business rule, so every new incident is fixed automatically." |
| 28–30 s | Text: **"Automate it → full video"** | "Full walkthrough in the long video." |

> ZZ_YY only controls visibility in the attachment list, not the image field. That's what your long video shows
> (around 2:30–3:05), so this Short is consistent with it.

### SHORT 5 — "Your Cleanup Script Might Delete Real Files" (~40 s)

| Time | On screen | Voiceover |
|---|---|---|
| 0–2 s | Hook: **"THIS SCRIPT DELETES REAL FILES"** (red) | "This cleanup script might be deleting real files." |
| 2–12 s | A typical orphan-attachment cleanup: look up `table_name`, then the record; if not found → delete | "A common cleanup job: for every attachment, find its record. If the record doesn't exist, delete the file." |
| 12–20 s | Highlight `table_name = ZZ_YYsc_req_item`, with **"table not found"** | "But there is no table called ZZ_YY sc_req_item. So the lookup fails, and a real, in-use file looks orphaned." |
| 20–34 s | The fixed code below | "Strip the ZZ_YY prefix before you look up the table. Then check the record." |
| 34–40 s | Text: **"Test with a dry run first"** | "And always run it as a dry run first. Log, don't delete." |

```javascript
var att = new GlideRecord('sys_attachment');
att.query();
while (att.next()) {
    var table = att.getValue('table_name').replace(/^ZZ_YY/, '');   // strip the prefix
    var rec = new GlideRecord(table);
    if (!rec.isValid() || !rec.get(att.getValue('table_sys_id'))) {
        gs.info('Orphan candidate: ' + att.getUniqueValue() + ' (' + table + ')'); // dry run: log only
    }
}
```

> Recording note: say that this is a **pattern to illustrate the trap**, not a ready-made production job.
> On a big instance, an unfiltered query on `sys_attachment` is heavy. Add a filter and run it in a sub-prod first.

---

### SHORT 6 — "Interview Question: What's ZZ_YY?" (~25 s)

| Time | On screen | Voiceover |
|---|---|---|
| 0–2 s | Hook: **"INTERVIEW Q 🎯"** + "What is ZZ_YY?" | "Interview question: what does ZZ_YY mean in ServiceNow?" |
| 2–5 s | Text: "Pause & answer ⏸" | "Pause and answer." |
| 5–20 s | Bullet build-up: ① prefix on `sys_attachment.table_name` ② file belongs to a field or variable (image, file attachment, attachment variable) ③ hidden from the paperclip list ④ copy with `GlideSysAttachment` if users need it | "It's a prefix on the attachment's table name. It means the file belongs to a field or variable, like an image field or an attachment variable. That's why it doesn't show in the attachment list. If people need it, copy it with GlideSysAttachment." |
| 20–25 s | Text: **"Got it right? Comment ✅"** | "Got it right? Comment yes." |

---

## 4. Posting plan

| Day | Short | Why this order |
|---|---|---|
| 1 | #1 Invisible Attachment | Broadest hook; introduces the term |
| 2 | #2 Find Them All | Quick win, very shareable |
| 3 | #3 Copy to Task | Most practical; highest save rate likely |
| 4 | #6 Interview Q | Different audience (job seekers) |
| 5 | #4 Don't Rename | Contrarian hook |
| 6 | #5 Cleanup Danger | Strongest fear hook, aimed at admins |

On each Short: set **"Related video"** to the long video, and pin a comment linking it.

**Title formulas:**
- "ServiceNow attachment invisible? It's ZZ_YY #servicenow"
- "Find hidden attachments in ServiceNow in 10 seconds"
- "Copy catalog attachments to SC Task (1 line) #servicenow"

---

## 5. Verify on your PDI before recording

- [ ] An attachment-variable upload: what is the exact `table_name` after submit (`ZZ_YYsc_req_item`? `ZZ_YYsc_cart_item`?)
- [ ] Short 3's business rule actually copies the file to the task on **your** release
- [ ] Short 4: what *actually* happens when you rename. Only claim what you saw.
- [ ] Image field (e.g. `sys_user.photo`) → confirm the `ZZ_YYsys_user` table name, for an extra example
- [ ] Record as **admin** for setup, but show the "can't see it" moment as a **fulfiller** if possible (more realistic)
- [ ] Blur instance names, user names and real company data in recordings
