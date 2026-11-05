# Upload sheet: Concept Shorts 1–3 ("concepts, not tricks")

All: 1080×1920 · PPT style · voice 9 · −14 LUFS · 71–75 s · captions burned in + `.srt`
Audience: not for kids · Category: Education · Altered content: No
Playlist: **ServiceNow Concepts** (new) · Related video: the ZZ_YY attachments video https://www.youtube.com/watch?v=RwLf7Vw4QGQ
(Shorts 1 and 3 are about sys_attachment, so it fits; for Short 2 it's optional.)

**Publish order:** 2 → 1 → 3, 2–3 days apart. Short 2 is a web-platform lesson, so it reaches past the usual audience.

---

## SHORT 2: Why a browser can't put files in folders (74 s)
**File:** `concept2_browser_cant_make_folders.mp4`

**Title (pick one):**
1. ✅ `"Download Into Folders, No Zip"? Here's Why You Can't`
2. `Why a Browser Can't Create Folders (Scope This in Week One)`
3. `The Requirement You Should Say No To in Week One`

**Description:**
```
"One folder per record, no zip." Every part of that is possible except the folders.
A web page can't touch your file system: it hands bytes to the browser, and the browser decides where they go.
Inside the browser you get three options: a ZIP, flat downloads, or the File System Access API (Chrome/Edge only, permission prompt, can be disabled by IT).
If folders are a must, plan a server-side export instead. Know the boundary before you scope the story.

#servicenow #webdevelopment #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```
**Tags:**
```
servicenow, service now, file system access api, browser download, javascript, web development, servicenow developer, requirements, solution architecture, servicenow tips
```
**Pinned comment:** `Have you had a requirement like this? What did you end up delivering? 👇`

---

## SHORT 1: Where attachments actually live (75 s)
**File:** `concept1_where_attachments_live.mp4`

**Title (pick one):**
1. ✅ `Your Attachment Query Returns 0 Rows. Here's Why (ServiceNow)`
2. `ServiceNow Table Inheritance: The Query That Silently Fails`
3. `sys_attachment and Extended Tables, Explained in 60 Seconds`

**Description:**
```
Querying sys_attachment by the parent table name returns nothing, because the record lives on the child table and that's what gets stored.
Fix: query by table_sys_id. A sys_id is a generated GUID, so the table name adds nothing.
One catch: files in image/attachment fields use a ZZ_YY prefix on table_name. Exclude those if you only want files users attached.
The bigger lesson: when you filter by table name on an extended table, ask which table the platform actually wrote.
Table names in the video are illustrative.

#servicenow #glidescript #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```
**Tags:**
```
servicenow, service now, sys_attachment, table inheritance, extended tables, gliderecord, servicenow developer, servicenow scripting, servicenow tutorial, servicenow tips
```
**Pinned comment (code):**
```
var ga = new GlideRecord('sys_attachment');
ga.addQuery('table_sys_id', caseSysId);
ga.addQuery('table_name', 'DOES NOT CONTAIN', 'ZZ_YY'); // optional: skip field files
ga.query();
```

---

## SHORT 3: Output became input (71 s)
**File:** `concept3_output_became_input.mp4`

**Title (pick one):**
1. ✅ `Works the First Time, Wrong the Second (ServiceNow Design Bug)`
2. `Your Output Became Your Input: A Bug That Hides From Your First Test`
3. `Don't Write Into the Set You Read From (ServiceNow)`

**Description:**
```
Generate a PDF listing a case's attachments, attach it to the same case, and the next run lists your own PDF too.
You wrote output into the set you read from, so output became input.
Don't filter by file name (a user's real file can vanish). Write the output somewhere your query never looks, and add a scheduled clean-up.
Same shape: generated files, logging into the table you log, a business rule updating the record it watches.

#servicenow #softwaredesign #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```
**Tags:**
```
servicenow, service now, pdf generation, sys_attachment, business rule, software design, servicenow developer, servicenow scripting, servicenow best practices, servicenow tips
```
**Pinned comment:** `Where else have you seen output come back as input? Recursive business rules count 👇`

---

## Check before publishing
- [ ] Short 1: run the `DOES NOT CONTAIN 'ZZ_YY'` line on your instance once (it's the only line not in your original brief)
- [ ] Short 2: "no mobile" for the File System Access API: confirm on caniuse.com (desktop support is confirmed: Chrome/Edge yes, Firefox/Safari no)
- [ ] Short 3: `convertToPDF` parameters vary slightly by release; the video labels it "one option, check the signature"
- [ ] Brand scan: only "ServiceNow Simplified" ✅
