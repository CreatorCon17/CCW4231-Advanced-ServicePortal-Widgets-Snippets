# ServiceNow Simplified — HR Leave Request Series
## Episode 2: Manager Approval & The HR Handoff
### Script v3 — two-instance setup (HRSD instance + Mock HRIS instance)

**Target length:** 16–18 minutes
**Format:** Build + demo, across **two ServiceNow instances**
**Voice:** Same as Episode 1 — senior colleague explaining over coffee

> **What's new in v3** (🆕) on top of v2: the HRIS table now lives on a **second ServiceNow instance** that plays the
> client's HRIS (Workday / SAP stand-in). Episode 2 stays manual (HR team logs in to the Mock HRIS and creates the row);
> Episode 3 integrates the two instances over REST with Basic Auth and OAuth 2.0.
> Slide numbers match `HRSD_Episode2_Hybrid_v3.pptx` (9 slides: new slide 5 "Our Demo Setup").

---

## THE TWO INSTANCES (keep this straight on camera)

| | **Instance A — HRSD** | **Instance B — Mock HRIS** |
|---|---|---|
| Plays | Your ServiceNow HRSD | The client's HRIS (stand-in for Workday / SAP) |
| Owns | Leave form, HR Case, approval, audit trail | The leave record (system of record) |
| Built in Ep 2 | Approval flow, no-manager guard, auto-assign | Scoped app **HRIS Leave** + **HRIS Leave table** (built in prep) |
| Ep 2 demo | Employee → Manager → HR team | HR team member creates the leave row **by hand** |
| Ep 3 | Calls Instance B's REST API (Connection & Credential alias) | Scripted REST API + integration user (Basic Auth, then OAuth 2.0) |

**On-screen labels:** every time you switch instance, show the instance overlay
(`overlay_instance_A_hrsd.png` / `overlay_instance_B_mock_hris.png`) **plus** the "Logged in as" lower-third.
Also give the two browser tabs different banner colours / titles (System Properties → Basic Configuration UI16 on each
instance), so viewers can tell them apart even without the overlay.

---

## ⚠️ DECIDE / CHECK BEFORE YOU RECORD

1. ✅ **Instance B exists.** Keep it active: developer instances are reclaimed after inactivity, so log in between episodes.
2. ✅ **App + table on Instance B:** scoped app **HRIS Leave**, table label **HRIS Leave table**
   (technical name will look like `x_<yourprefix>_hris_leave_…`). Not on Instance A any more.
3. ✅ **Authentication:** none set up yet, which is correct. **Basic Auth and OAuth 2.0 are both built on camera in Episode 3.**
   Don't create the integration user or API yet. Ep 2 is manual on purpose.
4. **Check on Instance A:** the exact close fields on the HR Case form ("Resolution code" / "Close notes" labels), and whether an
   approval email appears in **System Logs → Emails** after an approval. Use the matching Demo 1 line.
5. **Naming on screen:** call Instance B **"Mock HRIS"** or "our second instance". Say once that it stands in for Workday or SAP.
   Never show a client or employer name.

**Prep before you hit record**
- **Instance B:** create app **HRIS Leave** and the **HRIS Leave table** with the 7 fields (slide 7). Create module + menu.
  Create one HR team login on B (e.g. "HRIS Clerk") with the app's user role, so you can show the manual entry as a normal user.
- **Instance A:** Leave Management Team group with at least one member (not you); two test users (one **with** a manager, one **without**);
  one fresh Leave Request from Episode 1.
- Zoom 125% on the UI, 150% on Flow Designer.

---

## THE SCRIPT

### [0:00 — Cold open]
**[Screen: montage — submit on A → manager approves on A → HR team switches to B and creates the leave row → case closes on A]**

Here's what we're building today. An employee submits a leave request. It goes to their manager. The manager approves, and the case lands on the HR team's desk. They record the leave in the HRIS — Workday, SAP, whatever your client runs — and close the case.

Five steps, two systems, one real flow, based on an actual client project. Let's build it.

**[slide 1 / title clip]**

### [0:30 — Series intro] *(unchanged)*
Hey, I'm Krushikesh — everyone calls me KB — and welcome to ServiceNow Simplified. … *(same as v2)*

### [1:15 — Where we are] *(unchanged)*

### [2:00 — PPT walkthrough, slides 2–6]
> Read each numbered line, pause ~1 s between lines (for the highlight timing).

**Slide 2 — Where We Are** *(unchanged lines 1–3)*

**Slide 3 — The Full Flow at a Glance** *(unchanged lines 1–4)*

**Slide 4 — Two Systems, Two Jobs**
1. One principle before we build. HRSD and your HRIS do different jobs.
2. HRSD owns the request, the approval decision, and the audit trail.
3. The HRIS — Workday, SAP, or whatever your client runs — owns the real leave balance, and payroll.
4. A lot of projects try to make HRSD the system of record for leave. Don't. Payroll, finance, and auditors will all fight you. HRSD requests. The HRIS records.

🆕 **Slide 5 — Our Demo Setup: Two Instances**
1. I don't have a Workday tenant for a public channel, so here's the honest setup.
2. Instance A is our HRSD — the leave form, the approval, the HR case.
3. Instance B is a second ServiceNow instance playing the client's HRIS. It holds the HRIS Leave table.
4. Today the HR team updates Instance B by hand. In episode three, we connect the two over REST — with Basic Auth, and then OAuth 2.0. The pattern is the same one you'd use for Workday or SAP.

**Slide 6 — Today's Build Order**
1. Here's today's build order. Three builds, and two demos.
2. 🆕 First, the HRIS Leave table on our mock HRIS instance. Then, the manager approval in Flow Designer.
3. Then we demo the manager side.
4. Next, we build the auto-assignment to the Leave Management team.
5. 🆕 And finally, the HR team records the leave on the mock HRIS, and closes the case.

