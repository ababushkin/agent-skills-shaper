---
layer: node
id: N08
type: story
title: "PR finishing: Graphite-first, git fallback"
parent: D2
serves_kr: KR1
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    A PR-finishing skill exists that submits a stacked PR via Graphite when gt is
    present and falls back to plain git with an identical body/trail contract;
    every finish lands the What/Why/Focus body and the review-summary comment.
delegates_to: at-pickup task breakdown (story); authoring per docs/skill-anatomy.md
---

# N08 — PR finishing: Graphite-first, git fallback

**Type:** `story`.

> **Blocked by:** [N04](N04-execution-workflow-design-doc.md) — task breakdown waits until the
> design doc is accepted. Consumes the review-summary produced by
> [N03](../D1-review-gate-proven-on-seeded-defects/N03-personas-and-review-fan-out.md).

> **▶ On pickup:** break into build tasks per the at-pickup breakdown; verify the gt command
> surface against current Graphite docs before relying on it (the HS companion below).

## What

As a worker with a verified diff, I want a Graphite-first PR finishing skill with a plain-git
fallback, so that every drain ends in a stacked, reviewable PR carrying a What/Why/Focus body and
a review-summary comment instead of an unreviewed push. The trail artefacts this skill emits are
exactly what KR1's "full review trail" check greps for.

## Why

The bet: Graphite-first matches the owner's tooling and drain-cycle's half-built stack mode
(`.drain-handoff.json`), so stacking works where it matters without stranding environments that
lack `gt`. Rejected alternatives, both directions: plain-git-only (works everywhere but abandons
stacking — the reason Graphite is in the stack at all) and Graphite-only (breaks any repo or
worker without gt installed). Per-repo push policy (direct-to-main vs PR) stays with repo
instructions; the skill honours it rather than overriding it.

## Completion

- **Done when:** the skill detects `gt` and submits a stacked PR; when absent, the plain-git path
  produces a branch + PR with the identical body/trail contract.
- **Done when:** every finish lands the What/Why/Focus PR body and posts the review-summary
  comment to the Linear issue.

## Assumptions

- The gt command surface used (branch create / submit) is stable across the versions where workers run. *(to-verify — pin the verified command set during authoring; the source-driven-development companion fires on the skeleton task)*
- Per-repo push policy is readable from repo instructions. *(verified — this repo's AGENTS.md states it; the skill reads, not assumes)*

## Key Risks

- **Risk:** the Graphite and git paths drift — different bodies or trail artefacts — making
  KR1's trail check flaky depending on which path ran.
  *Mitigation:* one shared body/trail template both paths fill; the fallback task's Done-when
  asserts artefact parity, not just "a PR exists".

## Tasks

- [ ] `skeleton` — Author the Graphite-first flow (gt detection → branch → stacked submit) with the What/Why/Focus body template (skill dir + shared trail template folded in) · Done when: a toy diff lands as a stacked PR with the body contract filled · Model: Balanced · risk reversible · review elevated · axes RC·SC·HS·SR·OR = M·M·H·M·L · companions source-driven-development
- [ ] Write the plain-git fallback with trail parity · Done when: the same toy diff finished via the fallback yields identical body and trail artefacts · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·M·M·L·L
- [ ] Write the review-summary comment + Linear status update step · Done when: the issue shows the review-summary comment and status moves per governance at the moment of state change · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
