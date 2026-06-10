---
layer: node
id: N02
type: story
title: Pointer-only prompt template
parent: D1
serves_kr: KR3
maps_to: linear-issue
skeleton: true
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    drain_cycle/prompt.py emits a ≤15-line worker template carrying issue context,
    process segments, and a single skill pointer; grep for procedure-verb sequences
    over drain_cycle/ returns empty; pytest is green; one smoke drain reaches PR
    through the new template.
delegates_to: at-pickup task breakdown (story); change lands in the drain-cycle repo
---

# N02 — Pointer-only prompt template

**Type:** `story` · `skeleton: true` · lands in the **drain-cycle** repo. The initiative's
walking skeleton: the thinnest supervisor that still drains an issue end-to-end.

> **Blocked by:** [N01](N01-thin-supervisor-contract-design-doc.md) — task breakdown waits
> until the contract is accepted. Also initiative A's
> [N05](../../issues-drain-end-to-end/D2-execution-workflow-drains-issues/N05-entry-skill-front-door.md)
> (an entry skill must exist) and
> [N10](../../issues-drain-end-to-end/D3-cutover-off-third-party-packs/N10-drain-cycle-prompt-pointer.md)
> (the pointer swap lands first; this node deletes the machinery around the pointer, so the
> branches must chain in that order).

> **▶ On pickup:** break into build tasks per the at-pickup breakdown; the diff is subtractive —
> collapse, don't rewrite.

## What

As the drain-cycle supervisor, I want my worker prompt reduced to issue context plus process
segments plus a single skill pointer, so that the intra-issue workflow lives only in the pack
and any vendor's worker can follow it unchanged. Concretely: `_normal_preamble`,
`_stack_preamble`, `_TAIL`, and `_STACK_TAIL` in `drain_cycle/prompt.py` collapse into one
≤15-line template, and workflow routing the supervisor still carries (the shape-task directive;
`flow.py`'s verify-label branch) moves or dies per N01's boundary chart.

## Why

The bet: subtraction is the whole re-scope — KR3 is a brake measured by `wc -l`, grep, and
pytest, and every line that leaves the prompt is a line that can never again drift from the
pack's prose. Rejected alternative: keep the inlined procedure behind a fallback flag next to
the pointer — two sources of truth, and workers follow the stale one (the same rejection A/N10
recorded for its scope). Unblocks N05's validation cycles and opens the non-Claude-worker door.

## Completion

- **Done when:** `wc -l` on the emitted worker prompt template is ≤15 and grep for
  procedure-verb sequences (review/fix/commit/push) over `drain_cycle/` returns empty.
- **Done when:** pytest exits 0 with the test suite updated to the new template.
- **Done when:** one smoke drain on a low-stakes issue reaches PR through the new template with
  no inlined-procedure fallback observed in the transcript.

## Assumptions

- A/N10's pointer swap has landed before pickup — this node edits the same file and assumes the third-party reference is already gone. *(to-verify — checked at pickup via the blockedBy edge; if N10 slipped, this node halts rather than absorbing its scope)*
- The pack's PR-finishing skill (A/N08) carries the handoff-write and review-trail steps, so the prompt can drop them. *(to-verify — checked against the accepted A/N04 contract at pickup; a gap re-opens N01's boundary chart, not this node's scope)*

## Key Risks

- **Risk:** the ≤15-line budget proves too tight for genuine process context (resume directive,
  caps, worktree facts) and the cap gets quietly exceeded.
  *Mitigation:* N01 allocates the budget line by line before this node breaks tasks; if a
  process segment doesn't fit, the KR cap is challenged at plan-review — never silently blown.
- **Risk:** dropping the inlined procedure degrades worker behaviour mid-cycle.
  *Mitigation:* the kill condition is the brake — 3 consecutive halted drains the inlined
  prompt would have completed restores the inlined tail; the collapse is one commit, a two-way
  door.

## Tasks

- [ ] `skeleton` — Collapse the preamble/tail variants in `prompt.py` into the ≤15-line pointer template per the accepted contract (test updates folded in) · Done when: `wc -l` on the emitted template is ≤15 and pytest is green · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·L·L·M·L
- [ ] Remove or relocate the supervisor's workflow routing (shape-task directive, verify-label branch) per N01's boundary chart · Done when: grep for procedure-verb sequences over `drain_cycle/` returns empty and pytest is green · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·L·L·M·L
- [ ] Smoke-drain one low-stakes issue through the new template · Done when: the drain reaches PR with no inlined-procedure fallback observed in the transcript · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·M·L·L·L
