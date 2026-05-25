---
layer: capability
id: C2
title: Mechanical conversion & architecture decision
parent: D1
maps_to: linear-label
completion:
  form: the-capability-spec
  criterion: >
    A walk-script converts the worked file-set into a tracker manifest whose counts
    match the hand-count, AND the new-skill-vs-expand decision is recorded as an
    accepted ADR — together closing the kill gate.
---

# C2 — Mechanical conversion & architecture decision

**Capability:** prove the file-set converts to tracker artefacts mechanically, and decide the
shape of the skill that will emit such file-sets.

These two nodes are the gate (Linear ABA-282): the walk-script supplies the mechanical-conversion
half of the kill condition, and the ADR records whether the upper layers carried enough unique
structure to justify a **new** skill (A) or an **expansion** of `planning-and-task-breakdown` (B).

## Nodes

- [N02 — Walk-script: file-set → tracker manifest](N02-walk-script-fileset-to-manifest.md) · `story`
- [N03 — ADR: new skill vs expand planning-and-task-breakdown](N03-new-skill-vs-expand-task-breakdown.md) · `adr`
