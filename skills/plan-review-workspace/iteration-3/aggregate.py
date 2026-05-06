#!/usr/bin/env python3
"""Aggregate iter-3 benchmark results.

Per-cell pass counts are derived from the grading.json `assertions` array
(per-assertion `pass`/`passed`/`result == 'pass'`), with fallback to the
top-level summary keys. Schemas vary across agents because each was free-
form; this script normalises.

Tokens + wall time come from the harness-reported usage in the original
task notifications (recorded inline below) — agent-self-reported timings
were inconsistent and untrustworthy.
"""
import json
import statistics
from pathlib import Path

HARNESS_USAGE = {
    ("eval-roadmap-without-triage", "with_skill"):                {"tokens": 58030, "duration_ms": 128243},
    ("eval-roadmap-without-triage", "without_skill"):             {"tokens": 45181, "duration_ms":  75920},
    ("eval-prizecategoryselector-vue-removal", "with_skill"):     {"tokens": 55036, "duration_ms":  91995},
    ("eval-prizecategoryselector-vue-removal", "without_skill"):  {"tokens": 44207, "duration_ms":  63272},
    ("eval-clean-gem-bump", "with_skill"):                        {"tokens": 53622, "duration_ms":  62541},
    ("eval-clean-gem-bump", "without_skill"):                     {"tokens": 43515, "duration_ms":  62296},
    ("eval-schema-migration-no-rollback", "with_skill"):          {"tokens": 57002, "duration_ms": 123098},
    ("eval-schema-migration-no-rollback", "without_skill"):       {"tokens": 45178, "duration_ms":  84810},
    ("eval-redis-cache-solutionism", "with_skill"):               {"tokens": 56989, "duration_ms": 132402},
    ("eval-redis-cache-solutionism", "without_skill"):            {"tokens": 44167, "duration_ms":  74480},
}

EVAL_ORDER = [
    "eval-roadmap-without-triage",
    "eval-prizecategoryselector-vue-removal",
    "eval-clean-gem-bump",
    "eval-schema-migration-no-rollback",
    "eval-redis-cache-solutionism",
]

ITER3 = Path(__file__).parent

def assertion_passed(a):
    for k in ("passed", "pass", "met"):
        v = a.get(k)
        if isinstance(v, bool):
            return v
    if "result" in a and isinstance(a["result"], str):
        return a["result"].lower() in ("pass", "passed", "met", "true")
    return False

def normalise(grading):
    asserts = grading.get("assertions") or grading.get("expectations") or []
    if asserts:
        passed = sum(1 for a in asserts if assertion_passed(a))
        total = len(asserts)
        return passed, total
    s = grading.get("summary", {})
    passed = s.get("passed") or s.get("met") or s.get("pass_count") or 0
    total = s.get("total") or 0
    return passed, total

def load_grading(eval_dir, config):
    p = ITER3 / eval_dir / config / "run-1" / "grading.json"
    return json.loads(p.read_text())

rows = []
for ed in EVAL_ORDER:
    for cfg in ("with_skill", "without_skill"):
        g = load_grading(ed, cfg)
        passed, total = normalise(g)
        u = HARNESS_USAGE[(ed, cfg)]
        rows.append({
            "eval": ed,
            "config": cfg,
            "passed": passed,
            "total": total,
            "pass_rate": passed / total if total else 0.0,
            "tokens": u["tokens"],
            "duration_ms": u["duration_ms"],
        })

def stats(values):
    n = len(values)
    if n == 0:
        return (0.0, 0.0)
    mean = sum(values) / n
    sd = statistics.stdev(values) if n > 1 else 0.0
    return (mean, sd)

with_rows = [r for r in rows if r["config"] == "with_skill"]
without_rows = [r for r in rows if r["config"] == "without_skill"]

w_pr_mean, w_pr_sd = stats([r["pass_rate"] for r in with_rows])
b_pr_mean, b_pr_sd = stats([r["pass_rate"] for r in without_rows])
w_tok_mean, w_tok_sd = stats([r["tokens"] for r in with_rows])
b_tok_mean, b_tok_sd = stats([r["tokens"] for r in without_rows])
w_s_mean, w_s_sd = stats([r["duration_ms"] / 1000 for r in with_rows])
b_s_mean, b_s_sd = stats([r["duration_ms"] / 1000 for r in without_rows])

print("=" * 84)
print("ITER-3 BENCHMARK")
print("=" * 84)
print(f"With skill:    pass {w_pr_mean:.0%} ± {w_pr_sd:.0%}   tokens {w_tok_mean:7.0f} ± {w_tok_sd:5.0f}   wall {w_s_mean:6.1f}s ± {w_s_sd:5.1f}s")
print(f"Without skill: pass {b_pr_mean:.0%} ± {b_pr_sd:.0%}   tokens {b_tok_mean:7.0f} ± {b_tok_sd:5.0f}   wall {b_s_mean:6.1f}s ± {b_s_sd:5.1f}s")
print(f"Delta:         pass {w_pr_mean - b_pr_mean:+.2f}              tokens {w_tok_mean - b_tok_mean:+7.0f}              wall {w_s_mean - b_s_mean:+6.1f}s")
print()
print("Per-eval (with_skill / without_skill):")
print(f"  {'eval':<42} {'with':<12} {'without':<12} {'with-tok':<10} {'with-s':<7}")
for ed in EVAL_ORDER:
    w = next(r for r in rows if r["eval"] == ed and r["config"] == "with_skill")
    b = next(r for r in rows if r["eval"] == ed and r["config"] == "without_skill")
    print(f"  {ed:<42} {w['passed']}/{w['total']} ({w['pass_rate']:.0%})  {b['passed']}/{b['total']} ({b['pass_rate']:.0%})  {w['tokens']:<10} {w['duration_ms']/1000:<7.1f}")

result = {
    "iteration": 3,
    "model": "claude-opus-4-7",
    "summary": {
        "with_skill": {"pass_rate_mean": w_pr_mean, "pass_rate_sd": w_pr_sd,
                       "tokens_mean": w_tok_mean, "tokens_sd": w_tok_sd,
                       "wall_seconds_mean": w_s_mean, "wall_seconds_sd": w_s_sd},
        "without_skill": {"pass_rate_mean": b_pr_mean, "pass_rate_sd": b_pr_sd,
                          "tokens_mean": b_tok_mean, "tokens_sd": b_tok_sd,
                          "wall_seconds_mean": b_s_mean, "wall_seconds_sd": b_s_sd},
        "delta": {"pass_rate": w_pr_mean - b_pr_mean,
                  "tokens": w_tok_mean - b_tok_mean,
                  "wall_seconds": w_s_mean - b_s_mean},
    },
    "per_eval": rows,
}
(ITER3 / "benchmark.json").write_text(json.dumps(result, indent=2))
print()
print(f"Wrote {ITER3 / 'benchmark.json'}")
