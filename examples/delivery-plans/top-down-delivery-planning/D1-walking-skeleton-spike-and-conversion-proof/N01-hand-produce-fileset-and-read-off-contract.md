---
layer: node
id: N01
type: spike
title: Hand-produce the plan file-set + read off the contract
parent: D1
serves_kr: KR1
maps_to: linear-issue
tracker_ref: ABA-281
skeleton: true
external_window: none
completion:
  form: decision+stop-condition
  decision: >
    Whether a committed initiative's full hierarchy expresses as cross-referenced
    markdown that a human reads top-down and a script can walk.
  stop_condition: >
    If no walkable layout survives after trying the three candidate cross-reference
    conventions (front-matter links / relative paths / manifest file), stop and
    re-shape the seam before building any skill — do not extend the spike.
delegates_to: eng-principles-universal.md Rule C5 (time-box every spike; written decision at the box)
---

# N01 — Hand-produce the plan file-set + read off the contract

**Type:** `spike` · **Walking skeleton of the whole initiative** (`skeleton: true`).

> **▶ On pickup — before exploring:** time-box the spike per `eng-principles-universal.md` Rule C5;
> record the written decision at the box.

## What

Take one real already-shaped initiative and hand-produce the full delivery hierarchy —
deliverables → nodes → tasks — as a cross-referenced markdown file-set. Read the schema off
the example into the contract. Decide whether the standalone-markdown premise holds.

## Why

Proving the premise on real content before writing any skill prose costs one focused session.
Building the skill first and discovering the premise is wrong costs a rewrite. This spike is the
initiative's walking skeleton (`skeleton: true`): it exercises every layer (deliverable → node →
task) and the cross-reference convention before breadth is added.

Rejected alternative: sketching the schema first and then producing the example. Rejected because
the schema read off a real example is more honest than one designed in the abstract — the example
is the evidence, not the illustration.

## Completion

**Decision:** The hierarchy expresses as cross-referenced markdown and reads top-down (this
file-set). Whether it walks mechanically is the other half of the kill condition and belongs to
N02.

**Stop condition:** The three cross-reference conventions were trialled (front-matter links /
relative paths / manifest file); relative-path + directory-hierarchy + front-matter back-links was
chosen (see the contract). The stop condition did not fire.

## Assumptions

- Three cross-reference conventions cover the design space; one is walkable. *(verified — chosen convention passes the walk-script in N02)*
- A stdlib-only front-matter reader extracts the contract's keys without ambiguity. *(verified — `bin/walk-delivery-plan` demonstrates this)*

## Key Risks

- **Risk:** The chosen cross-reference convention requires a real schema or tool to walk, not
  bare markdown files — falsifying the standalone-markdown premise.
  *Falsifier:* `bin/walk-delivery-plan` (N02) walks the file-set with stdlib only. If it cannot,
  re-shape the seam before building any skill.

## Tasks

- [x] `skeleton` — Pick one real already-shaped initiative; lay out the deliverable → node → task file-set end-to-end. *(Foundational work folded in here: choose the cross-reference convention and create `examples/delivery-plans/<initiative>/` — not a separate silent setup task.)*
- [x] Read the schema off the example into `docs/delivery-shape-contract.md`: directory layout · cross-reference convention · per-node tags.
- [x] Define the node-type vocabulary grounded in the types this example exercises; list the unexercised types as a to-fill appendix.
