---
layer: node
id: N03
type: story
title: Personas + review fan-out skill
parent: D1
serves_kr: KR2
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    Three persona prompt files (code-reviewer, security-auditor, spec-compliance) exist
    per the N02 contract; the fan-out skill dispatches all three and aggregates a
    GO/NO-GO verdict; the grader reports ≥9/10 seeded findings surfaced.
delegates_to: at-pickup task breakdown (story); authoring per docs/skill-anatomy.md
---

# N03 — Personas + review fan-out skill

**Type:** `story`.

> **Blocked by:** [N02](N02-adr-persona-contract.md) — the personas are written to the contract
> it pins. Graded by [N01](N01-fixture-corpus-and-grader.md)'s harness.

> **▶ On pickup:** break into build tasks per the at-pickup breakdown; author skill + personas
> per `docs/skill-anatomy.md` and the accepted N02 contract.

## What

As a drain-cycle worker finishing a build, I want a first-party review fan-out skill that
dispatches code-reviewer, security-auditor, and spec-compliance personas over my diff and
aggregates a GO/NO-GO verdict, so that every PR carries a multi-lens review trail with no
third-party pack on the path. This is the replacement for the hardcoded
`/code-review-and-quality` dependency. Review order is fixed: spec compliance *before* code
quality — built-the-wrong-thing is caught before built-it-badly.

## Why

The bet: three narrow lenses surface more of the seeded findings than one broad reviewer, and the
spec-first ordering catches the failure class a quality-only reviewer is blind to. Rejected
alternative: port the third-party monolithic review skill verbatim — forbidden by the pack's
predecessor rule, and a single lens leaves the security and AC-violation defect classes
ungraded. Unlocks N05's review step and is the precondition for N11's uninstall.

## Completion

- **Done when:** three persona prompt files exist per the N02 contract, each emitting
  structured-format findings.
- **Done when:** the fan-out skill dispatches all three (Agent fan-out on Claude Code,
  inline-sequential fallback elsewhere) and aggregates one deduped GO/NO-GO verdict with a
  review-summary block.
- **Done when:** `bin/grade-execution-review` reports ≥9/10 seeded findings surfaced — the KR2
  observation.

## Assumptions

- The issue's Done-when / acceptance criteria are available at review time for the spec-compliance lens. *(to-verify — depends on the N04 handoff contract carrying the issue body into the review step; trial interactively until then)*
- ≥9/10 is reachable with three personas. *(to-verify — the iteration task exists for exactly this; two failed hardening rounds re-shape the persona split)*

## Key Risks

- **Risk:** persona findings overlap and the aggregate double-counts, inflating the grade.
  *Mitigation:* the grader and the fan-out aggregation both dedupe on the contract's match key
  (file · defect class) before scoring or verdicting.
- **Risk:** the persona set plateaus below 9/10.
  *Falsifier:* two hardening iterations with per-class miss analysis fail to clear the bar — that
  re-shapes the persona split (KR2 is a commit; the deliverable is re-worked, not shipped short).

## Tasks

- [ ] `skeleton` — Author the code-reviewer persona to the N02 contract and dispatch it through a minimal fan-out skill against one fixture (skill scaffold + persona directory folded in) · Done when: the persona's findings flow through the fan-out path into the grader and score · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·M·L·L·L
- [ ] Author the security-auditor and spec-compliance personas, spec-compliance reviewing the issue's acceptance criteria before code quality · Done when: all three personas emit contract-format findings across the corpus · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·M·L·L·L
- [ ] Aggregate the three verdicts into one deduped GO/NO-GO with a review-summary block ordered spec → security → quality · Done when: one invocation yields a single verdict artefact with no duplicate findings · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·M·L·L·L
- [ ] Iterate the persona set against the harness with per-class miss analysis from `_runs/` logs · Done when: `bin/grade-execution-review` reports ≥9/10 · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·M·L·L·L
