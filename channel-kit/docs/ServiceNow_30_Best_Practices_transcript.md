# ServiceNow: 30 Best Practices (transcript)

## Intro
Most ServiceNow performance problems come from the same few habits.
In this video: 30 best practices across 6 areas. Server-side scripting, client scripts, business rules, debugging, logs & queues, and update sets.
The chapters are in the description, so you can jump straight to what you need. Let's start.

## Server-side scripting
Chapter one. Server-side scripting. This is where most performance problems start.
Write code the next developer can read. Comment why the code exists, not what each line does. Use whitespace and descriptive names. And prefer a simple if else over clever nested ternaries.
Don't repeat yourself. If the same logic appears twice, move it into a function, or a script include. Store a function's result in a variable instead of calling it again. And have functions return a value, so the caller can check what happened.
Counting records? Get row count loads every matching record and then counts them, which gets slower as the table grows. GlideAggregate asks the database to do the count instead.
For complex filters, use one encoded query instead of a chain of add query and add or condition calls. It's easier to read, and you can copy it straight from a list filter.
Let the database do the work. If you only need one record, add set limit one, so the query stops early.
Never hard-code sys IDs. They can differ between instances, and nobody knows what they mean. Store them in a system property, and read it with gs dot get property.
Use get value for logic. A reference field already stores a sys ID, so get value returns it. No dot-walking needed. Use get display value only when you show something to a user, because display values can change, and can depend on the user's language.
And never use eval. It runs any string as code, which opens the door to injection attacks, and its errors don't give you useful line numbers. Call known functions explicitly instead.

## Client scripts
Chapter two. Client scripts. They run in the user's browser, so every extra call is time the user waits.
For mandatory, visible, or read-only fields, use a UI policy, not a client script. Save client scripts for logic UI policies can't handle. And think about list editing: if the form enforces a rule, make sure list edits can't bypass it.
Client scripts have no condition field, so they run every time. In on change scripts, exit early when the form is loading, when the new value is empty, or when it hasn't actually changed.
Use data that's already on the client whenever you can. Need server data at load time? Fill g scratchpad from a display business rule. Need it later? Use asynchronous GlideAjax, and only after checking you really need it. Client-side GlideRecord and get reference are no longer recommended.
When you set a reference field, pass the display value too. Without it, the form makes an extra call to the server just to look it up.
Avoid global client scripts. They load on every form. And avoid DOM manipulation, because it breaks when the UI is upgraded. Use the g form API instead. The exception is UI pages and Service Portal widgets, where you own the markup.

## Business rules
Chapter three. Business rules. They run on every database operation, so small mistakes multiply fast.
Pick the right when. Use before to change the current record, after to update other records, async for work that can wait, and display to send data to the form with g scratchpad.
Always add a condition. Conditions are checked before the script runs. Without one, the script runs on every single insert or update on the table.
Don't call current dot update in a business rule. It triggers the business rules again and can create a loop. ServiceNow stops a recursive rule and logs an error, but by then you've lost performance. In a before rule, just set the value. It's saved automatically.
If the user doesn't need the result right away, use async instead of after. The user gets control back faster, and the work happens in the background.
Keep your code inside the function wrapper that advanced business rules give you, so your variables don't leak into other scripts. And put reusable logic in a script include, not a global business rule, which loads on every page.

## Debugging
Chapter four. Debugging. Finding a bug fast matters as much as not writing one.
gs dot log and gs dot print don't work in scoped apps. Use gs dot info, or gs dot debug. They work in both scoped and global.
Wrap debug messages in a system property check. Then you can turn logging on or off without changing code, and without affecting other users.
Type debug in the navigator to see every debug module. Debug business rule shows which rules started, finished, or were skipped. Debug security rules shows how ACLs evaluate on each field. And stop debugging turns it all off.
On the client side, turn on the JavaScript log and field watcher, and use jslog in your scripts. Check the browser console too. It shows errors that appear nowhere else. And before production, remove leftover alerts and log statements.

## Logs & queues
Chapter five. Logs and queues. Your instance tells you what's wrong, if you know where to look.
Check System Logs, System Log, All, regularly during development. Every error should be fixed, or documented as a known issue.
Download the node log files and search for these messages: slow evaluate, slow business rule, recursive business rule, compiler exception, and extremely large result. Each one points to a script or query worth fixing. A log file that suddenly grows is a warning too.
Open Slow Queries in System Diagnostics. Sort by total execution time, and use the example column to find the script behind each slow query.
In the event log, sort by processing duration to find slow events, and group by name to find noisy ones. An event that nothing responds to is just noise. Consider disabling whatever logs it.

## Update sets & XML
Chapter six. Update sets and XML. Code that works in dev only matters if it arrives safely in production.
Keep a migration document. List the order to apply update sets, plus the plugins to activate, system properties to set, and servers to configure.
Some data isn't captured in update sets, like approval lookup records. Move it as XML, and note that in the update set description, so whoever installs it knows.
Importing XML doesn't run business rules, and doesn't update the instance cache. Plan for anything those rules would normally do.
An XML export contains only that record. Export a user, and their group memberships and roles don't come with it. Export those separately.

## Recap & wrap-up
To recap: readable, reusable server code; let the database do the work. Keep client scripts light. Business rules need conditions, and no current.update(). Debug with properties, not leftovers. Read your logs. Document every migration.
If this helped, subscribe, and check the Shorts playlist for a quick refresher on each chapter. See you in the next one.
