# ServiceNow Simplified: HR Leave Request Series
## Episode 2: Manager Approval & The HR Handoff
### FINAL recording script: everything in one file (replaces Script v3 + the slide VO script)

**Deck:** `HRSD_Episode2_Hybrid_v3.pptx` (9 slides) · **Target length:** 16–18 min · **Two instances:** A = HRSD, B = Mock HRIS
**Voice:** senior colleague explaining over coffee.

**How to read this file**
- **Bold [brackets]** = what's on screen / what you do. *Italics* = notes to you, don't read them out.
- Lines in the **SLIDE VO** boxes: read one numbered line, **pause about 1 second**, then the next. Record each slide as its own
  file (`slide1` … `slide9`) in a separate audio pass. Everything else is recorded with the screen/face-cam as normal.

---

## PART 1: CHECK BEFORE YOU RECORD (10 min, saves a re-shoot)

### Instance B: Mock HRIS
- [ ] Log in now (developer instances are reclaimed after inactivity)
- [ ] Scoped app **HRIS Leave**, table label **HRIS Leave table**, with **Create module** + menu ticked
- [ ] The 7 fields: Employee ID (String, 100) · Leave Type (Choice: Annual, Sick, Casual, Work From Home, Other) · Start Date (Date) ·
      End Date (Date) · Days Taken (Integer) · Approval Reference (String) · Recorded At (Date/Time)
- [ ] *Optional, recommended:* a **Number** field (auto-number, e.g. prefix `HRL`) so Demo 2 has an HRIS reference to copy back.
      If you skip it, copy the record's display value or sys_id instead and change that line in Demo 2.
- [ ] One user **"HRIS Clerk"** with the app's user role, so the manual entry is shown as a normal HR user, not admin
- [ ] **Do not** create an integration user, REST API or credentials. That's Episode 3.

### Instance A: HRSD
- [ ] **Leave Management Team** group with at least one member who is not you
- [ ] Two test users: one **with** a manager (employee), one **without** a manager (for the guard demo), plus the manager user
- [ ] Episode 1 form works: submitting it creates an HR Case with HR Service = Leave Request
- [ ] Look at the HR Case form and write down the **exact labels**: State values (Work in Progress / Closed Complete / Closed Incomplete),
      the close code field (e.g. "Resolution code") and its choices, and "Close notes". If "Approved and Recorded" / "Rejected by Manager"
      aren't choices, add them or use what exists, and say what's on screen.
- [ ] After a test approval, check **System Logs → Emails** for an approval email. Pick the matching line in Demo 1.
- [ ] **Which scope does the flow go in?** Use the same scope where your Episode 1 HR work lives. Test once off camera:
      a flow that updates `sn_hr_core_case` from another scope can fail on cross-scope access. If it does, build the flow in the HR scope,
      or check the table's Application Access ("Can update").

### Both instances / recording setup
- [ ] Different banner colour + title on each instance (so A and B are obvious even without the overlay)
- [ ] Zoom 125% on the UI, 150% in Flow Designer
- [ ] Nothing on screen that shows an instance URL, a client name or real people. Use test users only.
- [ ] Assets ready: BUILD/DEMO bumpers, "Logged in as" lower-thirds, `overlays/overlay_instance_A_hrsd.png` and `overlay_instance_B_mock_hris.png`

---

## PART 2: THE SCRIPT

### [0:00] Cold open
**[Screen: fast montage. Submit on A → manager approves on A → HR clerk creates the row on B → case closes on A]**

Here's what we're building today. An employee submits a leave request. It goes to their manager. The manager approves, and the case lands on the HR team's desk. They record the leave in the HRIS — Workday, SAP, whatever your client runs — and close the case.

Five steps, two systems, one real flow, based on an actual client project. Let's build it.

**[Slide 1 clip]**

> **SLIDE VO · slide 1** (`slide1`)
> 1. Episode two. Manager approval, and the HR handoff.

---

### [0:30] Series intro
**[Screen: your intro card]**

Hey, I'm Krushikesh — everyone calls me KB — and welcome to ServiceNow Simplified.

Quick note before we start. This isn't a standalone video. It's part of a series building a full HR Leave Request application end to end, based on a real client project. Each episode tackles one piece. You can follow along on your own instance, and by the end you'll have the whole thing running.

If you're new here — I make tutorials for people doing actual client work, not just certification prep. The playlist link is in the description.

