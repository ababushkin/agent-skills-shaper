---
layer: deliverable
id: D3
title: Full cycle drains on the pointer prompt
parent: ..
serves_kr: KR1
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR1 holds — ≥1 full cycle drains to completion with the pointer-only worker prompt
    at the execution initiative's quality bar (no manual fix commits), measured over
    the first 2 cycles after the re-scope lands. Observed by N05's experiment finding.
---

# D3 — Full cycle drains on the pointer prompt

**Serves:** KR1 *(bet)* — "a full cycle drains to completion with the worker prompt reduced to
issue context + a single skill pointer (zero inlined workflow steps), at the execution
initiative's quality bar (no manual fix commits)."

This deliverable is the initiative's bet, and only live cycles can grade it: the template can be
≤15 lines (D1 done), the verdicts can be wired (D2 done), and a full cycle can still fail to
drain — the workflow-prose handoff between supervisor and pack is exactly the seam a dry run
can't exercise. **N05** (experiment, `acceptance: true`) runs the first 2 cycles after the
re-scope lands, grades KR1 alongside the KR2 schema check, and watches the kill condition
(3 consecutive halted drains the inlined prompt would have completed → restore the inlined
tail). No Rule A1 trigger: one experiment node, no design decision.

## Nodes

- [N05 — Validation: 2 cycles on the pointer prompt](N05-validation-cycle-drains.md) · `experiment` · `acceptance`

## Done when

KR1 is observed: N05's finding is **confirmed** — ≥1 of the first 2 post-re-scope cycles drains
to completion with zero manual fix commits and the pointer-only template diff in evidence. The
acceptance node closes last, so this milestone reaching 100% coincides with the KR observation.
