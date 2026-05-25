---
layer: node
id: N06
type: story
title: Rule A1 design-doc branch + up/down delegation
parent: C3
serves_kr: KR2
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
delegates_to: design-doc (Rule A1 trigger); initiative-shape (upstream goal+KRs); planning-and-task-breakdown (downstream tasks)
---

# N06 — Rule A1 design-doc branch + up/down delegation

**Type:** `story`.

> **As** an agent invoking delivery-shape,
> **I want** the skill to branch on the Rule A1 design-doc trigger and to delegate up to
> `initiative-shape` and down to `planning-and-task-breakdown`,
> **so that** it never re-authors sub-skill gates (which guarantees drift, agentic P7) and a
> design-doc-worthy deliverable gets a design doc before tasks.

## Acceptance criteria

- **Done when:** a deliverable that meets a Rule A1 trigger routes to `design-doc` before task
  breakdown; one that does not proceeds on goal + deliverables. Both branches exercised in a test
  plan.
- **Done when:** the skill cites `initiative-shape` (up) and `planning-and-task-breakdown` (down)
  by current name and contains no copied gate text from either — checked by grep against the two
  SKILL.md files.

## Tasks

- [ ] Implement the Rule A1 branch (trigger met → delegate to design-doc; else proceed).
- [ ] Wire up delegation: consume `initiative-shape` output; hand each capability to `planning-and-task-breakdown`.