---

### [1:15] Where we are
**[Screen: face-cam, then into the slides]**

Quick recap. Episode 1 built the form your employees fill in — the HR Service, the Record Producer, and the client scripts. If you followed along, you've got a working form that creates an HR Case when someone submits it.

But right now, that case just sits there. Nobody approves it. Nobody processes it. It's a half-finished workflow.

That's what today fixes.

---

### [2:00] Slide walkthrough (slides 2–6)
*Play the slide clips here. The words below are what you record in the slide VO pass.*

> **SLIDE VO · slide 2: Where We Are** (`slide2`)
> 1. Five episodes in total. Episode one is done. It ended up split into one point one, and one point two, because it ran long.
> 2. Today is episode two. Manager approval, and the HR handoff.
> 3. After this, episode three builds the real HRIS integration. Episode four adds notifications and SLAs. And episode five polishes the portal.

> **SLIDE VO · slide 3: The Full Flow at a Glance** (`slide3`)
> 1. This is the end-to-end flow, in five steps.
> 2. The employee submits. The case routes to their manager. And the manager approves, or rejects.
> 3. The case gets assigned to the Leave Management team. Then the team updates the HRIS, and closes the case.
> 4. Step five is amber, because it's the manual step. In real life, the HR team types it into Workday or SAP by hand. In our demo, they type it into our mock HRIS. We keep it manual on purpose today, so you can see exactly where episode three's integration slots in.

> **SLIDE VO · slide 4: Two Systems, Two Jobs** (`slide4`)
> 1. One principle before we build. HRSD and your HRIS do different jobs.
> 2. HRSD owns the request, the approval decision, and the audit trail.
> 3. The HRIS — Workday, SAP, or whatever your client runs — owns the real leave balance, and payroll.
> 4. A lot of projects try to make HRSD the system of record for leave. Don't. Payroll, finance, and auditors will all fight you. HRSD requests. The HRIS records.
>
> *Say "H-R-S-D" slowly in line 4. It's the line the whole slide is about.*

> **SLIDE VO · slide 5: Our Demo Setup: Two Instances** (`slide5`)
> 1. I don't have a Workday tenant for a public channel, so here's the honest setup.
> 2. Instance A is our HRSD. The leave form, the approval, and the HR case.
> 3. Instance B is a second ServiceNow instance, playing the client's HRIS. It holds the HRIS Leave table.
> 4. Today, the HR team updates Instance B by hand. In episode three, we connect the two over REST, with Basic Auth, and then OAuth 2.0. It's the same pattern you'd use for Workday or SAP.

> **SLIDE VO · slide 6: Today's Build Order** (`slide6`)
> 1. Here's today's build order. Three builds, and two demos.
> 2. First, the HRIS Leave table on our mock HRIS instance. Then, the manager approval in Flow Designer.
> 3. Then we demo the manager side.
> 4. Next, we build the auto-assignment to the Leave Management team.
> 5. And finally, the HR team records the leave on the mock HRIS, and closes the case.

**[Face-cam]** Slides off. Let's build.

---

### [3:45] Build 1: The HRIS Leave table (Instance B)
**[BUILD 1 bumper → slide 7 clip → switch to Instance B + overlay "Instance B · Mock HRIS"]**

> **SLIDE VO · slide 7: The Mock HRIS Table** (`slide7`)
> 1. This table lives on Instance B, our mock HRIS. It stands in for Workday or SAP, and it's what episode three integrates with.
> 2. Employee ID, leave type, and the start and end dates.
> 3. Days taken, in calendar days for now. An approval reference, holding the HR case number, so we can trace back to HRSD. And recorded at.
> 4. Today, the HR team adds a row here by hand, on Instance B. In episode three, our HRSD instance creates it automatically, over REST.

**[Instance B: open the table definition]**

I'm on our second instance now — the mock HRIS. Look at the banner: this is Instance B, not our HRSD.

In a real project you'd never build this table. It already exists in Workday or SAP. But it gives us something real to integrate with, and in Episode 3 our HRSD instance talks to it exactly the way it would talk to a real HRIS: over an API, with credentials.

I've already created the scoped app, HRIS Leave, and the table, HRIS Leave table. Notice the table name got the scope prefix automatically. That `x_` prefix is standard for scoped tables.

