---
layer: node
id: N04
type: story
title: Decompose initiative → deliverables → nodes → tasks, AC by default
parent: D2
serves_kr: KR2
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
delegates_to: at-pickup task breakdown (per-node task breakdown)
---

# N04 — Decompose initiative → deliverables → nodes → tasks, AC by default

**Type:** `story`.

> **▶ On pickup — before coding:** break this node into task-sized pieces using your build agent's at-pickup task breakdown phase.

## What

As an agent invoking delivery-shape on a committed initiative, I want the skill to decompose
goal + KRs into deliverables → nodes → tasks with every `story` node carrying acceptance
criteria emitted **by default**, so that I stop getting low-level task lists that are missing
the "how do I know this is done?" check.

## Why

A story without acceptance criteria produces a spec gap that appears only at review — by then
the wrong thing may already be built. Mechanical enforcement (check-plan-framing) closes the
gap at plan time, not at code-review time. Without this gate, framing is optional; with it,
framing is the default.

Rejected alternative: deferring AC to per-node pickup (add them when you start coding). Rejected
because AC written before the node is picked up is a spec that constrains the build; AC written
after describes what got built.

## Completion

- **Done when:** given a fed initiative (goal + KRs as text), the skill emits a file-set whose
  every `story` node carries a Completion block with at least one `Done when:` condition —
  checked by `bin/check-plan-framing`.
- **Done when:** every deliverable carries a `serves_kr` tag and every node carries a `type` tag,
  so the hierarchy is walkable (N02's script succeeds on the emitted plan).

## Assumptions

- `bin/check-plan-framing` enforcing the gate mechanically is sufficient — a review step is not needed. *(verified — heuristic gate passes on the 9-node worked example)*
- Acceptance criteria (Done when conditions) are the right completion form for story nodes, not user-journeys or test scripts. *(verified — Cohn form + Done when is the grounded convention)*

## Key Risks

- **Risk:** The gate is bypassed — the plan is declared done without running check-plan-framing.
  *Mitigation:* Workflow step 10 is a [GATE] that requires both bin/walk-delivery-plan and
  bin/check-plan-framing to exit 0 before the plan is emitted.

## Tasks

- [ ] `skeleton` — Decompose one fed initiative end-to-end into the three layers on the thinnest path (one deliverable, one story node with AC) so the full pipeline runs before breadth is added.
- [ ] Emit acceptance criteria by default on every story node; fail loudly if a story has none.
