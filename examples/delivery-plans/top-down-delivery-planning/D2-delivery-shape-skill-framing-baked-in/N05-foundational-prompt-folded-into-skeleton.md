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
delegates_to: execution-breakdown (walking-skeleton-first rule; no pre-skeleton setup task)
---

# N05 — Foundational-work prompt folded into the walking skeleton

**Type:** `story`.

> **▶ On pickup — before coding:** expand this node via `execution-breakdown`.

## What

As an agent planning delivery, I want the skill to ask "what toolchain/setup must exist for the
skeleton to run?" and fold the answer **into** the walking-skeleton task, so that foundational
work is never silently dropped and never appears as a setup task *before* the skeleton.

## Why

A silent setup task placed before the skeleton defers integration discovery to day two — the
skeleton's whole purpose is to surface integration friction on day one. The fold-in prompt
prevents this. Without it, foundational work either disappears (dropped) or blocks the skeleton
(emitted as a pre-task), both of which hide risk.

Rejected alternative: a separate "setup/toolchain" task before the skeleton. Rejected because
it defers the integration discovery that is the skeleton's entire purpose (eng-universal Rule B2).

## Completion

- **Done when:** for an initiative needing toolchain setup, the emitted plan contains exactly one
  `skeleton`-flagged task whose description includes the foundational/toolchain work — and **no**
  separate setup task precedes it. Verified by `bin/check-plan-framing` (≥1 skeleton task; 0
  pre-skeleton setup tasks).

## Assumptions

- The "fold it in" prompt is sufficient to prevent a pre-skeleton setup task without a manual review step. *(to-verify — check-plan-framing enforces it mechanically; the self-trial in N07 confirms whether 0 re-prompts are needed)*
- Foundational work can always be described in a parenthetical within the skeleton task description — it never needs its own checklist task. *(verified — all 9 nodes in the worked example follow this pattern)*

## Key Risks

- **Risk:** An agent emits a setup task before the skeleton despite the prompt, and the plan
  passes without detection.
  *Mitigation:* `bin/check-plan-framing`'s pre-skeleton check catches any task placed before
  the first skeleton task, regardless of what it is named.

## Tasks

- [ ] Add the foundational-work prompt to the workflow; fold the response into the skeleton task's description.
- [ ] Guard against a pre-skeleton setup task: emit it folded, or flag it, never silent.
