---
title: History Tab
---

The Timeline tab tells the story. The History tab gives you the raw data. It's a full AG Grid of every historical version of this record — sortable, filterable, and equipped with the **As-Of** time-travel control.

## The History Grid

every historical version of the current record is displayed as a row. Each row represents a snapshot of the record at a specific point in time, with all field values captured at that moment.

The columns are the same as the main grid — plus additional history-specific fields:

| Column | What It Shows |
|---|---|
| **history_date** | When this version was recorded (system time) |
| **history_type** | The type of change: Created (`+`), Changed (`~`), Deleted (`−`) |
| **history_user** | Who made the change |
| *All model fields* | The values at that point in time |

You can [[interface/the-grid/filtering and sorting|filter and sort]] this grid like any other — for example, filter by `history_user` to see all changes made by a specific person, or sort by `history_date` to trace the evolution of the record.

<!-- 📸 SCREENSHOT: History tab showing a grid of historical versions with history_date, history_type columns visible -->

## The As-Of Control

At the top of the History tab, the **As-Of** button lets you time-travel. Click it, pick a date and time, and the entire grid transforms to show data **as it existed at that moment**.

This answers questions like:
- "What did this record look like on March 1st?"
- "What values were in place at the end of last quarter?"
- "Was this field already updated before the audit?"

<!-- 📹 VIDEO: Clicking the As-Of button, picking a date from last month, seeing the grid update to show historical state -->

The As-Of control uses the [[features/tracking/bitemporal history|system time dimension]] — it shows you what the system believed to be true at the timestamp you selected. To see when a change was *actually effective* in the business sense, use the [[interface/record-detail/timeline tab|Timeline tab's]] effective-time view.

### Clearing the Time Travel

Click the **Reset to Latest** button to exit time-travel mode and return to the current live data. The button is always visible when an As-Of date is active, so you never get stuck in the past.

## Jumping to Live Data

When viewing a historical record, a **Go to Live Data** button appears. Click it to navigate directly to the current live version of this record — useful when you've found something interesting in the history and want to check today's state.

## How History Is Created

You don't need to do anything to create history — it's automatic. Every `LexModel` in LEX APP tracks its changes via [django-simple-history](https://django-simple-history.readthedocs.io/). Every save, update, or delete creates a new historical version with a complete snapshot of all field values.

This means:
- History cannot be tampered with — it's append-only
- No data is ever lost — even deleted records are preserved in history
- You can always answer "what did this look like on date X?"

> [!note]
> For developers: see [[features/tracking/bitemporal history]] for the backend implementation, including valid-time support and history querying.
