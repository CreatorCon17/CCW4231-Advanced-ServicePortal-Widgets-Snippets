# ServiceNow Simplified — HR Leave Request Series
## Episode 2: Manager Approval & The HR Handoff
### Script — Conversational (professional-friendly)

**Target length:** 14–16 minutes
**Format:** Mix of build (approval + assignment config + mock table) and demo (manager approval flow + HR team closing)
**Voice:** Same as Episode 1 v2 — senior colleague explaining over coffee

**How to use this script:** Read it twice out loud before recording. Use it as a map, not a teleprompter. If something comes to you mid-recording that sounds better, keep it.

**Prep before you hit record:**
- Build the mock HRIS table (`x_[client]_hris_mock_leave_record`) in your scope before recording — don't do it on camera, that's a tangent
- Create the Leave Management Team assignment group with at least one member (not you)
- Have a test user with their Manager field set, so the approval has somewhere to go
- Submit one Leave Request from Episode 1's form so you have a fresh HR Case to work with
- Browser zoom 125% on the ServiceNow UI, 150% on anything with small text (Flow Designer especially)

---

## THE SCRIPT

### [0:00 — Cold open, show the whole flow before explaining it]

**[Screen: fast-cut montage — employee submits, manager approval email, HR team updates mock HRIS, case closes]**

Here's what we're building today. Employee submits a leave request. It goes to their manager for approval. Manager approves, case lands on the HR team's desk. They update the external HRIS — Workday, SAP, whatever your client runs — and close the case out.

Four moving parts, one real flow, based on an actual client project. Let's build it.

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

**[Screen: PPT slides 2 through 5]**

**On Slide 2 (Where We Are):**

Five episodes total. Episode 1 is done — split into Part 1.1 and Part 1.2 in the end because it ran long. Today's Episode 2. After this we do the real HRIS integration in Episode 3, then notifications and SLAs in Episode 4, then portal polish in Episode 5.

**On Slide 3 (The Full Flow at a Glance):**

This is the end-to-end flow. Five steps. Employee submits. Case routes to their manager. Manager approves or rejects. Case gets assigned to the Leave Management team. Team updates the external HRIS and closes the case.

Pay attention to Step 5 — I've marked it amber. That's the manual step. The HR team is physically going into Workday or SAP and typing stuff in. In Episode 3 we automate that. Today we leave it manual on purpose, so you can see where the integration slots in later.

**On Slide 4 (Two Systems, Two Jobs):**

Quick principle before we build. HRSD and your HRIS — Workday, SAP, whatever — do different jobs. HRSD owns the request and the audit trail. The HRIS owns the real leave balance and payroll. Your HR team is the bridge between them, until integration is built.

This matters because a lot of HRSD projects try to make HRSD the system of record for leave. Don't. Payroll will fight you, finance will fight you, and auditors will fight you. HRSD requests, HRIS records. That's the separation.

