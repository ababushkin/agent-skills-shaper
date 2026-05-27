---
layer: node
id: N02
type: adr
title: ADR — routing-not-cascading + 5-axis rubric
parent: D1
serves_kr: KR1
maps_to: linear-issue
external_window: none
completion:
  form: decision-record
  criterion: >
    An accepted ADR recording the routing-not-cascading decision, the 5 active
    axes, and the reversibility-gated default, with the rejected alternative
    (runtime cascading) named.
delegates_to: documentation-and-adrs (ADR discipline — Rule A3 / D3 living ADRs)
---

# N02 — ADR: routing-not-cascading + 5-axis rubric

**Type:** `adr`. The rubric's shape is an architecturally-significant decision (Rule A3), but it is
a single decision record, not a full design doc — Rule A1's lesser branch. `delivery-shape` does
not restate the ADR template here; that discipline lives in its owner.

> **▶ On pickup — before coding:** record this decision via the ADR discipline
> (`documentation-and-adrs`). The reference (`N01`) embodies the decision; the ADR records *why*.

## Completion

An accepted ADR: **Context** (model choice today is an ad-hoc gut call with no rubric),
**Decision** (planning-time routing — one tier picked per task before it runs — with 5 active axes
and a reversibility-gated default), **Consequences** (incl. the named rejected alternative: runtime
cascading / escalation, set aside as a future layer).

## Tasks

- [ ] Draft the ADR: context, the routing-not-cascading decision, the 5 active axes, the reversibility-gated default, and consequences.
- [ ] Name the rejected alternative (runtime cascading) and cross-link the ADR from the reference's decision note.
