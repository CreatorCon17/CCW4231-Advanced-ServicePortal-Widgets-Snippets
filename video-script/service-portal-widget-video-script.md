# Video Script — "Your Service Portal Widget Is Slow, Stale, and Leaking Data (Fix All 3)"

> Built on the code in this repo (Lab_1 → Lab_6). Every snippet shown on screen exists in the repo,
> plus the "pro fixes" called out below.

---

## 0. Read this first — what this script is (and isn't) based on

**Fact:** I could not open `youtube.com/@ServiceNowSimplifiedYT` from the environment this was written in
(YouTube is blocked by the network policy), and web search returned no indexed data for that handle.
So the "channel analysis" below is **not** an analysis of that channel's actual videos, views or retention.

**What it is instead:** the format patterns that are standard for ServiceNow tutorial channels
(screen-recorded PDI demos, problem → fix structure, interview/real-project framing). Treat them as
**hypotheses to check** against the channel, not findings.

**To make this script match the channel for real**, check these on the channel and adjust:

| Check on the channel | Why it matters | Where to adjust in this script |
|---|---|---|
| Top 5 videos by views (Sort → Popular) | Tells you which topics/titles actually win | Title options (§2) |
| Average length of the top 5 | Long-form 8–15 min vs. short 3–5 min | Cut sections 5–6 if they run short |
| First 15 s of 3 videos | Their real hook style (question? result-first? "interview question"?) | Hook (§3) |
| Face-cam or voice-only? Hindi/English mix? | Tone and delivery | Whole script |
| Do they post Shorts? | Whether to ship the 60 s cut | §8 |

---

## 1. Niche patterns (hypotheses — verify against the channel)

**Typical scenarios ServiceNow tutorial channels cover**
- "Interview question" framing: *"What's the difference between GlideRecord and GlideRecordSecure?"*
- Real-project problems: *"The client says the portal is slow."*
- Step-by-step builds on a Personal Developer Instance (PDI).
- Client script vs. server script vs. REST — "which one, when?"

**Hook types that generally work in technical tutorials**
1. **Result first** — show the finished thing in the first 5 s, then "let's build it".
2. **Mistake callout** — "90% of devs write this widget wrong" (only use a number you can back up — see note below).
3. **Interview hook** — "This question comes up in interviews and most people get it wrong."
4. **Pain hook** — "Your portal page takes 6 seconds to load. Here's why."

> ⚠️ Don't put made-up stats ("90% of developers…") on screen. Use phrasing you can defend:
> "This is one of the most common mistakes I see in widget code."

---

## 2. Title + thumbnail options

| # | Title | Thumbnail text |
|---|---|---|
| A (recommended) | Your ServiceNow Widget Is Slow, Stale & Leaking Data — Fix All 3 | "SLOW ❌ STALE ❌ UNSAFE ❌" |
| B | Service Portal Widget: Beginner vs Pro (Same Widget, 6 Upgrades) | "BEGINNER → PRO" |
| C | ServiceNow Interview Q: GlideRecord vs REST vs Record Watcher in Widgets | "Interview Q 🎯" |
| D | Build a Real-Time Service Portal Widget (No Page Refresh) | "LIVE UPDATES ⚡" |

Thumbnail: split screen — left: spinner + red X, right: live-updating list + green check.

**Target length:** ~11–13 min. **Shorts cut:** §8.

---

## 3. HOOK (0:00 – 0:30)

**[SCREEN: Portal page. Browser DevTools Network tab open. Page hangs on a blank panel for ~3 s.]**

> "This is a Service Portal widget. It lists active incidents. It works.
> And it has **three** problems that will hurt you in production —
> it blocks the page while it loads, it never updates unless you hit refresh,
> and — this is the one that gets people in trouble — it can show records the user **isn't allowed to see**."

**[SCREEN: Quick cut to the final version — a second user updates an incident in another window, list updates live, a counter widget ticks up.]**

> "By the end of this video you'll turn the first version into this one:
> lazy-loaded, configurable, real-time, and talking to another widget.
> Six upgrades. All the code is in the description. Let's go."

**[TEXT ON SCREEN: "6 upgrades · code in description"]**

---

## 4. SETUP (0:30 – 1:15)

**[SCREEN: Service Portal → Widgets → New. Name: `K17 List Widget`.]**

> "Quick context: a widget has three main pieces —
> the **HTML template** is what the user sees,
> the **server script** runs on the ServiceNow instance and fills a `data` object,
> and the **client script** is the AngularJS controller running in the browser.
> Keep those three in your head, because every upgrade today is about moving work between them."

**[GRAPHIC: 3 boxes — Template ↔ Client Script ↔ Server Script, arrow labeled `data`.]**

---

## 5. UPGRADES

### Upgrade 1 — The baseline (and why it's slow) (1:15 – 2:30)

**[SCREEN: `Lab_1/Original/ServerScript.js`]**

