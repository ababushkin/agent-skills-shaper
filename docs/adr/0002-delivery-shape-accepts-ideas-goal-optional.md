# ADR 0002 — `delivery-shape` accepts ideas; the goal/KR link is optional

- **Status:** Accepted
- **Date:** 2026-06-03
- **Amends:** ADR 0001 (`delivery-shape`: a new skill, not an expansion). The "separate skill that delegates the per-node breakdown down" decision **stands**; this ADR changes only `delivery-shape`'s *input clause*.
- **Decision driver:** the shaping-pipeline reconciliation (`docs/designs/shaping-pipeline.md`).

## Context

ADR 0001 drew `delivery-shape`'s boundary around a **committed initiative** (goal + key results), with `serves_kr` as "the outcome spine at every layer." In practice the owner most often arrives with a raw idea — single or in bulk — and no committed initiative, and wants consistent, right-sized, review-friendly tickets regardless. Forcing every idea through `initiative-shape` first, purely to satisfy `delivery-shape`'s input gate, is friction that produces re-prompting and hand-finishing.

Separately, the audience split (`docs/designs/shaping-pipeline.md`) settled that `delivery-shape` is the **product-facing** shaper a human reviews, and the renamed `execution-breakdown` is the **agent-facing** breakdown that runs at pickup. That split makes `delivery-shape`'s job "produce reviewable tickets," not "decompose a committed bet" — which is what motivates loosening the input.

## Decision

`delivery-shape` accepts **a single idea or a bulk set of ideas**, and the **goal/KR link is optional**:

- **With a goal** — tickets group under deliverables that each trace to a KR (ADR 0001's outcome spine, unchanged).
- **Without a goal** — tickets stand alone: no deliverable grouping layer, no `serves_kr` trace. The manifest still derives (milestones = 0; issues and sub-issues as before).

Unchanged from ADR 0001: `delivery-shape` is a standalone skill; it owns node-type selection, the Rule A1 design-doc branch, and the walkable file-set contract; it delegates the per-node breakdown **down** to `execution-breakdown` at pickup. The five-section node body (What / Why / Completion / Assumptions / Key Risks) is **kept**, softened to product language — so `bin/check-plan-framing` is unchanged.

## Consequences

**Positive**
- One shaper serves the everyday case (raw ideas) and the goal-directed case, with the same ticket format and review experience.
- `serves_kr` becomes a property of *goal-linked* tickets rather than a universal requirement, matching how the owner actually works.

**Negative / costs**
- `bin/walk-delivery-plan` currently exits 2 when `serves_kr` is absent; it must make the tag conditional and handle the goal-less manifest. This is the main engineering surface.
- `delivery-shape/SKILL.md` Step 2 (hard-stop without an initiative) and Step 3 (every deliverable serves exactly one KR) must become conditional on a goal being present.
- The contract (`docs/delivery-shape-contract.md`) must reframe its `serves_kr` clauses as optional.

## Scope

This ADR records the decision. The implementation (script + skill + contract changes, plus a goal-less example) is shaped as its own initiative with `docs/designs/shaping-pipeline.md` as the brief; three of its four open items (size gate, no-goal grouping detail, drain-cycle handoff signal) remain to confirm there, and the `drain-cycle` contract — not defined in this pack — must be located or defined as part of it.
