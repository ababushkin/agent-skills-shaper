---
name: execution-workflow
status: accepted
authors: Anton Babushkin
created: 2026-06-10
last_updated: 2026-06-10
supersedes: none
namespace_record: this doc + ADR 0004 are the record of the `exec:*` namespace decision; downstream skills bind to ADR 0004.
---

# Execution workflow — verb namespace, skill graph, handoff contract

## Problem

A drain-cycle worker picks up a Linear issue and must reach a merged PR with the full review trail. Today the worker improvises: there is no single front-door skill, no agreed verb namespace for the execution-side skills, and no contract for what each step receives from the previous one or hands to the next. The acceptance criteria written on the issue do not reliably reach the review step — reviewers grade code quality but cannot grade *built the wrong thing* because the AC never travelled. Workers running on non-Claude surfaces (codex, kimi) have no tool to fan out reviews and silently fall back to no review at all.

Affected parties: drain-cycle workers (every drained issue), reviewers (the persona dispatch in N03 + the human reading PRs), the supervisor prompt in initiative C (a single pointer is impossible until the front-door skill exists), the initiative B consolidation (cannot consolidate verbs it does not own).

Current behaviour: ad hoc steps, ad hoc names, AC drops between issue and review, no fan-out outside Claude Code. Desired behaviour: a named verb namespace, a graph of named delegations, and a single handoff contract that carries the issue's AC end-to-end on every worker surface this pack targets.

## Context

D1 has landed: ADR 0003 pins the persona contract (file format + `file:line · class · severity` finding triples + the Claude-Code-Agent / inline-sequential dispatch branches); N03's `execution-review` skill consumes that contract. N01 ships the fixture corpus + grader. D2's bet (KR1 — ≥4/5 drained issues reach Done with a merged PR and full review trail) lives in N05–N08, all blocked by this design doc.

The verb namespace is a one-way door. `drain_cycle/prompt.py` and any sibling supervisor prompt in initiative C will name these verbs literally; once workers' muscle memory and external prompts bind, a rename costs a coordinated migration across every drainer. Shaping verbs (`shape:*`) are already established — this doc names execution verbs only, but reserves both halves of the namespace in a single table so initiative B's consolidation has one source of truth.

**Supervisor-binding audit (performed before pinning, per the N04 to-verify assumption).** A read of current `drain_cycle/prompt.py` (and a grep of the rest of the drain-cycle source tree) shows the supervisor today emits exactly two execution-side verbs literally:

- `/shape:task` — once, only on `verify`-labelled issues, via the shape-task directive (check-first against an existing Task-Shaper block in the issue body).
- `/code-review-and-quality` — hard-coded in four string locations (`_TAIL`, `_STACK_TAIL`, and the numbered completion sequence in both the normal and stack preambles).

The rest of the completion sequence (commit/push → review-summary comment → Linear Done transition) is **inlined as prose in the preamble, not delegated to named verbs.** The `/shape:verify-implementation`, `/shape:pr-prepare`, and `/shape:pr-respond` verbs that an earlier draft of this doc assumed were live appear only in drain-cycle's `.entire/` git history — they are *not* in current source. Migration consequence: adopting `exec:*` is a **bounded string swap plus an additive replacement**, not a coordinated cross-drainer migration — see Open question Q1 (resolved) for the exact cutover.

Predecessor packs are tracker-blind: `addyosmani/agent-skills` (`/spec`, `/plan`, `/build`, `/test`, `/review`, `/ship`) and `obra/superpowers` (`subagent-driven-development`, `executing-plans`, `finishing-a-development-branch`) converge on the same shape — pickup → breakdown → red/green loop → review → finish — but neither carries issue acceptance criteria through the handoff and neither dispatches a persona fan-out.

## Constraints

**Functional.**

- Every D2 skill is reachable by *name* from the front-door skill — no inlined procedure (Rule P7). This includes `breakdown-at-pickup`, which is a **named delegation** invoked by `exec:pickup`, not an inlined sub-procedure (see the skill graph).
- The issue's acceptance criteria are carried by the handoff contract from pickup to the review step and surface verbatim as input to the spec-compliance persona.
- Persona dispatch follows ADR 0003: Claude-Code Agent fan-out by default, inline-sequential fallback on non-Claude workers; the supervisor — not the persona — chooses the branch.
- The PR-finishing step produces the trail artefacts KR1 greps for: What/Why/Focus PR body + review-summary comment + Linear status transition.

**Non-functional.**

