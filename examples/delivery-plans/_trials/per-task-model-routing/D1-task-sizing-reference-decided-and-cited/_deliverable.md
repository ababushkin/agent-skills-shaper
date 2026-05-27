---
layer: deliverable
id: D1
title: Task-sizing reference, decided and cited
parent: ..
serves_kr: KR1
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR1 holds — references/task-sizing.md exists and passes the reference-pattern
    checklist, the routing decision is recorded, and planning-and-task-breakdown
    cites the reference in Step 5 and References.
---

# D1 — Task-sizing reference, decided and cited

**Serves:** KR1 *(foundation)* — "`references/task-sizing.md` exists with all required sections,
and `planning-and-task-breakdown` cites it."

The foundation deliverable: the rubric has to exist as a cited reference before any task list can
carry its annotation. Its nodes record the decision (**N02**, ADR), write the reference
(**N01**, the walking skeleton), and wire the planning skill to cite it (**N03**).

Rule A1 was tested and **not** triggered: a markdown reference is reversible, touches no shared
runtime, and breaks into ≤3 nodes — so this deliverable proceeds straight to nodes with no
design-doc node. The architecturally-significant *decision* it embeds (routing, not cascading; a
5-axis rubric; a reversibility-gated default) is recorded as an `adr` node — Rule A1's "a short
ADR may suffice" branch.

## Nodes

- [N01 — Write `references/task-sizing.md`](N01-write-task-sizing-reference.md) · `story` · `skeleton`
- [N02 — ADR: routing-not-cascading + 5-axis rubric](N02-adr-routing-not-cascading.md) · `adr`
- [N03 — Cite the reference from `planning-and-task-breakdown`](N03-cite-from-planning-skill.md) · `story`

## Done when

KR1 is observed: `references/task-sizing.md` passes the reference-pattern checklist (frontmatter,
populated `cited_by`, 5-axis rubric, reversibility-gated rule, worked example) and
`grep -q task-sizing skills/planning-and-task-breakdown/SKILL.md` succeeds.
