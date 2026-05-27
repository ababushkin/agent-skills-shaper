---
layer: deliverable
id: D2
title: Annotation carried by every filed task list
parent: ..
serves_kr: KR2
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR2 holds — ≥90% of task lists filed under docs/tasks/ carry the model-tier
    and risk annotation, driven by the template fields and the enforcement hook.
---

# D2 — Annotation carried by every filed task list

**Serves:** KR2 *(bet)* — "After the layer lands, ≥90% of task lists filed under `docs/tasks/`
carry a model-tier and risk annotation per the reference."

This is the behaviour-change bet: the rubric existing (D1) is necessary but not sufficient; the
annotation has to actually appear on filed lists. Two nodes drive that — the **template** carries
the fields so a list is born annotated (**N04**), and an **enforcement hook** flags any filed list
that drops them (**N05**).

Rule A1 not triggered: a template edit and a hook are reversible, single-surface, ≤2 nodes — no
design-doc node.

## Nodes

- [N04 — `model` + `risk` fields in the task-list template](N04-model-risk-fields-in-template.md) · `story` · `skeleton`
- [N05 — Hook flags un-annotated task lists](N05-hook-flags-unannotated-lists.md) · `story`

## Done when

KR2 is observed: `grep -L 'Model:' docs/tasks/*.md` returns nothing across the measurement window
— every filed task list carries the annotation line.
