---
layer: node
id: N10
type: story
title: drain-cycle prompt pointer
parent: D3
serves_kr: KR3
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    drain_cycle/prompt.py points workers at the pack's entry skill; no reference to
    code-review-and-quality remains in drain_cycle/; one smoke drain completes
    pickup → PR through the pointer.
delegates_to: at-pickup task breakdown (story); change lands in the drain-cycle repo
---

# N10 — drain-cycle prompt pointer

**Type:** `story` · lands in the **drain-cycle** repo.

> **Blocked by:** [N05](../D2-execution-workflow-drains-issues/N05-entry-skill-front-door.md) —
> there must be an entry skill to point at.

> **▶ On pickup:** break into build tasks per the at-pickup breakdown; keep the diff to the
> pointer swap — the full prompt-template re-scope is initiative C's.

## What

As the drain-cycle supervisor, I want my worker prompt to point at the pack's entry skill instead
of inlining procedure and a third-party review skill, so that workers follow one source of truth
and uninstalling agent-skills breaks nothing. This removes the hardcoded
`/code-review-and-quality` dependency in `drain_cycle/prompt.py` — the conflict the deep review
flagged as the uninstall blocker.

## Why

The bet: a pointer is the smallest change that unblocks the uninstall (N11) and validates the
thin-supervisor seam before initiative C invests in it. Rejected alternative: keep the inlined
procedure as a parallel fallback next to the pointer — two sources of truth, and workers follow
the stale one. Scope fence: only the pointer swap; the ≤15-line template reform and procedure-verb
purge belong to initiative C, so this node deliberately does not chase them.

## Completion

- **Done when:** `prompt.py` references the entry skill, `grep -rn 'code-review-and-quality'
  drain_cycle/` returns empty, and drain-cycle's pytest suite is green.
- **Done when:** one smoke drain completes pickup → PR through the pointer with no
  inlined-procedure fallback.

## Assumptions

- The entry skill is visible to worker sessions drain-cycle spawns (`claude -p` in a worktree). *(to-verify — plugin/skill visibility under headless worktree sessions is the load-bearing unknown; the smoke-drain task checks it first)*

## Key Risks

- **Risk:** the prompt change degrades worker behaviour mid-cycle.
  *Mitigation:* smoke-drain a low-stakes issue before the validation drains start; the swap is
  one commit, reverted in one command — a two-way door.

## Tasks

- [ ] `skeleton` — Swap the inlined review/procedure reference in `prompt.py` for the entry-skill pointer (test updates folded in) · Done when: `grep -rn 'code-review-and-quality' drain_cycle/` is empty and pytest is green · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·L·L·M·L
- [ ] Run one smoke drain through the pointer on a low-stakes issue · Done when: the worker completes pickup → PR via the entry skill with no inlined-procedure fallback observed in the transcript · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·M·L·L·L
