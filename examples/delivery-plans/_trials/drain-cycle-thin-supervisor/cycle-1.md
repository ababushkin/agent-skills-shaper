# N05 Cycle 1 trial note — pointer-only prompt validation

Date: 2026-06-16
Cycle: `9e17380f` (current Linear cycle)
Status: **pending** — pre-condition not met at ABA-374 pickup

## Pre-condition check

The measurement window opens when N04's pointer-only template merges to `drain-cycle/main`.
At pickup (2026-06-16T12:26), N04's PR #29 (`collapse prompt to skill pointer, delete verify-flow machinery`) is submitted but not merged. Branch: `ABA-371`.

**No post-re-scope drain sessions exist.** All drain-cycle runs on 2026-06-16 used the old inlined prompt.

## Baseline measurements (pre-merge)

### 1. Prompt template line count

| State | Count | Notes |
|---|---|---|
| Current (main) | 175 lines (`prompt.py`) | four preamble variants + two tails + helpers |
| Target (N04 branch) | 9 lines emitted (non-resumed), 12 lines (resumed) | single `_preamble()` + `_TAIL` pointing at `/shape:exec:pickup` |

The template diff is in drain-cycle PR #29: commit `1ed6693` (collapse) + `66b57fb` (delete verify-flow machinery, `flow.py` removed, `runlog.py` `flow` field dropped).

ADR 0002 budget: ≤15 lines. N04 hits 9/12 — 3-line margin intact.

### 2. drain-cycle grade (runs before ABA-374 pickup)

Two drain-cycle sessions ran today:

| Run | Issues | Outcome | Prompt variant |
|---|---|---|---|
| T105539 (10:55–11:54) | ABA-373 Done (803s), ABA-328 Done (902s), ABA-393 halted (time cap, 1800s) | 2 Done / 1 halted | old inlined |
| T115934 (11:59–12:26) | ABA-393 Done (532s, $3.97), ABA-371 Done (1095s, $4.20) | 2 Done | old inlined |

ABA-371 in T115934 is N04 itself — the issue that writes the new template. Its drain used the old inlined prompt; the new template deployed to branch `ABA-371` after this session closed.

No post-re-scope session available. Cycle 1 grade: **pending**.

### 3. KR2 schema check

Tool: `drain_cycle/kr2_check.py` (from N03 branch `ABA-373`, not yet on `drain-cycle/main`).

Result over all `~/.drain-cycle/runs/*.json`:

```
exit 1 — every Done entry across all historical run logs is missing outcome_verdict and prep_verdict
```

This is the expected pre-N02/N03 baseline. N02 (verdict emission in pack skills, PR #52) and N03 (supervisor reads verdicts, PRs #22/#23) have not merged to their respective repos. The KR2 check itself (`kr2_check.py`) will only be available on main after N03 merges.

## Halt reason

All three measurements require post-re-scope drain sessions that do not exist at pickup. The experiment resumes after:

1. N04 PR #29 merges to `drain-cycle/main` (pointer-only template active)
2. N02 PR #52 merges to `agent-skills-shaper/main` (verdict emission active in pack skills)
3. N03 PRs #22/#23 merge to `drain-cycle/main` (supervisor reads verdicts; `kr2_check.py` available)
4. At least one full drain-cycle session completes with all three deployed

Kill condition: not yet applicable (requires 3 consecutive halted drains that the inlined prompt would have completed — no post-re-scope drains have run).
