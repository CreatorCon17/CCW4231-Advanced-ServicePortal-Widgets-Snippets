# HRSD Ep2: slide voice-over recording script (v3, 9 slides)

Matches `HRSD_Episode2_Hybrid_v3.pptx`. 🆕 = new or changed since the v2 recording script.

**How to record:** one audio file per slide, named `slide1` … `slide9` (.wav, .m4a or .mp3). Read each numbered line, then
**pause about 1 second** before the next one. The pause is how the highlight timing is found. You can change the wording,
but keep **one line = one pause** and the same number of lines per slide.
Room: quiet, phone or mic about 15 cm from your mouth, no music. Leave 1 second of silence at the start and the end.

---

## Slide 1: Title  →  `slide1`
1. Episode two. Manager approval, and the HR handoff.
   _highlight: none_

## Slide 2: Where We Are  →  `slide2`
1. Five episodes in total. Episode one is done. It ended up split into one point one, and one point two, because it ran long.
   _highlight: rows 1.1 + 1.2_
2. Today is episode two. Manager approval, and the HR handoff.
   _highlight: row 2 (TODAY)_
3. After this, episode three builds the real HRIS integration. Episode four adds notifications and SLAs. And episode five polishes the portal.
   _highlight: rows 3–5_

## Slide 3: The Full Flow at a Glance  →  `slide3`
1. This is the end-to-end flow, in five steps.
   _highlight: all five steps_
2. The employee submits. The case routes to their manager. And the manager approves, or rejects.
   _highlight: steps 1–3_
3. The case gets assigned to the Leave Management team. Then the team updates the HRIS, and closes the case.
   _highlight: steps 4–5_
4. 🆕 Step five is amber, because it's the manual step. In real life, the HR team types it into Workday or SAP by hand. In our demo, they type it into our mock HRIS. We keep it manual on purpose today, so you can see exactly where episode three's integration slots in.
   _highlight: step 5 + amber note_

## Slide 4: Two Systems, Two Jobs  →  `slide4`
1. One principle before we build. HRSD and your HRIS do different jobs.
   _highlight: top sentence_
2. HRSD owns the request, the approval decision, and the audit trail.
   _highlight: HRSD box_
3. The HRIS — Workday, SAP, or whatever your client runs — owns the real leave balance, and payroll.
   _highlight: HRIS box_
4. A lot of projects try to make HRSD the system of record for leave. Don't. Payroll, finance, and auditors will all fight you. HRSD requests. The HRIS records.
   _highlight: both boxes_

## 🆕 Slide 5: Our Demo Setup: Two Instances  →  `slide5`
1. I don't have a Workday tenant for a public channel, so here's the honest setup.
   _highlight: subtitle_
2. Instance A is our HRSD. The leave form, the approval, and the HR case.
   _highlight: Instance A box_
3. Instance B is a second ServiceNow instance, playing the client's HRIS. It holds the HRIS Leave table.
   _highlight: Instance B box_
4. Today, the HR team updates Instance B by hand. In episode three, we connect the two over REST, with Basic Auth, and then OAuth 2.0. It's the same pattern you'd use for Workday or SAP.
   _highlight: Ep 2 / Ep 3 lines_

## Slide 6: Today's Build Order  →  `slide6`
1. Here's today's build order. Three builds, and two demos.
   _highlight: subtitle_
2. 🆕 First, the HRIS Leave table on our mock HRIS instance. Then, the manager approval in Flow Designer.
   _highlight: rows 1–2_
3. Then we demo the manager side.
   _highlight: row 3_
4. Next, we build the auto-assignment to the Leave Management team.
   _highlight: row 4_
5. 🆕 And finally, the HR team records the leave on the mock HRIS, and closes the case.
   _highlight: row 5_

## Slide 7: The Mock HRIS Table  →  `slide7`
1. 🆕 This table lives on Instance B, our mock HRIS. It stands in for Workday or SAP, and it's what episode three integrates with.
   _highlight: table name header_
2. Employee ID, leave type, and the start and end dates.
   _highlight: employee_id → end_date_
3. Days taken, in calendar days for now. An approval reference, holding the HR case number, so we can trace back to HRSD. And recorded at.
   _highlight: days_taken → recorded_at_
4. 🆕 Today, the HR team adds a row here by hand, on Instance B. In episode three, our HRSD instance creates it automatically, over REST.
   _highlight: green note at bottom_

## Slide 8: What We're NOT Doing Today  →  `slide8`
1. Some things we're deliberately not covering today. Each one has its own episode.
   _highlight: none_
2. Multi-level approvals, and notifications and SLAs, come in episode four.
   _highlight: A + N rows_
3. 🆕 The real integration between our two instances is episode three. And Employee Center polish is episode five.
   _highlight: I + P rows_

## Slide 9: Next Episode  →  `slide9`
1. 🆕 Next episode: we automate the manual step you just watched. Our HRSD instance calls the mock HRIS over REST, first with Basic Auth, then with OAuth 2.0.
   _highlight: none_
2. Subscribe, so you don't miss it.
   _highlight: none_
