#!/usr/bin/env python3
"""Aggregate iter-4 benchmark results.

Iter-4 changes vs iter-3:
  1. Grading is done by isolated grader agents (blinded to condition,
     no SKILL.md access, strict bucket-evidence rules) — separate process
     from the runner that produced the review.
  2. n=3 per cell instead of n=1.
  3. Adds a drift-comparison: re-grades the n=1 iter-3 review outputs with
     the iter-4 isolated grader, to quantify how much of the iter-3
     baseline-pass jump was self-grading drift vs real signal.

Per-cell pass counts come from `assertions[]` PASS/FAIL counts in
grading.json (iter-4 schema) with fallback to legacy iter-3 fields.
"""
import json
import statistics
from pathlib import Path

EVAL_ORDER = [
    "eval-roadmap-without-triage",
    "eval-prizecategoryselector-vue-removal",
    "eval-clean-gem-bump",
    "eval-schema-migration-no-rollback",
    "eval-redis-cache-solutionism",
]
RUNS = [1, 2, 3]
ITER4 = Path(__file__).parent
ITER3 = ITER4.parent / "iteration-3"


def assertion_passed(a):
    for k in ("result", "verdict", "status"):
        r = a.get(k)
        if isinstance(r, str):
            return r.upper() in ("PASS", "PASSED", "MET", "TRUE")
    for k in ("passed", "pass", "met"):
        v = a.get(k)
        if isinstance(v, bool):
            return v
        if isinstance(v, str) and v.upper() in ("PASS", "PASSED", "TRUE", "YES"):
            return True
    return False


def normalise(grading):
    asserts = grading.get("assertions") or grading.get("expectations") or []
    if asserts:
        passed = sum(1 for a in asserts if assertion_passed(a))
        total = len(asserts)
        return passed, total
    s = grading.get("summary", {})
    return s.get("passed", 0), s.get("total", 0)


def load_grading(path):
    return json.loads(path.read_text())


def stats(values):
    if not values:
        return (0.0, 0.0)
    mean = sum(values) / len(values)
    sd = statistics.stdev(values) if len(values) > 1 else 0.0
    return (mean, sd)


# --- iter-4 sweep: 5 evals × 2 conditions × 3 runs ---
iter4_rows = []
for ed in EVAL_ORDER:
    for cfg in ("with_skill", "without_skill"):
        for run in RUNS:
            p = ITER4 / ed / cfg / f"run-{run}" / "grading.json"
            if not p.exists():
                continue
            g = load_grading(p)
            passed, total = normalise(g)
            iter4_rows.append({
                "eval": ed, "config": cfg, "run": run,
                "passed": passed, "total": total,
                "pass_rate": passed / total if total else 0.0,
            })

# --- iter-3 self-graded (re-derived from iter-3/<eval>/<cfg>/run-1/grading.json) ---
iter3_self = {}
for ed in EVAL_ORDER:
    for cfg in ("with_skill", "without_skill"):
        p = ITER3 / ed / cfg / "run-1" / "grading.json"
        if p.exists():
            g = load_grading(p)
            passed, total = normalise(g)
            iter3_self[(ed, cfg)] = (passed, total)

# --- iter-4 drift-graded (iter-4 isolated grader on iter-3 outputs) ---
iter3_drift = {}
for ed in EVAL_ORDER:
    for cfg in ("with_skill", "without_skill"):
        p = ITER4 / "drift-comparison" / ed / cfg / "grading.json"
        if p.exists():
            g = load_grading(p)
            passed, total = normalise(g)
            iter3_drift[(ed, cfg)] = (passed, total)


# --- aggregate iter-4 ---
def cell_mean(eval, cfg):
    rates = [r["pass_rate"] for r in iter4_rows
             if r["eval"] == eval and r["config"] == cfg]
    return stats(rates)


with_rates_per_run = []
without_rates_per_run = []
for run in RUNS:
    w = [r["pass_rate"] for r in iter4_rows
         if r["config"] == "with_skill" and r["run"] == run]
    b = [r["pass_rate"] for r in iter4_rows
         if r["config"] == "without_skill" and r["run"] == run]
    if w:
        with_rates_per_run.append(sum(w) / len(w))
    if b:
        without_rates_per_run.append(sum(b) / len(b))

w_mean, w_sd = stats(with_rates_per_run)
b_mean, b_sd = stats(without_rates_per_run)

print("=" * 92)
print("ITER-4 BENCHMARK (n=3 per cell, isolated grader)")
print("=" * 92)
print(f"With skill:    pass {w_mean:.0%} ± {w_sd:.0%}  (run means: "
      f"{', '.join(f'{r:.0%}' for r in with_rates_per_run)})")
