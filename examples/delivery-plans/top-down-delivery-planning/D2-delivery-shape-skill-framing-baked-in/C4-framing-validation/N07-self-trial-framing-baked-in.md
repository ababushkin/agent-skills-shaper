---
layer: node
id: N07
type: experiment
title: Self-trial against 2 already-shaped initiatives
parent: C4
serves_kr: KR2
maps_to: linear-issue
external_window: none
completion:
  form: hypothesis+success-metric
  hypothesis: >
    delivery-shape, fed only an initiative's goal + KRs as text, emits a plan that
    carries acceptance criteria on every story node and at least one foundational /
    walking-skeleton task — at zero framing re-prompts.
  success_metric: >
    2 / 2 trial initiatives pass bin/check-plan-framing (AC on every story + ≥1
    skeleton task) at 0 re-prompts. < 2/2, or any re-prompt, falsifies the bet.
delegates_to: product-spike (experiment discipline — hypothesis, success metric, written finding)
---

# N07 — Self-trial against 2 already-shaped initiatives

**Type:** `experiment`. Not a build node: its completion criterion is a **hypothesis plus a
success metric**, and its honest outcomes are *confirmed* or *falsified*, not *shipped*. This is
the node that grades the bet (KR2) — it can fail, and a falsified result re-shapes D2 rather than
extending it.

## Hypothesis

See front-matter `completion.hypothesis`: the framing is genuinely baked in, not re-prompted.

## Success metric

2/2 trial plans under `examples/delivery-plans/_trials/` pass `bin/check-plan-framing` at 0
framing re-prompts. The trial note records the re-prompt count per trial.

## Tasks

- [ ] `skeleton` — Run delivery-shape against one already-shaped initiative; record AC-coverage, foundational-task presence, and re-prompt count in a trial note.
- [ ] Repeat against a second initiative; evaluate against the 2/2-at-0-re-prompts success metric; write the finding (confirmed / falsified).
