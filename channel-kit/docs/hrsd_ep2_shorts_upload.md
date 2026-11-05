# Upload sheet: HRSD Episode 2 Shorts (3)

All: 1080×1920 · PPT style · voice 9 · −14 LUFS · captions burned in + `.srt` · Playlist: **HR Leave Request Series (HRSD)**
Audience: not for kids · Category: Education · Altered content: No
**Related video = Episode 2.** Publish Episode 2 first, then set it on each Short. Until then, use Episode 1.2.

Suggested order: **C** first (concept, widest audience, teases Ep 2 + Ep 3), **A** 1–2 days later, **B** 1–2 days after that.

---

## SHORT A: No-manager guard (35 s)
**File:** `hrsd_ep2_shortA_no_manager_guard.mp4` (+ `_captions.srt`, `_cover.jpg`)

**Title (pick one):**
1. ✅ `Approval Stuck Forever? Add This Guard (ServiceNow Flow Designer)`
2. `What Happens When the Employee Has No Manager? (ServiceNow)`
3. `The 10-Second Fix for Stuck Approvals in ServiceNow`

**Description:**
```
If the requester has no manager, a manager approval has nowhere to go and the case just sits there.
Fix in Flow Designer: before Ask for Approval, add an If (Requested for › Manager is empty). Inside it, update the HR case
(assign to the Leave Management team + a work note saying why), then End Flow.

From Episode 2 of the HR Leave Request series. Full build: related video above ⬆️

#servicenow #flowdesigner #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Tags:**
```
servicenow, service now, flow designer, servicenow approval, ask for approval, servicenow hrsd, hr case, servicenow developer, servicenow tutorial, servicenow tips
```

**Pinned comment:**
```
Where else do you guard against empty data before an approval? Contractors, new joiners, a delayed HR feed... 👇
```

---

## SHORT B: Approver = requester's manager + rejection rule (37 s)
**File:** `hrsd_ep2_shortB_manager_approval_rejection_rule.mp4` (+ `_captions.srt`, `_cover.jpg`)

**Title (pick one):**
1. ✅ `Ask for Approval: Use the Manager Pill + Add a Rejection Rule (ServiceNow)`
2. `Stop Hard-Coding Approvers in ServiceNow Flow Designer`
3. `ServiceNow Manager Approval in Flow Designer, the Right Way`

**Description:**
```
Don't hard-code the approver. In Ask for Approval, approve when Anyone approves, with the approver from the data pill:
Trigger › HR Case Record › Requested for › Manager.
Add a rejection rule too (reject when Anyone rejects). ServiceNow docs recommend rejection rules so the flow doesn't stay waiting.
Then branch: Approved → assign to the Leave Management team; otherwise close as rejected. Journal field = Work notes for the audit trail.

From Episode 2 of the HR Leave Request series. Full build: related video above ⬆️

#servicenow #flowdesigner #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Tags:**
```
servicenow, service now, flow designer, ask for approval, servicenow approval, approval rules, servicenow hrsd, servicenow developer, servicenow tutorial, workflow studio, servicenow tips
```

**Pinned comment:**
```
Docs: search "Ask for Approval action" on the ServiceNow docs site (Workflow Studio / Flow Designer). Labels can differ slightly by release.
```

---

## SHORT C: HRSD requests, the HRIS records (39 s)
**File:** `hrsd_ep2_shortC_hrsd_requests_hris_records.mp4` (+ `_captions.srt`, `_cover.jpg`)

**Title (pick one):**
1. ✅ `HRSD Is NOT Your Leave System of Record (ServiceNow Design Tip)`
2. `HRSD vs Workday/SAP: Who Owns Leave? (ServiceNow)`
3. `HRSD Requests. The HRIS Records. (ServiceNow Architecture)`

**Description:**
```
HRSD owns the request, the approval decision and the audit trail.
The HRIS (Workday, SAP, or whatever the client runs) owns the leave balance and payroll.
After approval, the leave is recorded in the HRIS and the HRIS reference comes back to the HR case.
Episode 2 does that handoff by hand; Episode 3 automates it over REST.

From Episode 2 of the HR Leave Request series. Full build: related video above ⬆️

#servicenow #hrsd #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Tags:**
```
servicenow, service now, servicenow hrsd, hr service delivery, hris, workday integration, sap successfactors, system of record, servicenow architecture, servicenow tips
```

**Pinned comment:**
```
In your projects, where does leave really live: Workday, SAP SuccessFactors, something custom, or HRSD itself? 👇
```

---

## Check before publishing
- [ ] Episode 2 is live → set it as the Related video on all three
- [ ] Labels in the Shorts match your Episode 2 build ("Leave Management Team", "Work in Progress", "Closed Incomplete").
      Mock UI is labelled "Illustrative" on screen.
- [ ] Brand scan done: only "ServiceNow Simplified" appears ✅
