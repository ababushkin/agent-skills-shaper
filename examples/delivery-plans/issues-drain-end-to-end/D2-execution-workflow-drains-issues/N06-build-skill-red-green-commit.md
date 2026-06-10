---
layer: node
id: N06
type: story
title: "Build skill: RED/GREEN/commit loop"
parent: D2
serves_kr: KR1
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    A build skill exists enforcing a gated RED → GREEN → commit loop per slice, with a
    verification-form fallback for non-code repos and a named escalation path into the
    debugging skill.
delegates_to: at-pickup task breakdown (story); authoring per docs/skill-anatomy.md
---

# N06 — Build skill: RED/GREEN/commit loop

**Type:** `story`.

> **Blocked by:** [N04](N04-execution-workflow-design-doc.md) — task breakdown waits until the
> design doc is accepted.

> **▶ On pickup:** break into build tasks per the at-pickup breakdown; author per
> `docs/skill-anatomy.md` against the accepted N04 contract.

## What

As a worker building a broken-down task, I want a gated RED/GREEN/commit loop, so that every
increment lands verified, smallest-first, with a commit trail a reviewer can replay. The loop is
per slice: a failing check first (RED), the minimal change that passes it (GREEN), one commit —
with `[GATE]` markers that are not optional.

## Why

The bet: the gated TDD loop is the discipline both external packs converged on independently
(superpowers' per-task implementer loop; agent-skills' /build RED/GREEN/commit) — convergent
evolution is the strongest signal in the deep review. Rejected alternative: advisory
"write tests first" prose without gates — advisory prose is precisely what a worker under token
pressure skips, and ungated discipline is the failure mode the pack's `[GATE]` convention exists
to prevent.

## Completion

- **Done when:** the skill enforces RED (failing check first) → GREEN (minimal pass) → commit per
  slice, with `[GATE]` markers.
- **Done when:** a verification-form fallback exists for repos with no test runner, chosen at
  breakdown time (gate script, grader, link check — a deterministic check, not necessarily a
  unit test).
- **Done when:** a named escalation path into the debugging skill (N07) replaces retry-flailing
  after consecutive red loops.

## Assumptions

- Drained repos expose a runnable verification command discoverable from repo instructions. *(to-verify — markdown-only repos like Shaper itself are the hard case; the verification-form fallback is the intended answer and the first validation drain checks it)*

## Key Risks

- **Risk:** in markdown-only repos RED/GREEN reads as meaningless and workers skip the skill
  wholesale.
  *Mitigation:* the verification-form fallback redefines RED as "the deterministic check fails"
  (e.g. `bin/check-plan-framing` non-zero) so the loop is exercised identically; the fallback is
  selected at breakdown time, not improvised mid-build.

## Tasks

- [ ] `skeleton` — Author the RED/GREEN/commit loop core with its gates and the per-slice commit convention (skill dir + frontmatter folded in) · Done when: the skill passes anatomy section order and the loop's gates are marked `[GATE]` · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·M·L·L·L
- [ ] Write the verification-form fallback and the consecutive-failure escalation into the debugging skill · Done when: both paths are named delegations selectable at breakdown time · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·M·L·L·L
- [ ] Trial the loop on one toy task and record the transcript as the skill's worked example · Done when: the transcript shows RED → GREEN → commit with no skipped gate · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
