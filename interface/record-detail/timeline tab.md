---
title: Timeline Tab
---

Data doesn't exist in a vacuum — it has a story. The Timeline tab tells that story visually. Every change to a record, from the moment it was created to its latest update, is plotted on a chronological timeline that you can explore, inspect, and compare.

## The Visual Timeline

The timeline displays a vertical sequence of events — most recent at the top. Each event shows:

- **When** it happened (date and time)
- **Who** made the change
- **What** changed (which fields were modified)
- **What type** of event (creation, update, correction)

<!-- 📸 SCREENSHOT: Timeline tab showing a vertical timeline with several change events -->

Events are color-coded by type:
- 🟢 **Create** — the record was first created
- 🔵 **Update** — one or more fields were modified
- 🟣 **Correction** — a past value was retroactively corrected (valid-time adjustment)

## Two Time Dimensions

This is where LEX APP's [[features/tracking/bitemporal history|bitemporal model]] comes to life. The timeline can show changes along two independent dimensions:

### System Time (When We Learned It)

This is the default view. It shows events in the order the system recorded them — the sequence of database writes. This is what happened from the system's perspective.

### Valid Time (When It Was True)

Switch to the **Effective Time** view to see when data was *actually valid* in the real world. A salary change recorded today but effective from January 1st would appear at January 1st in this view.

<!-- 📹 VIDEO: Switching between system-time and valid-time views on the same record, showing how events reposition -->

This distinction matters in industries where backdated corrections are common — finance, insurance, regulatory reporting. The timeline shows both "what we recorded" and "what was actually true."

## Inspecting a Version

Click any event on the timeline to open the **Version Details Drawer** — a slide-out panel showing the full state of the record at that point in time. You'll see:

- All field values at that moment
- Which specific fields changed compared to the previous version
- The author who made the change
- The exact system-time and valid-time timestamps

<!-- 📸 SCREENSHOT: Version details drawer open, showing field values with changed fields highlighted -->

This is invaluable for investigations: "Why does this number look wrong? When did it change? Who changed it?"

## Audit Feed

Below the timeline, the **Audit Feed** shows a chronological list of API operations that affected this record — create, update, delete events captured by the [[features/tracking/audit logs|audit log system]]. Each entry shows the author, timestamp, operation type, and status.

The timeline and audit feed are complementary: the timeline shows *what the data looked like*, the audit feed shows *what operations were performed*.

> [!tip]
> For full audit log details with payloads and error tracebacks, switch to the dedicated [[interface/record-detail/audit log tab|Audit Log tab]].
