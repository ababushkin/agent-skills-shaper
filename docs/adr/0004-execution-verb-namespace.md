# ADR 0004 — Execution verb namespace (`exec:*`)

- **Status:** Accepted (wrapper surface superseded in part by ADR 0006 — the `exec:*` verb names stand; they are no longer published as typed slash commands)
- **Date:** 2026-06-10
- **Serves:** Initiative D2 / KR1 — drained issues reach Done with a merged PR and full review trail (N04–N08).
- **Premise for:** Initiative B (verb consolidation consumes this namespace table) and Initiative C (the drain-cycle supervisor binds the front-door verb literally).
- **Record of:** the namespace decision in `docs/design-docs/execution-workflow/design-doc.md` (N04). The design doc carries the full alternatives analysis and skill graph; this ADR is the durable decision downstream skills bind to.

## Context

D2 authors five execution-side skills (front door, build, debug/simplify, review fan-out, verify, PR finishing). Each must be reachable by name from the front-door skill, and the drain-cycle supervisor in initiative C will name the front-door verb literally in `drain_cycle/prompt.py`. The verb namespace is a one-way door: once the supervisor prompt and workers' muscle memory bind, a rename costs a coordinated migration across every drainer.

Shaping verbs (`shape:*`) are already established. The execution half was unnamed. Four candidates were weighed in the N04 design doc:

1. **Bare verbs** (`/pickup`, `/build`, `/review`) — rejected: `/review` collides with installed packs (`code-review`, `crit`, built-in `review`); no slash-command grouping.
2. **`exec:*` prefix** — mirrors `shape:*`; two clean halves of one namespace; per-verb rename stays local to the prefix.
3. **`drain:*` prefix** — rejected: couples the namespace to one supervisor, re-creating the pack-vs-supervisor coupling initiative C exists to remove.
4. **Nameless** — rejected: no collision detection, nothing for initiative B to consolidate to.

**Supervisor-binding audit (performed before pinning).** A read of current `drain_cycle/prompt.py` confirmed the migration surface is bounded: the supervisor emits `/code-review-and-quality` (4 string locations) and `/shape:task` (verify-flow directive only); the rest of the completion sequence is inlined prose. Adopting `exec:*` is a bounded string swap plus an additive replacement, not a coordinated cross-drainer migration. The audit also corrected a stale assumption — `/shape:verify-implementation`, `/shape:pr-prepare`, and `/shape:pr-respond` are not in current source.

## Decision

**Adopt the `exec:*` prefix for every execution-side verb.** Reserved namespace table (both halves, single source of truth for initiative B):

| Half | Prefix | Verbs (this pack) |
|---|---|---|
| Shaping | `shape:` | `shape:idea-triage`, `shape:initiative`, `shape:roadmap`, `shape:delivery`, `shape:design-doc`, `shape:plan-review`, … (existing) |
| Execution | `exec:` | `exec:pickup` (front door), `exec:breakdown`, `exec:build`, `exec:debug`, `exec:simplify`, `exec:review`, `exec:verify`, `exec:finish` |

`exec:review` is N03's already-shipped `execution-review` skill, renamed under the prefix at N05 authoring time.

## Consequences

**Positive**
- Mirrors `shape:*`; one consistent namespacing rule across the whole pack.
- Per-verb renames stay local to the prefix — low reversal cost for a single verb.
- Initiative B consolidates against one reserved table; initiative C binds one front-door verb.

**Negative / costs**
- Verbose at the slash-command surface versus bare verbs. Accepted — discovery grouping and collision-avoidance outweigh verbosity.
- The drain-cycle cutover requires a bounded edit to `prompt.py` (the N10 pointer-swap). Scheduled, not free.

## Scope

This ADR pins the prefix and reserves the leaf names. The skill graph, handoff contract, and per-skill behaviour live in the N04 design doc; the skills themselves are authored in N05–N08. Any change to the prefix or a reserved leaf name requires a follow-up ADR.
