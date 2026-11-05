# HRSD Ep2: slide voice-over recording script

**How to record:** one audio file per slide, named `slide1.wav` (or .m4a/.mp3) … `slide8`. Read each numbered line, then **pause ~1 second** before the next.
The pause is how I find where each highlight starts. Change the wording freely, but keep **one line = one pause**, and keep the same number of lines per slide.
Room: quiet, phone or mic ~15 cm from your mouth, no music. Leave 1 second of silence at the start and end.


## Slide 1  →  `slide1.wav`

1. Episode two. Manager approval, and the HR handoff.  
   _highlight: (no highlight)_

## Slide 2  →  `slide2.wav`

1. Five episodes in total. Episode one is done. It ended up split into part one point one, and one point two, because it ran long.  
   _highlight: rows 1.1 + 1.2_
2. Today is episode two. Manager approval, and the HR handoff.  
   _highlight: row 2 (TODAY)_
3. After this, episode three builds the real HRIS integration. Episode four adds notifications and SLAs. And episode five polishes the portal.  
   _highlight: rows 3–5_

## Slide 3  →  `slide3.wav`

1. This is the end-to-end flow, in five steps.  
   _highlight: all five steps_
2. The employee submits. The case routes to their manager. And the manager approves, or rejects.  
   _highlight: steps 1–3_
3. The case gets assigned to the Leave Management team. Then the team updates the external HRIS, and closes the case.  
   _highlight: steps 4–5_
4. Step five is marked amber, because it's the manual step. The HR team types it into Workday or SAP by hand. We leave it manual on purpose today, so you can see exactly where episode three's integration slots in.  
   _highlight: step 5 + amber note_

## Slide 4  →  `slide4.wav`

1. One principle before we build. HRSD and your HRIS do different jobs.  
   _highlight: top sentence_
2. HRSD owns the request, the approval decision, and the audit trail.  
   _highlight: HRSD box_
3. The HRIS, Workday, SAP, or whatever your client runs, owns the real leave balance, and payroll.  
   _highlight: HRIS box_
4. A lot of projects try to make HRSD the system of record for leave. Don't. Payroll, finance, and auditors will all fight you. HRSD requests. The HRIS records.  
   _highlight: both boxes_

## Slide 5  →  `slide5.wav`

1. Here's today's build order. Three builds, and two demos.  
   _highlight: subtitle_
2. First, we build the mock HRIS table. Then, the manager approval in Flow Designer.  
   _highlight: rows 1–2_
3. Then we demo the manager side.  
   _highlight: row 3_
4. Next, we build the auto-assignment to the Leave Management team.  
   _highlight: row 4_
5. And finally, we demo the team updating the mock HRIS, and closing the case.  
   _highlight: row 5_

## Slide 6  →  `slide6.wav`

1. This mock table stands in for Workday or SAP. Episode three's integration writes to this exact table, so what we build now gets reused.  
   _highlight: table name header_
2. Employee ID, leave type, and the start and end dates.  
   _highlight: employee_id → end_date_
3. Days taken, in calendar days for now. An approval reference, holding the HR case number, so we can trace back to HRSD. And recorded at.  
   _highlight: days_taken → recorded_at_
4. Today, the HR team adds a row here by hand. In episode three, Flow Designer does it automatically on approval.  
   _highlight: green note at bottom_

## Slide 7  →  `slide7.wav`

1. Some things we're deliberately not covering today. Each one has its own episode.  
   _highlight: (no highlight)_
2. Multi-level approvals, and notifications and SLAs, come in episode four.  
   _highlight: A + N rows_
3. The real HRIS integration is episode three. And Employee Center polish is episode five.  
   _highlight: I + P rows_

## Slide 8  →  `slide8.wav`

1. Next episode: external HRIS integration. We automate the manual step you just watched the team do.  
   _highlight: (no highlight)_
2. Subscribe, so you don't miss it.  
   _highlight: (no highlight)_
