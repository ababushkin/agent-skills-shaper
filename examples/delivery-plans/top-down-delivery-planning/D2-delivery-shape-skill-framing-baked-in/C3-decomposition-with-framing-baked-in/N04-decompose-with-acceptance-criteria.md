---
layer: node
id: N04
type: story
title: Decompose initiative → deliverables → capabilities → stories, AC by default
parent: C3
serves_kr: KR2
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
delegates_to: planning-and-task-breakdown (per-capability task breakdown)
---

# N04 — Decompose initiative → deliverables → capabilities → stories, AC by default

**Type:** `story`.

> **As** an agent invoking delivery-shape on a committed initiative,
> **I want** the skill to decompose goal + KRs into deliverables → capabilities → stories with
> acceptance criteria emitted **by default**,
> **so that** I stop getting low-level tasks that are missing the "how do I know this is done?"
> check.

## Acceptance criteria

- **Done when:** given a fed initiative (goal + KRs as text), the skill emits a file-set whose
  every `story` node carries an Acceptance-criteria block — checked by `bin/check-plan-framing`.
- **Done when:** every deliverable carries a `serves_kr` tag and every node carries a `type` tag,
  so the hierarchy is walkable (N02's script succeeds on the emitted plan).

## Tasks

- [ ] `skeleton` — Decompose one fed initiative end-to-end into the four layers on the thinnest path (one deliverable, one capability, one story with AC) so the full pipeline runs before breadth is added.
- [ ] Emit acceptance criteria by default on every story node; fail loudly if a story has none.
