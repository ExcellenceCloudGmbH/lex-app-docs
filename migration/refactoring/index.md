---
title: "Refactoring Guide"
---

This is a hands-on, step-by-step guide for migrating a V1 (`generic_app`) project to the current LEX framework. Work through it in order — each part builds on the previous one.

If you're starting a new project from scratch, skip this entirely and follow the [[tutorial/index|TeamBudget Tutorial]] instead.

## Before You Start

Make sure you have:

- A working V1 project that you want to migrate
- Access to the project's database
- `lex-app` installed (`pip install lex-app`)
- Familiarity with the V1 codebase (model files, `generic_app` imports)

> [!important]
> **Back up your database before starting.** The database migration pipeline (Part 6) modifies your schema. Always have a restore point.

## The Series

1. [[migration/refactoring/Part 1 — Project Structure & Imports|Part 1 — Project Structure & Imports]] — flatten your project layout and update all imports from `generic_app` to `lex.*`
2. [[migration/refactoring/Part 2 — Models & Fields|Part 2 — Models & Fields]] — convert your model base classes and clean up legacy fields
3. [[migration/refactoring/Part 3 — Calculations|Part 3 — Calculations]] — migrate `ConditionalUpdateMixin` to `CalculationModel`
4. [[migration/refactoring/Part 4 — Lifecycle Hooks|Part 4 — Lifecycle Hooks]] — replace `UploadModelMixin` with explicit `@hook` decorators
5. [[migration/refactoring/Part 5 — Logging & Permissions|Part 5 — Logging & Permissions]] — upgrade `CalculationLog` to `LexLogger` and `ModificationRestriction` to `permission_*` methods
6. [[migration/refactoring/Part 6 — Database Migration & Go-Live|Part 6 — Database Migration & Go-Live]] — run the automated migration pipeline and verify everything works

## How Long Does It Take?

| Project Size | Estimated Time |
|---|---|
| Small (< 10 models) | 1–2 days |
| Medium (10–30 models) | 3–5 days |
| Large (30+ models) | 1–2 weeks |

Most of the time is spent in Parts 1–5 (code refactoring). Part 6 (database migration) is largely automated.

## Quick Reference

Keep these open while you work:

- [[reference/V1 to V2 Import Map]] — complete import replacement table
- [[migration/import migration]] — systematic import update walkthrough
- [[migration/invocation modes]] — CLI flags for the migration pipeline
- [[migration/verification checklist]] — post-migration health checks
