# Skill Benchmark: plan-review

**Model**: <model-name>
**Date**: 2026-05-05T02:51:59Z
**Evals**: 1, 2, 3, 4, 5 (3 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 90% ± 22% | 42% ± 20% | +0.48 |
| Time | 112.5s ± 16.0s | 61.1s ± 9.0s | +51.3s |
| Tokens | 55575 ± 881 | 44204 ± 524 | +11372 |

## Per-eval breakdown (vs. iteration-1)

| Eval | iter-2 with-skill | iter-1 with-skill | iter-2 baseline | Note |
|---|---|---|---|---|
| 1 roadmap-without-triage | 9/9 (100%) | 9/9 (100%) | 1/9 (11%) | Stable. With-skill recommended KILL (stricter than expected REVISE — both are non-APPROVE). |
| 2 prizecategoryselector-vue-removal | 6/6 (100%) | 6/6 (100%) | 3/6 (50%) | Stable. Skill explicitly evaluated and rejected the Quick-tier carve-out (correct — no rollback path stated). |
| 3 clean-gem-bump | **3/6 (50%)** | 2/6 (33%) | 4/6 (67%) | **Calibration defect persists.** The B2/B3 carve-out fix from iter-1 helped (B8 now caught with revert kill-switch), but the agent SUSTAINED B1 (no problem statement) on a routine gem bump and B1 is not in the carve-out list. Verdict came back REVISE; expected APPROVE. Baseline still beats with-skill on this eval. |
| 4 schema-migration-no-rollback | 8/8 (100%) | 8/8 (100%) | 3/8 (38%) | Stable. Strongest framework win — explicit B5/B6 SUSTAINED with rollback + backfill metrics named as missing. |
| 5 redis-cache-solutionism | 7/7 (100%) | 7/7 (100%) | 3/7 (43%) | Stable. Skill explicitly invokes Agentic P3 for solutionism callout. |

## Analyst observations

1. **Carve-out partial fix (eval-3)** — iteration-1 added a Quick-tier reversibility carve-out covering B2/B3 SUSTAINEDs. The carve-out is working as written: the agent's review explicitly applies it to B2 and B3. **But B1 (problem framing) is not in the carve-out list, and the agent SUSTAINED B1** on the rubocop bump because the plan does not include a problem statement. This was a foreseeable gap — Universal Rule A5 (KTLO carve-out) and the Quick-tier reversibility frame both apply to B1 in the same way they apply to B2/B3. The agent itself surfaced this gap in its own review notes. **Recommended iteration-3 fix:** add B1 to the Quick-tier reversibility carve-out (or, more cleanly, recognize KTLO/maintenance plans at B0 and skip B1 entirely — Rule A5 says minor maintenance does not require outcome framing).

2. **Length proportionality remains a problem at Quick tier** — eval-3 with-skill review ran ~76 lines with full B-bucket tables, three-column assumption matrices, and six conditions. This is heavier than a Quick-tier review should be for a 30-min reversible change. The skill's B-bucket discipline is right; the level of structure imposed is not. Worth considering a lighter-weight Quick-tier output template (single-paragraph verdict per bucket, no tables).

3. **Discriminating power confirmed** — assertions cleanly separate framework adherence from substantive content. Baseline reviews caught real issues in 4/5 evals (correctly identifying solutionism, missing rollback, unverified scope) but lacked Cynefin classification, tier selection, B-bucket verdicts with falsifying conditions, and Gilad confidence scoring. Skill's lift is auditable structure + verifiability.

4. **Recommendation convergence** — 4/5 evals with-skill and baseline reach equivalent recommendations (REVISE/REJECT). Eval-3 is the only divergence — and the divergence is in the wrong direction (skill more restrictive than baseline on a reversible change). This continues to be the calibration anomaly, not noise.

5. **Cost** — +51s wall time (+84%), +11K tokens (+26%). Justified for Full-tier evals 1, 4, 5; arguably justified for eval 2; **excessive for eval 3** (Quick-tier with full reversibility — should not pull this much process).

6. **Variance** — with-skill stddev 22% (down from iter-1's 30% — improvement). Driven entirely by eval-3 outlier. Drop eval-3 and stddev collapses to ~0% (4/4 perfect).

7. **Iter-1 → iter-2 deltas:** with-skill pass rate moved from 87% → 90% (small positive), baseline shifted from 44% → 42% (within noise). The carve-out fix lifted eval-3 from 33% to 50% but not all the way to APPROVE. Three more assertion fails out of six remain — all on the calibration axis (verdict, length, B-bucket overload), not on framework adherence.