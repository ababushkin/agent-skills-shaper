# Skill Benchmark: plan-review

**Model**: <model-name>
**Date**: 2026-05-04T05:49:33Z
**Evals**: 1, 2, 3, 4, 5 (3 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 87% ± 30% | 44% ± 16% | +0.43 |
| Time | 99.3s ± 20.0s | 46.9s ± 9.7s | +52.4s |
| Tokens | 52969 ± 1225 | 41852 ± 488 | +11117 |

## Per-eval breakdown

| Eval | With-skill | Baseline | Gap | Note |
|---|---|---|---|---|
| 1 roadmap-without-triage | 9/9 (100%) | 2/9 (22%) | +78% | Strong framework win. Both REVISE. |
| 2 prizecategoryselector-vue-removal | 6/6 (100%) | 3/6 (50%) | +50% | Both catch unverified scope; only with-skill names B2 + grep falsifying condition. |
| 3 clean-gem-bump | 2/6 (33%) | 4/6 (67%) | **−33%** | **Calibration defect** — skill over-flags Quick-tier reversible KTLO plan. Recommends REVISE; baseline approves-with-adjustments. |
| 4 schema-migration-no-rollback | 8/8 (100%) | 3/8 (38%) | +62% | Both REVISE; only with-skill structures by B5/B6 with named falsifying conditions. |
| 5 redis-cache-solutionism | 7/7 (100%) | 3/7 (43%) | +57% | Both catch solutionism; only with-skill demands measurable latency target as named falsifying condition. |

## Analyst observations

1. **Calibration defect (eval-3)** — skill scored 33% vs baseline 67%. With-skill returned REVISE on a 30-min reversible dev-dependency bump where APPROVE was expected. Root cause: B3 confidence-threshold and B2 scope checks fire on a Quick-tier plan where Rule A5 (KTLO carve-out) and two-way-door reversibility should dominate. Iteration-2 fix candidate: at Quick tier with full reversibility, soften B3 from "block APPROVE" to "note + recommend". The over-flag was substantively partly correct (`bundle update` without `--conservative` does widen the diff) — but recommending REVISE on a reversible 30-min change is a poor calibration.

2. **Discriminating power is clean** — assertions cleanly separate framework adherence from substantive content. Baseline reviews caught the same substantive concerns in 4/5 evals but lacked Cynefin classification, tier selection, B-bucket verdicts, and named falsifying conditions. The skill's added value is structure + verifiability, not different conclusions.

3. **Recommendation convergence** — 4/5 evals: both runs reach the same recommendation (REVISE). Eval-3 is the only divergence. This means the skill's primary lift is the auditable bucket structure, not catching things baselines miss.

4. **Cost** — +52s wall time (+112%), +11K tokens (+27%) per review. Justified for Full-tier (production data, one-way doors). Excessive for Quick-tier reversible plans. Tier auto-select is doing some work here (4/5 with-skill runs auto-selected Full appropriately; eval-3 was Quick — but Quick still pulled in too many bucket checks).

5. **Eval-3 expected output may need a softer reframe** — "APPROVE" is the right tier verdict for a 30-min reversible bump, but the skill's catch on unconstrained `bundle update` is substantively correct. Consider revising eval-3 expected output to "APPROVE with named scope constraint (`bundle update --conservative`)" — keeps the eval honest about what a good review notices.

6. **Variance flag** — with-skill pass-rate stddev = 30% (driven entirely by eval-3 outlier). Drop eval-3 and stddev collapses. Confirms eval-3 is the calibration anomaly, not noise.
