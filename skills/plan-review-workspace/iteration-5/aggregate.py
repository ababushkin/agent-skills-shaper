#!/usr/bin/env python3
"""Aggregate iter-5 benchmark results.

Iter-5 vs iter-4:
  - Runner + grader on sonnet (claude-sonnet-4-6) instead of opus, ~50% cost.
  - Same isolated-grader protocol, same n=3 per cell.
  - SKILL.md fast-track template now requires explicit Cynefin and Tier labels
    (the iter-4 → iter-5 fix; aimed at eval-3 calibration gap).
  - No drift comparison in iter-5 (deferred to a separate task with sandboxing).
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
ITER5 = Path(__file__).parent
ITER4 = ITER5.parent / "iteration-4"


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


def collect(root):
    rows = []
    for ed in EVAL_ORDER:
        for cfg in ("with_skill", "without_skill"):
            for run in RUNS:
                p = root / ed / cfg / f"run-{run}" / "grading.json"
                if not p.exists():
                    continue
                g = load_grading(p)
                passed, total = normalise(g)
                rows.append({
                    "eval": ed, "config": cfg, "run": run,
                    "passed": passed, "total": total,
                    "pass_rate": passed / total if total else 0.0,
                })
    return rows


def cell_mean(rows, ev, cfg):
    rates = [r["pass_rate"] for r in rows if r["eval"] == ev and r["config"] == cfg]
    return stats(rates)


def run_means(rows, cfg):
    means = []
    for run in RUNS:
        rs = [r["pass_rate"] for r in rows if r["config"] == cfg and r["run"] == run]
        if rs:
            means.append(sum(rs) / len(rs))
    return means


def summarize(label, rows):
    w_means = run_means(rows, "with_skill")
    b_means = run_means(rows, "without_skill")
    w_mean, w_sd = stats(w_means)
    b_mean, b_sd = stats(b_means)
    print("=" * 92)
    print(f"{label}")
    print("=" * 92)
    print(f"With skill:    pass {w_mean:.0%} ± {w_sd:.0%}  (run means: "
          f"{', '.join(f'{r:.0%}' for r in w_means)})")
    print(f"Without skill: pass {b_mean:.0%} ± {b_sd:.0%}  (run means: "
          f"{', '.join(f'{r:.0%}' for r in b_means)})")
    print(f"Delta:         pass {w_mean - b_mean:+.2f}")
    print()
    print("Per-eval (with_skill | without_skill, mean ± stddev across n=3):")
    for ed in EVAL_ORDER:
        wm, ws = cell_mean(rows, ed, "with_skill")
        bm, bs = cell_mean(rows, ed, "without_skill")
        print(f"  {ed:<42} {wm:.0%} ± {ws:.0%}{'':<6}  {bm:.0%} ± {bs:.0%}")
    print()
    return {
        "with_skill": {"pass_rate_mean": w_mean, "pass_rate_sd": w_sd, "run_means": w_means},
        "without_skill": {"pass_rate_mean": b_mean, "pass_rate_sd": b_sd, "run_means": b_means},
        "delta": w_mean - b_mean,
        "per_eval": [
            {"eval": ed,
             "with_skill": dict(zip(("mean", "sd"), cell_mean(rows, ed, "with_skill"))),
             "without_skill": dict(zip(("mean", "sd"), cell_mean(rows, ed, "without_skill")))}
            for ed in EVAL_ORDER
        ],
    }


iter5_rows = collect(ITER5)
iter4_rows = collect(ITER4)

iter5_summary = summarize("ITER-5 BENCHMARK (sonnet runner + sonnet grader, n=3)", iter5_rows)
iter4_summary = summarize("ITER-4 BENCHMARK (opus runner + opus grader, n=3) — for comparison", iter4_rows)

print("=" * 92)
print("ITER-4 → ITER-5 PER-EVAL DELTA")
print("=" * 92)
print(f"  {'eval':<42} {'iter-4 with':<14} {'iter-5 with':<14} {'Δ':<8}")
for ed in EVAL_ORDER:
    w4, _ = cell_mean(iter4_rows, ed, "with_skill")
    w5, _ = cell_mean(iter5_rows, ed, "with_skill")
    print(f"  {ed:<42} {w4:.0%}{'':<10}  {w5:.0%}{'':<10}  {w5 - w4:+.0%}")

result = {
    "iteration": 5,
    "model": "claude-sonnet-4-6",
    "n_per_cell": 3,
    "skill_change_vs_iter4": "fast-track template requires explicit Cynefin + Tier labels",
    "grader": "isolated agent, blinded to condition, strict bucket-evidence rules",
    "iter5": iter5_summary,
    "iter4_comparison": iter4_summary,
    "raw_iter5": iter5_rows,
}
(ITER5 / "benchmark.json").write_text(json.dumps(result, indent=2))
print()
print(f"Wrote {ITER5 / 'benchmark.json'}")