| NFR | Target | Fitness function |
|---|---|---|
| Headless-first | The front door, build, debug, simplify, review-fan-out, verify, and PR-finishing skills run end-to-end inside one non-interactive `claude -p` invocation against a seeded issue with no human prompt between steps. | The N09 validation-drain harness runs 5 issues headlessly; any step that re-prompts a human fails the drain and the skill that re-prompted is named in the failure. |
| Vendor portability | Every execution verb resolves to one skill file authored against this pack's anatomy; no skill depends on a Claude-Code-only tool except via the ADR-0003 dispatch branch (which has a documented inline-sequential fallback). | A grep over the D2 skills' workflow sections finds zero references to vendor-specific tool names outside the dispatch branch's `# Claude Code` / `# Other workers` split. |
| Front-door size | The front-door skill stays ≤ 200 lines so the named-delegation discipline is structurally enforced (inlining is structurally impossible at that size). | `wc -l skills/<front-door>/SKILL.md` ≤ 200 at acceptance. |
| Verb collision | Zero collisions between shaping (`shape:*`) and execution verbs at the slash-command surface. | A diff over `.claude/commands/` after authoring shows no two commands sharing a leaf name. |
| AC carry-through | The spec-compliance persona's input includes the verbatim issue AC checklist on every drained issue. | An N09 drain inspects the review-step prompt log — absence of the verbatim AC list is a drain failure attributed to the handoff contract, not the persona.|

## Alternatives considered

**Alt 1 — Bare verbs (`/pickup`, `/build`, `/review`, `/finish`).**

*Description.* No namespace prefix on execution verbs; only shaping keeps `shape:*`.
*Blast radius if wrong.* Hostile to slash-command discovery (autocomplete shows shaping and execution interleaved), and `/review` collides with several installed packs the owner already uses (`code-review`, `crit`, the built-in `review` command). Rename later means rewriting `drain_cycle/prompt.py`, every initiative-C supervisor prompt, and any reference in installed plugins.
*Reversal cost.* High — once the supervisor in initiative C binds, every downstream worker has to be re-keyed.

**Alt 2 — `exec:*` prefix on every execution verb (`exec:pickup`, `exec:build`, `exec:review`, `exec:verify`, `exec:finish`).**

*Description.* Mirrors the established `shape:*` discipline on the execution half. Two clean halves of one namespace.
*Blast radius if wrong.* Low. Verbose at the slash-command surface but unambiguous; autocomplete groups every execution verb. Recovers if a single verb name turns out wrong by renaming inside one prefix without touching the rest.
*Reversal cost.* Low per verb, because the prefix anchors the others.

**Alt 3 — `drain:*` prefix (`drain:pickup`, `drain:build`, …).**

*Description.* Names the workflow that owns the verbs.
*Blast radius if wrong.* Couples the verb namespace to one supervisor (`drain-cycle`). Initiative C's premise is that the workflow lives in the *pack*, not in the supervisor; binding the verb to the supervisor's name re-creates the very coupling the initiative exists to remove.
*Reversal cost.* High — same problem as Alt 1 plus a semantic miscue.

**Alt 4 (do nothing) — leave the execution skills nameless.**

*Description.* Each D2 skill chooses its own leaf name; no shared prefix.
*Blast radius if wrong.* The front door and the supervisor prompt both end up referencing each skill by an ad-hoc string. No collision detection. No grouping at the slash-command surface. The initiative-B consolidation has no namespace to consolidate to.
*Reversal cost.* High — picking the namespace later means renaming after binding.

## Recommended approach

**Adopt Alt 2: `exec:*` prefix on every execution verb.** Recorded as the decision of record in **ADR 0004**. Namespace table reserved here:

| Half | Prefix | Verbs (this pack) |
|---|---|---|
| Shaping | `shape:` | `shape:idea-triage`, `shape:initiative`, `shape:roadmap`, `shape:delivery`, `shape:design-doc`, `shape:plan-review`, … (existing) |
| Execution | `exec:` | `exec:pickup` (front door), `exec:build`, `exec:debug`, `exec:simplify`, `exec:review` (persona fan-out), `exec:verify`, `exec:finish` |

`exec:` wins on the named constraint (vendor portability + verb-collision). It mirrors `shape:` so the worker reads one consistent rule across the whole pack. It is the only candidate that survives initiative C's portability premise (Alt 3 fails), keeps clean slash-command discovery (Alt 1 fails), and avoids a deferred naming bill (Alt 4 fails).

**Skill graph (named delegations only, no inlined procedure).**

