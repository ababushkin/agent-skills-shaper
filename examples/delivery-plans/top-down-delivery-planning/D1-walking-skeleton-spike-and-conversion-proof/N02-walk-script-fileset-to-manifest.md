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
delegates_to: at-pickup task breakdown (task breakdown + walking-skeleton-first sequencing)
---

# N02 — Walk-script: file-set → tracker manifest

**Type:** `story`.

> **▶ On pickup — before coding:** break this node into task-sized pieces using your build agent's at-pickup task breakdown phase.

## What

As an adapter author wiring delivery plans into a tracker, I want a script that walks the
markdown file-set and emits a tracker manifest, so that the seam to Linear (milestones /
issues / sub-issues) is mechanical and I never hand-transcribe the hierarchy.

## Why

A hand-transcribed manifest drifts from the file-set within one sprint. A mechanically-derived
manifest is always current and gives the kill-condition proof that the standalone-markdown premise
holds end-to-end — every layer (deliverable → node → task) reads out by structure alone, not by
human copying. This is the second half of KR1.

## Completion

- **Done when:** `bin/walk-delivery-plan examples/delivery-plans/top-down-delivery-planning/`
  prints `3 milestones / 9 issues / 19 sub-issues` — all equal to the hand-count manifest in the
  example [README](../README.md#hand-count-manifest) — and exits 0.
- **Done when:** each emitted issue carries its node `type`, its `serves_kr` link, and its
  completion criterion, read from front-matter — verified against N01–N09.

Delivered: [`bin/walk-delivery-plan`](../../../../bin/walk-delivery-plan) (Python 3, stdlib only).

## Assumptions

- Front-matter scalar-key parsing (no YAML library) is sufficient for the contract's keys. *(verified — stdlib reader passes on all 9 nodes)*
- Node count is 9; task count is 19 — consistent with the README oracle. *(verified — walk-script confirms)*

## Key Risks

- **Risk:** The README hand-count oracle drifts from the actual file-set as nodes are added or
  removed.
  *Mitigation:* `bin/walk-delivery-plan` exits 1 on any mismatch; the oracle is the gate, not
  a doc. Any drift is caught immediately.

## Tasks

- [x] `skeleton` — Walk-script that descends the directory tree, reads each file's front-matter, and prints deliverable / node / task counts. *(Toolchain choice — language and front-matter parser — folded in here, not a silent pre-task.)*
- [x] Emit a tracker manifest (milestones ← deliverables, issues ← nodes, sub-issues ← tasks) from the parsed front-matter.
- [x] Mechanical-conversion proof: assert the emitted counts equal the README hand-count and that the script exits non-zero on any unparseable node.
