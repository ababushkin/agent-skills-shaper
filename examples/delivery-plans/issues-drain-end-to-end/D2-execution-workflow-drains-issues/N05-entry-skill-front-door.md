---
layer: node
id: N05
type: story
title: "Entry skill: the front door"
parent: D2
serves_kr: KR1
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    A front-door skill exists per docs/skill-anatomy.md that walks the N04 graph by
    named delegation — pickup, breakdown-at-pickup, build, review, verify, PR — and a
    dry run on one real issue reaches the PR step without re-prompting.
delegates_to: at-pickup task breakdown (story); authoring per docs/skill-anatomy.md
---

# N05 — Entry skill: the front door

**Type:** `story`.

> **Blocked by:** [N04](N04-execution-workflow-design-doc.md) — task breakdown waits until the
> design doc is accepted.

> **▶ On pickup:** break into build tasks per the at-pickup breakdown; author per
> `docs/skill-anatomy.md` against the accepted N04 contract.

## What

As a drain-cycle worker picking up a Linear issue, I want one front-door skill that takes me from
pickup through breakdown-at-pickup, build, review, verify, and PR finishing, so that the
supervisor prompt can be a single pointer and the whole procedure lives in the pack. This is the
skill `drain_cycle/prompt.py` will point at (N10) — the keystone of the thin-supervisor
architecture.

## Why

The bet: breakdown-at-pickup on fresh context beats plan-time task expansion (detail decays
before the node is reached), and one front door is what lets the supervisor prompt shrink to a
pointer — the premise initiatives A and C share. Rejected alternative: a prompt-side checklist
inside drain-cycle — the workflow gets trapped in one vendor's supervisor, which is exactly the
coupling this initiative exists to remove. Unblocks N10's pointer swap. **Genuinely new
authoring** — both predecessor packs are tracker-blind; superpowers' `subagent-driven-development`
is the nearest relative for the loop structure (reference, not port).

## Completion

- **Done when:** the skill exists per `docs/skill-anatomy.md`, walks the N04 graph with every
  step a *named delegation* to its owning skill, and carries the issue's acceptance criteria
  through the handoff contract to the review step.
- **Done when:** a dry run on one real issue reaches the PR step without re-prompting.

## Assumptions

- Linear issue context (body, AC, labels) is available to the worker at pickup. *(verified — drain-cycle injects issue context into the worktree prompt today)*
- The five-section node body emitted by delivery-shape is sufficient input for at-pickup breakdown. *(to-verify — checked on the first validation drain; a gap re-opens the handoff contract, not this skill)*

## Key Risks

- **Risk:** the front door bloats into re-authored copies of the steps it orchestrates, drifting
  from their sources.
  *Mitigation:* P7 gate at review — every step is a named delegation, no inlined procedure; the
  ~150-line execution-skill target makes inlining structurally impossible.

## Tasks

- [ ] `skeleton` — Author the front door end-to-end with each workflow step a named delegation to the build, debug/simplify, review (N03), verify, and PR skills (skill dir + frontmatter folded in) · Done when: a toy-issue dry run reaches the PR step with every step delegated by name · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·M·L·M·L
- [ ] Write the breakdown-at-pickup section: size check and a Done-when clause on every build task · Done when: breakdown of a sample node yields tasks that each carry exactly one verifiable Done-when clause · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·M·L·L·L
- [ ] Write the blocked/halt path per workflow governance: comment naming the blocker, issue stays In Progress, no false Done · Done when: a dry run of a blocked issue ends with a Linear comment naming the blocker and unchanged status · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·M·L·L·L
