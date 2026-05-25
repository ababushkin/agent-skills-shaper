---
layer: deliverable
id: D3
title: Trigger reliability & discoverability
parent: ..
serves_kr: KR3
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR3 holds — on a fixed eval set of 8–10 "plan a project"-style phrasings,
    delivery-shape is the selected skill with zero collisions in either direction
    against initiative-shape or planning-and-task-breakdown.
---

# D3 — Trigger reliability & discoverability

**Serves:** KR3 *(brake)* — "On a fixed eval set of 8–10 'plan a project'-style phrasings,
delivery-shape is the selected skill, with zero collisions in either direction against
initiative-shape or planning-and-task-breakdown."

This is the guardrail deliverable: a third `-shape` skill that sits between `initiative-shape`
and `planning-and-task-breakdown` is worthless if it fires for the wrong prompts or steals
theirs. The eval set protects the two neighbours from regression, and the README/flowchart
registration makes the new skill discoverable.

## Capabilities

- [C5 — Trigger reliability & discoverability](C5-trigger-reliability-and-discoverability/_capability.md)

## Done when

KR3 is observed: `eval/delivery-shape-triggers.md` holds 8–10 labelled phrasings and
`bin/eval-triggers` prints matched-vs-expected per phrasing, exiting 0 only on 0 collisions;
delivery-shape appears in the README skill table and the `using-this-pack` flowchart.