Quick walk through the fields, because these are our integration contract for Episode 3:
- Employee ID — a string. In a real HRIS this is the employee number. We'll use the requester's email.
- Leave Type — a choice: Annual, Sick, Casual, Work From Home, Other.
- Start Date and End Date — dates.
- Days Taken — an integer. Calendar days for now.
- Approval Reference — the HR case number from Instance A, so the two systems can be traced to each other.
- Recorded At — when the HRIS recorded it.

That's Instance B done. Notice what we're **not** doing yet: no API, no integration user, no credentials. That's Episode 3. Today a human is the integration.

---

### [5:30] Build 2: Manager approval in Flow Designer (Instance A)
**[BUILD 2 bumper → switch to Instance A + overlay "Instance A · HRSD" → Flow Designer, 150% zoom]**

Back to Instance A — our HRSD.

We're doing the approval in Flow Designer, because that's where ServiceNow is heading. The classic workflow approval activities still work, but if you're starting new, Flow Designer is where you go.

New Flow. Name: Leave Request Approval Flow. Application: the same scope as our Episode 1 work. Run as: System User, for now. On a real project you'd think harder about this.

**[Trigger]**

Trigger. We want this flow to run when an HR Case is created with our leave service. So: trigger type Created, table HR Case — `sn_hr_core_case`. Condition: HR Service is Leave Request. Done.

One honest call-out: triggering only on Created is simple. In a real project you'd also think about what happens when someone edits the request. For today, Created is fine.

**[No-manager guard, before the approval]**

Before we ask for approval, one guard. Not every user has a manager on their record — contractors, new joiners, data that hasn't synced yet. If the manager is empty, the approval has nowhere to go, and the case just sits there.

So: Add Flow Logic → If. Condition: Trigger → HR Case Record → Requested for → Manager → is empty.

Inside the If: Update Record on the HR Case. Assignment group: Leave Management Team. Work notes: "No manager on the requester's profile — routed to HR for manual approval." Then End Flow.

Ten seconds of config, and it saves you the "why is my case stuck?" ticket later.

**[Ask for Approval, after the If]**

Now add an action. Search for approval. I'm using Ask For Approval.

Record: the HR Case from the trigger. Table: HR Case.

Approval rules — this is the key part. Approve when: Anyone approves. Approver: dynamic, the manager of the Requested for user. Click the data pill picker: Trigger → HR Case Record → Requested for → Manager. That's the chain. The platform grabs whoever is in the Manager field on the requester's user record.

And add the rejection rule too: Reject when Anyone rejects, same manager pill. Without a rejection rule, a reject doesn't end the approval cleanly, and the flow can sit there waiting.

Journal field: Work notes, so the decision shows up in the case history.

**[Save, activate]**

Save. Activate.

What this does right now: when a Leave Request case is created, the manager gets an approval. They can approve or reject. Nothing happens *after* that yet. That's the next build.

---

### [8:00] Demo 1: Manager approves (Instance A)
**[DEMO 1 bumper → lower-third "Logged in as: [employee] · Employee"]**

Let's test what we have. I'm the employee now — a user whose manager is set.

I submit the leave request form from Episode 1. Annual leave, a start date, an end date. Submit. HR Case created.

**[Lower-third "Logged in as: [manager] · Manager"]**

Now I'm the manager. My Approvals — and the approval is there.

*Pick the line that matches your prep check:*
- *If an email appeared in System Logs → Emails:* "There's even an approval email in the log. That's an out-of-the-box notification. We'll design proper notifications in Episode 4."
- *If nothing appeared:* "No email yet. Notifications are Episode 4."

Approve. Done.

**[Back on the HR Case]**

Open the HR Case. Approval: approved. Great. But notice — the case state hasn't changed, and the assignment group is empty. Nothing routes it to anyone for the next step.

That's what the next build fixes.

---

### [10:00] Build 3: Auto-assign on approval (Instance A)
**[BUILD 3 bumper → Flow Designer]**

Back to the flow. After Ask For Approval, I add Flow Logic → If: Approval State is Approved.

Inside the If: Update Record on the HR Case.
- Assignment group: Leave Management Team
- State: Work in Progress

That's the approved branch.

**[Else branch]**

Else — the manager rejected. Update Record again:
- State: Closed Incomplete
- Close code: Rejected by Manager *(use the exact field and choice you checked in prep)*
- Close notes: "Rejected by manager."

Save. Activate.

