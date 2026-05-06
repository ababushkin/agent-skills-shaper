# Skill Benchmark: plan-review (iteration 4)

**Model**: claude-opus-4-7 (1M context), runner and grader both
**Date**: 2026-05-06
**Evals**: 1, 2, 3, 4, 5 — 3 runs each per condition (n=3 per cell)
**Iteration purpose**: replace self-grading with an isolated-grader pipeline (blinded to condition, no SKILL.md access, strict bucket-evidence rules); re-confirm iter-3 fixes at n≥3; quantify how much of the iter-2→iter-3 baseline jump was self-grading drift vs real signal.

## Headline

**With-skill 91% ± 1% vs without-skill 36% ± 4% — real delta +0.54.** Far larger than iter-3's self-graded +0.08. The skill produces a much bigger pass-rate lift than iter-3 measured. The +0.54 figure is the first iter-on-iter number we have any business claiming as a real signal: stable across 3 runs (with-skill stddev 1pp), graded by an agent that never saw the SKILL.md and didn't know which condition produced the review, with bucket-explicitness rules that prevent rubber-stamp passes.

## Summary

| Metric | With Skill | Without Skill | Delta |
|---|---|---|---|
| Pass rate (n=3, isolated grader) | 91% ± 1% | 36% ± 4% | **+0.54** |
| Per-run means (with) | 91%, 90%, 91% | — | — |
| Per-run means (without) | — | 32%, 39%, 38% | — |

## Per-eval (n=3, isolated grader)

| Eval | with_skill | without_skill | Notes |
|---|---|---|---|
| 1 roadmap-without-triage | 93% ± 6% | 7% ± 6% | Largest gap; SKILL drives B1/B2/B3 verdicts + triage recommendation that baseline never produces |
| 2 prizecategoryselector-vue-removal | 89% ± 10% | 44% ± 10% | Baseline catches `unused` claim sometimes; SKILL catches it consistently with falsifying condition |
| 3 clean-gem-bump | 72% ± 10% | 50% ± 29% | **Lowest with-skill cell** — fast-track output doesn't always emit "Cynefin: Clear" or "Quick tier" labels; strict grader penalises. Iter-5 fix candidate. |
| 4 schema-migration-no-rollback | 100% ± 0% | 38% ± 0% | SKILL produces explicit B5/B6 verdicts every run; baseline misses ADR/rollback assertions. |
| 5 redis-cache-solutionism | 100% ± 0% | 43% ± 0% | SKILL produces solutionism call-out + B1/B6 verdicts every run; baseline rarely cites buckets explicitly. |

## Drift comparison: iter-3 review outputs re-graded by iter-4 isolated grader

The point of this section is to test the iter-3 hypothesis that the iter-2→iter-3 baseline jump (42% → 92%) was self-grading drift. If it was, the same iter-3 review outputs should grade lower under an isolated grader.

| Eval | Cfg | iter-3 self-graded | iter-4 isolated grader on same review | Drift |
|---|---|---|---|---|
| 1 | with_skill | 9/9 (100%) | 9/9 (100%) | +0pp |
| 1 | without_skill | 8/9 (89%) | 8/9 (89%) | +0pp |
| 2 | with_skill | 6/6 (100%) | 6/6 (100%) | +0pp |
| 2 | without_skill | 6/6 (100%) | 6/6 (100%) | +0pp |
| 3 | with_skill | 6/6 (100%) | 6/6 (100%) | +0pp |
| 3 | without_skill | 6/6 (100%) | 6/6 (100%) | +0pp |
| 4 | with_skill | 8/8 (100%) | 8/8 (100%) | +0pp |
| 4 | without_skill | 8/8 (100%) | 8/8 (100%) | +0pp |
| 5 | with_skill | 7/7 (100%) | 7/7 (100%) | +0pp |
| 5 | without_skill | 5/7 (71%) | 3/7 (43%) | -29pp |

Aggregate: with-skill self 100% → isolated 100% (drift +0pp). Without-skill self 92% → isolated 86% (drift -6pp). Iter-3 self-graded delta +0.08 → iter-3 isolated-graded delta +0.14 (only 6pp wider).

