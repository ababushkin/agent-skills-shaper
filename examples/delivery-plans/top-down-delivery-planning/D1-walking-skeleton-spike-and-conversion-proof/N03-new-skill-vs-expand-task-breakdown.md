---
layer: node
id: N03
type: adr
title: New skill vs expand planning-and-task-breakdown
parent: D1
serves_kr: KR1
maps_to: linear-issue
tracker_ref: ABA-282
external_window: none
completion:
  form: decision-record
  criterion: >
    An accepted ADR exists recording Context / Decision / Consequences for choosing
    (A) a new delivery-shape skill or (B) an expansion of planning-and-task-breakdown.
delegates_to: documentation-and-adrs (ADR authoring + supersession discipline)
status: proposed
---

# N03 — ADR: new skill vs expand planning-and-task-breakdown

**Type:** `adr`. An architecturally significant decision (it determines whether the pack grows a
new skill directory or extends an existing skill's territory). Its completion criterion is the
**accepted decision record itself** — Context / Decision / Consequences — not an acceptance test.
Authoring and supersession are delegated to `documentation-and-adrs`.

> This node decides the **form of deliverable D2**. D2 cannot start until this ADR is accepted —
> see the dependency note in [D2's `_deliverable.md`](../D2-delivery-shape-skill-framing-baked-in/_deliverable.md).

## Context (to be completed at the gate)

How much unique structure did the upper layers — the deliverable, and the capability grouping
(now a node *type* rather than a structural layer) — actually carry in the worked example? Signal
toward **B (expand)** if every good name for a new skill crowds
`planning-and-task-breakdown`'s territory; signal toward **A (new skill)** if the
initiative-decomposition + framing + delegation logic is large enough to stand alone.

## Decision

`proposed` — recorded at the ABA-282 gate, informed by N01 (structure carried) and N02 (whether
the seam needed a real schema/tool rather than files).

## Consequences

To be filled when the decision is accepted: directory/skill layout, the `using-this-pack`
flowchart edit, and which downstream nodes in D2 change shape.

## Tasks

- [ ] Record Context: quantify the unique structure the upper layers carried in the N01 example.
- [ ] Record the Decision (A or B) with Consequences; set `status: accepted`.
