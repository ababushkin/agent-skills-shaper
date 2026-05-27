---
layer: deliverable
id: D3
title: Routing reproducible and discriminating
parent: ..
serves_kr: KR3
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR3 holds — two independent applications of the rubric agree on (tier,
    review-flag) for the worked example and ≥4 of 5 held-out tasks, and the
    sample spans ≥2 distinct tiers.
---

# D3 — Routing reproducible and discriminating

**Serves:** KR3 *(brake)* — "Two independent applications of the rubric agree on (tier,
review-flag) across a worked example + 5 held-out tasks, spanning ≥2 tiers."

The brake: a rubric that produces a different answer each time, or always the same tier, has no
decision value (it is the kill condition made measurable). One `experiment` node tests both
properties — reproducibility (two applications agree) and discrimination (≥2 tiers appear).

Rule A1 not triggered: the eval is a throwaway measurement, reversible, single node.

## Nodes

- [N06 — Rubric reproducibility + discrimination eval](N06-reproducibility-discrimination-eval.md) · `experiment`

## Done when

KR3 is observed: re-running the rubric twice over the worked example + 5 held-out tasks yields
agreement on (tier, flag) for the example and ≥4/5 held-out tasks, with ≥2 distinct tiers present.
