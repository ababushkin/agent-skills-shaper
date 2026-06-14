# Benchmarks

On a five-scenario benchmark of the [`plan-review`](../skills/plan-review/SKILL.md) skill on Claude Sonnet 4.6, with-skill runs catch **93%** of the issues a senior reviewer should catch. Baseline (the same model, same plan, no skill loaded) catches **19%**. Delta **+0.74**, stable across n=3 and confirmed stable after a 69-line prose reform (iter-6, 2026-06-14): aggregate unchanged at 93%.

The number isn't the point on its own. The point is that without a skill, the model does what models do — it summarises the plan back. With the skill, it produces an explicit verdict that names the actual failure mode (no rollback, unverified scope claim, no problem statement). That difference is what calibration is for, and it's what this page tries to show with numbers and source links.

Only `plan-review` has been calibrated against an eval set today. The methodology is reusable; benchmarking the other nine skills is on the roadmap.

---

## What we measured

Five scenarios from [`skills/plan-review/evals/evals.json`](../skills/plan-review/evals/evals.json), each one a plan with at least one named class of defect that a senior reviewer should catch. Each eval has a set of binary assertions (e.g. "did the review classify Cynefin domain as Complicated", "did it produce verdict REVISE", "did it name a falsifying condition for the scope concern"). Pass rate = passed assertions / total assertions, averaged across n=3 runs per cell.

The scenarios:

1. **Roadmap without triage** — Allocate next quarter across three themes (shareable shortlist, push notifications, onboarding rewrite) with no triage records and no measurable outcomes. The defect: B1 problem framing missing, B3 confidence scoring missing, recommendation should be REVISE with idea-triage as the prerequisite.
2. **Vue component removal, unverified claim** — "Remove unused Vue components, starting with PrizeCategorySelector." The defect: "unused" is asserted, not verified; B2 scope verdict should be SUSTAINED with `grep` as the falsifying condition.
3. **Clean gem bump (the fast-track target)** — Bump rubocop 1.60 → 1.65, run tests, commit, 30 minutes. The shape: Cynefin Clear, Quick tier, fully reversible — should fast-track to APPROVE without inflating into Full-tier review. The skill must classify and downgrade, not invent concerns to look thorough.
4. **Schema migration without rollback** — Add NOT NULL column to a 50M-row users table, backfill during deploy. The defect: B5 reversibility (no ADR, no alternatives), B6 operability (no rollback, no backfill metrics, no capacity headroom). Recommendation should be REVISE.
5. **Redis cache, solutionism** — Introduce Redis caching for catalog reads. The defect: solution-first framing — no problem statement, no latency target. B1 SUSTAINED, B6 SUSTAINED, REVISE.

Together they cover the most common plan-review failure surfaces: missing problem statements, scope inflation, unverified assertions, irreversibility hidden behind plain language, and solutionism.

---

## How we measured

**n=3 per cell.** Each (eval × condition) cell is run three times. We report the mean and standard deviation so the reader can see the run-to-run variance, not just a single point.

**Two conditions.**
- *With skill*: the runner has the [`plan-review`](../skills/plan-review/SKILL.md) `SKILL.md` loaded.
- *Baseline*: the runner gets the same plan, on the same model, with no skill in context — the closest analogue to "what generic prompting produces."

**Isolated grader.** A separate agent grades each review. The grader is blinded to which condition produced the review, has no access to `SKILL.md`, and operates under strict rules: assertions only PASS with quotable evidence; bucket verdicts must be explicit (e.g. literal "B5 SUSTAINED", not paraphrased); Cynefin domain and tier must be named, not inferred.

**Why isolated grading matters.** In iter-3 we discovered the grader (which had visibility into adjacent metadata files in the workspace) was inflating baseline scores — apparent baseline jumped from 42% to 92% across one iteration with no SKILL.md change. Switching to an isolated, blinded grader in iter-4 dropped the apparent baseline back to 36%. The +0.54 delta from iter-4 onward is the first trustworthy number this benchmark produced. Catching that measurement bug is what calibration is for.

---

## Results

Iter-5, the latest run. Claude Sonnet 4.6 on both runner and grader. n=3 per cell.

| Eval | With skill | Without skill | Delta |
|---|---|---|---|
| 1 — roadmap without triage | 81% ± 6% | 4% ± 6% | **+77pp** |
| 2 — vue removal, unverified claim | 94% ± 10% | 22% ± 10% | **+72pp** |
| 3 — clean gem bump | 100% ± 0% | 11% ± 10% | **+89pp** |
| 4 — schema migration, no rollback | 100% ± 0% | 25% ± 0% | **+75pp** |
| 5 — redis cache, solutionism | 90% ± 8% | 33% ± 8% | **+57pp** |
| **Aggregate (iter-5, pre-reform)** | **93% ± 2%** | **19% ± 5%** | **+0.74** |
| **Aggregate (iter-6, post-reform)** | **93% ± 4%** | **19% ± 1%** | **+0.74** |

Every scenario shows a large delta. The smallest (eval-5, +57pp) is still substantial. The biggest (eval-3, +89pp) is the calibration target the skill was tuned to handle correctly — not over-reviewing a 30-minute reversible change.

---

## What the skill is actually doing differently

The number is one thing. The texture of the difference is another. Three things show up consistently across runs.

