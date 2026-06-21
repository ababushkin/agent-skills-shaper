# Design doc: role-based review panel for `exec:review`

- **Status:** Draft — ready for review
- **Date:** 2026-06-21
- **Author:** Anton Babushkin
- **Routed from:** `docs/idea-bank/role-based-review-panel.md` (shape:idea → shape:design, Track A)
- **Trigger:** architecture decision spanning ≥5 verifiable slices, with a one-way-door risk (ADR 0003 / D1 acceptance harness)

---

## Context — why this change

`exec:review` is the GO/NO-GO gate run before any issue moves to Done. Today it dispatches
three personas — `spec-compliance`, `security-auditor`, `code-quality` — each a narrow,
near-deterministic pattern matcher tuned to one seeded defect class. A complete five-axis
judgement reviewer (`agents/code-reviewer/AGENT.md`) already exists but **no skill dispatches
it**. So whole review disciplines a senior team would catch — architecture, correctness,
reliability/resilience, intent — pass unreviewed, and the gate reports GO when it has not
reviewed those disciplines.

The fix: replace the three narrow personas with a **role-based judgement panel** — one persona
per discipline, always-on personas plus conditional personas dispatched by the surface the diff
touches — while keeping the cheap mechanical floor that proves the gate never silently loses
coverage on the three enumerable classes.

---

## Problem

- **Affected users:** the implementing/review agents that run `exec:review`, and the human who
  trusts its GO/NO-GO verdict before marking an issue Done.
- **Current behaviour:** three personas check three enumerable defect classes
  (`ac-violation`, `security-hole`, `type-suppression`). A diff with an architecture flaw, a
  correctness bug, a resilience gap, or a subtly-wrong-intent implementation passes the gate
  with zero findings.
- **Desired behaviour:** the gate reviews the disciplines a senior team reviews, dispatches the
  right personas for the surface the diff touches, and still proves — cheaply and continuously —
  that it has not lost coverage on the three enumerable classes.

No measurable runtime baseline exists (Markdown pack, no `docs/app-context.md`). The aim is
qualitative discipline coverage, with one hard fitness number: grader recall on the seeded corpus.

---

## Context and constraints

**Artefacts loaded:** ADR 0003 (persona contract + dispatch), `skills/exec-review/SKILL.md`,
`agents/code-reviewer/AGENT.md`, `docs/sub-agent-anatomy.md`, the three `personas/*.md`,
`hooks/stop-the-line/HOOK.md`, `bin/grade-execution-review`, the `fixtures/execution-review/`
corpus, and the drain-cycle consumption surface (`handoff.py`, `kr2_check.py`, `grade.py`,
`orchestrator.py`, `prompt.py`).

**Findings that reshape the original spike scope:**

1. **The grader greps triples out of free text.** `bin/grade-execution-review` runs each
   persona `.md` as a `claude -p` system prompt and matches `^<file> <class> <Critical|Required>$`
   on stdout. A persona that emits prose *and* a triple line is already grader-compatible — the
   grep ignores prose. So "extend the contract to allow prose alongside triples" needs **no
   grader change** and **no ADR superseding**; the triple stays mandatory only for a graded class.

2. **drain-cycle does not consume the review finding format — the cross-repo "one-way door" is
   mostly not one.** `handoff.py` reads only the `verify` section (AC pass/fail) and
   `finish.pr_urls` from `exec-state.json`; it never parses the `review` section. The `findings`
   in `handoff.py`/`orchestrator.py`/`runlog.py` are *verify*-section failed-AC items, not
   `exec:review` defect triples. The triage conflated two `grade` tools: `drain_cycle/grade.py`
   (silent-Done check on `outcome_verdict`) vs shaper's `bin/grade-execution-review` (triple-recall
   grader). Only the shaper-internal one cares about the format.
   **The single real cross-repo constraint:** `prompt.py` instructs the worker in natural language
   to "fix any Critical or Required findings" — so the **severity vocabulary**
   (`Critical`/`Required`/`Suggested`) must stay stable. The triple *format* is free to change.

