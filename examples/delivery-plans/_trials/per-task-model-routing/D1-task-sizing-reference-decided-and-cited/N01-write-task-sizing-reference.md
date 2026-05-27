---
layer: node
id: N01
type: story
title: Write references/task-sizing.md
parent: D1
serves_kr: KR1
maps_to: linear-issue
skeleton: true
external_window: none
completion:
  form: acceptance-criteria
delegates_to: planning-and-task-breakdown (per-node task breakdown)
---

# N01 — Write `references/task-sizing.md`

> **As** an agent breaking work into tasks in Shaper, **I want** a task-sizing reference that
> carries the 5-axis rubric, the tier mapping, and a worked example, **so that** I can assign a
> model tier and risk profile to every task from a single authoritative source.

> **▶ On pickup — before coding:** expand this node via `planning-and-task-breakdown`.

## Acceptance criteria

- **Done when:** `references/task-sizing.md` exists and passes the reference-pattern checklist —
  `type: reference` frontmatter, a populated `cited_by`, the 5 active axes scored Low/Med/High,
  the reversibility-gated default rule, and a worked example.
- **Done when:** the worked example assigns a (tier, review-flag) to ≥1 task and spans the three
  tiers in the mapping (Fast / Balanced / Frontier).
- **Done when:** the 3 set-aside dimensions (cost/volume, latency, context size) are named as
  set-aside, so a reader knows they were considered and excluded, not forgotten.

## Tasks

- [ ] `skeleton` — scaffold the reference end-to-end: `type: reference` frontmatter + one fully-worked axis + the worked example, then validate it against the reference-pattern checklist (toolchain: the checklist lives in `docs/` reference-anatomy guidance — folded in, no separate setup).
- [ ] Fill the remaining 4 active axes and name the 3 set-aside dimensions.
- [ ] Add the tier mapping (Fast = Haiku · Balanced = Sonnet · Frontier = Opus) as a single line, and the reversibility-gated default rule.
- [ ] Add the annotation-line format the downstream surfaces will emit, with the worked example spanning ≥2 tiers.
