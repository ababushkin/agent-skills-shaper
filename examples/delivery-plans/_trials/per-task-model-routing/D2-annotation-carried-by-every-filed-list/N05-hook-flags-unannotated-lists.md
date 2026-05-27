---
layer: node
id: N05
type: story
title: Hook flags un-annotated task lists
parent: D2
serves_kr: KR2
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
delegates_to: planning-and-task-breakdown (per-node task breakdown)
---

# N05 — Hook flags un-annotated task lists

> **As** Anton reviewing filed work, **I want** an automated hook to flag any task list under
> `docs/tasks/` that drops the model/risk annotation, **so that** the ≥90% target holds by
> enforcement rather than by everyone remembering.

> **▶ On pickup — before coding:** expand this node via `planning-and-task-breakdown`.
> **Blocked by:** N04 (the hook checks for the fields the template introduces).

## Acceptance criteria

- **Done when:** the hook is authored per `docs/hook-anatomy.md` with a deterministic pass/fail —
  it passes an annotated fixture list and fails an un-annotated one.
- **Done when:** the fail message names the missing annotation and points at
  `references/task-sizing.md`, so the fix path is obvious.

## Tasks

- [ ] `skeleton` — author the hook per `docs/hook-anatomy.md` with a deterministic pass/fail over a two-file fixture (one annotated list, one not), end-to-end from invocation to verdict (the fixture is folded into this slice).
- [ ] Wire the fail message to name the missing `Model:`/`Risk:` line and point at the reference.
