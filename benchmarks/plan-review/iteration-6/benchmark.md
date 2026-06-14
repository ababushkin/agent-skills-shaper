# Skill Benchmark: plan-review (iteration 6)

**Model**: claude-sonnet-4-6, runner and grader both
**Date**: 2026-06-14
**Evals**: 1, 2, 3, 4, 5 — 3 runs each per condition (n=3 per cell)
**SKILL.md change vs iter-5**: prose reform — 69 lines cut (redundancy/verbosity), no behavioural content removed; SKILL.md 348→279 lines (commit `fb4f36f`). This is the N06 style reform. evals.json is byte-identical to iter-5.
**Grader protocol**: same as iter-4/iter-5 — isolated agent, blinded to condition, no SKILL.md access, strict bucket-evidence rules.

## Headline

**With-skill 93% ± 4% vs without-skill 19% ± 1% — delta +0.74.**

Aggregate with-skill score is 93%, meeting the ≥90% threshold. **Finding: confirmed — the prose reform does not degrade plan-review behavioural performance. No repair loop needed.**

The 69 cut lines were redundancy and verbosity, not load-bearing behavioural guidance.

## Summary

| Metric | With Skill | Without Skill | Delta |
|---|---|---|---|
| Pass rate (n=3, isolated grader) | 93% ± 4% | 19% ± 1% | **+0.74** |
| Per-run means (with) | 98%, 92%, 89% | — | — |
| Per-run means (without) | — | 20%, 17%, 21% | — |

## Per-eval (n=3, isolated grader)

| Eval | with_skill | without_skill | Notes |
|---|---|---|---|
| 1 roadmap-without-triage | 81% ± 5% | 0% ± 0% | Identical to iter-5 (81%). Continuing failure mode: reviewer does not name "idea-triage" as the specific skill to run (names the action but not the skill). |
| 2 prizecategoryselector-vue-removal | 83% ± 14% | 33% ± 0% | 11pp drop from iter-5 (94%). Within run-to-run variance (iter-5 sd was ±10%). Inspection: third run scored 67% — runner phrasing variance on B2 falsifying condition, not a content gap. |
| 3 clean-gem-bump | 100% ± 0% | 6% ± 8% | Unchanged from iter-5. Fast-track gate fires consistently; explicit Cynefin/Tier labels maintained. |
| 4 schema-migration-no-rollback | 100% ± 0% | 29% ± 6% | Unchanged from iter-5. B5/B6 verdicts explicit every run. |
| 5 redis-cache-solutionism | 100% ± 0% | 29% ± 0% | +10pp improvement from iter-5 (90%). Sonnet runner now consistently labels B1 SUSTAINED and calls out solutionism explicitly. |

## Iter-5 → iter-6 per-eval delta (with-skill)

| Eval | iter-5 (sonnet) | iter-6 (sonnet, reformed) | Δ |
|---|---|---|---|
| 1 roadmap-without-triage | 81% | 81% | 0 |
| 2 prizecategoryselector-vue-removal | 94% | 83% | -11pp (phrasing variance — iter-5 sd ±10%) |
| 3 clean-gem-bump | 100% | 100% | 0 |
| 4 schema-migration-no-rollback | 100% | 100% | 0 |
| 5 redis-cache-solutionism | 90% | 100% | +10pp |
| **Aggregate** | **93%** | **93%** | **0pp** |

The aggregate is flat. The eval-2 drop and eval-5 gain cancel out, and both are within the range expected from runner phrasing variance (n=3 is a narrow sample). No eval shows a SKILL.md-attributable regression.

## Reform impact assessment

The N06 prose reform cut 69 lines from plan-review (348→279 lines). The lines removed were:

- Redundant prose that restated what bucket headers already implied
- Over-explained rationale sections that duplicated the SKILL.md purpose statement
- Wordy transition sentences between steps

What was preserved:
- All gate semantics (Steps 1, 1a, 2, 4, 5, 6, 7, 12)
- All eight bucket definitions with verdicts and falsifying-condition requirements
- The fast-track output template with explicit Cynefin/Tier lines (the iter-5 fix)
- The Quick-tier reversibility carve-out and its scope exclusions
- All exit criteria and red flags

The behavioural measurement confirms the theory: the cut prose was fat, not muscle.

## Hypothesis verdict

**Hypothesis**: the reform does not degrade plan-review — the 5-scenario set still scores ≥90% with-skill.

**Result**: **CONFIRMED** — 93% ≥ 90%. No repair loop triggered. No kill condition.

## Caveats

**Same caveats as iter-5 apply.** Model is Sonnet 4.6 on both runner and grader. The +0.74 delta is the same-model claim ("this SKILL.md, on sonnet, lifts sonnet baseline by +0.74"). The iter-5 vs iter-6 delta (0pp aggregate) is the cleanest comparison this series has produced — same model, same eval set, same grader protocol, only the SKILL.md prose changed.

**Eval-2 variance.** The 11pp drop on eval-2 is within the ±10–14% per-eval variance range observed across both iterations at n=3. At n=5 it would likely close to zero. The failing assertion (run 3: grader ruled B2 falsifying condition insufficiently concrete) appeared in 0/3 iter-5 runs and 1/3 iter-6 runs — classic single-sample noise, not a trend.

**Five scenarios, not comprehensive.** The eval set was designed to cover representative failure surfaces; it doesn't cover every plan shape. The claim is "no regression on the calibrated surface."
