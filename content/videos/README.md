# Video Snippets — Recording Checklist

Each video is 30–60 seconds, screen-captured as mp4, and placed in `docs/videos/`.
Collapsed by default in the docs via `> [!example]- 🎬 Video — ...` callouts.

---

## The Grid

| # | Filename | Duration | Doc page | What to record |
|---|----------|----------|----------|----------------|
| 1 | `grid-inline-editing.mp4` | ~30s | `interface/the-grid/index.md` | Double-click a cell → type an invalid value → see validation error → correct it → save |
| 2 | `grid-column-filter.mp4` | ~30s | `interface/the-grid/filtering and sorting.md` | Click filter icon on Amount column → type a value → grid filters instantly |
| 3 | `grid-multi-filter.mp4` | ~45s | `interface/the-grid/filtering and sorting.md` | Apply date range → add category filter → sort by amount descending → show row count in status bar |
| 4 | `grid-drag-to-group.mp4` | ~30s | `interface/the-grid/grouping and pivoting.md` | Drag "team" column header to the group bar → groups expand/collapse → show aggregate totals |
| 5 | `grid-pivot-mode.mp4` | ~45s | `interface/the-grid/grouping and pivoting.md` | Enable pivot mode → drag Quarter to pivot area → grid transforms to cross-tabulation with totals |
| 6 | `grid-create-saved-view.mp4` | ~30s | `interface/the-grid/saved views.md` | Set up filters/grouping → type "Q1 Travel Expenses" in view selector → press Enter → preset appears |
| 7 | `grid-export.mp4` | ~30s | `interface/the-grid/exporting data.md` | Set up a grouped, filtered view → click Export → show the downloaded Excel file |

## Record Detail

| # | Filename | Duration | Doc page | What to record |
|---|----------|----------|----------|----------------|
| 8 | `record-column-toggle.mp4` | ~20s | `interface/record-detail/summary tab.md` | Click 1 → 2 → 3 column toggle in toolbar, see layout reflow |
| 9 | `record-analytics-tab.mp4` | ~30s | `interface/record-detail/analytics tab.md` | Click a record in grid → open Analytics tab → Streamlit dashboard loads with charts/metrics |
| 10 | `record-history-as-of.mp4` | ~30s | `interface/record-detail/history tab.md` | Click As-Of button → pick a past date → history grid filters to show versions at that time → click Reset to Latest |

## Setup notes

- **Resolution:** 1920×1080 or 1280×720 (consistent across all videos)
- **Format:** mp4 (H.264, web-friendly)
- **Audio:** None (silent screen captures — the docs provide the narration)
- **Cursor:** Use a visible cursor highlight if possible (e.g., yellow circle)
- **Data:** Use the TeamBudget project with sample data loaded (teams, employees, expenses, calculated budget summaries)
- **Browser:** Clean browser, no bookmarks bar, no extensions visible
- **Theme:** Light mode (default) for consistency

## Embedding format (already wired into docs)

```markdown
> [!example]- 🎬 Video — Description
> <video controls width="100%">
>   <source src="../../videos/filename.mp4" type="video/mp4">
> </video>
> Brief caption describing what happens in the video.
```

Works in both Obsidian (native callout, collapsed by default) and Quartz 4 (ObsidianFlavoredMarkdown plugin).
