---
title: Filtering & Sorting
aliases:
  - "interface/the-grid/filtering and sorting"
---

Finding the right data shouldn't require a database query. Lex App's grid lets you filter and sort visually — tick, type, click — and the table refreshes as soon as you apply a filter.

## Column Filters

Every column header has a built-in filter. Click the menu icon on any column to open its filter panel. The filter type adapts to the data:

| Column Type | Filter Style | Example |
|---|---|---|
| **Text** | A [value list](#value-lists), plus contains, begins with, equals, does not equal, blank, not blank | Tick *North* and *South* in a region column |
| **Long text** | Contains, begins with, equals, does not equal, blank, not blank | Find invoices whose notes *contain* "reminder" |
| **Whole number** | A value list, plus equals, greater than, less than, between, blank, not blank | Tick the years *2025* and *2026* |
| **Decimal number** | Equals, greater than, less than, between, blank, not blank | Find amounts *greater than* 5,000 |
| **Date** | A value list, plus before, after, between, exact date, blank, not blank | Invoices dated *after* January 1, 2026 |
| **Date and time** | Before, after, between, exact date, blank, not blank | Orders placed *between* two dates |
| **Yes / No** | A value list: Yes, No, (Blank) | Show only *paid* invoices |
| **Choice** | A value list of the choices the column holds | Tick *Open* and *Overdue* |
| **Foreign Key** | A value list of the related records, by name | Filter by two or three customers |

![The grid with a filter in force — five funds narrowed to one](images/the-grid/filter-applied.svg)

A value list applies as you tick: each value you tick or untick refreshes the table at once, and the list stays open for the next one. **Reset** unticks them all. A condition waits for **Apply**: type it, then click **Apply** (or press Enter) and the table refreshes — nothing reloads while you're still typing. **Reset** clears it. The date-and-time filter needs no Apply either: it applies as soon as you pick a date, and has its own **Clear Filter** button.

The **Filters** tab on the grid's right edge holds the same filters, column by column, so you can set several without opening each column's menu.

### Text Filters

For text columns, type in the filter input and apply. The condition dropdown chooses how the text has to match:

- **Contains** — the default; matches anywhere in the text
- **Begins with** — useful for codes or identifiers
- **Equals** — exact match only
- **Does not equal** — exclude specific values
- **Blank / Not blank** — find missing data

### Date Filters

Date columns use a calendar picker for precision. Select a range with "between" to isolate a specific period — like all invoices from Q1 2026. When you enter a date without a time, Lex App treats it as the whole day rather than a single instant. The built-in date picker handles timezones automatically.


### Foreign Key Filters

When a column references another model (like an invoice's customer), its filter is a value list of the related records, shown by name. It lists the records the column actually refers to — not every record of that model — so tick one or more to narrow the view.

## Value Lists

Most columns list their own values, each with the number of rows that have it. Tick the values you want, and the table keeps the rows that have any of them.

- **Nothing ticked means no filter.** A list opens with nothing ticked, and there is no *Select All* button. Pressing **Enter** in the search box is the exception: it ticks every value the search currently shows, all at once.
- **Every value shows its row count**, so you can see how many invoices are *Overdue* before you tick it.
- **The lists narrow each other.** The counts follow every other filter in force: once a region is ticked, the customer list only offers that region's customers. A column's own filter never narrows its own list, so you can always tick one more value.
- **A ticked value stays.** If the other filters leave no rows with a value you ticked, it stays in the list with a count of 0, so you can still untick it.
- **Values appear by label.** Related records appear by name, choices by their label, yes/no columns as *Yes* and *No*, and dates as `YYYY-MM-DD`. Values are sorted by label — numbers in numeric order — with *(Blank)* last.
- **(Blank) is a value too.** It stands for rows with nothing in the column. On a text column, empty text counts as blank, so *(Blank)* finds both.
- **Up to 1,000 values.** A list shows at most 1,000 values, and its search box searches only those. To reach a value that isn't listed, narrow the other filters first — or, on text, whole-number and date columns, use the condition instead: it checks every row, not just the first 1,000.

The lists only count rows you're allowed to see, and never offer a value you couldn't see in the grid.

On text, whole-number and date columns the filter has two parts: the condition on top and the value list below. Use either or both — with both, a row has to match both. Each part has its own **Reset**, and only the condition waits for **Apply**.

### Which Columns Have a Value List

| Value list | Conditions only |
|---|---|
| Text, whole numbers, dates, yes/no, choices, foreign keys | Long text, decimal numbers, date and time, JSON, files, many-to-many, the ID column |

A few columns keep their conditions even though their type would get a list: a column the [[model-your-data/serializers#Value lists|serializer]] computes or reformats, for example. And a developer can turn value lists off for a whole table — the audit log has none.

### Saved Views Keep Working

Views saved before value lists existed still open as they did. When the view loads, its filters are converted to the column's new filter: a foreign-key or yes/no filter becomes a value list with that one value ticked, and a text, number or date condition carries on as the column's condition. A saved filter that can't be shown that way is dropped rather than half-applied.

## Multi-Column Sorting

Click any column header to sort by that column. Click again to reverse the order. A small arrow indicator shows the current sort direction.

For **multi-column sorting**, hold `Shift` and click additional columns. This creates a sort priority chain — for example, sort by Team first, then by Amount within each team.

| Sort Order | Column | Direction |
|---|---|---|
| 1st | Team | A → Z |
| 2nd | Amount | High → Low |
| 3rd | Date | Newest first |

The sort indicators show the priority number next to each sorted column header.

> [!tip]
> To clear all sorting, right-click any column header and select **Reset Columns** from the context menu.

## Combining Filters

Filters stack. Apply a date filter, then a category filter, then sort by amount — each filter narrows the dataset further. The grid shows the total visible row count in the status bar, so you always know how much data you're looking at.

This is especially powerful with [[using-the-app/the-grid/saved views|saved views]]: set up a complex filter combination once, save it, and switch to it instantly whenever you need it.

> [!example]- 🎬 Video — Building a multi-filter view
> <video controls width="100%">
>   <source src="../../videos/grid-multi-filter.mp4" type="video/mp4">
> </video>
> Build up a view step by step: apply a date range, then category filter, then sort by amount.
