---
title: Documentation Plan — September 2026
draft: true
---

# Documentation Plan — September 2026

> Internal working plan. Not part of the published site (`draft: true`).
> Companion to [[DOCS_AUDIT_2026-05|the May 2026 audit]], which this plan
> partly discharges. Where the two disagree, this file is newer: several
> audit items were fixed between May and September and are marked below as
> already done rather than repeated as work.

## Why this exists

Two things had accumulated:

1. **Fourteen unmerged release PRs.** One per release from `v2.0.0rc217`
   through `v2.2.0` — every one a Copilot draft, none reviewed, going back to
   1 July. The docs therefore describe roughly the `rc215` framework while
   customers run `v2.2.0`.
2. **The `v2.2.0` interface.** The redesign that shipped in `v2.1.3` and was
   withdrawn in `v2.1.4` is back, so every interface page describing the old
   design is now wrong — and the new Streamlit widget API has no page at all.

The approach is top-down: land the release backlog oldest-first so each page
reaches its current state through the same sequence the code did, then fill
the gaps the releases exposed, then discharge the audit, then verify.

## Ground rules

- **Verify every claim against the framework source**, not against the PR that
  proposes it. Four of the fourteen PRs contain claims that do not match the
  code (see the triage table).
- **One commit per release**, oldest first, following the precedent set by
  [PR #141](https://github.com/ExcellenceCloudGmbH/lex-app-docs/pull/141)
  (`rc181`–`rc215` consolidation). The Copilot drafts are then closed as
  superseded, not merged.
- **Two audiences, one page.** Feature and interface pages answer "what does
  this do and how do I use it"; `reference/` pages carry signatures, flags and
  defaults. Internals never leak into feature pages.
- **No API gets documented that does not exist.** See BUG-020 below for why
  this rule earns its place.

## Phase 0 — Recover what was already in flight ✅

- [x] Rebase the unmerged local `2.1.3` work onto `origin/main` (12 files;
      one real conflict in `logging.md`, resolved by keeping main's HTTP `202`
      detail *and* the branch's execution-tree and collapsible-section text).
- [x] Commit the drafted **logging / warning env vars** section
      (`LOG_LEVEL`, `LEX_LOG_LEVEL`, `LEX_SUPPRESS_INSECURE_WARNING`,
      `LEX_SUPPRESS_WARNINGS`) — all four verified against
      `lex_app/settings.py`, defaults included.
- [x] Evaluate two abandoned stashes. One was stale (it would have deleted
      main's threading and worker-recovery sections). The other was 95%
      already merged, and its only unique content documented
      **`suspend_bitemporal()` — a context manager that does not exist**.
      That is BUG-020 in the framework's own test suite: *"docs reference a
      `suspend_bitemporal()` CM that does not exist yet — only the lower-level
      guards are exposed today."* Discarded rather than recovered. The real
      API is three guards: `suppress_main_table_sync()`,
      `suppress_history_valid_to_chaining()`, `suppress_meta_sys_to_chaining()`.

## Phase 1 — Land the release backlog

One commit per release, oldest first. Verdicts are from reading each diff
against the framework source.

| PR | Release | Verdict | Action |
|---|---|---|---|
| #143 | `rc217` | | |
| #145 | `rc219` | | |
| #147 | `rc220` | **committed `node_modules/`** — 2.7M lines, 100 files, for 4 lines of real content | lift content by hand; never merge |
| #149 | `2.1.1` | | |
| #151 | `2.1.2` | | |
| #153 | `2.1.3` | overlaps the Phase 0 cherry-pick | reconcile |
| #155 | `2.1.4` | | |
| #157 | `2.1.5` | | |
| #159 | `2.1.6` | | |
| #161 | `2.1.7` | | |
| #163 | `2.1.8` | | |
| #165 | `2.1.9` | **`v2.1.9` no longer exists** — it never published to PyPI and its release and tag were deleted; the changes shipped in `2.1.10` | retarget to `2.1.10` |
| #167 | `2.1.11` | | |
| #169 | `2.2.0` | 4 verified errors: deep import path, wrong light background hex, wrong dark palette, broken wikilink | correct, then land |

## Phase 2 — Gaps the releases exposed

The `v2.2.0` interface work is larger than any single PR touched.

- [ ] **Table settings panel** — density, status bar, header wrapping, time in
      date columns, column filter button, row-index column, selection and
      calculation-status pinning. Per user, per table, no Save step.
- [ ] **Column formats** — number / currency / percentage, currency choice,
      decimals, the backend-declared default and *Reset to backend defaults*.
- [ ] **The Streamlit widget API** — a reference page for `lex_calculation`,
      `lex_calculation_log`, `lex_calculation_log_tree`, `lex_widgets()` and
      `lex_view`, with the canonical flat import and the `main()` contract.
- [ ] **Export from the toolbar** — the selection contract (nothing selected
      exports the view as shown; rows selected exports exactly those).
- [ ] **Cell range selection** and the status-bar aggregation.
- [ ] **Log-tree export scopes** — a step, or a step and everything under it.
- [ ] **Record page layout** — the record leads; audit fields collapse into
      *Record details*.
- [ ] **Create-in-a-drawer** — create and edit share one layout over the list.
- [ ] Correct guidance for **suppressing bitemporal writes** using the three
      guards that actually exist (replaces the BUG-020 phantom).

## Phase 3 — Discharge the May audit

Verify each item against the current tree first; several are already fixed.

- [x] `lex create_db` present in `reference/CLI Commands.md` (fixed since audit)
- [x] `lex start` flags documented (fixed since audit)
- [x] `reference/lex_config.md` exists (fixed since audit)
- [x] `reference/Environment Variables.md` exists (fixed since audit)
- [ ] `lex generate-configs` — audit says it does not exist; confirm and correct
- [ ] `streamlit_main` signature — one canonical form across all three pages
- [ ] Streamlit launch command — one canonical command site-wide
- [ ] `PROJECT_GROUPS` forward-reference in tutorial Part 2
- [ ] `permissions.md` helper/factory tables vs `LexModel Internals.md`
- [ ] Remaining Django management commands in the CLI reference
- [ ] `📸 TODO` / `SCREENSHOT` placeholders shipping in published pages
- [ ] `installation.md` vs tutorial Part 1 on `lex setup` artefacts

## Phase 4 — Hygiene

- [ ] Remove `content/PFE - Lund User Calculation Permissions.md` — customer-specific,
      no frontmatter, and it must not be in a public docs repo
- [ ] `ignorePatterns` for `quartz_style_docs`, `DOCS_AUDIT_*`, `DOCS_PLAN_*`
- [ ] Root-level duplicate tree (`features/`, `interface/`, `migration/`,
      `reference/`, `index.md`, …) — strays outside `content/`, delete
- [ ] Stray binaries under `content/images/record-detail/` (three customer PDFs
      and a `.py` file)
- [ ] Broken wikilinks, repo-wide check

## Phase 5 — Verify

- [ ] Every wikilink resolves to a real page or heading
- [ ] No page claims an API that is absent from the framework source
- [ ] Close the fourteen drafts as superseded, referencing the commit that
      replaced each
