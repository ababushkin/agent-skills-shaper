# Skill Benchmark: plan-review (iteration 3)

**Model**: claude-opus-4-7 (1M context)
**Date**: 2026-05-05
**Evals**: 1, 2, 3, 4, 5 (1 run each per configuration)
**Iteration purpose**: validate Step 1a fast-track gate fix for the eval-3 calibration defect identified in iter-2.

## Headline

**Eval-3 calibration defect resolved.** With-skill went from 3/6 (iter-2) → 6/6 (iter-3). The Step 1a fast-track gate fired correctly: emitted a 16-line APPROVE with three sanity checks and a B8 one-liner, hit all six assertions including length-proportionality. The skill no longer over-restricts routine, fully-reversible KTLO changes.

## Summary

| Metric | With Skill | Without Skill | Delta |
|---|---|---|---|
| Pass rate | 100% ± 0% | 92% ± 12% | +0.08 |
| Tokens | 56,136 ± 1,774 | 44,450 ± 721 | +11,686 |
| Wall time | 107.7s ± 29.8s | 72.2s ± 9.4s | +35.5s |

## Per-eval

| Eval | iter-3 with | iter-2 with | iter-3 baseline | iter-2 baseline | Note |
|---|---|---|---|---|---|
| 1 roadmap-without-triage | 9/9 (100%) | 9/9 (100%) | 8/9 (89%) | 1/9 (11%) | Stable on with-skill. Baseline shifted upward — see drift caveat. |
| 2 prizecategoryselector-vue-removal | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) | 3/6 (50%) | Fast-track gate correctly did NOT fire (component removal isn't KTLO — deletion can break runtime). Quick-tier flow ran as before. |
| **3 clean-gem-bump** | **6/6 (100%)** | **3/6 (50%)** | 6/6 (100%) | 4/6 (67%) | **Calibration defect resolved.** Fast-track gate fired on all four preconditions; emitted 16-line APPROVE with `bundle update --conservative rubocop` recommendation and B8 revert kill-switch. |
| 4 schema-migration-no-rollback | 8/8 (100%) | 8/8 (100%) | 8/8 (100%) | 3/8 (38%) | Fast-track gate correctly did NOT fire (precondition 2 fails — schema migration touches production data). Full-tier flow surfaced B5 + B6 SUSTAINEDs as before. |
| 5 redis-cache-solutionism | 7/7 (100%) | 7/7 (100%) | 5/7 (71%) | 3/7 (43%) | Fast-track gate correctly did NOT fire (precondition 2 fails — vendor introduction). Full-tier flow surfaced B1 solutionism callout. |

## Analyst observations

1. **The fix works as designed.** Step 1a fast-track gate fired exactly once across the five evals — on eval-3 — and produced a calibration-target output (15-25 line APPROVE with sanity checks + B8 one-liner). On the four other evals, the gate's preconditions correctly failed and the agent fell through to the normal flow with no behaviour change vs iter-2. Zero false positives, zero false negatives, in this single-run sweep.

2. **Token cost did not drop on eval-3 despite the shorter output.** Eval-3 with-skill ran 53.6k tokens (iter-3) vs 55.0k tokens (iter-2) — a ~3% reduction, far less than the ~70% drop expected from the iter-3 plan. Cause: the dominant cost is loading the SKILL.md (now 362 lines, ~10k tokens), not producing the review. The fast-track output is ~12 lines instead of ~76, but the loading cost is fixed. To realise the projected token savings, the SKILL.md itself would need an early short-circuit section that the agent could process before reading the full workflow. **Action item for a future iteration:** restructure SKILL.md so Step 1a sits near the top of the file in a self-contained ~30-line block, and the agent can decide to stop reading there. Out of scope for iter-3.

3. **Baseline self-grading drift is significant.** Without-skill pass rates jumped from 42% (iter-2) to 92% (iter-3) — a delta far larger than any plausible content shift, given the prompts and skill contents are unchanged. The same baseline reviews would have hit ~3-5/N assertions under iter-2 grading, vs 5-9/N under iter-3 grading. The drift contaminates the headline +0.08 delta number and means iter-2 vs iter-3 deltas should not be compared directly. This is a known eval-stability problem — single-agent self-grading is not adversarial enough. **Action item:** for iter-4 onward, route grading through a separate, isolated grader agent (with no knowledge of which condition produced the review) before any further calibration claims.

4. **The eval-3 win is robust to the drift.** Even setting aggregate numbers aside, the eval-3 specific finding holds: the with-skill output went from 76 lines REVISE (blocking APPROVE on a B1 SUSTAINED) to 16 lines APPROVE — a structural verdict change, not a grading nuance. The fast-track gate produced the calibration-target shape on every assertion, and the agent's own grading.json notes confirm the gate fired by design.

5. **Wall time delta dropped from +51s (iter-2) to +36s (iter-3).** Driven by eval-3 fast-tracking from ~96s to ~63s (33s reduction). Other evals are within noise of iter-2.

6. **Variance dropped from 22% to 0% on with-skill.** The eval-3 outlier was the entire stddev driver in iter-2; with eval-3 calibrated, the with-skill condition is now uniform 100% across all five evals (n=1 per cell, so this should be re-confirmed at n≥3 before claiming stability).

## Limitations of this run

- **n=1 per cell.** Single run per (eval, condition). Iter-2 was n=3 per cell; iter-3 was scoped to a single sweep to confirm the fast-track gate behaves correctly. Re-run at n≥3 before claiming the +0.08 delta or the 0% stddev are stable signals.
- **Self-grading.** Each runner agent self-grades against the assertions in the same context window where it produced the review. The drift in baseline pass rates between iter-2 and iter-3 (despite identical prompts and assertions) is the smoking gun for this. Future iterations need a grader agent.
- **Token-cost target missed.** The Step 1a plan projected a ~70% token reduction on KTLO eval-3; actual reduction is ~3%. The reason is mechanical (SKILL.md loading cost dominates), not a flaw in the gate logic.

## Conclusion

The Step 1a fast-track gate resolves the eval-3 calibration defect that persisted across iter-1 and iter-2. Verdict shape on routine KTLO/minor-version changes is now APPROVE with proportionate sanity checks, instead of REVISE blocked on a B1 (problem framing) SUSTAINED. The fix is sound and scoped. The remaining open items — token-cost reduction, grader-agent isolation, n≥3 re-confirmation — are tracked for a future iteration.
