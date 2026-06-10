# Skill Benchmark: plan-review (iteration 5)

**Model**: claude-sonnet-4-6, runner and grader both
**Date**: 2026-05-06 / 2026-05-07
**Evals**: 1, 2, 3, 4, 5 — 3 runs each per condition (n=3 per cell)
**SKILL.md change vs iter-4**: fast-track template (Step 1a) now requires explicit `Cynefin domain:` and `Tier:` lines (commit 440a15f). Targeted at the eval-3 calibration gap.
**Grader protocol**: same as iter-4 — isolated agent, blinded to condition, no SKILL.md access, strict bucket-evidence rules.

## Headline

**With-skill 93% ± 2% vs without-skill 19% ± 5% — delta +0.74.**

Larger than iter-4's +0.54, with the eval-3 fix landing as predicted (72% → 100% with-skill on the calibration target). Stable across n=3 (with-skill stddev 2pp).

The +0.74 figure is **not directly comparable to iter-4's +0.54** — model changed (sonnet vs opus on both runner and grader). The valid claim is "the iter-5 SKILL.md, run on sonnet, produces a +0.74 lift over a sonnet baseline." See "Caveats" below.

## Summary

| Metric | With Skill | Without Skill | Delta |
|---|---|---|---|
| Pass rate (n=3, isolated grader) | 93% ± 2% | 19% ± 5% | **+0.74** |
| Per-run means (with) | 96%, 93%, 92% | — | — |
| Per-run means (without) | — | 20%, 23%, 14% | — |

## Per-eval (n=3, isolated grader)

| Eval | with_skill | without_skill | Notes |
|---|---|---|---|
| 1 roadmap-without-triage | 81% ± 6% | 4% ± 6% | Lowest with-skill cell. Failure modes: "REVISE" verdict sometimes phrased differently ("REWORK", "DO NOT APPROVE"); "idea-triage" recommendation not always cited by name. |
| 2 prizecategoryselector-vue-removal | 94% ± 10% | 22% ± 10% | Strong signal. SKILL drives B2 verdict + concrete falsifying condition consistently; baseline rarely. |
| 3 clean-gem-bump | 100% ± 0% | 11% ± 10% | **Eval-3 fix landed.** Iter-4 was 72% (lowest cell); explicit Cynefin/Tier labels in fast-track template close the gap to 100%. Baseline collapses (50% → 11%) — sonnet without skill rarely emits "Clear" or "Quick" labels. |
| 4 schema-migration-no-rollback | 100% ± 0% | 25% ± 0% | SKILL produces explicit B5/B6 verdicts every run; baseline misses ADR/rollback assertions. |
| 5 redis-cache-solutionism | 90% ± 8% | 33% ± 8% | Slight regression vs iter-4 (100% → 90%). Sonnet runner sometimes uses different bucket-verdict phrasing on B1; not a SKILL.md issue. |

## Iter-4 → iter-5 per-eval delta (with-skill)

| Eval | iter-4 (opus) | iter-5 (sonnet) | Δ |
|---|---|---|---|
| 1 roadmap-without-triage | 93% | 81% | -11pp |
| 2 prizecategoryselector-vue-removal | 89% | 94% | +6pp |
| 3 clean-gem-bump | 72% | **100%** | **+28pp** ← eval-3 fix |
| 4 schema-migration-no-rollback | 100% | 100% | 0pp |
| 5 redis-cache-solutionism | 100% | 90% | -10pp |
| **Aggregate** | **91%** | **93%** | **+2pp** |

The aggregate movement is small (+2pp) because the eval-3 fix is offset by minor regressions on eval-1 and eval-5. Inspecting the failing assertions on eval-1 and eval-5 shows the regressions are **runner phrasing variance**, not SKILL.md content gaps:

- Eval-1 failures: runner says "DO NOT APPROVE" or "REWORK" instead of literal "REVISE"; runner cites the triage idea but not the skill name "idea-triage". The grader's strict literal matching catches these as FAIL even though the underlying reasoning is correct.
- Eval-5 failures: bucket-verdict phrasing variance ("solution-first" called out without an explicit "B1 SUSTAINED" label).

