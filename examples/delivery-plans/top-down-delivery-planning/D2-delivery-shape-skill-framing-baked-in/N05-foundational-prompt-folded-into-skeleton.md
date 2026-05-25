---
layer: node
id: N05
type: story
title: Foundational-work prompt folded into the walking skeleton
parent: D2
serves_kr: KR2
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
delegates_to: planning-and-task-breakdown (walking-skeleton-first rule; no pre-skeleton setup task)
---

# N05 — Foundational-work prompt folded into the walking skeleton

**Type:** `story`.

> **As** an agent planning delivery,
> **I want** the skill to ask "what toolchain/setup must exist for the skeleton to run?" and fold
> the answer **into** the walking-skeleton task,
> **so that** foundational work is never silently dropped and never appears as a setup task
> *before* the skeleton (the failure mode `planning-and-task-breakdown` Red flags call out).

## Acceptance criteria

- **Done when:** for an initiative needing toolchain setup, the emitted plan contains exactly one
  `skeleton`-flagged task whose description includes the foundational/toolchain work — and **no**
  separate setup task precedes it. Verified by `bin/check-plan-framing` (≥1 skeleton task; 0
  pre-skeleton setup tasks).

## Tasks

- [ ] Add the foundational-work prompt to the workflow; fold the response into the skeleton task's description.
- [ ] Guard against a pre-skeleton setup task: emit it folded, or flag it, never silent.
