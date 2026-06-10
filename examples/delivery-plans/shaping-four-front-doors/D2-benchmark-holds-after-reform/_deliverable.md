---
layer: deliverable
id: D2
title: Benchmark holds after reform
parent: ..
serves_kr: KR2
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR2 holds — the 5-scenario plan-review eval set re-run scores ≥90% pass with-skill
    after the reform, with results appended to docs/benchmarks.md.
---

# D2 — Benchmark holds after reform

**Serves:** KR2 *(brake)* — "the plan-review benchmark holds after reform: the 5-scenario
eval set re-run scores ≥90% pass with-skill" (baseline 93% ± 2%, n=3, Sonnet 4.6 —
`docs/benchmarks.md:52`, verified 2026-06-10).

This deliverable is the brake on D1's compression bet: line counts and gate greps prove form,
only the benchmark proves the compressed plan-review still *behaves*. One node — **N07**, an
experiment with `acceptance: true` — re-runs the existing harness against the reformed pack,
with the repair loop and the kill condition's second clause (below 80% after two repair
attempts) encoded in its success metric. No Rule A1 trigger: nothing here is decided, only
measured.

## Nodes

- [N07 — Benchmark re-run post-reform](N07-benchmark-rerun.md) · `experiment` · `acceptance`

## Done when

KR2 is observed: the re-run aggregate is ≥90% with results appended to `docs/benchmarks.md`.
Irreducible to D1's children being done — hence the acceptance flag on N07; close it last.