```
            [issue picked up]
                  │
                  ▼
            exec:pickup        ─── front door (N05)
                  │
                  ▼
    exec:breakdown             ─── named delegation invoked by exec:pickup;
                  │                emits the ordered task list (NOT inlined)
        ┌─────────┴──────────┐
        ▼                    │
    exec:build (N06)         │  per slice
        │  RED → GREEN → commit
        │
        ├─ red-loop stuck ──▶ exec:debug (N07)  ──▶ back to RED
        │
        ├─ green ───────────▶ exec:simplify (N07) ─▶ commit
        │
        └─ slice done ───────▶ next slice ↑ or ↓
                  │
                  ▼
           exec:review        ─── N03's execution-review (already shipped)
                  │            fans out personas per ADR 0003
                  ▼
            exec:verify       ─── checks the AC checklist against the diff
                  │
                  ▼
            exec:finish (N08) ─── Graphite-first, git fallback, trail artefacts
                  │
                  ▼
        [PR open + status moved to In Review/Done]
```

Each arrow is a named delegation in the front-door skill's workflow section. `exec:breakdown` is the published verb form of breakdown-at-pickup — it satisfies Rule P7 (the front door names it, does not inline it) and keeps `exec:pickup` under the 200-line NFR.

**Inter-skill handoff contract (the envelope each step receives + emits).**

| Step | Receives | Emits |
|---|---|---|
| `exec:pickup` | issue id + branch + worktree path | `pickup-envelope.json`: `{issue_id, branch, ac_checklist[], body_md, labels[], blocked_by[]}` and an ordered task list (each task: `id`, `done_when`, `model_tier`, `axes`, `risk`) |
| `exec:build` (per slice) | one task + `pickup-envelope.json` | a commit per slice + an updated `build-log.md` recording RED/GREEN gates |
| `exec:debug` | the failing-check output + the current envelope | a written root-cause note (gate) + handed control back to `exec:build` |
| `exec:simplify` | the green diff + envelope | a before/after rationale appended to `build-log.md` |
| `exec:review` *(provisional — see Q2)* | working-tree diff + `pickup-envelope.json` (so personas see `ac_checklist`) | the deduped GO/NO-GO verdict + finding triples per ADR 0003 |
| `exec:verify` *(provisional — see Q2)* | `ac_checklist` + diff | a structured pass/fail per AC item; any fail loops back into `exec:build`; on the final pass, `outcome_verdict: {result, failed_ac[]}` written back into the envelope |
| `exec:finish` | envelope + review verdict + verify result | PR body (What/Why/Focus), review-summary comment, Linear status move, and `prep_verdict: {route, reasoning}` written back into the envelope |

The envelope is the carrier. The `ac_checklist` field is the answer to the original failure mode: the spec-compliance persona consumes it directly, so *built-the-wrong-thing* is reviewable. As the run progresses the envelope accumulates two verdict fields — `outcome_verdict` (from `exec:verify`) and `prep_verdict` (from `exec:finish`) — so a downstream supervisor can grade the run from the one pack-owned file the pack already writes, without the pack having to know the supervisor's own exit-record format. The two rows marked *provisional* are settled at N05 authoring if `exec:verify` and `exec:review` collapse (Q2); if they collapse, those two rows merge into one.

