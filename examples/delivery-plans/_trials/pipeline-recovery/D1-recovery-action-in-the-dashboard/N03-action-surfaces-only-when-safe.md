---
layer: node
id: N03
type: story
title: Action surfaces only when safe
parent: D1
serves_kr: KR1
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
delegates_to: planning-and-task-breakdown (per-node task breakdown)
---

# N03 — Action surfaces only when safe

> **As** the Nestl operator, **I want** the clear action offered only on runs that are actually
> stuck, **so that** I don't kill a job that is merely slow or whose worker is asleep.

> **▶ On pickup — before coding:** expand this node via `planning-and-task-breakdown`.
> **Blocked by:** N01 (the stuck-detection threshold is decided in the design doc).

## Acceptance criteria

- **Done when:** a run younger than its longest expected duration shows **no** clear action — the
  UI offers the escape hatch only past the stuck threshold from the design doc.
- **Done when:** a run past the threshold surfaces the action, with its age shown so the operator
  acts on evidence, not a guess.

## Tasks

- [ ] `skeleton` — gate the action on the design-doc threshold end-to-end: a below-threshold seeded run hides it, an above-threshold one surfaces it (the threshold value from N01 is the only input, folded in).
- [ ] Show the run's age in the row so the operator sees why the action is (or isn't) offered.
