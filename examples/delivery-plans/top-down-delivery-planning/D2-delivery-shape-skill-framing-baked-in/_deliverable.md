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
deliverable → capability → story → task hierarchy with the framing baked in (so the user never
re-prompts it) and foundational/toolchain work never silently dropped. The skill **delegates**
up to `initiative-shape` (goal + KRs) and down to `planning-and-task-breakdown` (tasks per
capability) rather than re-authoring their gates.

> The form this deliverable takes — a new skill **or** an expansion of
> `planning-and-task-breakdown` — is decided by the ADR in
> [C2 / N03](../D1-walking-skeleton-spike-and-conversion-proof/C2-mechanical-conversion-and-architecture-decision/N03-new-skill-vs-expand-task-breakdown.md).
> D2 is gated on that decision.

## Capabilities

- [C3 — Decomposition with framing baked in](C3-decomposition-with-framing-baked-in/_capability.md)
- [C4 — Framing validation](C4-framing-validation/_capability.md)

## Done when

KR2 is observed: 2/2 trial plans under `examples/delivery-plans/_trials/` carry an
Acceptance-criteria block on every story node and at least one `skeleton`-flagged foundational
task, produced at 0 framing re-prompts, confirmed by `bin/check-plan-framing <plan>`.