*Note: the case from Demo 1 ran on the old version of the flow. Use a fresh request in Demo 2.*

Quick design note: in a real project you'd notify the employee on rejection, with the reason. That's Episode 4. For now, the state change is enough.

---

### [11:30] Demo 2: HR team records the leave in the Mock HRIS
**[DEMO 2 bumper → Instance A overlay → lower-third Employee]**

Fresh test. New leave request. Submit.

**[Lower-third Manager]** Approve.

**[Lower-third "Logged in as: Leave Management Team member · HR Team"]**

Here's the case — assigned to the Leave Management Team, Work in Progress. The team picks it up.

**[Switch to Instance B → overlay "Instance B · Mock HRIS" + lower-third "Logged in as: HRIS Clerk · HR Team"]**

Now the manual bit — and this is exactly what happens in real companies before integration. The team member logs in to the HRIS — here, our second instance — and records the leave.

New HRIS Leave record. Employee ID: the requester's email. Leave type: Annual. Start and end date: copied from the case. Days taken: 3. Approval reference: I paste the HR case number. Recorded at: now. Save.

And notice — Instance B gave this record its own number. I copy it.
*(If you didn't add a Number field: "I copy the record reference.")*

**[Switch back to Instance A → overlay "Instance A · HRSD"]**

Back in HRSD, I close the case. State: Closed Complete. Close code: Approved and Recorded. Close notes: "Leave recorded in HRIS, reference" — and I paste the HRIS number. Save.

That's the full loop. Two systems, each pointing at the other: HRSD has the HRIS reference, and the HRIS has the HR case number.

**[20-second reject check, Instance A]**
One more, fast. New request, and this time the manager clicks Reject. Open the case: Closed Incomplete, "Rejected by manager" in the close notes. Both branches work.

**[20-second no-manager check, Instance A]**
And the guard. I submit as the user with no manager. The case goes straight to the Leave Management Team, with our work note explaining why. Nothing stuck.

---

### [13:30] The honest bridge to Episode 3
**[Face-cam]**

Pause here, because this is the important bit.

What just happened: someone copied data from one system into another, by hand, and copied a reference back. With hundreds of leave requests a week, that's a full-time job — with typos.

Episode 3 removes that. On Instance B we'll expose an API and create an integration user. On Instance A we'll set up a Connection and Credential alias — first with Basic Auth, then we'll upgrade it to OAuth 2.0, which is what you'd use in production. Then Flow Designer calls the API on approval, handles failures, and writes the HRIS reference back to the case.

And that pattern isn't specific to Workday or SAP. It's the same for any external system of record — payroll, benefits, whatever.

---

### [14:30] Outro
**[Slide 8 clip → face-cam → slide 9 clip as end screen]**

> **SLIDE VO · slide 8: What We're NOT Doing Today** (`slide8`)
> 1. Some things we're deliberately not covering today. Each one has its own episode.
> 2. Multi-level approvals, and notifications and SLAs, come in episode four.
> 3. The real integration between our two instances is episode three. And Employee Center polish is episode five.

**[Face-cam]**

That's Episode 2. Manager approval, the no-manager guard, auto-assignment, and the HR handoff across two systems.

If this helped, subscribe. And tell me in the comments: **in your projects, where does leave really live — Workday, SAP SuccessFactors, something custom, or HRSD itself?** I'll read the interesting answers at the start of Episode 3.

See you next time.

> **SLIDE VO · slide 9: Next Episode** (`slide9`)
> 1. Next episode: we automate the manual step you just watched. Our HRSD instance calls the mock HRIS over REST, first with Basic Auth, then with OAuth 2.0.
> 2. Subscribe, so you don't miss it.

---

## PART 3: PRODUCTION NOTES
- **Every instance switch:** instance overlay top-right. **Every user switch:** "Logged in as" lower-third. Cut the impersonation clicks.
- **BUILD / DEMO bumpers** at the start of each section: clean chapter points.
- Builds can move fast (viewers pause); demos carry the story. Speed-ramp every save spinner.
- Raw recording target 25–30 min. Past 35, cut while recording, not in the edit.
- **Before upload:** scrub the timeline for instance URLs, client names and real people's names. Only "ServiceNow Simplified" on screen.
- **Send me:** the 9 slide VO files (`slide1` … `slide9`). I'll rebuild the slide clips with highlights in your voice.

## CHAPTERS (adjust times after editing)
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
