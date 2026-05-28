---
layer: node
id: N06
type: story
title: Rule A1 design-doc branch + up/down delegation
parent: D2
serves_kr: KR2
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
delegates_to: design-doc (Rule A1 trigger); initiative-shape (upstream goal+KRs); planning-and-task-breakdown (downstream tasks)
---

# N06 — Rule A1 design-doc branch + up/down delegation

**Type:** `story`.

> **▶ On pickup — before coding:** expand this node via `planning-and-task-breakdown`.

## What

As an agent invoking delivery-shape, I want the skill to branch on the Rule A1 design-doc
trigger and to delegate up to `initiative-shape` and down to `planning-and-task-breakdown`, so
that it never re-authors sub-skill gates (which guarantees drift, agentic P7) and a
design-doc-worthy deliverable gets a design doc before tasks.

## Why

Copying gate text from a delegated skill into delivery-shape is the definition of drift: the
source updates, the copy rots, and the next agent reads a stale protocol with full confidence.
Delegation keeps the boundary clean. Selecting the branch and pointing `delegates_to` is the
work; authoring the gate content is not. This is agentic P7 as a skill behavior.

Rejected alternative: re-author the Rule A1 trigger logic inline so the skill is
self-contained. Rejected — self-contained is drift waiting to happen; link and delegate instead.

## Completion

- **Done when:** a deliverable that meets a Rule A1 trigger routes to `design-doc` before task
  breakdown; one that does not proceeds on goal + deliverables. Both branches exercised in a test
  plan.
- **Done when:** the skill cites `initiative-shape` (up) and `planning-and-task-breakdown` (down)
  by current name and contains no copied gate text from either — checked by grep against the two
  SKILL.md files.

## Assumptions

- Rule A1's four triggers (>5 nodes, one-way door, shared infra, user/cost/compliance impact) cover the relevant architectural-significance cases. *(to-verify — grounded by the `_tests/rule-a1-branch/` fixture, which exercises both arms of the branch)*
- `design-doc` skill exists and is the right delegation target for Rule A1. *(verified — the skill is in this pack and handles the design-doc discipline)*

## Key Risks

- **Risk:** Both trigger arms (design-doc-worthy and not) are not exercised in the worked
  example, so the branch logic is unverified on real content.
  *Mitigation:* `_tests/rule-a1-branch/` fixture explicitly exercises both arms — one deliverable
  that triggers a design-doc node and one that does not.

## Tasks

- [ ] Implement the Rule A1 branch (trigger met → delegate to design-doc; else proceed).
- [ ] Wire up delegation: consume `initiative-shape` output; hand each node to `planning-and-task-breakdown`.