PPT off. Let's build.

---

### [3:45 — Build 1: The HRIS Leave table on Instance B]
**[BUILD 1 bumper → slide 7 clip → overlay "Instance B · Mock HRIS"]**

🆕 First, I'm switching to our second instance — the mock HRIS. Look at the banner: this is Instance B, not our HRSD.

This table plays the client's HRIS. In a real project you'd never build this table — it already exists in Workday or SAP. But it gives us something real to integrate with, and in Episode 3 our HRSD instance talks to it exactly the way it would talk to a real HRIS: over an API, with credentials.

I've already created the scoped app — **HRIS Leave** — and the table, **HRIS Leave table**. Quick walk through the fields, because these are our integration contract for Episode 3:

- Employee ID — string. In a real HRIS this is the employee number; we'll use the requester's email.
- Leave Type — choice: Annual, Sick, Casual, Work From Home, Other.
- Start Date, End Date — dates.
- Days Taken — integer, calendar days for now.
- Approval Reference — the HR case number from Instance A, so the two systems can be traced to each other.
- Recorded At — when the HRIS recorded it.

That's Instance B done. 🆕 Notice what we're **not** doing yet: no API, no integration user, no credentials. That's Episode 3. Today a human is the integration.

### [5:30 — Build 2: Manager approval via Flow Designer — Instance A]
**[BUILD 2 bumper → overlay "Instance A · HRSD" → Flow Designer (150%)]**

🆕 Back to Instance A — our HRSD.

*(Rest of Build 2 unchanged from v2: New Flow → trigger Created on `sn_hr_core_case`, HR Service is Leave Request → **no-manager guard** (If Requested For.Manager is empty → assign to Leave Management Team + work note → End Flow) → Ask For Approval with approver = Requested For → Manager, Anyone, Work notes → save, activate.)*

✏️ One change from v2: the flow lives on **Instance A**, with the rest of your Episode 1 work. There's no cross-scope issue any more, because the HRIS table isn't on this instance at all.

### [8:00 — Demo 1: Manager approves — Instance A] *(unchanged from v2; overlay Instance A + lower-thirds Employee → Manager)*

### [10:00 — Build 3: Auto-assign on approval — Instance A] *(unchanged from v2)*

### [11:30 — Demo 2: HR team records the leave in the Mock HRIS]
**[DEMO 2 bumper → Instance A: Employee submits → Manager approves → HR team member opens the case]**

Here's the case — assigned to the Leave Management Team, Work In Progress. The team picks it up.

🆕 **[Switch to Instance B → overlay "Instance B · Mock HRIS" + lower-third "Logged in as: HRIS Clerk · HR Team"]**

Now the manual bit — and this is exactly what happens in real companies before integration. The team member logs in to the HRIS — here, our second instance — and records the leave.

New HRIS Leave record. Employee ID — the requester's email. Leave type — Annual. Start and end date — copied from the case. Days taken — 3. Approval reference — I'll paste the HR case number. Save.

🆕 And notice — Instance B gave this record its own number. Copy it.

🆕 **[Switch back to Instance A → overlay "Instance A · HRSD"]**

Back in HRSD, close the case. State — Closed Complete. Close code — Approved and Recorded. Close notes — "Leave recorded in HRIS, reference" — paste the HRIS number. Save.

That's the full loop: two systems, each pointing at the other. HRSD has the HRIS reference, the HRIS has the HR case number.

**[20-second reject check]** *(unchanged)* · **[20-second no-manager check]** *(unchanged)*

### [13:30 — The honest bridge to Episode 3]
Pause here, because this is the important bit.

What just happened: someone copied data from one system into another, by hand, and copied a reference back. Hundreds of leave requests a week, and that's a full-time job — with typos.

🆕 Episode 3 removes that. On Instance B we'll expose an API and create an integration user. On Instance A we'll set up a **Connection & Credential alias** — first with **Basic Auth**, then we'll upgrade it to **OAuth 2.0**, which is what you'd use in production. Then Flow Designer calls the API on approval, handles failures, and writes the HRIS reference back to the case. Same pattern as Workday, SAP, or any other system of record.

### [14:30 — Outro]
**[slide 8 clip ("What we're NOT doing today") → face-cam → slide 9 end card]**

That's Episode 2. Manager approval, the no-manager guard, auto-assignment, and the HR handoff across two systems.

Honest flags: multi-level approvals and notifications are Episode 4. The real integration — Basic Auth and OAuth 2.0 between our two instances — is Episode 3.

If this helped, subscribe. And tell me in the comments: **in your projects, where does leave really live — Workday, SAP SuccessFactors, something custom, or HRSD itself?**

See you next time.

---

## PRODUCTION NOTES
- 🆕 **Two instances = two overlays.** Instance overlay top-right whenever the instance changes; "Logged in as" lower-third whenever the user changes.
- 🆕 Give the instances visibly different banners (colour + title) so screenshots and thumbnails make sense on their own.
- Build sections fast, demo sections carry the story. Cut every impersonation click and save spinner.
- 🆕 **Slide voice-over:** slides 2–6 now include the new slide 5 (4 lines). Record the same way (1 s pauses) and send it to me.

## CHAPTERS (update after editing)
```
0:00 What we're building
0:30 Series intro
1:15 Where we are
2:00 The flow, two instances & build order
3:45 Build 1: HRIS Leave table (Mock HRIS instance)
5:30 Build 2: Manager approval + no-manager guard
8:00 Demo 1: Manager approves
10:00 Build 3: Auto-assign on approval
11:30 Demo 2: HR team records leave in the Mock HRIS
13:30 Episode 3: connecting the two instances
14:30 Wrap-up
```
