# Plan review: execution-workflow

## Plan reference

`docs/design-docs/execution-workflow/design-doc.md` (ABA-361 / N04 — Rule-A1 execution-workflow design doc). Pins the `exec:*` verb namespace (one-way door), the execution skill graph, and the inter-skill handoff contract. Blocks N05–N08.

## Inputs
- **Appetite**: design doc gating a 4-node deliverable (N05–N08); decision-once, not a single slice
- **Cynefin domain**: Complicated — knowable with expertise; namespace + contract design with a clear right answer reachable by analysis
- **Tier**: Full — selected because the plan contains a one-way-door decision (published verb namespace) AND gates > 5 downstream nodes

## Trigger
Auto-fire #4 (one-way-door decision — a published verb namespace is a public-API-class commitment that `drain_cycle/prompt.py` and initiative-C supervisor prompts will bind to literally). Trigger #2 also fires (gates multiple independently verifiable nodes).

## B1 — Problem framing
Opens problem-first: worker improvises, the issue's AC drops before the review step, non-Claude workers silently skip review. Measurable desired state tied to KR1 (≥4/5 drained issues reach Done with a merged PR + full review trail). **OVERTURNED** (no defect). Falsifying condition: if the Problem section had led with "we will adopt `exec:*`" before naming the failure mode — it does not.

## B2 — Scope clarity
| Item | Verdict | Falsifying condition |
|---|---|---|
| Renames N03's already-shipped `execution-review` skill to `exec:review` ("renamed-on-publication") — a mutation of a shipped D1 artefact, not declared in N04's "design doc only" charter | PARTIAL | Would be OVERTURNED if a one-line note in N03/N05 scope confirmed the rename is owned by N05 authoring, not silently assumed here. Right call, undeclared owner. |
| `breakdown-at-pickup` shown "inside `exec:pickup`" — unclear whether it is a sub-step or its own delegated skill; the front-door ≤200-line NFR depends on which | PARTIAL | OVERTURNED if the doc stated breakdown is a named delegation (consistent with the no-inlining NFR) rather than an inlined procedure. As drawn it reads as inlined, contradicting the P7 constraint two lines above. |
| Mandates two new carrier artefacts (`pickup-envelope.json`, `build-log.md`) that N05–N08 must author | OVERTURNED | These are the handoff contract — squarely in scope for a contract-defining design doc. |

No SUSTAINED scope drift. Two PARTIALs are documentation-clarity fixes, not blockers.

## B3 — Assumptions + evidence quality
| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| `drain_cycle/prompt.py`'s current verify-flow (`/shape:task`, `/shape:verify-implementation`, `/shape:pr-prepare`, `/shape:pr-respond`) can be migrated/aliased to `exec:*` | **0.1** (assertion — no audit performed) | Audit `drain_cycle/prompt.py` now — grep the literal verb strings it emits, confirm an alias path exists. The ticket's own Assumptions block flagged this **"to-verify — audit drain_cycle/prompt.py … before pinning the namespace."** The doc deferred it to open-question N10 *after* pinning. | **SUSTAINED** |
| Non-Claude inline-sequential dispatch yields review parity with the Claude-Agent fan-out | 0.5 (ADR-0003 prose asserts identical persona text; not yet drained) | N01 grader on first validation drain; acceptable to defer — fitness function already named | OVERTURNED |
| `/review` (bare) would collide with installed packs (`code-review`, `crit`, built-in `review`) | 5 (verifiable by listing installed commands; drives the Alt-1 rejection) | `ls .claude/commands` + installed-plugin scan | OVERTURNED |

One SUSTAINED, Confidence 0.1, and it is the load-bearing one: the namespace is the one-way door, and it was pinned without the audit the ticket required before pinning.

## B4 — Dependencies (Full)
| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Initiative C (`drain_cycle/prompt.py`) — the literal consumer of the front-door verb | "initiative-C owner" named, **not confirmed** the verb adopts cleanly | N10 (deferred) | SUSTAINED (same root as B3 row 1 — counts once) |
| Initiative B consolidation — consumes the naming table | Named; the table is provided here as the single source | n/a | OVERTURNED |
| Linear API, GitHub/Graphite | Named in operability with failure modes | n/a | OVERTURNED |

## B5 — Reversibility + ADR pairing (Full)
| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| `exec:*` verb namespace (prefix + leaf names) | **Yes** — 4 alternatives, each with blast radius + reversal cost; rejection reasoning sound (Alt 3 `drain:*` rejected on the initiative-C coupling premise — holds up) | **No ADR committed.** ADR 0003 exists for personas; the namespace — a higher-blast-radius decision — gets only an `in-review` design doc | **PARTIAL** |