```js
data.list = [];
var gr = new GlideRecord('incident');
gr.addQuery('active', true);
gr.query();
while (gr.next()) {
    var record_obj = {};
    record_obj.number = gr.number.getDisplayValue();
    record_obj.short_description = gr.short_description.getDisplayValue();
    record_obj.priority = gr.priority.getDisplayValue();
    record_obj.category = gr.category.getDisplayValue();
    data.list.push(record_obj);
}
```

> "Classic widget. Server script queries incidents, builds a list, template does an `ng-repeat`.
> The problem: this server script runs **before the page renders**.
> If this query takes two seconds, your whole page waits two seconds."

> "And look closely — two more issues I'll come back to:
> there's **no limit** on this query, and it uses plain `GlideRecord`."

**[TEXT ON SCREEN: "Problem #1: blocks page load"]**

---

### Upgrade 2 — Lazy load with `server.update()` (2:30 – 4:00)

**[SCREEN: `Lab_1/Updated/ServerScript.js` — highlight `if (input)`]**

```js
if (input) {
    data.list = [];
    // ...same query...
}
```

**[SCREEN: `Lab_1/Updated/ClientScript.js`]**

```js
function($scope) {
    var c = this;
    c.data.loading = true;
    $scope.server.update().then(function() {
        c.data.loading = false;
    });
}
```

> "Here's the trick. On the first page load, `input` is undefined — so the server script does basically nothing
> and the page renders immediately.
> Then the client script calls `server.update()`. That sends `c.data` back to the server as `input`,
> now the `if (input)` block runs, and the list comes back."

**[SCREEN: Template with spinner — `ng-if="c.data.loading"` + `sr-only` "Loading..."]**

> "Meanwhile we show a spinner. And notice the `sr-only` span — that's for screen readers. Small thing, matters for accessibility."

**[DEMO: Reload page — panel appears instantly with spinner, list fills in.]**

> "Same data. Page no longer waits for it."

---

### Upgrade 3 — Skip the server script: Table API from the client (4:00 – 5:30)

**[SCREEN: `Lab_2/ClientScript.js`]**

```js
function($scope, $http) {
    var c = this;
    c.data.loading = true;
    $http.get('/api/now/table/incident?sysparm_query=active%3Dtrue').success(function(response) {
        c.data.loading = false;
        c.data.list = response.result;
    });
}
```

> "Option two: call the REST Table API straight from the browser with `$http`.
> No server script at all."

> "Here's the interview-worthy point — **this one respects ACLs**. The Table API runs as the logged-in user,
> so they only get rows they're allowed to read.
> Plain `GlideRecord` in a server script does **not** enforce ACLs.
> If you stay server-side, use **`GlideRecordSecure`** instead."

**[TEXT ON SCREEN: "GlideRecord = no ACL check · GlideRecordSecure / Table API = ACLs enforced"]**

**[PRO FIX callout — show on screen, not in the lab file]**

> "Three things I'd change before shipping this:"

```js
// 1. .success() is deprecated in AngularJS — use .then()
// 2. Always set a limit
// 3. Ask for display values, or priority shows "1" instead of "1 - Critical"
$http.get('/api/now/table/incident', {
    params: {
        sysparm_query: 'active=true',
        sysparm_limit: 50,
        sysparm_display_value: true,
        sysparm_fields: 'number,short_description,priority,category,sys_id'
    }
}).then(function(response) {
    c.data.loading = false;
    c.data.list = response.data.result;
}, function() {
    c.data.loading = false;
    c.data.error = true;   // show an error state instead of spinning forever
});
```

> "Notice `response.data.result` — with `.then()` the payload is one level deeper than with `.success()`.
> That's a classic bug when people migrate. And using `params` means Angular URL-encodes the query for you."

---

### Upgrade 4 — Reusable row templates with `ng-include` (5:30 – 6:30)

**[SCREEN: Widget → Angular ng-templates related list. Show `task-category` and `task-priority`.]**

```html
<!-- task-category -->
<span>{{item.number}} - {{item.short_description}} - {{item.category}}</span>
<!-- task-priority -->
<span>{{item.number}} - {{item.short_description}} - {{item.priority}}</span>
```

**[SCREEN: `Lab_3/BodyTemplate.html` — highlight `ng-include="'task-category'"`]**

> "Instead of hard-coding the row layout, the row is an Angular ng-template.
> Note the **quotes inside the quotes** — `"'task-category'"`. `ng-include` takes an expression,
> so without the inner quotes Angular looks for a *variable* called task-category. Very common mistake."

---

### Upgrade 5 — Make it configurable with instance options (6:30 – 8:00)

**[SCREEN: `Lab_4/ClientScript.js`]**

```js
c.data.table    = c.options.table    || "incident";
c.data.query    = c.options.query    || "";
c.data.template = c.options.template || "task-category";
```

**[SCREEN: `Lab_4/BodyTemplate.html` — highlight `panel-{{c.options.color}}`, `{{c.options.title}}`, `ng-include="c.data.template"`]**

**[DEMO: Page Designer → drop the widget twice. Instance 1: incident / red / "My P1s". Instance 2: problem / blue / "Open Problems".]**

