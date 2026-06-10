---
layer: node
id: N04
type: design-doc
title: Execution-workflow design doc (before build)
parent: D2
serves_kr: KR1
maps_to: linear-issue
external_window: none
completion:
  form: the-design-doc
  criterion: >
    An accepted design doc covering the execution verb namespace, the skill graph
    with its inter-skill handoff contract, headless-first and vendor-portability
    constraints, and persona-dispatch integration.
delegates_to: design-doc (Rule A1 design doc — produced before the build nodes are picked up)
---

# N04 — Execution-workflow design doc (before build)

**Type:** `design-doc`. D2 met two Rule A1 triggers (>~5 nodes; one-way-door namespace), so the
design doc comes first.

> **▶ On pickup — before any build node here:** produce the design doc via the `design-doc`
> skill and accept it through the `plan-review` exit gate. Build nodes **N05–N08 are blocked by
> this node**: their task breakdown waits until this doc is accepted.

## What

The design doc for the execution workflow: the verb namespace (the one-way door — `ship:*` or
whatever wins), the skill graph (pickup → breakdown-at-pickup → build → debug/simplify → review
fan-out → verify → PR finishing), the inter-skill handoff contract — what each step receives and
emits, including how the issue's acceptance criteria travel to the spec-compliance review lens —
plus headless-first / vendor-portability constraints and how persona dispatch (per N02)
integrates. `delivery-shape` does not restate the design-doc structure here — that discipline
lives in the `design-doc` skill.

## Why

The bet: one accepted design decides the namespace and the seams once, so five skills are
authored against a stable contract instead of five locally-sensible interfaces. Rejected
alternative: let each skill define its own interface ad hoc and reconcile later — guarantees
incompatible handoffs, and a namespace chosen by accident becomes permanent the moment drain-cycle
prompts bind to it. Unblocks N05–N08 and gives initiative B a single naming table to consume.

## Completion

An accepted design doc covering: the verb namespace with rationale and rejected alternatives; the
skill graph and its handoff contract; the headless-first and non-Claude-worker constraints; and
persona-dispatch integration. Accepted through the `plan-review` gate.

## Assumptions

- Shaping verbs stay `shape:*`; only the execution verb is open. *(verified — confirmed in the parked initiative shape; not re-litigated here)*
- drain-cycle's verify-flow expectations (`/shape:task`, `/shape:verify-implementation`, `/shape:pr-prepare`, `/shape:pr-respond`) can be satisfied or migrated by the new graph. *(to-verify — audit drain_cycle/prompt.py and the verify flow at pickup, before the namespace is pinned)*

## Key Risks

- **Risk:** the verb chosen now collides with initiative B's four-front-door consolidation
  naming, forcing a rename after habits form.
  *Mitigation:* the design doc reserves both verb sets (shaping + execution) in one naming table;
  B consumes that table — the naming decision is made once, here.

## Tasks

- [ ] Frame the problem and constraints and draft ≥2 alternatives for the verb namespace and skill graph · Done when: the doc presents the alternatives with trade-offs against headless-first and vendor portability · Model: Frontier · risk one-way · review elevated · axes RC·SC·HS·SR·OR = H·H·L·H·L · companions code-review-and-quality
- [ ] Record the decision and the inter-skill handoff contract and pass the plan-review exit gate · Done when: the design doc is accepted and N05–N08 can break tasks against it · Model: Frontier · risk one-way · review elevated · axes RC·SC·HS·SR·OR = H·H·L·H·L · companions code-review-and-quality