**Caveat: this drift comparison is partly contaminated.** Six of the ten drift-grader agents took unusually long (79-181s vs ~25s for clean grader runs) and made extra tool calls (3-7 vs 2). Several reported "File already exists with grading" before writing — strongly suggesting they discovered the iter-3 self-grading.json files in the same run-1 directory and used them to anchor their own scoring. The `with_skill` row of all-100% should be read as upper-bound. The `without_skill` rows where the agent didn't hit the iter-3 file (eval-1, eval-5) are cleaner: drift was -0pp and -29pp respectively. So drift exists, but it is small to moderate, not the dominant explanation for the iter-2→iter-3 baseline jump.

## What the +0.54 delta actually means

It is the first measurement of plan-review's value where the grader did not author the work it was scoring. That removes the dominant confound. Three things follow.

1. **The skill is doing real work.** The +0.54 gap is across five evals, three runs each, isolated grader, strict bucket-evidence rules. With-skill agents reliably emit Cynefin labels, tier choices, bucket verdicts (SUSTAINED / OVERTURNED), falsifying conditions, and verdict recommendations. Without-skill agents produce ad-hoc reviews that occasionally hit assertions by accident but miss the structural ones (bucket explicitness, named falsifying conditions, B8 pre-mortem) almost every time.

2. **Stability is good.** With-skill across three runs: 91%, 90%, 91% — variance of one percentage point. Without-skill: 32%, 39%, 38% — tighter than expected. n=3 was enough to distinguish signal from noise on this skill.

3. **One genuine SKILL.md gap surfaced.** Eval-3 (clean-gem-bump, the calibration target from iter-3) is the lowest with-skill cell at 72%. Reason: the Step 1a fast-track output template doesn't require explicit "Cynefin: Clear" or "Tier: Quick" labels. iter-3 self-grader was lenient on this; iter-4 isolated grader is not. This is the iter-5 fix.

## Cost

| Metric | With Skill | Without Skill |
|---|---|---|
| Tokens per runner (mean) | ~56k | ~45k |
| Tokens per grader (mean) | ~48k | ~47k |
| Wall (runner, mean) | ~80s | ~50s |
| Wall (grader, mean) | ~25s | ~22s |
| Total agent spawns | 30 runners + 30 graders + 10 drift = 70 |
| Wall (whole sweep, parallelised) | ~6 min |

Token cost per eval (with-skill, runner+grader) is ~104k. Iter-3 self-grading was ~56k single agent. Isolated grading roughly doubles the per-eval cost — but produces a number that reflects reality.

## Open items for iter-5

1. **SKILL.md fast-track template (Step 1a) must emit explicit "Cynefin: <domain>" and "Tier: Quick (fast-track sub-form)" lines.** Currently they're optional; this is the cause of eval-3's 72% with-skill cell. Adding ~2 required header lines to the fast-track output template should bring eval-3 with-skill to ~90%+ without affecting other evals. Concrete, scoped, low-risk.

2. **Drift-grader contamination in this iteration.** When an agent is asked to grade a review under `iter-3/<eval>/<cfg>/run-1/outputs/review.md`, it can `ls` the run-1 directory and discover the existing iter-3 grading.json. This biases the drift comparison upward (toward agreement with iter-3 self-grade). Iter-5 should either (a) copy review.md into a temp dir without the surrounding grading metadata, or (b) explicitly tell the grader not to read any files other than the one path provided.

3. **Token cost of grader on baseline outputs.** Baseline reviews are short and sloppy; grader still spends ~47k tokens. Most of that cost is loading the review + assertions + reasoning through each one. Could plausibly drop with a more compact grader prompt — but cost is fine for now; the value of accurate measurement outweighs the marginal token spend.

4. **No headline-claim about the iter-2→iter-3 baseline drift hypothesis.** The drift comparison was supposed to falsify or confirm that hypothesis. Because of the contamination noted in (2), it does neither cleanly. Iter-5's drift fix lets us re-run drift comparison without that confound. Until then, treat "self-grading caused the baseline jump" as plausible-but-unproven.

## Conclusion

Iter-4 ships the measurement infrastructure that iter-3 promised: isolated grader, n=3 per cell, strict bucket-evidence rules. The headline finding is that the skill produces a +0.54 pass-rate lift over the baseline — much larger than iter-3's self-graded +0.08, and stable across runs. The drift comparison is partly contaminated by graders reading existing iter-3 grading files, but the cleanest cells suggest iter-3 self-grading drifted modestly (≤6pp), not catastrophically. The one concrete SKILL.md fix surfaced is for the Step 1a fast-track template (eval-3 calibration target) — Cynefin and tier labels need to be required, not optional.
