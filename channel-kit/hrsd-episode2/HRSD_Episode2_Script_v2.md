# ServiceNow Simplified — HR Leave Request Series
## Episode 2: Manager Approval & The HR Handoff
### Script v2 — Conversational (professional-friendly)

**Target length:** 15–17 minutes (v2 adds ~60 s: the no-manager guard + a 20-second reject demo)
**Format:** Mix of build (approval + assignment config + mock table) and demo (manager approval flow + HR team closing)
**Voice:** Same as Episode 1 v2 — senior colleague explaining over coffee

> **What changed from v1** is marked with 🆕 (new) or ✏️ (reworded). Everything else is your original.
> Slide lines match `HRSD_Episode2_Hybrid_v2.pptx` and the slide clips, so the highlights still line up if you reuse them.

---

## ⚠️ DECIDE BEFORE YOU RECORD (2 minutes, saves a re-shoot)

1. ✅ **Scope name — decided: "HRIS Leave".** Slide 6 now says **HRIS Leave table** (no client name anywhere in the deck).
   Create the app as **HRIS Leave** and the table with label **HRIS Leave table**. ServiceNow adds your vendor prefix
   automatically, so the technical name on screen will look like `x_<yourprefix>_hris_leave_…`. That's fine, because
   the slide shows the label, not the technical name.
2. 🆕 **One scope for everything.** Create the **table AND the flow in the same scoped app**. v1 had the flow in
   "Advanced Solutions", and Episode 3 writes to this table from the flow, so a cross-scope mismatch will bite you there.
3. 🆕 **Check two things on your PDI** so what you say matches the screen:
   - The exact close fields on the HR Case form (v1 says "Resolution Code" / "Close notes"; confirm the labels on `sn_hr_core_case`).
   - Whether an approval email appears in **System Logs → Emails** after an approval (OOB approval notifications can generate one
     even with nothing configured). Use the matching line in Demo 1 below.

**Prep before you hit record:**
- Build the mock HRIS table in your scope before recording — don't do it on camera, that's a tangent
- Create the Leave Management Team assignment group with at least one member (not you)
- Have **two** test users: one **with** a Manager set, 🆕 and one **without** a manager (for the guard demo)
- Submit one Leave Request from Episode 1's form so you have a fresh HR Case to work with
- Browser zoom 125% on the ServiceNow UI, 150% on anything with small text (Flow Designer especially)

---

## THE SCRIPT

### [0:00 — Cold open, show the whole flow before explaining it]

**[Screen: fast-cut montage — employee submits, manager approves, HR team updates mock HRIS, case closes]**

Here's what we're building today. Employee submits a leave request. It goes to their manager for approval. Manager approves, case lands on the HR team's desk. They update the external HRIS — Workday, SAP, whatever your client runs — and close the case out.

✏️ Five steps, one real flow, based on an actual client project. Let's build it.

**[Screen: slide 1 / title clip]**

---

### [0:30 — Reusable series intro, same one from Episode 1]

**[Screen: your intro card]**

Hey, I'm Krushikesh — everyone calls me KB — and welcome to ServiceNow Simplified.

Quick note before we start. This isn't a standalone video, it's part of a series building a full HR Leave Request application end to end, based on a real client project I've been working on. Each episode tackles one piece. You can follow along on your own instance, and by the end you'll have the whole thing running.

If you're new here — I make tutorials for people doing actual client work, not just certification prep. Playlist link's in the description.

---

### [1:15 — Where we are and why this episode exists]

**[Screen: face-cam, transitioning to PPT]**

Quick recap. Episode 1 built the form your employees fill in — the HR Service, the Record Producer, all the client scripts. If you followed along, you've got a working form that creates an HR Case when someone submits it.

But right now, that case just sits there. Nobody approves it. Nobody processes it. It's a half-finished workflow.

That's what today fixes.

---

### [2:00 — PPT walkthrough, 4 slides]

> Read each numbered line, pause ~1 s between lines (same as last time, so the highlights can follow you).