> **Boundary note.** The envelope is where verdicts land; mapping them into any supervisor-side exit record (e.g. drain-cycle's `.drain-handoff.json`) is the supervisor's job, not the pack's. The pack does not name, write, or version that file, and carries no routing `flow` field — verification is universal (drain-cycle ADR 0002), so there is no route to record.

**Persona-dispatch integration.** `exec:review` is N03's already-shipped `execution-review` skill, renamed to live under the `exec:` prefix. **The rename is owned at N05 authoring time** (N05 publishes the front door and the verb namespace together); N04 reserves the name, N05 performs the rename. ADR 0003's dispatch branches are the skill's responsibility, not the front door's — the front door delegates by name and is dispatch-agnostic.

## Consequences

**Positive.**

- One naming table covers both halves; initiative B's consolidation consumes it.
- The envelope's `ac_checklist` field closes the AC-carry-through gap on every drained issue.
- The front-door skill stays ≤ 200 lines because every step is a one-line delegation.
- Vendor portability holds: only `exec:review` knows about ADR 0003's branches; the rest of the graph is dispatch-agnostic.
- N05–N08 can break their tasks against a stable contract without further negotiation.

**Negative.**

- `exec:` is verbose at the slash-command surface compared to bare verbs.
- The envelope is a new artefact workers must write; envelope drift (a field renamed in one skill, not the others) becomes a real failure mode and must be policed by `exec:pickup`'s skeleton task.
- N09's validation drain becomes the only place envelope-field drift surfaces; an envelope schema lint should follow if drift recurs.

**Walking skeleton (Rule B2).** Required. The skeleton is one issue drained end-to-end with the simplest possible body in each step — `exec:build` doing a one-line edit, `exec:review` running with one persona, `exec:finish` opening a draft PR. The N05 skeleton task ("a dry run on one real issue reaches the PR step") is the walking skeleton for the whole graph. It must land before N06–N08's substantive content is filled in. Pre-skeleton estimates of envelope correctness are uncalibrated.

## Operability plan

- **Metrics.** Per drained issue: time-to-PR, AC-pass-rate at `exec:verify`, persona finding count by class/severity, count of `exec:debug` escalations, count of post-push manual fix commits.
- **Structured logs.** Each skill emits one JSON line per step: `{skill, issue_id, step, gate_result, duration_ms, envelope_hash}`. The hash detects envelope drift between steps.
- **Traces.** Spans per skill invocation parented to the pickup span; an attribute `envelope.ac_count` makes AC-carry-through queryable.
- **Alerts.** None at this stage — drain volume is too low for thresholds. The N09 validation drain is the alert surface.
- **Rollback plan.** If a verb name turns out wrong: (1) author the new name as a sibling skill, (2) leave the old name as a one-line redirect for one cycle, (3) update `drain_cycle/prompt.py` and initiative-C supervisor prompts, (4) delete the redirect. Verification gate at each step: run one validation drain and confirm zero re-prompts.
- **Capacity headroom.** The envelope is small (≤ 2 KB per drain). No capacity concern in this pack.
- **Known failure modes.** (a) Envelope field drift between skills → policed by envelope hash in logs + N09 drift check. (b) Persona dispatch branch mis-selected on a non-Claude worker → ADR 0003's persona prose is identical across branches; failure surfaces as zero findings, caught by the N01 grader on the next validation drain. (c) `exec:debug` infinite loop → bound by a "consecutive-failure escalation" gate inside `exec:build` (per N06).
- **Upstream dependencies.** Linear API (read AC + write status), GitHub/Graphite (open PR). Failure mode: Linear API down → `exec:pickup` halts with a comment; `exec:finish` halts and queues the PR move locally.
- **Downstream dependencies.** `drain_cycle/prompt.py` (initiative C) consumes only the front-door verb; the rest of the graph is the front door's concern.

## Open questions

| Q | Owner | Resolution gate |
|---|---|---|
| **Q1 (RESOLVED by the supervisor-binding audit above).** Does `drain_cycle/prompt.py`'s current flow need to migrate to `exec:*`, or can it be adapted in-place? | initiative-C owner | **Resolved.** The audit found two live bindings: `/code-review-and-quality` (4 string locations) → swap to `exec:review`; `/shape:task` (verify-flow directive) → folds into `exec:pickup`'s breakdown. The inlined completion-sequence prose is where `exec:verify`/`exec:finish` land *additively*. Cutover is a bounded edit to `prompt.py`, scheduled at the initiative-C pointer-swap (N10); no coordinated cross-drainer migration. The earlier-assumed `/shape:verify-implementation`/`/shape:pr-prepare`/`/shape:pr-respond` verbs are not in current source. |
| **Q2.** Should `exec:verify` and `exec:review` collapse into one skill (both consume AC)? The two *provisional* rows in the handoff-contract table depend on this. | N05 skeleton task | Resolved when the front-door skill is first authored. If the two collapse cleanly without inlining a procedure, do so and merge the two table rows; otherwise keep separate. |
| **Q3.** Does the envelope need a versioned schema field from day one, or can drift detection wait for N09 to find a real case? | N05 skeleton task | Resolved at N05 authoring. Default: no version field; add only if N09 surfaces drift in the first 5 drains. |
| **Q4.** Are there worker surfaces beyond Claude Code, codex, and kimi that need explicit treatment in the dispatch branch? | initiative-C owner | Resolved before initiative C cutover; not blocking D2. |

## Review record

Accepted through the `plan-review` exit gate (REVISE → conditions cleared). Review record: `docs/plan-reviews/execution-workflow/review.md`. Blocking conditions 1 (supervisor-binding audit) and 2 (ADR of record) closed by the Context audit + ADR 0004; clarity conditions 3–4 folded into the skill graph, the handoff table, and the persona-dispatch note above.