> "Now it's one widget, many uses. Table, filter, title, colour and row template all come from instance options.
> Define them in the widget's **Option Schema** so admins get a nice form instead of raw JSON."

**[PRO FIX callout]**

> "One warning: this builds the URL by string concatenation.
> If someone puts `&` or `^` in the query option, the URL breaks.
> Use `params` like I showed earlier, or at minimum `encodeURIComponent(c.data.query)`."

---

### Upgrade 6 — Real-time updates with Record Watcher (8:00 – 9:30)

**[SCREEN: `Lab_5/ClientScript.js`]**

```js
function getData() { /* $http call */ }
getData();

snRecordWatcher.initList(c.data.table, c.data.query);
$scope.$on('record.updated', function(name, data) {
    getData();
});
```

**[DEMO: Two browser windows side by side. Window B updates an incident's short description → Window A list updates without refresh.]**

> "This is the 'wow' moment. Record Watcher opens a channel to the instance,
> and whenever a record matching this table and filter changes, we re-fetch."

**[PRO FIX callout]**

> "Two production notes.
> First — every update triggers a **full re-fetch**. On a busy table that's a lot of calls; debounce it.
> Second — in current Service Portal code you'll more often see `spUtil.recordWatch($scope, table, filter, callback)`,
> which also cleans itself up when the widget is destroyed. Check which one your release documents before you pick."

---

### Upgrade 7 (bonus) — Widgets talking to each other (9:30 – 10:45)

**[SCREEN: `Lab_6/ClientScript.js` — highlight broadcast]**

```js
$rootScope.$broadcast("K17ListWidgetUpdated", c.data.list);
```

**[SCREEN: `Lab_6/CountDisplayWidget/ClientScript.js`]**

```js
$scope.$on("K17ListWidgetUpdated", function(evt, results) {
    c.data.count = results.length;
});
```

**[DEMO: List widget + "Total Records" jumbotron on the same page. Update a record → both change.]**

> "The list widget broadcasts its data on `$rootScope`; the counter widget listens.
> Two independent widgets, zero coupling."

> "Gotchas: the event name is a contract — namespace it so it doesn't collide with other widgets.
> The listener has to be registered **before** the first broadcast, or it misses the first value.
> And delete that `console.log` before you ship."

---

## 6. RECAP (10:45 – 11:30)

**[GRAPHIC: checklist animating in]**

> "So, from version one to version seven:
> 1. Lazy-load with `server.update()` — page renders instantly.
> 2. Table API or `GlideRecordSecure` — respect ACLs.
> 3. Always limit, always handle errors, use `.then()`.
> 4. ng-templates for reusable rows.
> 5. Instance options + Option Schema for one widget, many uses.
> 6. Record Watcher for real-time.
> 7. `$broadcast` / `$on` for widget-to-widget communication."

---

## 7. CTA / OUTRO (11:30 – 12:00)

> "All the code — every lab — is linked in the description.
> If you're preparing for interviews, the GlideRecord vs GlideRecordSecure point alone is worth remembering.
> Comment which upgrade you didn't know about, and tell me what widget you want me to build next.
> See you in the next one."

**[END SCREEN: next video + subscribe]**

---

## 8. SHORTS CUT (≤ 60 s, vertical)

> **[0–3 s]** "Your ServiceNow widget might be showing data users shouldn't see."
> **[3–20 s]** *(code on screen)* "Plain `GlideRecord` in a widget server script doesn't check ACLs.
> So whatever this query returns, the user sees."
> **[20–40 s]** "Fix one: use `GlideRecordSecure`. Fix two: call the Table API from the client — it runs as the logged-in user."
> **[40–55 s]** "And while you're there — add a limit. An unlimited query on incident is a slow page waiting to happen."
> **[55–60 s]** "Full widget build is on the channel."

---

## 9. Description template

```
Turn a basic ServiceNow Service Portal widget into a lazy-loaded, ACL-safe,
configurable, real-time widget — step by step.

⏱ Chapters
0:00 The 3 problems
0:30 Widget anatomy
1:15 Baseline widget
2:30 Lazy loading with server.update()
4:00 Table API + ACLs (GlideRecord vs GlideRecordSecure)
5:30 ng-include row templates
6:30 Instance options
8:00 Real-time with Record Watcher
9:30 Widget-to-widget communication
10:45 Recap

💻 Code: <repo link>

#ServiceNow #ServicePortal #ServiceNowDeveloper
```

---

## 10. Pre-recording fact-check list

Verify these on **your** PDI release before recording — don't state them from memory on camera:

- [ ] `spUtil.recordWatch` signature and whether `snRecordWatcher` is still documented on your release.
- [ ] AngularJS version shipped with your Service Portal (affects whether `.success()` still runs at all).
- [ ] Table API default row limit when `sysparm_limit` is omitted on your instance.
- [ ] Demo user in window B has rights to update incidents; demo user in window A can read them (or the live-update demo silently fails).
- [ ] Record the ACL demo with a non-admin user — admin bypasses most ACLs and the point won't show.
