# Upload sheet: HRSD Episode 1.2 Shorts (2)

Both: 1080×1920 · PPT style · voice 9 · −14 LUFS · captions burned in + `.srt` · **Related video = Episode 1.2**
Playlist: **HR Leave Request Series (HRSD)** · Audience: not for kids · Category: Education · Altered content: No

Suggested order: **Short A** first (it continues the Episode 1.1 Short's "employee type" catch), **Short B** 1–2 days later.

---

## SHORT A: Employee type via GlideAjax (43 s)
**File:** `hrsd_ep12_shortA_employee_type_glideajax.mp4` (+ `_captions.srt`, `_cover.jpg`)

**Title (pick one):**
1. ✅ `Get Employee Type from the HR Profile (ServiceNow GlideAjax)`
2. `Auto-Populate Can't Do This, but GlideAjax Can (ServiceNow HRSD)`
3. `ServiceNow GlideAjax + Script Include in 40 Seconds`

**Description:**
```
Employee type lives on the HR profile, not sys_user, so variable auto-populate can't reach it.
Fix: an onChange client script on Requested for calls a client-callable Script Include via GlideAjax, which reads sn_hr_core_profile and returns the display value.
Gotchas: tick Client callable (GlideAjax enabled), and return getDisplayValue(), not the back-end value.

From Episode 1.2 of the HR Leave Request series. Full build: related video above ⬆️

#servicenow #glideajax #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Tags:**
```
servicenow, service now, glideajax, script include, client script, servicenow hrsd, hr profile, servicenow developer, servicenow tutorial, record producer, servicenow tips
```

**Pinned comment (code):**
```
Client script (onChange · requested_for):
var ga = new GlideAjax('LeaveRequestHelper');
ga.addParam('sysparm_name', 'getEmployeeType');
ga.addParam('sysparm_user_id', newValue);
ga.getXMLAnswer(function (answer) { g_form.setValue('employee_type', answer); });

Script Include (Client callable):
getEmployeeType: function () {
  var userId = this.getParameter('sysparm_user_id');
  var gr = new GlideRecord('sn_hr_core_profile');
  if (gr.get('user', userId)) return gr.getDisplayValue('employee_type');
  return '';
}
Match the variable/field names to your own instance.
```

---

## SHORT B: Leave duration + remaining balance (40 s)
**File:** `hrsd_ep12_shortB_leave_duration_balance.mp4` (+ `_captions.srt`, `_cover.jpg`)

**Title (pick one):**
1. ✅ `Calculate Leave Days & Remaining Balance (ServiceNow Client Script)`
2. `One Typo Broke My ServiceNow Form (Here's How I Found It)`
3. `ServiceNow onChange Client Script: Date Difference in Days`

**Description:**
```
Calculate leave duration and remaining balance the moment the dates change: an onChange client script on End date.
Days = ceil((end − start) / ms per day) + 1. Remaining = current balance − days.
When it broke, the browser console showed the cause straight away: a typo in parseInt.
Counts calendar days for now; working days & holidays come later in the series.

From Episode 1.2 of the HR Leave Request series. Full build: related video above ⬆️

#servicenow #clientscript #shorts

Voice: Piper TTS, LibriTTS dataset (CC BY 4.0)
```

**Tags:**
```
servicenow, service now, client script, onchange client script, servicenow hrsd, date calculation, servicenow debugging, servicenow developer, servicenow tutorial, servicenow tips
```

**Pinned comment:**
```
Tip: add the same calculation onChange of Start date too, so changing either date recalculates. What would you add next: working days or holidays? 👇
```

---

## Check before publishing (accuracy)
- [ ] **HR profile lookup:** the Short shows `gr.get('user', userId)` (look up the HR profile by its *user* field).
      If your episode used `gr.get(userId)`, it only works if the IDs happen to match. Worth a quick check on your PDI.
- [ ] **Variable/field names** (`employee_type`, `leave_duration`, `current_balance`, `remaining_balance`, `start_date`, `end_date`) are labelled illustrative. Tell me yours and I'll re-render with the exact names.
- [ ] **Date parsing:** `new Date(g_form.getValue(...))` assumes the system date format (yyyy-MM-dd). Users with a different date format can get wrong results; `getDateFromFormat(value, g_user_date_format)` is the safer option if you see odd numbers.
- [ ] Brand scan done: only "ServiceNow Simplified" appears ✅
