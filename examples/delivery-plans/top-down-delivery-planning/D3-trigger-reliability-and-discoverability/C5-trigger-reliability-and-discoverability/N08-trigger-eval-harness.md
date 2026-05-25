---
layer: node
id: N08
type: story
title: Trigger-eval set + harness, 0 collisions
parent: C5
serves_kr: KR3
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
delegates_to: skill-creator (external plugin — description-tuning + trigger evals; not a Shaper-native skill)
---

# N08 — Trigger-eval set + harness, 0 collisions

**Type:** `story`.

> **As** Anton relying on shape skills to fire at the right decision moment,
> **I want** a fixed eval set of "plan a project"-style phrasings and a harness that checks which
> skill each one selects,
> **so that** delivery-shape never steals a bet-definition prompt from `initiative-shape` or a
> task-breakdown prompt from `planning-and-task-breakdown`, in either direction.

## Acceptance criteria

- **Done when:** `eval/delivery-shape-triggers.md` holds 8–10 labelled phrasings, and
  `bin/eval-triggers` prints matched-skill vs expected-skill per phrasing and **exits 0 only on 0
  collisions** in either direction.

## Tasks

- [ ] `skeleton` — Author the labelled phrasing set (8–10) and a harness that prints matched-vs-expected per phrasing.
- [ ] Drive collisions to 0 in both directions; harness exits non-zero on any collision.
