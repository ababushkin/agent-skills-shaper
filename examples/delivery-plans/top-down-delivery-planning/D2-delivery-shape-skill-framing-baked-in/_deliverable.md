---
layer: deliverable
id: D2
title: The delivery-shape skill, framing baked in
parent: ..
serves_kr: KR2
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR2 holds — on a self-trial against 2 already-shaped initiatives, the emitted
    plan carries acceptance criteria on every story and at least one explicit
    foundational / walking-skeleton task, at zero framing re-prompts.
---

# D2 — The delivery-shape skill, framing baked in

**Serves:** KR2 *(bet)* — "On a self-trial against 2 already-shaped initiatives, delivery-shape's
emitted plan carries acceptance criteria on every story and at least one explicit foundational /
walking-skeleton task, with zero framing re-prompts."

This deliverable is the actual bet: a skill that takes a committed initiative and emits the full
deliverable → node → task hierarchy with the framing baked in (so the user never
re-prompts it) and foundational/toolchain work never silently dropped. The skill **delegates**
up to `initiative-shape` (goal + KRs) and down to `planning-and-task-breakdown` (tasks per
node) rather than re-authoring their gates.

> The form this deliverable takes — a new skill **or** an expansion of
> `planning-and-task-breakdown` — is decided by the ADR in
> [N03](../D1-walking-skeleton-spike-and-conversion-proof/N03-new-skill-vs-expand-task-breakdown.md).
> D2 is gated on that decision.

Its four nodes split the bet: **N04–N06** (stories) build the decomposition with framing baked in
— acceptance criteria by default, foundational work folded into the skeleton, the Rule A1 branch
and up/down delegation; **N07** (experiment) grades the bet on a self-trial that can falsify it
rather than extend it.

## Nodes

- [N04 — Decompose initiative → deliverables → nodes → tasks, AC by default](N04-decompose-with-acceptance-criteria.md) · `story`
- [N05 — Foundational-work prompt folded into the walking skeleton](N05-foundational-prompt-folded-into-skeleton.md) · `story`
- [N06 — Rule A1 design-doc branch + up/down delegation](N06-rule-a1-branch-and-delegation.md) · `story`
- [N07 — Self-trial against 2 already-shaped initiatives](N07-self-trial-framing-baked-in.md) · `experiment`

## Done when

KR2 is observed: 2/2 trial plans under `examples/delivery-plans/_trials/` carry an
Acceptance-criteria block on every story node and at least one `skeleton`-flagged foundational
task, produced at 0 framing re-prompts, confirmed by `bin/check-plan-framing <plan>`.
