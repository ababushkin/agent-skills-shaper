---
layer: node
id: N03
type: story
title: Cite the reference from planning-and-task-breakdown
parent: D1
serves_kr: KR1
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
delegates_to: planning-and-task-breakdown (per-node task breakdown)
---

# N03 — Cite the reference from `planning-and-task-breakdown`

> **As** an agent running `planning-and-task-breakdown`, **I want** the planning skill to point me
> at `references/task-sizing.md` at the sizing step, **so that** the tier/risk lens is applied at
> breakdown time without me having to remember the rubric exists.

> **▶ On pickup — before coding:** expand this node via `planning-and-task-breakdown`.
> **Blocked by:** N01 (the reference must exist), N02 (the decision it cites must be recorded).

## Acceptance criteria

- **Done when:** `planning-and-task-breakdown` cites `references/task-sizing.md` in Step 5 and in
  its References section — `grep -q task-sizing skills/planning-and-task-breakdown/SKILL.md`
  succeeds.
- **Done when:** the citation frames the rubric as a *second lens* on the existing
  verification-granularity Size check, not a replacement for it.
- **Done when:** a sample breakdown run against the cited skill annotates every emitted task with a
  (tier, risk) line.

## Tasks

- [ ] `skeleton` — add the Step-5 two-lens citation and the References entry, then confirm a sample breakdown run annotates every task end-to-end (the reference from N01 is the only dependency, folded in).
- [ ] Update `references/task-sizing.md`'s `cited_by` to point back at the planning skill, closing the reference-pattern loop.
