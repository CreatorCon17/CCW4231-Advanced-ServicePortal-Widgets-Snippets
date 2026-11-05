# HRSD Episode 3 — External HRIS Integration (outline)

**Goal:** replace Episode 2's manual step. On approval, **Instance A (HRSD)** creates the leave record on
**Instance B (Mock HRIS)** over REST, then writes the HRIS reference back to the HR case.
Auth is shown twice: **Basic Auth** first (simple, to get it working), then **OAuth 2.0** (what you'd use in production).
**Target length:** 18–22 min (this is the most technical episode, so split into 3.1 / 3.2 if it runs long).

> Verify every menu path below on your instances before recording; labels move between releases.
> Lines marked ⚠️ are the ones most likely to differ.

---

## 0. Architecture slide (open with this)
```
Instance A (HRSD)                                   Instance B (Mock HRIS)
HR Case approved ──► Flow Designer                   Scripted REST API
                     └─ REST step ──POST /leave──►   └─ creates HRIS Leave record
                        (Connection & Credential  ◄── 201 + { number, sys_id }
                         alias: Basic → OAuth 2.0)
HR Case ◄── write back HRIS reference + work note
```
Say once: "Instance B stands in for Workday or SAP. The pattern — contract, credentials, call, handle errors, write back — is the same."

## 1. The integration contract (2 min)
Request (A → B), JSON:
| Field | Source on Instance A |
|---|---|
| `employee_id` | Requested for → email |
| `leave_type` | Leave category variable |
| `start_date`, `end_date` | Date variables (send as `yyyy-MM-dd`) |
| `days_taken` | Leave duration variable |
| `approval_reference` | HR case number |

Response (B → A): `201 Created` with `{ "number": "...", "sys_id": "..." }`.
Errors: `400` (validation, e.g. missing field / end before start), `401` (auth), `5xx` (HRIS down).

## 2. Instance B — build the API (5–6 min)
1. **App role** in the HRIS Leave app, e.g. `hris_leave.integration` (name it as you like), with create/read on the HRIS Leave table (ACLs).
2. **Integration user**, e.g. `hris.integration`: tick **Web service access only** (can't log in to the UI), grant only the app role.
3. **Scripted REST API** (System Web Services → Scripted REST APIs) in the HRIS Leave scope:
   - API name `HRIS Leave`, resource `POST /leave`, **Requires authentication** ✓.
   - Script outline:
     ```javascript
     (function process(request, response) {
         var body = request.body.data;
         // validate required fields
         var required = ['employee_id', 'leave_type', 'start_date', 'end_date', 'days_taken', 'approval_reference'];
         for (var i = 0; i < required.length; i++) {
             if (!body[required[i]]) {
                 response.setStatus(400);
                 return { error: 'Missing field: ' + required[i] };
             }
         }
         var gr = new GlideRecord('x_<prefix>_hris_leave_hris_leave_table');   // your exact table name
         gr.initialize();
         gr.setValue('employee_id', body.employee_id);
         gr.setValue('leave_type', body.leave_type);
         gr.setValue('start_date', body.start_date);
         gr.setValue('end_date', body.end_date);
         gr.setValue('days_taken', body.days_taken);
         gr.setValue('approval_reference', body.approval_reference);
         gr.setValue('recorded_at', new GlideDateTime());
         var id = gr.insert();
         response.setStatus(201);
         return { sys_id: id, number: gr.getValue('number') };   // if the table has a number field
     })(request, response);
     ```
     ⚠️ Add a **Number** field (auto-number) to the HRIS Leave table if you want a human-readable HRIS reference.
4. **Test it** with the REST API Explorer on B, authenticated as the integration user → `201`.
   Talking point: "In a real project this API already exists. Workday or SAP give you their contract, and you never build it."

## 3. Instance A — Basic Auth (4–5 min)
1. **Connection & Credential Alias** (Connections & Credentials → Connection & Credential Aliases): e.g. `HRIS Leave`, type HTTP.
2. **HTTP(s) Connection** on the alias: Connection URL = `https://<instanceB>.service-now.com`.
3. **Basic Auth Credentials**: user `hris.integration` + password → attach to the alias / connection.
   Talking point: "Credentials live in the credential store, never in scripts or flow inputs."
4. **Custom action** in Flow Designer (Action Designer): `Create HRIS Leave Record`
   - Inputs: the 6 contract fields. **REST step**: Connection = the alias, Resource path `/api/<namespace>/hris_leave/leave`, Method POST, JSON body.
   - ⚠️ The **REST step needs IntegrationHub** to be available on your instance. If it isn't, use a **Script step** with
     `sn_ws.RESTMessageV2` and a REST Message record that uses the same credentials.
   - Outputs: `status_code`, `hris_number`, `hris_sys_id`, `error_message` (parse the response body with a Script step or the JSON parser step).
5. **Call it from the Episode 2 flow**, in the *Approved* branch, after the assignment step.

## 4. Error handling & write-back (3–4 min)
- In the action: don't let the flow die silently on a non-201. Set outputs, then in the flow:
  - **If status = 201** → Update HR case: work note "Recorded in HRIS: <hris_number>", store `hris_number` in a case field
    (e.g. `u_hris_reference`, created on Instance A), then close as *Approved and Recorded*.
  - **Else** → work note with the error, keep the case **Work In Progress** with the Leave Management Team, so a human can retry.
    This is the Episode 2 manual path becoming the *fallback*.
- ⚠️ **Retry:** show one retry for 5xx/timeouts (a loop with a counter + wait, or the retry options your release offers on the action/connection). Never retry a 400; it will fail the same way.
- Demo the failure on purpose: temporarily break the password → `401` → case stays with the team and a clear work note.

## 5. Upgrade to OAuth 2.0 (5–6 min)
**Why:** no long-lived password sent on every call; tokens expire and can be revoked; it's the standard for production integrations.
1. **Instance B — OAuth endpoint:** System OAuth → Application Registry → *Create an OAuth API endpoint for external clients*
   → note **Client ID** and **Client Secret**. Token URL: `https://<instanceB>.service-now.com/oauth_token.do`.
2. **Instance A — OAuth provider:** System OAuth → Application Registry → *Connect to a third party OAuth Provider*:
   Client ID/Secret from B, **Token URL** as above, **Default grant type**:
   - ⚠️ **Password** grant (resource-owner, using the `hris.integration` user) works broadly on ServiceNow-to-ServiceNow, so it's the safest for the demo.
   - ⚠️ **Client credentials** grant (no user password) is cleaner, but inbound support depends on your release/configuration. Check on Instance B before promising it on camera.
3. **Instance A — OAuth 2.0 Credentials:** create an *OAuth 2.0 Credentials* record using that OAuth profile, then **swap it onto the same Connection & Credential alias**.
4. **Point to make on camera:** *the flow and the action didn't change at all*. Only the credential on the alias did. That's why aliases exist.
5. Run the leave request again → 201 → write-back works with OAuth.

## 6. Recap + bridge to Episode 4 (1 min)
Contract → API → integration user → alias with Basic Auth → action + flow → errors + retry → write-back → OAuth 2.0 swap.
Next: Episode 4, notifications & SLAs (tell the employee, chase slow approvers).

---

## Prep checklist (before recording Episode 3)
- [ ] Instance B active (log in; developer instances are reclaimed after inactivity)
- [ ] HRIS Leave table has the 7 fields (+ optional Number field)
- [ ] Decide namespace/resource path and note the **exact** table name on B
- [ ] Instance A: confirm the REST step is available (IntegrationHub); otherwise prepare the RESTMessageV2 fallback
- [ ] Instance A: create `u_hris_reference` on the HR case (or decide where the reference goes)
- [ ] Overlays: `overlay_instance_A_hrsd.png` / `overlay_instance_B_mock_hris.png` on every switch
- [ ] Never show real passwords/secrets. Blur the client secret and password fields in the edit
- [ ] Brand rule: only "ServiceNow Simplified" on screen; call B "Mock HRIS", never a client name

## Short ideas from this episode
1. "Never put credentials in a script — use a Connection & Credential alias"
2. "Basic Auth → OAuth 2.0 without touching the flow"
3. "Don't retry a 400" (error-handling rule of thumb)
