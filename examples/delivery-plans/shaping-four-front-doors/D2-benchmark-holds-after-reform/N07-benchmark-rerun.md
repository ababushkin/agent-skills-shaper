---
layer: node
id: N07
type: experiment
title: Benchmark re-run post-reform
parent: D2
serves_kr: KR2
maps_to: linear-issue
acceptance: true
external_window: none
completion:
  form: hypothesis+success-metric
  verifies_parent: D2
  hypothesis: >
    The style reform — plan-review compressed 369 → ≤300 and the pack consolidated to four
    doors — does not degrade plan-review's measured effectiveness: the 5-scenario eval set
    still scores ≥90% pass with-skill.
  success_metric: >
    The existing harness re-run (n=3 per cell, same runner/grader model) aggregates ≥90%
    with-skill, appended to docs/benchmarks.md. Below 90%: up to two repair attempts
    (restore cut prose implicated by the failing scenario, re-run). Below 80% after two
    repairs fires the initiative kill condition — keep the flat layout, ship style reform
    only.
delegates_to: experiment discipline (hypothesis, success metric, written finding) per the spike protocol — hosted post-fold in the shape:design door
---

# N07 — Benchmark re-run post-reform

**Type:** `experiment` · `acceptance: true` (verifies D2). Not a build node: its honest
outcomes are *confirmed*, *repaired-then-confirmed*, or *kill-condition fired* — not
*shipped*. This is the brake on the whole initiative.

> **Blocked by:** [N02](../D1-four-front-doors-under-cap/N02-shape-delivery-front-door.md),
> [N03](../D1-four-front-doors-under-cap/N03-shape-idea-front-door.md),
> [N04](../D1-four-front-doors-under-cap/N04-shape-project-front-door.md),
> [N05](../D1-four-front-doors-under-cap/N05-shape-design-front-door.md), and
> [N06](../D1-four-front-doors-under-cap/N06-utilities-under-cap.md) — the benchmark measures
> the pack's *final* reformed state; a mid-reform measurement would attribute later changes
> to nothing.

> **▶ On pickup:** run the experiment and write the finding (confirmed / repaired /
> kill-condition) following the experiment discipline.

## What

Re-run the existing 5-scenario plan-review benchmark — same harness, same eval definitions,
same n=3-per-cell protocol, same runner/grader model — against the reformed pack, and append
the results to `docs/benchmarks.md` next to the 93% baseline. If the aggregate lands below
90%, run the defined repair loop (at most two attempts, each restoring cut prose implicated
by the failing scenario); record every attempt.

## Why

KR2 is the brake: D1's bet is that plan-review's 69 cut lines are redundancy, and only a
behavioural measurement can falsify that. Rejected alternative: trust the gate grep and
byte-identical eval set as sufficient proof — that is the unverified-claim failure this pack
exists to prevent, measuring the ruler instead of the patient. This node carries
`acceptance: true` because D2's Done is irreducible to build-node completion: there is
nothing to build here, only an observation that can fail.

## Completion

**Hypothesis:** the reform does not degrade plan-review — the 5-scenario set still scores
≥90% with-skill.

**Success metric:** harness re-run aggregate ≥90% (n=3 per cell, same models as iter-5),
appended to `docs/benchmarks.md`.

Below 90% **falsifies** the no-degradation hypothesis and triggers the repair loop: up to two
attempts, each restoring the cut prose the failing scenario implicates, then re-run. Below
80% after two repairs fires the initiative **kill condition**: keep the flat 14-skill layout;
ship style reform only.

## Assumptions

- The benchmark harness is reproducible on the reformed layout. *(verified — `docs/benchmarks.md:101-104` pins eval definitions at `skills/plan-review/evals/evals.json` and the n=3 aggregator scripts under `benchmarks/plan-review/`; N06 keeps evals.json byte-identical)*
- n=3 variance (±2% at baseline) is small enough to call the 90% threshold. *(to-verify — if the re-run lands within one standard error of 90%, widen to n=5 before declaring either way rather than calling a coin flip)*

## Key Risks

- **Risk:** a repair attempt restores prose into plan-review and pushes it back over 300,
  trading KR2 against KR1.
  *Mitigation:* repairs restore the implicated prose only, re-checking the cap in the same
  attempt; if both cannot hold simultaneously after two attempts, that is the kill condition
  doing its job — record it, don't force it.

## Tasks

- [ ] `skeleton` — Re-run the 5-scenario benchmark with the existing harness against the reformed pack and append results to docs/benchmarks.md · Done when: a results row with aggregate and per-scenario scores exists next to the iter-5 baseline · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·L·L·L·L
- [ ] `acceptance` — Evaluate the ≥90% metric, run the repair loop if needed (max two attempts), and write the finding (confirmed / repaired / kill-condition) — this finding is D2's Done condition · Done when: the finding is written with per-scenario deltas and a log of any repair attempts · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·M·L·L·L