The alternatives discipline is genuinely strong (this is the doc's best section). The gap: a one-way-door namespace that five skills + two external prompts will bind to should be captured in an ADR, not only in an `in-review` design doc that downstream authors won't re-read. Recommend committing an ADR (or flipping this doc to `accepted` and treating it as the namespace ADR of record) before N05 binds.

## B6 — Operability + success metrics (Full)
- Metrics: **named** — time-to-PR, AC-pass-rate at `exec:verify`, persona finding count by class/severity, `exec:debug` escalations, post-push manual fix commits
- Alerts: **named as deliberately none** — drain volume too low; N09 drain is the alert surface (justified)
- Rollback path: **named** — 4-step verb-rename redirect with a per-step validation-drain gate
- Runbook: partial — failure modes enumerated with mitigations; no standalone runbook (acceptable at this stage)
- Capacity headroom: **named** — envelope ≤2 KB/drain
- User-visible outcome metric: **named** — KR1 (drained issues reaching Done with merged PR + full trail) is an outcome, not a delivery metric

Strongest bucket. **OVERTURNED.**

## B7 — Sequencing + capacity (Full)
Critical path surfaced: N04 blocks N05–N08; the whole-graph walking skeleton is explicitly placed at the N05 skeleton task (Rule B2 satisfied, correct read). Two structural decisions are deferred to N05 authoring (`exec:verify`/`exec:review` collapse; envelope schema versioning) — acceptable as open questions *provided* the handoff-contract table is marked provisional where the collapse would rewrite it. Minor. No SUSTAINED.

## B8 — Pre-mortem (Full — top 3)
1. **(most likely)** The namespace is pinned and N05–N08 bind to `exec:*`; only at N10 does the deferred `drain_cycle/prompt.py` audit reveal the `/shape:*` verify-flow cannot be cleanly aliased — forcing exactly the coordinated cross-drainer migration this doc exists to prevent. *Kill-switch:* run the audit **before** N05 authoring binds the names (collapses B3-row-1 + B4-row-1).
2. Envelope field drift across six independently-authored skills; a field renamed in one and not the others surfaces only at the N09 drain, after all are written. *Kill-switch:* commit a shared envelope schema (or schema lint) at N05, not "later if drift recurs."
3. The N05 author resolves the `exec:verify` vs `exec:review` collapse by merging them, silently invalidating two rows of the handoff-contract table. *Kill-switch:* decide now, or stamp those table rows "provisional pending N05 collapse decision."

No generic reasons; each names a specific mode with an early-catch condition.

## Recommendation
**REVISE** — the doc is well-structured and the alternatives analysis is strong, but it pins a one-way-door namespace while leaving the one assumption the ticket explicitly required verified-before-pinning at Confidence 0.1.

### Conditions
1. **(blocking, B3/B4)** Perform the `drain_cycle/prompt.py` audit the ticket's Assumptions block required *before pinning* — grep the literal verb strings the supervisor emits and confirm a clean alias/migration path to `exec:*`. Fold the result into the doc; if no clean path exists, scope the supervisor-prompt rewrite here rather than deferring to N10. This is the named condition that moves the load-bearing assumption above Confidence 5.
2. **(blocking, B5)** Commit an ADR recording the `exec:*` namespace decision (or promote this doc from `in-review` to `accepted` and designate it the namespace record of record), so downstream authors bind to a decision of record, not an in-review draft.
3. **(non-blocking, B2)** Add one line declaring that the N03→`exec:review` rename is owned at N05 authoring, and clarify whether `breakdown-at-pickup` is a named delegation (per the no-inlining NFR) or an inlined sub-step.
4. **(non-blocking, B7/B8)** Mark the `exec:verify`/`exec:review` rows of the handoff-contract table provisional pending the N05 collapse decision.

Conditions 1–2 must be addressed before the doc is accepted and N05 picks up. Conditions 3–4 are clarity fixes that can land in the same revision.

## Resolution (2026-06-10)

All four conditions addressed in the same revision; doc moved to `status: accepted`.

1. **Closed.** Supervisor-binding audit performed against current `drain_cycle/prompt.py`: only `/code-review-and-quality` (4 string locations) and `/shape:task` (verify-flow directive) are live bindings; the rest of the completion sequence is inlined prose. Migration to `exec:*` is a bounded string swap + additive replacement, scheduled at the N10 pointer-swap — no coordinated cross-drainer migration. The audit also corrected a factual error: `/shape:verify-implementation`, `/shape:pr-prepare`, `/shape:pr-respond` are not in current source (only in `.entire/` history). Folded into the doc's Context section and Open question Q1 (now RESOLVED). Assumption Confidence 0.1 → ~8 (verified by reading source).
2. **Closed.** `ADR 0004 — Execution verb namespace` committed as the decision of record; doc promoted to `accepted` and cross-linked. Downstream skills bind to ADR 0004.
3. **Closed.** N03→`exec:review` rename declared owned at N05 authoring; `breakdown-at-pickup` renamed `exec:breakdown` and shown as a named delegation (Rule P7), not an inlined sub-step.
4. **Closed.** `exec:review` and `exec:verify` rows of the handoff-contract table marked *provisional* pending the N05 collapse decision (Q2).

**Post-revision verdict: APPROVE.**