**Naming the failure mode, not just describing the plan.** Baseline reviews tend to summarise the plan back and add a few generic concerns. With-skill reviews produce explicit verdicts attached to specific buckets. On the schema-migration eval, baseline produces text like "this looks risky, consider a rollback plan." With-skill produces "B6 SUSTAINED — no rollback path named, no backfill progress metric, no capacity headroom analysis on a 50M-row backfill." The grader's strict literal-evidence rule rewards this; it's also what a senior reviewer would write.

**Classifying the work before reviewing it.** The skill's first step is Cynefin classification + tier (Quick or Full). This is what fixed eval-3 from 72% to 100% — explicit `Cynefin: Clear` and `Tier: Quick` labels in the fast-track output template (added between iter-4 and iter-5, commit `440a15f`). Baseline rarely classifies anything; it reviews every plan as though it were the same shape, which is how 30-minute gem bumps end up with the same review template as 50M-row schema migrations.

**Catching one-way doors.** Two of the five evals (schema migration, vue removal) hide irreversibility behind plain language. Baseline accepts both; with-skill names the falsifying condition that should overturn the verdict — `grep PrizeCategorySelector` for the "unused component" claim, "no `docs/adr/*.md` for this migration" for the schema change. This is the bucket of work that's most expensive to get wrong in production, and it's where the delta is largest.

---

## The trajectory

Five iterations.

- **Iter-1 / iter-2**: drafted the SKILL.md, found a calibration defect on the fast-track eval (eval-3, baseline-ish behaviour: skill kept inflating a 30-min reversible change into Full-tier review).
- **Iter-3**: added the Step 1a fast-track gate. Baseline appeared to jump to 92% — suspicious. Investigation showed the self-grader was reading adjacent `grading.json` files in the workspace, contaminating its judgement.
- **Iter-4**: switched to an isolated, blinded grader with no workspace metadata access and strict literal-evidence rules. Baseline collapsed back to 36%. Aggregate delta **+0.54** — the first trustworthy number this benchmark produced.
- **Iter-5**: closed the eval-3 gap (72% → 100%) by making `Cynefin domain:` and `Tier:` lines mandatory in the fast-track output template. Re-ran the full sweep on Sonnet 4.6 (≈30% cheaper than Opus 4.7). Aggregate delta **+0.74**, stable across n=3.
- **Iter-6**: prose reform (N06) cut 69 lines from SKILL.md (348→279 lines). Same harness, same eval set, same models as iter-5. Aggregate **93% ± 4%** — identical to iter-5 (0pp delta). Reform confirmed: the cut prose was redundancy, not load-bearing guidance.

Each iteration's analysis lives in [`benchmarks/plan-review/iteration-{1..5}/benchmark.md`](../benchmarks/plan-review/).

---

## Caveats

**Model swap on iter-5.** Iter-4 was Opus 4.7 on both runner and grader; iter-5 was Sonnet 4.6 on both. The +0.74 vs iter-4's +0.54 numbers are not apples-to-apples — the sonnet baseline produces less structured output (without-skill score dropped 36% → 19%), which the strict grader penalises more heavily. The clean claim from iter-5 is "the iter-5 SKILL.md, run on sonnet, produces a +0.74 lift over a sonnet baseline." Running the iter-4 SKILL.md on sonnet (a same-model comparison) would isolate the SKILL.md improvement from the model change. That comparison is an open item.

**One skill calibrated.** The other nine skills in this pack haven't been benchmarked yet. The methodology — eval scenarios with binary assertions, isolated blinded grader, n=3 per cell — is reusable, and benchmarking is on the roadmap. Today the +0.74 number speaks for `plan-review` specifically.

**Runner phrasing variance.** Eval-1 and eval-5 dropped slightly with-skill in iter-5 (93% → 81% and 100% → 90%). Inspection of the failing assertions shows runner phrasing differences ("REWORK" or "DO NOT APPROVE" instead of literal "REVISE"; bucket reasoning correct but missing the explicit "B1 SUSTAINED" label) tripping the grader's strict literal-matching rule. These aren't skill-content gaps; they're a candidate target for a future SKILL.md tightening pass on the output template's literal-string requirements.

**Five scenarios is not a comprehensive surface.** The scenarios were chosen to cover representative failure modes (Cynefin classification, fast-track gate, irreversibility, missing rollback, solutionism). They don't cover every plan shape a reader might bring. Adding scenarios is cheap; they're plain JSON in `evals.json`.

**This is one number, not a leaderboard.** The benchmark is here to answer "does the skill make the agent better at the task it's meant to do." It's not a comparison across models, prompting strategies, or competing skill packs.

---

## Reproducibility

| Artefact | Path |
|---|---|
| Eval definitions (5 scenarios, assertions) | [`skills/plan-review/evals/evals.json`](../skills/plan-review/evals/evals.json) |
| Per-iteration analysis writeups | [`benchmarks/plan-review/iteration-{1..6}/benchmark.md`](../benchmarks/plan-review/) |
| Per-iteration machine-readable results | `benchmarks/plan-review/iteration-{1..6}/benchmark.json` |
| Aggregator scripts (n=3 stats, iter comparison) | `benchmarks/plan-review/iteration-{3,4,5}/aggregate.py` |
| Iter-4 grader prompt (isolated grader rules) | `benchmarks/plan-review/iteration-4/grader-prompt.md` |

Raw per-cell run data (60+ runner outputs and grading files per iteration) is gitignored — workspace bloat with no durable analytical value. The analysis files (`benchmark.md`, `benchmark.json`, `aggregate.py`, `grader-prompt.md`) are in git and tell the full story across iterations.
