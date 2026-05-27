---
layer: node
id: N06
type: experiment
title: Rubric reproducibility + discrimination eval
parent: D3
serves_kr: KR3
maps_to: linear-issue
external_window: none
completion:
  form: hypothesis+success-metric
  criterion: >
    Two independent applications agree on (tier, flag) for the worked example and
    ≥4 of 5 held-out tasks, and ≥2 distinct tiers appear; otherwise falsified.
delegates_to: product-spike (experiment discipline — hypothesis, success metric, written finding)
---

# N06 — Rubric reproducibility + discrimination eval

**Type:** `experiment`. Not a build node: its completion is a **hypothesis + success metric**, and
its honest outcomes are *confirmed* or *falsified*. `delivery-shape` does not re-author the
experiment protocol here — that discipline lives in `product-spike`.

> **▶ On pickup:** run this as an experiment under `product-spike` — hypothesis, success metric,
> written finding. It is **not** built as a task list, so `planning-and-task-breakdown` does not
> apply.

## Hypothesis

The 5-axis rubric is reproducible (two independent applications produce the same (tier, flag)) and
discriminating (it assigns more than one tier across a realistic task sample).

## Success metric

Across the worked example + 5 held-out tasks, two independent applications agree on (tier, flag)
for the worked example and ≥4/5 held-out tasks, and ≥2 distinct tiers appear. Below either bar
falsifies — the rubric is non-reproducible or non-discriminating, triggering the initiative's kill
condition.

## Tasks

- [ ] `skeleton` — apply the rubric once to the worked example + 5 held-out tasks and record the (tier, flag) per task (the rubric in `references/task-sizing.md` and the held-out sample are the only inputs, folded in).
- [ ] Re-apply the rubric independently, diff the two (tier, flag) outputs, confirm ≥2 distinct tiers and the agreement threshold, then write the finding (confirmed / falsified).
