# Plan review: drain-cycle-thin-supervisor

## Plan reference

`examples/delivery-plans/drain-cycle-thin-supervisor/` — delivery plan for initiative C
("drain-cycle supervises; the pack owns the workflow", Linear project `b313da89`), emitted by
`delivery-shape` 2026-06-10. 3 deliverables / 5 nodes / 12 tasks; `bin/walk-delivery-plan` and
`bin/check-plan-framing` both green at review time.

## Inputs

- **Appetite**: ~7 issues (initiative cap); plan emits 5 nodes — under, flagged in README
- **Cynefin domain**: Complicated — bounded refactor + contract design, knowable with expertise;
  the one emergent surface (live cycle behaviour) is governed by an experiment node with a
  falsification condition rather than a deterministic milestone
- **Tier**: Full — selected because the plan contains a one-way-door decision (the
  supervisor↔worker contract, N01)
- **Trigger**: an LLM just produced the plan and the owner is about to bind it into Linear;
  auto-fire also holds (one-way door). Fast-track gate does not fire (not KTLO, multi-slice).

## B1 — Problem framing

**OVERTURNED** (no defect). The README opens with the outcome ("unattended cycle drains run with
the supervisor owning only process concerns…") and three measured KRs before any solution
content. *Falsifying condition:* the bet section opening with "rewrite prompt.py" instead of an
operator outcome.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| Per-issue stack/push-policy signal: `stack` is supervisor-resolved (`orchestrator.py:505`) and today reaches the worker only via the preamble variant N02 deletes; the plan didn't name how it survives | **SUSTAINED → resolved in-session** | N01's decision surface names the signal (fixed: What + Completion now require the segment allocation to carry it) |
| drain-cycle docs (AGENTS.md, README, design-decisions) will need rewriting when the prompt collapses — not named as scope | PARTIAL | at-pickup breakdown of N02 includes doc updates without new nodes; if it can't, scope was under-declared |
| "Procedure verb" grep is gameable as written (which verbs?) | PARTIAL → governed | N01's Completion now requires pinning the grep pattern; if the accepted doc omits it, this re-opens |
| `drain-cycle grade` itself (KR1 instrument) needs no verdict-awareness | OVERTURNED | grade reads `final_linear_state`/`exit_code` only — sufficient for "cycle drains to completion" |
| Overlap with A/N10 (pointer swap, code-review-and-quality purge) | OVERTURNED | grep of the plan finds the pointer swap only in Blocked-by callouts; N02's Why records the same fallback-rejection A/N10 made, scoped to the *remaining* template |

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| Initiative A's N04/N05–N08/N10 land before C's nodes are picked up | 2 (planned work, tracker-backed, not yet built) | Linear blockedBy edges at binding; cycle planning won't pull C before A's stack lands | PARTIAL — governed by edges |
| ≤15 lines fits all process segments (incl. resume + stack signal) | 0.1 (assertion — it is the KR target, not evidence) | N01's first task drafts the template and spends the budget line by line; a miss challenges the cap at plan-review, never silently | PARTIAL — test named |
| Verdicts can attach at A's verify/PR-finishing seams | 2 (contract exists in A's accepted plan, skills not yet authored) | read A/N04's accepted doc at N03 pickup; tagged *(to-verify)* in N03 | PARTIAL — test named |

All three are <5 confidence but each carries a named test or governing mechanism encoded in the
plan itself; none is silent.

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Initiative A issues (ABA-359–369) | yes — same owner, bound in Linear | A occupies the next cycle(s) first; C slots later by design ("third of three") | OVERTURNED |
| Graphite/gh tooling on the runner | yes — landed 2026-06-10 (stacking default) | n/a | OVERTURNED |
| Linear MCP + workflow governance | yes — installed, governs binding | n/a | OVERTURNED |

No cross-team dependencies; single-owner workspace.

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Handoff schema v2 + prompt-segment allocation | N01 task 1 requires ≥2 drafted alternatives with trade-offs | committed — N01 is a design-doc node accepted through plan-review; amends A/N04's handoff table in place (one source) | OVERTURNED |
| Prompt collapse itself | two-way door — one-commit revert + kill condition restores inlined tail | n/a | OVERTURNED |

## B6 — Operability + success metrics

- Metrics: named — `drain-cycle grade`, `wc -l` on template, KR2 schema check
- Alerts: n/a (single-user CLI); halt surface is stderr + run-log `halt_reason`, documented
- Rollback path: named — kill condition restores the inlined tail, re-scope kept to guardrails + logging
- Runbook: drain-cycle halt/resume semantics already documented in its repo; N02/N04 fold doc updates in
- Capacity headroom: n/a
- User-visible outcome metric: ≥1 clean full-cycle drain with zero manual fix commits (outcome, not output)

## B7 — Sequencing + capacity

Critical path surfaced: N01 → {N02, N03, N04} → N05, with cross-initiative edges (A/N05, A/N08
stack, A/N09, A/N10) named per node and bound as Linear blockedBy at binding time — which also
fixes the Graphite stack order per repo. Appetite is a fixed cap (~7; emitting 5, under-run
flagged with its reason in the README — subtractive re-scope, no padding). Single-owner FTE
consistent with a one-cycle drain plus a two-cycle measurement window.

## B8 — Pre-mortem

Assume the plan shipped and failed within its appetite. Top 3, ranked:

1. **The pointer-only worker under-performs on real cycles** — the prose that kept weaker
   contexts on rails is gone, and drains halt mid-cycle. *Kill-switch:* the initiative kill
   condition (3 consecutive halts the inlined prompt would have completed), with N05's
   per-halt judgement note making "would have completed" decidable.
2. **Initiative A slips and C's nodes sit blocked**, draining nothing in their cycle slot.
   *Kill-switch:* blockedBy edges make the block visible at cycle planning — C is not pulled
   into a cycle until A's D2 stack has landed; no mid-cycle discovery.
3. **Schema-v2 drift between the two repos** (pack writes ≠ supervisor reads), silently nulling
   KR2. Mitigated structurally: one schema table (N01 amends A/N04's), and N04's fixture test
   parses a handoff written verbatim from it — drift fails a test before it fails a drain.

## Recommendation

**APPROVE** — the one SUSTAINED finding (stack/push-policy signal absent from the contract's
decision surface) was fixed during review: N01's What and Completion now require the segment
allocation to carry the per-issue stack signal and to pin KR3's procedure-verb grep pattern.
Both mechanical gates re-run green after the edit.

### Conditions

1. Bind the blockedBy edges (intra-plan: N01 → N02/N03/N04; N02+N03+N04 → N05; cross-initiative:
   A/N05+A/N10 → N02, A's D2 stack → N03, A/N09 → N05) when the issues are created — the plan's
   sequencing and the Graphite stack order both depend on them.
2. N01's accepted doc must spend the ≤15-line budget explicitly (line-by-line) — a budget miss
   goes back through plan-review as a KR challenge, never a silent overrun.