**Slide 2 — Where We Are**
1. Five episodes in total. Episode one is done — it ended up split into part 1.1 and 1.2, because it ran long.
2. Today is episode two — manager approval, and the HR handoff.
3. After this, episode three builds the real HRIS integration, episode four adds notifications and SLAs, and episode five polishes the portal.

**Slide 3 — The Full Flow at a Glance**
1. This is the end-to-end flow, in five steps.
2. The employee submits. The case routes to their manager. And the manager approves, or rejects.
3. The case gets assigned to the Leave Management team. Then the team updates the external HRIS, and closes the case.
4. Step five is marked amber, because it's the manual step — the HR team types it into Workday or SAP by hand. We leave it manual on purpose today, so you can see exactly where episode three's integration slots in.

**Slide 4 — Two Systems, Two Jobs**
1. One principle before we build. HRSD and your HRIS do different jobs.
2. HRSD owns the request, the approval decision, and the audit trail.
3. The HRIS — Workday, SAP, or whatever your client runs — owns the real leave balance, and payroll.
4. ✏️ A lot of projects try to make HRSD the system of record for leave. Don't. Payroll, finance, and **auditors** will all fight you. **HRSD** requests. The **HRIS** records.
   *(Say "H-R-S-D" slowly here, because it's the line the whole slide is about.)*

**Slide 5 — Today's Build Order**
1. Here's today's build order. Three builds, and two demos.
2. First, we build the mock HRIS table. Then, the manager approval in Flow Designer.
3. Then we demo the manager side.
4. Next, we build the auto-assignment to the Leave Management team.
5. And finally, we demo the team updating the mock HRIS, and closing the case.

PPT off. Let's build.

---

### [3:30 — Build 1: The mock HRIS table]

**[Screen: BUILD 1 bumper → slide 6 clip → PDI, System Applications → Studio or Tables]**

First thing we do is build the mock HRIS table. This table stands in for Workday or SAP for the demo. In Episode 3, our integration writes to this exact table — so what we build now gets reused.

✏️ I'm creating it in my application scope — **HRIS Leave**. Table label — **HRIS Leave table**. Notice the table name gets the scope prefix automatically — that `x_` prefix is standard for scoped tables. 🆕 And I'm going to build the flow in this **same** scope later, so the flow can write to this table without cross-scope headaches in Episode 3.

**[Open the table creation form]**

✏️ Label — HRIS Leave table. The name fills in automatically from the label. Create module and menu — yes, so I can see the records easily during the demo.

Fields I need — and I'm matching what Episode 3's integration will send:

- Employee ID — string, 100 characters. In the real integration this is probably an email or an employee number.
- Leave Type — Choice. Values: Annual, Sick, Casual, Work From Home, Other.
- Start Date — date.
- End Date — date.
- Days Taken — integer. Calendar days today — Episode 3 refines this to working days.
- Approval Reference — string. This holds the HRC number so we can trace from the HRIS back to HRSD.
- Recorded At — date/time. When the row was created in the mock.

Save.

This isn't a real HRIS. It's a stand-in so we can see the flow working end to end, and so Episode 3's integration has something concrete to write to. In a real project the external HRIS has its own schema, API, and rules — the point isn't to model Workday perfectly. Keep it simple.

---

### [5:30 — Build 2: Manager approval via Flow Designer]

**[Screen: BUILD 2 bumper → Filter navigator → Flow Designer → New Flow (150% zoom)]**

Now the approval. We're doing this in Flow Designer because that's where ServiceNow is heading. Classic approval activities still work, but if you're starting new, Flow Designer is where you go.

✏️ New Flow. Name — Leave Request Approval Flow. Application — **HRIS Leave**, the same scope as our table. Run as — System User, for now. On a real project you'd think harder about this.

**[Trigger setup]**

Trigger. We want this flow to run when an HR Case gets created with our leave service. So — trigger type is Created, table is `sn_hr_core_case`. Add a condition: HR Service is Leave Request. Save.

Important call-out — only triggering on Created is naive. In a real project you'd also handle the Updated case, in case someone edits the request. For today, Created is fine.

🆕 **[Add the no-manager guard — before the approval]**

Before we ask for approval, one guard. Not every user has a manager on their record — contractors, new joiners, data that hasn't synced yet. If the manager is empty, the approval has nowhere to go and the case just sits there.

So — Add Flow Logic → **If**. Condition: Trigger → HR Case Record → Requested For → Manager → **is empty**.

Inside the If: **Update Record** on the HR Case — Assignment Group: Leave Management Team, Work notes: "No manager on the requester's profile — routed to HR for manual approval." Then **End Flow**.

Ten seconds of config, and it saves you the "why is my case stuck?" ticket later.

**[Add Approval action — after the If]**

Add an action. Search for Approval — I'm using "Ask For Approval."

Table — HR Case, current record.
Approvers — this is the key field. Dynamic lookup. I want the approver to be the manager of the Requested For user.

Click the data pill picker. Trigger → HR Case Record → Requested For → Manager. That's the chain. Platform grabs whoever's in the Manager field on the requester's user record.

Approval type — Anyone. Only one approver anyway. Journal field — Work notes, so the approval decision shows up in the case history.

**[Save and activate]**

Save the action. Save the flow. Activate it.

What this does right now — when a Leave Request case is created, the manager gets an approval. They can approve or reject. Nothing happens *after* that yet. We add the "what happens next" in the next build step.

---

### [8:00 — Demo 1: Manager receives, approves, case transitions]

**[Screen: DEMO 1 bumper → lower-third "Logged in as: Dougie Macarthur · Employee"]**

Let's test what we have. I'm the employee now — Dougie Macarthur, whose manager is set.

Submit the leave request form from Episode 1. Annual Leave, pick a start date, end date. Submit. HR Case created — HRC00050-something.

**[Lower-third "Logged in as: Narvdasaver Dubey · Manager"]**

Now I'm the manager. My Approvals — the approval record is there.

✏️ *Pick the line that matches what you saw in prep step 3:*
- *If an email appeared in the log:* "There's even an approval email in the outbox — that's an out-of-the-box notification. We'll design proper notifications in Episode 4."
- *If nothing appeared:* "No email yet — notifications are Episode 4."

Click Approve. Done.

**[Back on the HR Case]**

Open the HR Case. Approval section — approved. Great. But notice — the case state hasn't changed. It's still sitting in whatever state the Record Producer created it in. Assignment group is empty. There's nothing routing this to anyone to actually do the next step.

That's what the next build fixes.

Quick honest callout — if you approved and your flow didn't update the case, check your flow context. The approval action completed, but no step after it did anything. That's expected right now.

---

### [10:00 — Build 3: Auto-assign to Leave Management on approval]

**[Screen: BUILD 3 bumper → Flow Designer]**

Back to the flow. After the Approval action, I'm adding a Conditional step — If Approval State is Approved.

Inside the If: Update Record action. Record is current HR Case. Fields to update:
- Assignment Group — Leave Management Team
- State — Work In Progress

That's it for the approved branch.

**[Else branch]**

Else — approval rejected. Update Record again, this time:
- State — Closed Incomplete
- ✏️ Close code / resolution field — "Rejected by Manager" *(use the exact field label you checked in prep; add the choice if your instance doesn't have it)*
- Close notes — "Rejected by manager."

Save, activate.

Quick design note — in a real project you'd send the employee a notification on rejection with the reason. That's Episode 4. For now the state change is enough.

---

### [11:30 — Demo 2: Approved case lands with the team, team closes it]

**[Screen: DEMO 2 bumper → lower-third Employee]**

Fresh test. New leave request. Submit.

**[Lower-third Manager]** Approve.

**[Lower-third "Logged in as: Leave Management Team member · HR Team"]**

Here's the case — assigned to the Leave Management Team, state Work In Progress. The team picks it up.

Now the manual bit. The team member goes into their HRIS — Workday, SAP, whatever — and records the leave. For us, that's the mock table.

**[Navigate to the mock table list, New record]**

New Leave Record. Employee ID — I'll grab the requester's sys_id or email, depending on how your real HRIS keys records. Leave Type — Annual. Start Date, End Date — copy from the case. Days Taken — 3. Approval Reference — I'll paste the HRC number so we can trace. Recorded At — now. Save.

**[Back to the HR Case]**

Row's in the mock HRIS. Now close the case. State — Closed Complete. ✏️ Close code — Approved and Recorded *(your exact field label)*. Close notes — "Leave recorded in HRIS, reference [row number]."

Save. Done. That's the happy path working end to end.

🆕 **[20-second reject check]**
One more, fast. New request, and this time the manager clicks **Reject**. Open the case — Closed Incomplete, "Rejected by manager" in the close notes. Both branches work.

🆕 **[20-second no-manager check]**
And the guard — submit as the user with **no manager**. Case goes straight to the Leave Management Team, with our work note explaining why. Nothing stuck.

---

### [13:30 — The honest bridge to Episode 3]

**[Screen: face-cam or brand card]**

Pause here, because this is the important bit.

What just happened — the HR team member spent two or three minutes copy-pasting data from one system to another. In a real company with hundreds of leave requests a week, that adds up. One person, maybe two, doing nothing but data entry between HRSD and HRIS.

That's what Episode 3 fixes. We take that manual Step 5 and replace it with a Flow Designer REST step that writes to the HRIS automatically on approval. Error handling, retry on failure, log the response back to the HR Case. End result — the team never touches the HRIS for standard leave requests.

The pattern you learn in Episode 3 isn't specific to Workday or SAP either. It's the pattern you'd use for any external system of record integration — payroll, benefits, certificates, whatever.

---

### [14:30 — Outro]

**[Screen: slide 7 clip ("What we're NOT doing today") → face-cam → slide 8 clip as end screen]**

That's Episode 2. Manager approval working, the no-manager guard, auto-assignment, and the team handoff end to end — with the mock HRIS as our Episode 3 target.

Honest flags on what we didn't cover today — multi-level approvals, HR Business Partner co-approvals, notification emails, SLAs on time-to-approve. Those are Episode 4. The real integration is Episode 3.

Next episode — Episode 3 — External HRIS Integration. We automate the manual step you just watched the team do. Drops in two weeks.

If this helped, subscribe. And a genuine question for the comments — **in your real projects, where does the leave data actually live? Is it Workday, SAP SuccessFactors, something custom, or does HRSD try to own it?** I'll read the interesting answers at the start of Episode 3.

See you next time.

---

## PRODUCTION NOTES (unchanged + 🆕)

- Build sections move faster than demo sections — viewers can pause the builds; the demos carry the story.
- 🆕 Use the **lower-third PNGs** every time you switch user (employee → manager → HR team). Cut the impersonation menu clicks entirely.
- 🆕 Use the **BUILD / DEMO bumpers** at the start of each section — they make chapters obvious and give you clean cut points.
- Flow Designer at 150% zoom. Speed-ramp every save spinner.
- Raw recording target: 25–30 minutes. If you go past 35, cut *in the recording*, not in editing.
- 🆕 **Recording the slides:** record them as a separate audio pass (like you did), 1 s pause between lines — send it to me and I'll rebuild the slide clips with highlights in your voice.

## CHAPTERS (update after editing)
```
0:00 What we're building
0:30 Series intro
1:15 Where we are
2:00 The flow & build order
3:30 Build 1: Mock HRIS table
5:30 Build 2: Manager approval + no-manager guard
8:00 Demo 1: Manager approves
10:00 Build 3: Auto-assign on approval
11:30 Demo 2: Team closes, reject & no-manager checks
13:30 Why Episode 3 matters
14:30 Wrap-up & next episode
```
