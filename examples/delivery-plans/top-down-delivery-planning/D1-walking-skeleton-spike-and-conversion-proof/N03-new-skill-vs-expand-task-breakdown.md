---
layer: node
id: N03
type: adr
title: New skill vs expand execution-breakdown
parent: D1
serves_kr: KR1
maps_to: linear-issue
tracker_ref: ABA-282
external_window: none
completion:
  form: decision-record
  criterion: >
    An accepted ADR exists recording Context / Decision / Consequences for choosing
    (A) a new delivery-shape skill or (B) an expansion of execution-breakdown.
delegates_to: documentation-and-adrs (ADR authoring + supersession discipline)
status: accepted
adr_ref: ../../../../docs/adr/0001-delivery-shape-new-skill-vs-expand-execution-breakdown.md
---

# N03 — ADR: new skill vs expand execution-breakdown

**Type:** `adr`.

> **▶ On pickup:** author the decision record via `documentation-and-adrs`; set `status: accepted`
> when the decision is made. This ADR gates D2 — the build nodes under D2 cannot start until this
> is accepted.

## What

An ADR deciding whether delivery-shape is a new standalone skill (`delivery-shape/`) or an
expansion of `execution-breakdown`. The choice determines the pack's directory layout
and whether two adjacent skills exist whose triggers must be disambiguated.

## Why

D2 cannot start without this decision — the right structure cannot be chosen without examining
how much unique structure the upper hierarchy layers carry (from N01's evidence). Building on
the wrong premise requires a rewrite. Rule A1 flags this as design-doc-worthy in adjacent cases
but an ADR suffices here: one-way-door decision, single surface, bounded consequences.

Rejected alternative: deciding by intuition before seeing the N01 evidence. Rejected because the
upper layers' reducibility (whether capabilities collapse into deliverables) is not predictable in
advance — the spike must run first.

## Completion

**Decision:** Accepted — A, a standalone `delivery-shape` skill.

The polymorphic node layer carries large unique structure (eight completion forms with delegation
targets) that PTB has no concept of and that is too far from "task breakdown" to bolt on. DS
delegates per-node breakdown back down to PTB, so the two compose rather than merge; and the
initiative's own KR3 ("0 collisions against execution-breakdown") already presupposes two
distinct skills.

Full Context / Decision / Consequences record: [`docs/adr/0001`](../../../../docs/adr/0001-delivery-shape-new-skill-vs-expand-execution-breakdown.md).

**Consequences:** New `skills/delivery-shape/`; PTB unchanged and becomes DS's delegation target.
Cost: two adjacent skills whose triggers must be disambiguated (gated by KR3 / N08).

## Assumptions

- N01's spike adequately quantifies the unique structure the upper layers carry — sufficient to make the call. *(verified — capability layer fully collapsible; deliverable layer adds only milestone-grouping + serves_kr; node layer carries 8 completion forms)*
- The two skills' triggers can be disambiguated (KR3). *(to-verify — gated by N08)*

## Key Risks

- **Risk:** The trigger boundary between DS and PTB blurs in practice and DS fires on PTB
  prompts (or vice versa), eroding trust in the pack.
  *Falsifier:* N08's trigger eval set shows 0 collisions in either direction. If it cannot reach
  0 collisions, the skills should merge — the ADR decision was wrong.

## Tasks

- [x] Record Context: quantify the unique structure the upper layers carried in the N01 example.
- [x] Record the Decision (A or B) with Consequences; set `status: accepted`.