**On Slide 5 (Today's Build Order):**

Five things we're doing. Three builds, two demos. Build the mock HRIS table. Build the manager approval. Demo the manager side. Build the auto-assignment to the Leave Management team. Demo the team closing it out.

PPT off. Let's build.

---

### [3:30 — Build 1: The mock HRIS table]

**[Screen: PDI, System Applications → Studio or Tables]**

First thing we do is build the mock HRIS table. This table stands in for Workday or SAP for the demo. In Episode 3, our integration writes to this exact table — so what we build now gets reused.

I'm creating it in my application scope — [client] HR Mock. Call the table whatever makes sense in your scope — I'm using `x_[client]_hris_mock_leave_record`. The `x_` prefix is standard for scoped tables.

**[Open the table creation form]**

Label — Leave Record (Mock HRIS). Name — leave_record. Create module and menu — yes, so I can see the records easily during the demo.

Fields I need — and I'm matching what Episode 3's integration will send:

- Employee ID — string, 100 characters. In the real integration this is probably an email or an employee number.
- Leave Type — Choice. Values: Annual, Sick, Casual, Work From Home, Other.
- Start Date — date.
- End Date — date.
- Days Taken — integer. Calendar days today — Episode 3 refines this to working days.
- Approval Reference — string. This holds the HRC number so we can trace from the HRIS back to HRSD.
- Recorded At — date/time. When the row was created in the mock.

Save.

Quick honest note — in a real project the external HRIS has its own schema, API, and rules. The point here isn't to model Workday perfectly. It's to have something concrete the HR team can update manually today, that Episode 3 can automate against. Keep it simple.

---

### [5:30 — Build 2: Manager approval via Flow Designer]

**[Screen: Filter navigator → Flow Designer → New Flow]**

Now the approval. We're doing this in Flow Designer because that's where ServiceNow is heading. Classic approval activities still work, but if you're starting new, Flow Designer is where you go.

New Flow. Name — Leave Request Approval Flow. Application — Advanced Solutions. Run as — System User, for now. On a real project you'd think harder about this.

**[Trigger setup]**

Trigger. We want this flow to run when an HR Case gets created with our leave service. So — trigger type is Created, table is `sn_hr_core_case`. Add a condition: HR Service is Leave Request. Save.

Important call-out — only triggering on Created is naive. In a real project you'd also handle the Updated case, in case someone edits the request. For today, Created is fine.

**[Add Approval action]**

Add an action. Search for Approval — I'm using "Ask For Approval." 

Table — HR Case, current record. 
Approvers — this is the key field. Dynamic lookup. I want the approver to be the manager of the Requested For user.

Click the data pill picker. Trigger → HR Case Record → Requested For → Manager. That's the chain. Platform grabs whoever's in the Manager field on the requester's user record.

Approval type — Anyone. Only one approver anyway. Journal field — Work notes, so the approval decision shows up in the case history.

**[Save and test the data path mentally]**

Save the action. Save the flow. Activate it.

What this does right now — when a Leave Request case is created, the manager gets an approval. They can approve or reject. Nothing happens *after* that yet. We add the "what happens next" in the next build step.

---

### [8:00 — Demo 1: Manager receives, approves, case transitions]

**[Screen: switch user to an employee — the one whose manager is set]**

Let's test what we have. I'm switching to the employee user — Dougie Macarthur, whose manager is set to someone in my demo instance.

Submit the leave request form from Episode 1. Annual Leave, pick a start date, end date. Submit. HR Case created — HRC00050something.

**[Impersonate the manager user]**

Now switch to the manager user. Impersonate. Their My Approvals, or the approval email if we had notifications on, which we don't yet — that's Episode 4.

Approval record is there. Click Approve. Done.

**[Back on the HR Case]**

Switch back. Open the HR Case. Approval section — approved. Great. But notice — the case state hasn't changed. It's still sitting in whatever state the Record Producer created it in. Assignment group is empty. There's nothing routing this to anyone to actually do the next step.

That's what the next build fixes.

Quick honest callout — if you approved and your flow didn't update the case, check your flow context. The approval action completed, but no step after it did anything. That's expected right now. We add the "do something after approval" bit next.

---

### [10:00 — Build 3: Auto-assign to Leave Management on approval]

**[Screen: back to Flow Designer, open the flow]**

Back to the flow. After the Approval action, I'm adding a Conditional step — If Approval State is Approved.

Inside the If: Update Record action. Record is current HR Case. Fields to update:
- Assignment Group — Leave Management Team (the group you set up before recording)
- State — Work In Progress

That's it for the approved branch.

**[Else branch]**

Else — approval rejected. Update Record again, this time:
- State — Closed Incomplete
- Resolution Code — I'll add one called "Rejected by Manager" if your instance doesn't have it OOB
- Close notes — set to "Rejected by manager."

Save, activate.

Quick design note — in a real project you'd probably send the employee a notification on rejection with the reason. That's Episode 4. For now the state change is enough.

---

### [11:30 — Demo 2: Approved case lands with the team, team closes it]

**[Screen: switch to the employee user, submit a new request]**

Fresh test. New leave request. Submit.

Switch to the manager. Approve.

Switch to a user who's a member of Leave Management Team.

**[Open their work list]**

Here's the case — assigned to the Leave Management Team, state Work In Progress. The team picks it up.

Now the manual bit. The team member goes into their HRIS — Workday, SAP, whatever — and records the leave. For us, that's the mock table.

**[Navigate to the mock table list, New record]**

New Leave Record. Employee ID — I'll grab the requester's sys_id or email, depending on how your real HRIS keys records. Leave Type — Annual. Start Date, End Date — copy from the case. Days Taken — 3. Approval Reference — I'll paste the HRC number so we can trace. Recorded At — now. Save.

**[Back to the HR Case]**

Row's in the mock HRIS. Now close the case. State — Closed Complete. Resolution Code — Approved and Recorded. Close notes — "Leave recorded in HRIS, reference [row number]."

Save. Done.

That's the end-to-end flow working.

---

### [13:00 — The honest bridge to Episode 3]

**[Screen: face-cam or brand card]**

Pause here, because this is the important bit.

What just happened — the HR team member spent two or three minutes copy-pasting data from one system to another. In a real company with hundreds of leave requests a week, that adds up. One person, maybe two, doing nothing but data entry between HRSD and HRIS.

That's what Episode 3 fixes. We take that manual Step 5 and replace it with a Flow Designer REST step that writes to the HRIS automatically on approval. Error handling, retry on failure, log the response back to the HR Case. End result — the team never touches the HRIS for standard leave requests.

The pattern you learn in Episode 3 isn't specific to Workday or SAP either. It's the pattern you'd use for any external system of record integration — payroll, benefits, certificates, whatever.

---

### [14:00 — Outro]

**[Screen: face-cam, outro card]**

That's Episode 2. Manager approval working, auto-assignment working, the team handoff flow end to end, with the mock HRIS as our Episode 3 target.

Honest flags on what we didn't cover today — multi-level approvals, HR Business Partner co-approvals, notification emails, SLAs on time-to-approve. Those are Episode 4. The real integration is Episode 3.

Next episode — Episode 3 — External HRIS Integration. We automate the manual step you just watched the team do. Drops in two weeks.

If this helped, subscribe. And a genuine question for the comments — **in your real projects, where does the leave data actually live? Is it Workday, SAP SuccessFactors, something custom, or does HRSD try to own it?** Curious what patterns people are seeing. I'll read the interesting answers at the start of Episode 3.

See you next time.

---

## PRODUCTION NOTES

**Recording tips given the hybrid format:**
- This has more config than Episode 1.2 and more demo than Episode 1.1 — pace will matter. Build sections should move faster than demo sections, because viewers can pause the build if they're following along, but demo sections carry the story.
- When you switch users on camera (employee → manager → team member), add a visible on-screen label every time: "Logged in as: Dougie Macarthur (Employee)" / "Logged in as: Narvdasaver Dubey (Manager)" etc. Impersonation is confusing without the label.
- Flow Designer screens are dense. Zoom to 150% on them, not 125%.

**Editing cuts to make ruthlessly:**
- Every Flow Designer save spinner — speed-ramp or hard cut
- Every impersonation menu click sequence — cut, just appear as the new user
- Any pause where you're thinking about which pill to pick in Flow Designer

**Time budget warning:**
- Raw recording target: 25-30 minutes. If you go past 35, pause and look at what you can cut *in the recording*, don't push it to editing.
- First try at Episode 1 went 46 minutes for a 12-minute target. This script is already scoped tighter but still has 3 builds + 2 demos. Budget accordingly.

**Honest flag on the mock table approach:**
When you record, acknowledge that the mock table is just a demonstration vehicle — don't let viewers think you're building a production HRIS. A single sentence covers it: "This isn't a real HRIS. It's a stand-in so we can see the flow working end to end, and so Episode 3's integration has something concrete to write to." Transparent, honest, moves on.
