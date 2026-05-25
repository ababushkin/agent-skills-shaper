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
status: accepted
adr_ref: ../../../../docs/adr/0001-delivery-shape-new-skill-vs-expand-planning-and-task-breakdown.md
---

# N03 — ADR: new skill vs expand planning-and-task-breakdown

**Type:** `adr`. An architecturally significant decision (it determines whether the pack grows a
new skill directory or extends an existing skill's territory). Its completion criterion is the
**accepted decision record itself** — Context / Decision / Consequences — not an acceptance test.
Authoring and supersession are delegated to `documentation-and-adrs`.

> This node decides the **form of deliverable D2**. D2 cannot start until this ADR is accepted —
> see the dependency note in [D2's `_deliverable.md`](../D2-delivery-shape-skill-framing-baked-in/_deliverable.md).

## Decision

**Accepted: A — a standalone `delivery-shape` skill.** The full Context / Decision / Consequences
record lives in [`docs/adr/0001`](../../../../docs/adr/0001-delivery-shape-new-skill-vs-expand-planning-and-task-breakdown.md).

In brief, on the spike's evidence: the **upper layers carried little unique structure** (the
fourth `capability` layer collapsed entirely; the deliverable layer adds only milestone-grouping +
a `serves_kr` tag — the B-signal), but the **polymorphic node layer carries large unique
structure** (eight completion-forms with delegation targets, five exercised on real content) that
PTB has no concept of and that is too far from "task breakdown" to bolt on. DS *delegates* per-node
breakdown back down to PTB, so the two compose rather than merge; and the initiative's own KR3
("0 collisions against planning-and-task-breakdown") already presupposes two distinct skills.

## Consequences

Directory/skill layout: a new `skills/delivery-shape/`; PTB is unchanged and becomes DS's
delegation target. The `using-this-pack` flowchart gains a routing entry (node N09). D2's nodes
keep their shape — they build the chosen skill A. Cost: two adjacent skills whose triggers must be
disambiguated (gated by KR3). Full positive/negative ledger in the ADR.

## Tasks

- [x] Record Context: quantify the unique structure the upper layers carried in the N01 example.
- [x] Record the Decision (A or B) with Consequences; set `status: accepted`.
