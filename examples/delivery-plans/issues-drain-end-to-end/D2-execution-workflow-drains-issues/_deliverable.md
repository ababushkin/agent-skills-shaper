---
layer: deliverable
id: D2
title: Execution workflow drains issues end-to-end
parent: ..
serves_kr: KR1
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR1 holds — ≥4 of the next 5 drained issues reach Done with a merged PR, zero
    manual fix commits after the worker's final push, and the full review trail
    present. Observed by N09's experiment finding.
---

# D2 — Execution workflow drains issues end-to-end

**Serves:** KR1 *(bet)* — "≥4 of the next 5 drained issues reach Done with a merged PR and zero
manual fix commits after the worker's final push, with the full review trail present."

This deliverable is the initiative's bet: the execution-verb skills that take a worker from issue
pickup to a finished, reviewable PR. It trips **two Rule A1 triggers** — more than ~5 nodes, and
a one-way-door decision (a published verb namespace is expensive to rename once drain-cycle
prompts and muscle memory bind to it) — so its **first node is a `design-doc` node (N04)** and
the build nodes N05–N08 are blocked by it: their task breakdown waits until the design doc is
accepted.

**N04** (design-doc) decides the namespace, the skill graph, and the inter-skill handoff
contract. **N05–N08** (stories) author the skills: the front-door entry skill, the
RED/GREEN/commit build loop, the debugging + simplification pair, and Graphite-first PR
finishing. **N09** (experiment, `acceptance: true`) drains 5 real issues and grades the KR1 bet —
D2's Done is irreducible to its children: every skill can individually pass and the workflow
still fail end-to-end.

## Nodes

- [N04 — Execution-workflow design doc](N04-execution-workflow-design-doc.md) · `design-doc`
- [N05 — Entry skill: the front door](N05-entry-skill-front-door.md) · `story`
- [N06 — Build skill: RED/GREEN/commit loop](N06-build-skill-red-green-commit.md) · `story`
- [N07 — Debugging + simplification skills](N07-debugging-and-simplification.md) · `story`
- [N08 — PR finishing: Graphite-first, git fallback](N08-pr-finishing-graphite-first.md) · `story`
- [N09 — Validation drains](N09-validation-drains.md) · `experiment` · `acceptance`

## Done when

KR1 is observed: N09's finding is **confirmed** — ≥4/5 validation drains reach Done + merged PR
with zero post-push manual fix commits and the full review trail. The acceptance node closes
last, so this milestone reaching 100% coincides with the KR observation.
