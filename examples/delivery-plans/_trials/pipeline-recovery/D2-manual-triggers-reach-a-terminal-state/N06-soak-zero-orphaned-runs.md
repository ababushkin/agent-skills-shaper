---
layer: node
id: N06
type: story
title: Soak — zero orphaned runs over the window
parent: D2
serves_kr: KR2
maps_to: linear-issue
acceptance: true
external_window: 30-day post-deploy soak (KR2 measurement window)
completion:
  form: acceptance-criteria
  verifies_parent: D2
delegates_to: planning-and-task-breakdown (per-node task breakdown)
---

# N06 — Soak: zero orphaned runs over the window

> **As** the Nestl operator, **I want** the production Pipeline Runs table to show zero orphaned
> `"running"` rows across all three job categories over the soak window, **so that** the prevention
> guarantee is proven in real operation, not just in tests.

> **▶ On pickup — before coding:** expand this node via `planning-and-task-breakdown`.
> **Blocked by:** N04, N05 (all three categories must carry the guarantee before the soak begins).

This is the **acceptance node** for D2 (`acceptance: true`, `verifies_parent: D2`). It does **not**
re-run the per-category proofs in N04/N05 — those verify each category in controlled conditions.
N06 verifies the *aggregate production behaviour over the window* that no single child owns
(interactions, scheduler, sleep/wake). It closes last, so D2 reaching 100% coincides with KR2 being
observed.

## Acceptance criteria

- **Done when:** across the 30-day post-deploy soak window, the admin Pipeline Runs table shows
  zero `"running"` rows older than the longest expected job duration, for all three categories.
- **Done when:** any orphaned row that does appear is captured with its category and cause, feeding
  the kill condition (orphans persisting after one remediation cycle ⇒ cancel).

## Tasks

- [ ] `skeleton` — stand up the soak observation end-to-end: a query/dashboard view that reports the oldest `"running"` row age per category, run against live data (the view is folded into this slice, no separate setup).
- [ ] `acceptance` — over the soak window, confirm zero `"running"` rows exceed the longest expected job duration across all three categories; record the verdict against KR2.
