---
layer: node
id: N09
type: experiment
title: Validation drains (5 issues, ≥4/5)
parent: D2
serves_kr: KR1
maps_to: linear-issue
acceptance: true
external_window: none
completion:
  form: hypothesis+success-metric
  verifies_parent: D2
  hypothesis: >
    A drain-cycle worker on first-party skills alone completes ≥4 of 5 real issues to
    Done with a merged PR, zero manual fix commits after its final push, and the full
    review trail present.
  success_metric: >
    drain-cycle grade over ~/.drain-cycle/runs/*.json + git log scan for post-push fix
    commits + Linear/PR trail check = ≥4/5. Below 4/5 falsifies the bet; 3 consecutive
    manual-fix drains fires the initiative kill condition.
delegates_to: product-spike (experiment discipline — hypothesis, success metric, written finding)
---

# N09 — Validation drains (5 issues, ≥4/5)

**Type:** `experiment` · `acceptance: true` (verifies D2). Not a build node: its honest outcomes
are *confirmed* or *falsified*, not *shipped*. This is the node that grades the KR1 bet.

> **Blocked by:** [N05](N05-entry-skill-front-door.md)–[N08](N08-pr-finishing-graphite-first.md)
> (the skills under test) and
> [N10](../D3-cutover-off-third-party-packs/N10-drain-cycle-prompt-pointer.md) — the supervisor
> must point at the entry skill before a drain can exercise it.

> **▶ On pickup:** run the experiment and write the finding (confirmed / falsified) via
> `product-spike`.

## What

Drain 5 real issues of ordinary cycle work end-to-end through the new execution skills and grade
KR1: how many reach Done with a merged PR, zero manual fix commits after the worker's final push,
and the full review trail (verify verdict, What/Why/Focus PR body, review-summary comment).
Write the finding.

## Why

KR1 is the stretch bet, and only live drains can grade it — D1's fixture scores prove the review
gate, not the workflow; a skill that passes every dry run can still fail on a real issue's mess.
Rejected alternative: declare victory on dry runs and toy issues — the exact unverified-claim
failure this pack exists to prevent. This node carries `acceptance: true` because D2's Done is
irreducible to its children: every skill can individually pass and the workflow still fail
end-to-end. Close it last — D2 reaching 100% coincides with the KR observation.

## Completion

**Hypothesis:** a worker on first-party skills alone completes ≥4 of 5 real issues to Done +
merged PR with zero post-push manual fix commits and the full review trail.

**Success metric:** `drain-cycle grade` over `~/.drain-cycle/runs/*.json` + `git log` scan for
post-push fix commits + Linear/PR trail check = **≥4/5**, measured over the first 5 issues
drained after the skills land.

Below 4/5 **falsifies** the bet — D2 is re-shaped, not extended. Three consecutive drains
needing manual fixes or third-party fallback fires the initiative **kill condition** (reinstall
agent-skills, keep Shaper shaping-only, fold learnings into the README).

## Assumptions

- 5 issues of ordinary cycle work are available in the measurement window. *(verified — the backlog convention keeps a cycle/ops stream; the KR's own "measured over" clause anticipates this window)*

## Key Risks

- **Risk:** the 5 issues are too uniform (all markdown-pack work) and a 4/5 pass overstates
  generality.
  *Mitigation:* include at least one drain-cycle (Python) issue in the 5 so both repo types are
  exercised.

## Tasks

- [ ] `skeleton` — Drain the first validation issue end-to-end; record grade, post-push fix-commit count, and trail completeness in a trial note · Done when: the run log and trial note for issue 1 exist with all three measurements · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·M·L·L·L
- [ ] `acceptance` — Drain the remaining 4; evaluate the ≥4/5 success metric; write the finding (confirmed / falsified) — this finding is D2's Done condition · Done when: the finding is written with per-issue evidence links · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·M·L·L·L
