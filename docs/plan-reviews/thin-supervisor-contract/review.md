# Plan review: thin-supervisor-contract

## Plan reference

`docs/design-docs/thin-supervisor-contract/design-doc.md` (ABA-370 / C-D1-N01 — Rule-A1 design doc). Decides three things: the ≤15-line worker prompt template's segment allocation, `.drain-handoff.json` schema v2 (verdict fields + halt-reason taxonomy), and the process/workflow boundary chart for every concern `drain_cycle/` carries today. Extends A/N04's inter-skill handoff contract with the supervisor-seam columns. Blocks N02, N03, N04.

## Inputs

- **Appetite**: design doc gating a 3-node deliverable (N02–N04 here, plus initiative B/C work that will reference the boundary chart); decision-once, not a single slice
- **Cynefin domain**: Complicated — the supervisor source has been audited (A/N04's binding audit + this doc's segment classification table); the right answer is reachable by analysis from one inspectable codebase
- **Tier**: Full — selected because the plan contains a one-way-door decision (handoff schema bound by two repos and a future-vendor worker) AND gates ≥3 downstream nodes

## Trigger

Auto-fire #4 (one-way-door decision — `.drain-handoff.json` schema is bound by drain-cycle and the pack's `exec:*` skills across two repos; rename costs a coordinated edit). Trigger #2 also fires (gates multiple independently verifiable nodes).

## B1 — Problem framing

Opens problem-first: the prompt today inlines the workflow it expects the worker to follow, creating two sources of truth and a vendor-portability hole; the handoff carries grade-points but not inspection-points. Measurable desired state tied to KR3 (`wc -l` + grep) and KR2 (one parseable run-log entry per exit). **OVERTURNED** (no defect). Falsifying condition: a Problem section that led with "we will collapse `prompt.py`" before naming the failure mode — it does not.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| The doc carries the `halt_reason` taxonomy as a *closed set* | **OVERTURNED** | A closed set with a documented extension path (one-line schema edit) is the right shape here — open strings drift silently across the two repos; the closed set surfaces drift at parse |
| `flow.py` deletion is named in the boundary chart but the supervisor-side rewrite cost is not quantified | PARTIAL | OVERTURNED if N02's task breakdown lists the `flow.py` deletion as a named slice; this doc legitimately defers cost to the build node, but the reader has to trust the breakdown will surface it |
| The schema fitness function points at `references/drain-handoff-schema-v2.md` | **OVERTURNED → resolved in-session** | the contract artefact lands at the design-doc surface (this commit), not as a build-node deliverable; N03 + N04 read it as a contract reference. Matches Condition 3 below |
| Prompt template's 13-line budget leaves only 2 lines of margin under the 15-line cap | PARTIAL | OVERTURNED if a future process-fact addition forces a re-negotiation through plan-review rather than a silent template edit. The doc states this explicitly ("not silently raised"); the discipline is named |