print(f"Without skill: pass {b_mean:.0%} ± {b_sd:.0%}  (run means: "
      f"{', '.join(f'{r:.0%}' for r in without_rates_per_run)})")
print(f"Delta:         pass {w_mean - b_mean:+.2f}")
print()
print("Per-eval (with_skill | without_skill, mean ± stddev across n=3):")
print(f"  {'eval':<42} {'with':<18} {'without':<18}")
for ed in EVAL_ORDER:
    wm, ws = cell_mean(ed, "with_skill")
    bm, bs = cell_mean(ed, "without_skill")
    print(f"  {ed:<42} {wm:.0%} ± {ws:.0%}{'':<6}  {bm:.0%} ± {bs:.0%}")

# --- drift comparison ---
print()
print("=" * 92)
print("DRIFT COMPARISON: iter-3 review outputs, self-graded vs iter-4 isolated grader")
print("=" * 92)
print(f"  {'eval':<42} {'cfg':<14} {'iter-3 self':<14} {'iter-4 isolated':<16} drift")
self_with, self_without = [], []
drift_with, drift_without = [], []
for ed in EVAL_ORDER:
    for cfg in ("with_skill", "without_skill"):
        sp, st = iter3_self.get((ed, cfg), (None, None))
        dp, dt = iter3_drift.get((ed, cfg), (None, None))
        sr = sp / st if st else None
        dr = dp / dt if dt else None
        delta = (dr - sr) if sr is not None and dr is not None else None
        sr_s = f"{sp}/{st} ({sr:.0%})" if sr is not None else "—"
        dr_s = f"{dp}/{dt} ({dr:.0%})" if dr is not None else "—"
        delta_s = f"{delta:+.0%}" if delta is not None else "—"
        print(f"  {ed:<42} {cfg:<14} {sr_s:<14} {dr_s:<16} {delta_s}")
        if cfg == "with_skill":
            if sr is not None: self_with.append(sr)
            if dr is not None: drift_with.append(dr)
        else:
            if sr is not None: self_without.append(sr)
            if dr is not None: drift_without.append(dr)
print()
sw_m = sum(self_with) / len(self_with) if self_with else 0
dw_m = sum(drift_with) / len(drift_with) if drift_with else 0
sb_m = sum(self_without) / len(self_without) if self_without else 0
db_m = sum(drift_without) / len(drift_without) if drift_without else 0
print(f"With-skill:    iter-3 self-grade {sw_m:.0%} → iter-4 isolated {dw_m:.0%}  "
      f"(drift {dw_m - sw_m:+.0%})")
print(f"Without-skill: iter-3 self-grade {sb_m:.0%} → iter-4 isolated {db_m:.0%}  "
      f"(drift {db_m - sb_m:+.0%})")
print(f"iter-3 self-graded delta:    {sw_m - sb_m:+.2f}")
print(f"iter-3 isolated-graded delta: {dw_m - db_m:+.2f}  (this is the real signal "
      f"on iter-3 outputs)")
print(f"iter-4 isolated-graded delta: {w_mean - b_mean:+.2f}  (iter-4 outputs, n=3)")

# --- write benchmark.json ---
result = {
    "iteration": 4,
    "model": "claude-opus-4-7",
    "n_per_cell": 3,
    "grader": "isolated agent, blinded to condition, strict bucket-evidence rules",
    "summary": {
        "with_skill": {"pass_rate_mean": w_mean, "pass_rate_sd": w_sd,
                       "run_means": with_rates_per_run},
        "without_skill": {"pass_rate_mean": b_mean, "pass_rate_sd": b_sd,
                          "run_means": without_rates_per_run},
        "delta": w_mean - b_mean,
    },
    "per_eval": [
        {"eval": ed,
         "with_skill": dict(zip(("mean", "sd"), cell_mean(ed, "with_skill"))),
         "without_skill": dict(zip(("mean", "sd"), cell_mean(ed, "without_skill")))}
        for ed in EVAL_ORDER
    ],
    "drift_comparison": {
        "with_skill": {
            "iter3_self_grade_mean": sw_m,
            "iter4_isolated_grade_mean": dw_m,
            "drift": dw_m - sw_m,
        },
        "without_skill": {
            "iter3_self_grade_mean": sb_m,
            "iter4_isolated_grade_mean": db_m,
            "drift": db_m - sb_m,
        },
        "iter3_self_graded_delta": sw_m - sb_m,
        "iter3_isolated_graded_delta": dw_m - db_m,
        "iter4_isolated_graded_delta": w_mean - b_mean,
    },
    "raw_iter4": iter4_rows,
}
(ITER4 / "benchmark.json").write_text(json.dumps(result, indent=2))
print()
print(f"Wrote {ITER4 / 'benchmark.json'}")
