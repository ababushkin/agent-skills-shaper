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

A spike is not a build node and carries no acceptance criteria. Its completion criterion is a
**decision plus a stop condition** (eng-universal Rule C5): by hand, take one real already-shaped
initiative, produce the full delivery hierarchy as a markdown file-set, then read the schema off
the example into the contract — and decide whether the standalone-markdown premise holds.

This node *is* the thinnest end-to-end slice of the initiative: it exercises every layer
(deliverable → node → task) and the cross-reference convention on real content,
before a single line of skill prose is written. Foundational/toolchain work — choosing the
cross-reference convention and standing up the `examples/` directory — is **folded into the
skeleton task below, never a silent pre-task**.

## Decision recorded

The hierarchy expresses as cross-referenced markdown and reads top-down (this file-set).
Whether it **walks mechanically** is the other half of the kill condition and belongs to N02.

## Stop condition

See front-matter `completion.stop_condition`. The three conventions were trialled; relative-path
+ directory-hierarchy + front-matter back-links was chosen (see the contract). The stop condition
did not fire.

## Tasks

- [x] `skeleton` — Pick one real already-shaped initiative; lay out the deliverable → node → task file-set end-to-end. *(Foundational work folded in here: choose the cross-reference convention and create `examples/delivery-plans/<initiative>/` — not a separate silent setup task.)*
- [x] Read the schema off the example into `docs/delivery-shape-contract.md`: directory layout · cross-reference convention · per-node tags.
- [x] Define the node-type vocabulary grounded in the types this example exercises; list the unexercised types as a to-fill appendix.
