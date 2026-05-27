---
layer: node
id: N04
type: story
title: model + risk fields in the task-list template
parent: D2
serves_kr: KR2
maps_to: linear-issue
skeleton: true
external_window: none
completion:
  form: acceptance-criteria
delegates_to: planning-and-task-breakdown (per-node task breakdown)
---

# N04 — `model` + `risk` fields in the task-list template

> **As** an agent filing a task list under `docs/tasks/`, **I want** the template to carry `Model:`
> and `Risk:` fields already, **so that** every list I file is born annotated instead of needing
> the annotation bolted on afterwards.

> **▶ On pickup — before coding:** expand this node via `planning-and-task-breakdown`.
> **Blocked by:** N01 (the annotation format the fields follow lives in the reference).

## Acceptance criteria

- **Done when:** the task-list template carries a `Model:` and a `Risk:` field, with an inline
  pointer to `references/task-sizing.md` for how to fill them.
- **Done when:** a task list filed from the updated template carries a populated annotation line
  for every task — verified on one sample list under `docs/tasks/`.

## Tasks

- [ ] `skeleton` — add the `Model:` and `Risk:` fields to the template and populate them in one sample list filed under `docs/tasks/`, end-to-end from template to filed list (the reference's annotation format is the only input, folded in).
- [ ] Document the annotation-line format inline in the template, citing the reference so a filer needs no external lookup.
