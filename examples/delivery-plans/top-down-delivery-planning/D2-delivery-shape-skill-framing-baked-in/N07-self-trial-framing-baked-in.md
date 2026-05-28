---
layer: node
id: N07
type: experiment
title: Self-trial against 2 already-shaped initiatives
parent: D2
serves_kr: KR2
maps_to: linear-issue
acceptance: true
external_window: none
completion:
  form: hypothesis+success-metric
  verifies_parent: D2
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

> **▶ On pickup:** run the experiment and write the finding (confirmed / falsified) via
> `product-spike`.

## What

Run delivery-shape against 2 already-shaped initiatives (not edge cases — normal shaped
initiatives) and record whether the emitted plan carries AC on every story and ≥1 skeleton task
at zero framing re-prompts. Write the finding.

## Why

A skill that requires re-prompting to emit its framing is not doing its job. The self-trial is
the KR2 grader: it can falsify the bet. If it falsifies, D2's nodes need rework — not an
extension. A passing self-trial on 2 real initiatives is the minimum credible evidence that
framing is baked in, not re-prompted in.

This node carries `acceptance: true` because it verifies D2's aggregate done condition — whether
the KR2 bet is confirmed. Close it last: D2 reaching 100% coincides with the KR observation.

## Completion

**Hypothesis:** delivery-shape, fed only an initiative's goal + KRs, emits a plan with AC on
every story and ≥1 skeleton task — at zero framing re-prompts.

**Success metric:** 2/2 trial initiatives pass `bin/check-plan-framing` at 0 re-prompts.
Trials live under `examples/delivery-plans/_trials/` with a re-prompt count per trial.

< 2/2, or any re-prompt, **falsifies** the bet. D2 is re-shaped, not extended.

## Assumptions

- 2 trials is a sufficient first-pass sample for a stretch KR. *(verified — this is not a production gate; 2 trials confirms the hypothesis is testable and the framing is not accidental)*
- Already-shaped initiatives (not edge cases) are the right input for the framing trial. *(verified — if framing fails on normal inputs, it fails the bet; edge cases test robustness, not the core claim)*

## Key Risks

- **Risk:** The trial initiatives chosen are too simple and don't surface framing gaps, making
  the 2/2 result a false positive.
  *Falsifier:* if a more complex initiative (>5 nodes, multiple types) later requires re-prompting,
  the trial criteria were underspecified — the 2/2 is a first-pass gate, not a proof.

## Tasks

- [ ] `skeleton` — Run delivery-shape against one already-shaped initiative; record AC-coverage, foundational-task presence, and re-prompt count in a trial note.
- [ ] `acceptance` — Repeat against a second initiative; evaluate aggregate result against the 2/2-at-0-re-prompts success metric; write the finding (confirmed / falsified) — this finding is D2's Done condition.