3. **`type-suppression` is mechanical and already owned by `stop-the-line`.** The `code-quality`
   persona greps for silenced errors / `//nolint` / discarded `ok` checks — stack-flavored Go
   patterns that (a) violate the pack's stack-agnostic rule and (b) duplicate the `stop-the-line`
   hook's deterministic suppression scan. `sub-agent-anatomy.md` is explicit: mechanical checks
   belong in a hook, not a persona. This grounds the decision to retire `code-quality` as a
   judgement persona.

**Constraints (NFRs — qualitative pack, so mostly fitness functions, not latency numbers):**

| Requirement | Fitness function |
|---|---|
| Gate never silently loses coverage on the 3 enumerable classes | `bin/grade-execution-review fixtures/execution-review` ≥ 9/10 recall — runs during persona authoring (CI-free pack; run by author + on the grader's own change) |
| Judgement axes actually catch discipline defects | Held-out diff corpus with expected verdicts + periodic human spot-check (new harness; see Open Questions) |
| Finding format does not drift silently | Triple-format lint on graded personas (ADR 0003 N03 note); prose personas need no triple |
| Severity vocabulary stable for drain-cycle | `Critical`/`Required`/`Suggested` unchanged; assert in review-summary template |
| Personas stay portable to non-Claude workers | Prose is free-text after the (optional) triple — inline-sequential path already handles it; no harness change |
| Persona length | ≤ 150 lines (sub-agent-anatomy hard cap), Frontier tier each |
| **Stack-agnostic** — no persona or the suppression floor may prescribe a language/stack | Detection and prose are written stack-agnostic; concrete patterns appear only as labelled examples (the `stop-the-line` placeholder style), never as the rule. Pack constraint, restated here because the retired `code-quality` persona violated it. |

---

## Alternatives

**Alt 0 — Do nothing.** Effect: the gate keeps passing architecture/correctness/
reliability defects; it reports GO without reviewing them. Reversal cost: zero (no change).
Rejected: the gate's core promise is unmet.

**Alt 1 — One layer, judgement personas also emit triples (triage's literal recommendation).**
Every discipline becomes a Frontier judgement persona; the ones owning an enumerable class emit
prose + the gradable triple. Scope: medium — the grader grades judgement personas
directly. Reversal cost: low (revert persona files). Weakness: forces a Frontier judgement
reviewer to also be a deterministic triple-emitter for `type-suppression`, which is mechanical
and stack-specific — the same problem `code-quality` has. Keeps a persona the anatomy doc says
should be a hook.

**Alt 2 — Two-tier: Fast mechanical scanners (grader floor) + Frontier judgement panel
(recommended).** Mechanical enumerable-class detection lives in Fast-tier leaf checks /
the `stop-the-line` hook; the judgement panel is the real review. The two graded classes that a
judgement persona *does* own cleanly (`ac-violation` → spec-compliance; `security-hole` →
security-engineer) emit the triple as a by-product so the grader grades them directly;
`type-suppression` is re-anchored on a Fast leaf check consolidated with `stop-the-line`. Scope:
medium. Reversal cost: low. Strength: implements the confirmed model-tier rule
("Frontier for every review persona; Fast only for a mechanical, deterministic leaf check")
exactly, and retires `code-quality` as a persona.

**Alt 3 — Full retire of ADR 0003's triple + grader.** Drop the mechanical floor entirely; rely
only on held-out judgement eval. Scope: **high — the genuine one-way door**: breaks D1/KR2's
seeded-recall acceptance harness. Reversal cost: high (re-derive the corpus + grader contract).
Rejected: throws away a cheap, working regression guard for no benefit.

---

## Recommended approach — Alt 2

**Two tiers, one skill.**

**Tier 1 — Fast mechanical floor (keeps the grader green).** Deterministic enumerable-class
detection, reclassified from "judgement personas" to Fast leaf checks. `type-suppression`
detection consolidates with the `stop-the-line` hook (a single mechanical suppression check).
This tier is *not* the review; it is the regression floor `bin/grade-execution-review` exercises
during authoring.

**Tier 2 — Frontier judgement panel (the review).** One role-based persona per discipline:

- **Always-on (every diff):**
  - `spec-compliance` — did we build what the AC asked? (emits the `ac-violation` triple as a
    by-product when it finds a removed/disabled AC, so the grader grades it directly)
  - `correctness` — does what we built actually work? logic, edge cases, broken behaviour
  - `intent-alignment` — did the work achieve the intent *behind* the AC, not just the literal
    AC? Own persona. Stays silent on most diffs; escalates to a human on a critical intent/result
    deviation. This persona would have caught the 2026-06-18 grep-for-absence AC that passed
    trivially.
- **Conditional by surface:**
  - `system-architect` — boundaries, coupling, complexity proportionality
  - `security-engineer` — input validation, secrets, injection (emits the `security-hole` triple
    as a by-product, so the grader grades it directly)
  - `performance` — N+1, unbounded loops, hot-path allocations (structural, not profiling)
  - `reliability-resilience` — **new persona**: failure modes, retries/timeouts/idempotency,
    partial-failure and rollback behaviour
  - `readability-quality` — naming, comment quality, surgical scope (the *judgement* successor to
    `code-quality`; mechanical suppression detection stays in the hook)

All panel personas: Frontier tier, prose verdict + severity, ≤150 lines, authored to
`sub-agent-anatomy.md`.

**Surface-detection heuristic (which conditional personas fire):**

| Surface signal (path + content) | Fires |
|---|---|
| Always | spec-compliance, correctness, intent-alignment |
| DB schema / migration / query files | reliability-resilience, system-architect |
| Auth / crypto / input-boundary / deserialization | security-engineer |
| Hot path / loops / N-query patterns / batch jobs | performance |
| Public API / module boundary / new package | system-architect |
| Error handling / retry / timeout / external-call code | reliability-resilience |
| Any non-trivial logic change | readability-quality |

Detection is best-effort path + content matching; when ambiguous, dispatch the persona (firing
wrongly costs one dispatch, a miss costs a defect class). Documented in the SKILL and ADR 0003.

**De-duplication:** split `agents/code-reviewer/AGENT.md`'s five axes into the individual
conditional personas above; **delete the standalone agent** so review happens in one place.

**Contract change — extend ADR 0003, do not supersede it:**
- A persona may emit a prose verdict + severity (judgement output). The leading triple stays
  **mandatory only for a graded enumerable class** the persona owns; pure judgement personas emit
  no triple.
- Record the two reviewer types (Fast mechanical scanner vs Frontier judgement persona) and the
  model-tier rule.
- Add the conditional-dispatch surface heuristic alongside the existing parallel /
  inline-sequential dispatch protocol (which is unchanged and still portable).
- No superseding ADR: the triple survives for the graded classes; the grep-based grader is
  untouched.

**Update `sub-agent-anatomy.md`:** tier table changes from "focused lane = Balanced" to "review
persona = Frontier; mechanical leaf check = Fast" — matching the confirmed rule.

---

## Consequences

**Positive:** the gate reviews real disciplines; one review path (no dormant duplicate);
mechanical detection sits where the anatomy doc says it belongs (the hook); the grader floor
survives unchanged; no cross-repo lockstep change.

**Negative / costs:** more personas to author and maintain (8 panel + floor); conditional
dispatch adds a surface-detection step that can mis-route (mitigated by fire-when-ambiguous);
the judgement axes have no automated grader yet — they need a held-out eval that does not exist.

**Walking skeleton:** yes — build in this order so each slice is independently verifiable:
1. Extend ADR 0003 + update `sub-agent-anatomy.md` (contract first).
2. Author `correctness` + `reliability-resilience` + `intent-alignment` (the net-new always-on
   value), wire into `exec:review`, confirm grader still ≥9/10 via the surviving
   spec-compliance/security floor.
3. Split `code-reviewer` axes into `system-architect` / `performance` / `readability-quality` /
   `security-engineer`; delete the standalone agent.
4. Add conditional dispatch + surface heuristic to the SKILL.
5. Stand up the held-out judgement eval.

Estimates beyond this skeleton are uncalibrated until the contract slice lands.

---

## Operability — adapted for a Markdown pack

- **Fitness functions:** grader recall ≥9/10 (the floor); held-out judgement eval + human
  spot-check (the panel). Both named above.
- **Drift detection:** triple-format check on graded personas; severity-vocabulary assertion in
  the review-summary template (protects drain-cycle's NL coupling).
- **Rollback:** git revert of the persona files + SKILL + ADR — ordered reverse of the skeleton;
  the grader is the per-step verification gate (must stay ≥9/10 after each revert).
- **Failure modes:** (a) judgement persona emits no actionable file/class → review-summary names
  file + discipline per finding; (b) surface heuristic misses a class → fire-when-ambiguous + the
  always-on trio backstops; (c) grader regresses on a refactor → authoring gate catches it before
  merge.
- **Dependency failure:** drain-cycle drift — bounded to the severity vocabulary; assert it.

---

## Open questions

| # | Question | Owner | Resolution gate |
|---|---|---|---|
| 1 | Held-out judgement eval: what corpus + expected-verdict format, and run cadence (author-time vs periodic)? | Anton | Blocks skeleton slice 5; panel ships without it but coverage of judgement axes is unproven until it exists |
| 2 | ~~`type-suppression` floor placement~~ **Resolved:** fold onto `stop-the-line` — **conditioned on the detection being stack-agnostic** (the hook already is; the Go-specific `code-quality` persona was not). The grader's Go fixtures are example instances of stack-agnostic patterns, not the rule. Remaining sub-task: the small grader-harness tweak so the `type-suppression` fixture grades the hook, not a persona `.md`. | Anton | — |
| 3 | Does any *other* drain-cycle consumer (beyond the audited 5 modules) read the `review` section? Audit confirmed none in `drain_cycle/*.py`, but verify no external script greps the review-summary comment. | Anton | Blocks any change to the review-summary block shape |

---

## Appendix — implementation outline (for the follow-up build, not part of this doc's acceptance)

**Files created:**
- `personas/correctness.md`, `personas/intent-alignment.md`, `personas/reliability-resilience.md`,
  `personas/system-architect.md`, `personas/performance.md`, `personas/readability-quality.md`,
  `personas/security-engineer.md`

**Files modified:**
- `docs/adr/0003-persona-contract-and-dispatch-protocol.md` — extend (prose + conditional dispatch)
- `skills/exec-review/SKILL.md` — new roster, conditional dispatch, surface heuristic
- `docs/sub-agent-anatomy.md` — tier table → Frontier/Fast
- `hooks/stop-the-line/HOOK.md` — absorb `type-suppression` floor; keep stack-agnostic placeholders
- `bin/grade-execution-review` — small harness tweak so the `type-suppression` fixture grades the hook, not a persona `.md`
- `personas/spec-compliance.md`, `personas/security-auditor.md` — reframe as Fast floor scanners (or
  fold into the judgement personas that emit their triple as a by-product, per the contract)

**Files deleted:**
- `agents/code-reviewer/AGENT.md` (axes split into conditional personas)
- `personas/code-quality.md` (retired; detection moves to the hook)

**Verification:**
- `bin/grade-execution-review fixtures/execution-review` exits 0 (≥9/10 recall) after each slice.
- `exec:review` dispatches the always-on trio on every diff and the right conditional personas per
  the surface table (spot-check against 3–4 representative diffs).
- `agents/code-reviewer/AGENT.md` no longer referenced anywhere (`grep -r code-reviewer`).
- Severity vocabulary `Critical`/`Required`/`Suggested` unchanged (drain-cycle `prompt.py` NL coupling).
- Held-out judgement eval runs and reports per-axis verdicts (once OQ#1 resolved).

---

## Related

- `docs/idea-bank/role-based-review-panel.md` — upstream triage record
- `docs/adr/0003-persona-contract-and-dispatch-protocol.md` — contract this doc extends
- `skills/exec-review/SKILL.md`, `agents/code-reviewer/AGENT.md`, `personas/*.md` — artefacts changed
- `hooks/stop-the-line/HOOK.md` — absorbs the `type-suppression` floor
- `docs/sub-agent-anatomy.md` — model-tier rule updated by this design
