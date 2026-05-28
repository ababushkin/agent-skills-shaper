---
layer: node
id: N08
type: story
title: Trigger-eval set + harness, 0 collisions
parent: D3
serves_kr: KR3
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
delegates_to: skill-creator (external plugin — description-tuning + trigger evals; not a Shaper-native skill)
---

# N08 — Trigger-eval set + harness, 0 collisions

**Type:** `story`.

> **▶ On pickup — before coding:** expand this node via `planning-and-task-breakdown`.

## What

As Anton relying on shape skills to fire at the right decision moment, I want a fixed eval set
of "plan a project"-style phrasings and a harness that checks which skill each one selects, so
that delivery-shape never steals a bet-definition prompt from `initiative-shape` or a
task-breakdown prompt from `planning-and-task-breakdown`, in either direction.

## Why

Trigger collisions are invisible until a real session: the wrong skill fires, produces wrong
output, and the user re-runs — wasting time and eroding pack trust. The eval set makes
collisions visible before they hit a session. This is KR3's brake on D2's scope: the two
adjacent skills need demonstrable trigger separation before DS is shipped.

Rejected alternative: rely on manual testing and usage to surface collisions. Rejected — manual
testing is retroactive; a harness is proactive and gives a repeatable signal.

## Completion

- **Done when:** `eval/delivery-shape-triggers.md` holds 8–10 labelled phrasings, and
  `bin/eval-triggers` prints matched-skill vs expected-skill per phrasing and **exits 0 only on
  0 collisions** in either direction.

## Assumptions

- 8–10 phrasings adequately cover the collision-prone surface between DS, IS, and PTB. *(to-verify — harness must include both DS-correct and IS-correct phrasings; count is the minimum, not the ceiling)*
- `skill-creator` (external plugin) is available and can perform description-tuning + trigger evals. *(to-verify — plugin is installed; if unavailable, the eval harness falls back to manual review)*

## Key Risks

- **Risk:** The eval set only exercises collisions the author anticipated, missing novel phrasings.
  *Mitigation:* re-run the eval set when new collision-prone phrasings are discovered in real
  sessions (living eval, not a one-time gate).

## Tasks

- [ ] `skeleton` — Author the labelled phrasing set (8–10) and a harness that prints matched-vs-expected per phrasing.
- [ ] Drive collisions to 0 in both directions; harness exits non-zero on any collision.