These are sonnet-runner verbosity / phrasing differences vs opus, not skill-content regressions. They suggest a future iteration could tighten the SKILL.md "always-emit-this-literal" requirements (e.g. "verdict line MUST be exactly APPROVE / REVISE / KILL"). Out of scope for iter-5.

## Caveats — the +0.74 vs +0.54 comparison is confounded

The model changed between iterations. Three things could be moving in the iter-5 vs iter-4 comparison:

1. **SKILL.md fix** (the intended change) — explicit Cynefin/Tier in fast-track template. Verified at the eval-3 cell (+28pp).
2. **Runner model** (sonnet vs opus) — sonnet baseline produces less structured reviews, which the strict grader penalises more heavily. Without-skill dropped 36% → 19%.
3. **Grader model** (sonnet vs opus) — sonnet grader may apply the literal-evidence rule more strictly, which inflates with-skill scores (where the SKILL.md output is highly structured) relative to baseline (where it isn't).

Effects (2) and (3) inflate the iter-5 delta. The clean apples-to-apples comparison would require running iter-4's SKILL.md on sonnet — i.e. sonnet baseline vs sonnet+iter-4-skill — to isolate the SKILL.md fix from the model swap. We didn't do that.

What we *can* claim from iter-5:

- The SKILL.md change closed the iter-4 eval-3 calibration gap (72% → 100%).
- The skill produces a large pass-rate lift on sonnet (+0.74, stable across n=3).
- No other eval regressed in a SKILL.md-attributable way; the small drops on eval-1/5 are runner phrasing variance.

What we *cannot* claim:

- That iter-5 SKILL.md is "+0.20 better" than iter-4 SKILL.md. The +0.74 vs +0.54 numbers are not on the same scale.

## Cost

| Metric | With Skill | Without Skill |
|---|---|---|
| Tokens per runner (mean) | ~37k | ~28k |
| Tokens per grader (mean) | ~31k | ~30k |
| Wall (runner, mean) | ~80s | ~40s |
| Wall (grader, mean) | ~35s | ~33s |
| Total agent spawns | 27 runners + 30 graders + 3 reused = 60 |
| Wall (whole sweep, parallelised) | ~6 min runners, ~7 min graders |

Sonnet token cost vs iter-4 opus: ~33% reduction on the runner side, ~35% reduction on the grader side. Aggregate ~30% reduction in tokens for the full sweep. (Pricing-adjusted savings are larger because sonnet is also cheaper per token.)

## Open items for iter-6 (or later)

1. **Drift comparison with sandboxing.** Iter-4's drift comparison was contaminated by graders discovering iter-3 self-grading.json files in adjacent dirs. A clean drift run requires either (a) copying review.md to a sandbox path with no metadata neighbours, or (b) restricting grader file-read tools. Not done in iter-5.

2. **Runner phrasing tightness.** Eval-1's runner-side failures (REWORK vs REVISE, missing "idea-triage" by name) suggest the SKILL.md output template should be more prescriptive about literal verdicts. Low-risk small change; defer to iter-6 unless it shows up as a real-world issue.

3. **Same-model comparison.** To prove the iter-4 → iter-5 SKILL.md change is itself an improvement (independent of the model swap), run iter-4's SKILL.md on sonnet against the same evals. ~30 runner agents, no SKILL.md change required. Useful but not urgent.

4. **Token diet on with_skill runner.** With-skill runner mean is ~37k tokens (down from iter-4's ~56k via model swap, but still loading the full SKILL.md). Loading SKILL.md only when the trigger fires would drop typical-case cost further. Owner descoped in iter-3.

## Conclusion

Iter-5 ships the SKILL.md fix surfaced by iter-4 (Cynefin + Tier required in fast-track output) and re-runs the full eval sweep on sonnet for a ~30% cost reduction. The eval-3 calibration gap closes cleanly (72% → 100%). The aggregate skill delta on sonnet is +0.74, stable across n=3 — bigger than iter-4's +0.54, but not directly comparable due to the model swap. The skill is doing real work: every assertion class with explicit bucket / Cynefin / tier requirements passes consistently with-skill and rarely without. Two small with-skill regressions (eval-1 81%, eval-5 90%) are runner phrasing variance, not skill-content gaps.