No SUSTAINED scope drift. Three PARTIALs are governance-of-future-work points rather than blockers.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| A/N04 is accepted and stable enough that this doc can extend its handoff table without competing | **5** (verified — A/N04 carries `status: accepted` and a closed plan-review at `docs/plan-reviews/execution-workflow/review.md`) | Read A/N04's status field | OVERTURNED |
| `drain_cycle/orchestrator.py:505` resolves `stack` per-run from `--no-stack` + `push_to_main_repos` | 5 (A/N04's binding audit confirmed the supervisor source state; this doc cites it directly) | A/N04 audit record | OVERTURNED |
| `flow.py`'s verify-label branching can collapse into `exec:pickup` without losing the shape-task check-first behaviour | 2 (the current branch is a single label test + a body-parse for an existing Task-Shaper block; reasoning, not measured) | N02's pickup-envelope test fixture exercises the verify-flow path | PARTIAL — test named, fixture not yet authored |
| The 13-line template skeleton survives the next plausible process-fact addition (cycle id, sandbox id) | 2 (assertion — the template has been measured at 13 lines for the present fact set only) | N02's first build slice attempts the template emit; if a fact has to be added immediately, the brake re-negotiates | PARTIAL — governed |
| `prep_verdict.route == "human-review"` corresponds to a halt rather than a Done-equivalent state | 0.5 (open question Q1 — default reasoning, not measured against a live `shape:pr-prepare` run) | Open question Q1's resolution at N04 wiring | PARTIAL — flagged as Q1, owner named |

No SUSTAINED. Three PARTIALs each carry a named test or a flagged open question; none is silent. The most load-bearing one (the `flow.py` collapse) is fact-tested at N02 fixture authoring before any code lands.

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Initiative A's `pickup-envelope.json` shape (consumed by this contract as the in-flight carrier) | Same owner; A/N04 accepted; envelope columns owned in A/N04 | n/a | OVERTURNED |
| `drain-cycle` repo (consumes the template + schema v2; emits per-run handoffs) | Same owner; landing path is N02 (drain-cycle) + N04 (drain-cycle); cross-repo edges named per node in C's plan | Cycle planning slots C after A's D2 stack | OVERTURNED |
| `agent-skills-shaper` (this repo) — landing surface for the schema reference + `exec:*` skills updates | Same owner; N03 lands here | n/a | OVERTURNED |
| Linear MCP + workflow governance | Installed | n/a | OVERTURNED |

No cross-team dependencies; single-owner workspace.

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| `.drain-handoff.json` schema v2 (bound by two repos and a future vendor worker) | **Yes** — 3 alternatives (flat extension, versioned envelope, per-skill handoff files), each with blast radius + reversal cost; rejection reasoning sound (per-skill files break the single grade-point that KR2 commits to) | The design doc itself carries `status: accepted` and is the namespace record of record per the frontmatter note. No separate ADR — pattern matches A/N04's resolution (the doc *is* the record) | OVERTURNED |
| Prompt template segment allocation | **Yes** — 3 alternatives (process + minimal + pointer; inlined resume prose; pointer-only via env vars), with the pointer-only rejected on portability grounds (env-var conventions vary by worker) — same logic that ruled out `drain:*` in A/N04 | The template change is two-way (one-file revert restores prior behaviour); kill condition already encoded in the initiative ("3 consecutive halts → restore inlined tail") | OVERTURNED |
| Process-vs-workflow boundary chart | Implicit — the boundary chart *is* the alternatives table compressed: every row is a "kept process / moved workflow" decision with the reasoning in the body | The ambiguous edges (verify-flow routing, `/shape:task` directive, stack-mode signal) are called out by name with explicit allocations | OVERTURNED |

The doc lands its three one-way-door decisions with alternatives, named blast radius, and named reversal costs. The frontmatter explicitly says this doc *extends* A/N04 rather than competing with it — the namespace-record discipline that A/N04's plan-review forced.

## B6 — Operability + success metrics

- Metrics: **named** — `flow` distribution, `outcome_verdict.result` rate, `prep_verdict.route` split, `halt_reason` histogram, wall-clock per `flow`
- Alerts: **named as deliberately none** — single-user CLI; halt surface is stderr + run-log (justified)
- Rollback path: **named** — 3 ordered steps (template revert, parser revert, taxonomy extension), each with a verification gate
- Capacity headroom: **named** — handoff ≤4 KB/run; envelope ≤2 KB/drain (cited from A/N04); run-log trim cadence stated
- Known failure modes: **named with mitigations** — 5 rows (template re-grows, procedure verb leaks, writer/reader drift, taxonomy outgrown, envelope/handoff confusion)
- User-visible outcome metric: KR3 brake (mechanical, two greps) + KR2 schema-check one-liner — both outcomes, not delivery metrics

**OVERTURNED.** Operability is genuinely strong — every failure mode has a fitness function named on the same line.

## B7 — Sequencing + capacity

Critical path: this doc → N02 (drain-cycle template + `flow.py` deletion) ‖ N03 (pack skills write verdicts) → N04 (supervisor records verdicts) → N05 (validation cycles). The blockedBy edges already named per node in C's delivery plan, and bound as Linear edges at issue creation. Three open questions (Q1, Q2, Q4) defer cleanly to specific later nodes; Q3 has a stated default. Appetite-against-emit: this doc is the design surface for 5 nodes — under the initiative's ~7-issue cap, consistent with the under-emit flagged in C's README.

No SUSTAINED.

## B8 — Pre-mortem

Assume the doc shipped and the initiative failed within its appetite. Top 3, ranked:

1. **(most likely)** N02 collapses the template and a `flow.py`-equivalent reappears inside `exec:pickup` because the verify-flow routing turned out to need a per-issue body parse that the boundary chart claimed was "workflow only" but actually requires a process-side label-list shape the prompt template did not pre-encode. *Kill-switch:* the labels list is already on line 6 of the prompt; the N02 fixture exercises the verify-flow path before any `flow.py` deletion lands, surfacing the gap before it ships.
2. Schema v2 fields are written by `exec:verify` / `shape:pr-prepare` but with the wrong shape (e.g., `failed_ac` becomes `{ac_id: reason}` in one writer, `string[]` in another). *Kill-switch:* the NFR table commits a `jq` schema-fitness check on every run; the discipline lands at N03 schema-test authoring, before N04 wires the supervisor read. Drift fails parse at the writer, not at the reader.
3. The `halt_reason` closed set is too small — a fourth halt path appears at the first validation drain (N05) and the schema fails to parse the run. *Kill-switch:* the taxonomy extension cost is one schema-file edit and one writer update (per the design doc's own rollback step 3); cost is named in advance, so the response at N05 is "edit, re-run" not "renegotiate the contract."

Each pre-mortem names a specific mode with an early-catch condition; none is generic.

## Recommendation

**APPROVE** — the doc opens problem-first, names three decisions each with a clean alternatives table, pins KR3's grep pattern explicitly, and extends A/N04's handoff table in place (one source of truth across the two repos, exactly the pattern A/N04's REVISE forced into this initiative). Every NFR carries a fitness function. Open questions all have named owners and resolution gates.

### Conditions

1. **(non-blocking, B2 + B7)** When N02's tasks are broken out, list the `flow.py` deletion as a named slice rather than folding it silently into the template edit — gives the reviewer a single revertable commit.
2. **(non-blocking, B3 row 3)** N02's first task authors the pickup-envelope fixture that exercises the verify-flow path *before* `flow.py` deletes. The doc names this implicitly via "the labels list is at line 6"; making it the first slice of N02 closes the only sub-5-confidence assumption.
3. **(resolved in-session, B8 #2)** N03's pack-skill schema test reads the JSON Schema fenced inside `references/drain-handoff-schema-v2.md` (landed in this design-doc slice), not a future build-node artefact — keeps the schema as a contract artefact owned by this doc.

All three conditions are non-blocking. The doc is accepted; N02–N04 can break tasks against it.
