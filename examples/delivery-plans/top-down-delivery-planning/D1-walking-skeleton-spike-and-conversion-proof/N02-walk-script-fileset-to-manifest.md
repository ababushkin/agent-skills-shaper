---
layer: node
id: N02
type: story
title: Walk-script — file-set → tracker manifest
parent: D1
serves_kr: KR1
maps_to: linear-issue
tracker_ref: ABA-282
external_window: none
completion:
  form: acceptance-criteria
delegates_to: planning-and-task-breakdown (task breakdown + walking-skeleton-first sequencing)
---

# N02 — Walk-script: file-set → tracker manifest

**Type:** `story` (Cohn form).

> **As** an adapter author wiring delivery plans into a tracker,
> **I want** a script that walks the markdown file-set and emits a tracker manifest,
> **so that** the seam to Linear (milestones / issues / sub-issues) is mechanical and I never
> hand-transcribe the hierarchy.

A `story` node's completion criterion is its **acceptance criteria** — observable behaviour, not
"the script is written."

## Acceptance criteria

- **Done when:** `bin/walk-delivery-plan examples/delivery-plans/top-down-delivery-planning/`
  prints `3 milestones / 9 issues / 19 sub-issues` — all equal to the hand-count manifest in the
  example [README](../README.md#hand-count-manifest) — and exits 0.
- **Done when:** each emitted issue carries its node `type`, its `serves_kr` link, and its
  completion criterion, read from front-matter — verified against N01–N09.

Delivered: [`bin/walk-delivery-plan`](../../../../bin/walk-delivery-plan) (Python 3, stdlib only).

## Tasks

- [x] `skeleton` — Walk-script that descends the directory tree, reads each file's front-matter, and prints deliverable / node / task counts. *(Toolchain choice — language and front-matter parser — folded in here, not a silent pre-task.)*
- [x] Emit a tracker manifest (milestones ← deliverables, issues ← nodes, sub-issues ← tasks) from the parsed front-matter.
- [x] Mechanical-conversion proof: assert the emitted counts equal the README hand-count and that the script exits non-zero on any unparseable node.
