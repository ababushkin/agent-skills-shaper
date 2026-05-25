---
layer: deliverable
id: D1
title: Walking-skeleton spike + mechanical-conversion proof
parent: ..
serves_kr: KR1
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR1 holds — the contract doc names all three schema elements, one worked
    file-set exists, and the walk-script emits a manifest whose counts equal the
    hand-count in the example README.
---

# D1 — Walking-skeleton spike + mechanical-conversion proof

**Serves:** KR1 *(foundation)* — "A documented plan-artefact contract and a worked file-set
for one real already-shaped initiative exist, and a walk-script converts that file-set into
the expected tracker manifest."

This deliverable is the riskiest assumption and the kill gate for the whole initiative. It
proves — before any skill is built — that a committed initiative's full hierarchy expresses
as cross-referenced markdown a human reads top-down and a script walks deterministically. If
it can't, the standalone-markdown premise is wrong and the initiative is re-shaped or killed
(see the initiative kill condition).

Its three nodes carry the proof end-to-end: **N01** (spike) hand-produces the file-set and reads
the schema off it; **N02** (story) supplies the mechanical-conversion half of the kill condition
with a walk-script; **N03** (ADR) records whether the upper layers carried enough unique structure
to justify a new skill or an expansion of `planning-and-task-breakdown`. N02 + N03 are the gate
(Linear ABA-282).

## Nodes

- [N01 — Hand-produce the plan file-set + read off the contract](N01-hand-produce-fileset-and-read-off-contract.md) · `spike` · `skeleton`
- [N02 — Walk-script: file-set → tracker manifest](N02-walk-script-fileset-to-manifest.md) · `story`
- [N03 — ADR: new skill vs expand planning-and-task-breakdown](N03-new-skill-vs-expand-task-breakdown.md) · `adr`

## Done when

KR1 is observed: `docs/delivery-shape-contract.md` names directory layout · cross-reference
convention · per-node tags; `examples/delivery-plans/<initiative>/` exists and reads top-down;
and `bin/walk-delivery-plan <dir>` prints milestone / issue / sub-issue counts equal to the
hand-count recorded in this example's [README](../README.md#hand-count-manifest).
