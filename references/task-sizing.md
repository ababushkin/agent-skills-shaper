---
name: task-sizing
description: >
  Risk-weighted model-routing rubric — five axes scored Low/Med/High that route a
  single task to a model tier and a review-attention flag at planning time. Not effort
  estimation; a second lens on the verification-granularity Size check.
type: reference
cited_by:
  - skills/roadmap-shape/SKILL.md
  - skills/initiative-shape/SKILL.md
---

# Task sizing — the 5-axis routing rubric

This rubric routes a single task to a **model tier** and a **review-attention flag** at planning time. It is risk-weighted *routing*, not effort estimation: the output is "which model should run this, and how much review does it warrant," never "how long will this take." You score five axes Low/Med/High, the stakes axis sets a default direction, the other axes adjust it, and a tier and a flag fall out.

Routing is not cascading. **Routing** is planning-time pre-classification — one model is chosen per task *before* it runs. **Cascading** is runtime escalation — start on a cheap model and retry on a bigger one mid-execution when the cheap one fails. This rubric only does routing; cascading is a named, separate, out-of-scope layer (see *What this is not for*).

**Reconciliation with eng-agentic P8.** P8 says effort is measured in slices and gates, not calendar time, and warns against importing a "how long will this take" frame. A sizing rubric could look like it smuggles effort estimation back in. It does not: it emits a capability tier keyed to *risk*, never a duration or a size. It is orthogonal to — and applied *after* — the slice-based Size check performed during at-pickup task breakdown. Two lenses on the same already-sized slice: one asks "is this one verifiable change" (Size), the other asks "what does it cost to get it wrong, and what capability does it need" (this rubric). Neither uses calendar time.

## The 5 active axes

Score each axis Low / Med / High by **routing pressure** — High means "argues for a more capable model." Four axes read naturally (more demanding = higher pressure). **Specification completeness runs inverted**: a *less* complete spec is *higher* pressure, because the model must infer intent rather than follow it.

| Axis | Low pressure | Medium | High pressure |
|---|---|---|---|
| **Reasoning complexity** | mechanical edit, lookup, rename, reformat | bounded logic following a known pattern | open-ended design, cross-cutting synthesis, subtle algorithmic correctness |
| **Specification completeness** *(inverted)* | fully specified — concrete acceptance criteria, named files, no judgment left | mostly specified, a few gaps to fill | sparse or ambiguous — intent must be inferred, acceptance criteria absent |
| **Hallucination sensitivity** | self-contained; no external API or library surface | familiar, stable APIs the model knows well | unfamiliar or fast-moving APIs, version-specific behaviour, high fabricated-signature risk |
| **Stakes / reversibility** | trivially reversible two-way door — one file, easy revert, low blast radius | reversible with effort; bounded blast radius | one-way door — schema migration, public API, auth, production data, security |
| **Orchestration role** | leaf worker on a single delegated slice | worker doing local sequencing within its slice | orchestrator — decomposes, delegates, integrates sub-agent output |

## Set-aside dimensions

Three dimensions that matter for production routing are **near-constant for slice-bounded async dev tasks**, so they do not discriminate between tasks here and are deliberately not scored:

- **Cost / volume** — a planning-time slice runs once, not at scale. Per-task cost is dominated by the tier you pick, not by call volume, so volume is ~1 across every task and tells you nothing.
- **Latency** — no human waits in real time on an async slice; seconds-vs-minutes never trades off against output quality, so wall-clock latency does not move the routing.
- **Context size** — slices are already size-checked to one verifiable change (Step 5), so the working set fits comfortably inside every tier's context window; context length rarely forces a tier.

If a task violates one of these assumptions (a real-time path, a high-QPS call site, a genuinely large working set), it is not a slice-bounded async dev task and this rubric is the wrong tool.

## Model tiers

**`Fast = Haiku 4.5` · `Balanced = Sonnet 4.6` · `Frontier = Opus 4.7`.** (One mapping line by design: a model bump is a one-line edit here, not a rewrite of every reference to a tier.)

**Orchestrator / worker.** The default assignment is static, not per-call: an orchestrator (decomposes, delegates, integrates) runs **Frontier**; workers run **Balanced**; mechanical leaf workers drop to **Fast**. This is the orchestrator/worker pattern, applied at planning time — not runtime model selection.

## Routing rule (reversibility-gated)

Stakes/reversibility sets the default direction; the capability axes adjust it. Grounded in eng-universal P3 — deliberation scales with cost-of-reversal, not with how hard the task feels.

1. **Set the floor from stakes/reversibility.**
   - One-way door / high-stakes (**SR = High**) → **default up**: floor is **Frontier**. The cost of being wrong dominates the cost of the model; any downgrade needs a written reason.
   - Reversible / mechanical (**SR = Low/Med**) → **default down**: floor is **Fast**. Escalate only on a *demonstrated* capability gap, not on suspicion.
2. **Lift for capability.** Among the three capability axes — reasoning complexity, specification completeness, hallucination sensitivity — each one at **High pressure** lifts the tier one step above the floor (Fast → Balanced → Frontier), capped at Frontier. (This is the "escalate on a capability gap" path for reversible tasks.)
3. **Orchestrator pin.** Orchestration role **High** pins **Frontier** outright — the orchestrator's mistakes propagate to every worker it directs.
4. **Resolve the SR = Med middle upward.** SR = Med shares the Fast floor with Low, but its blast radius is real, not trivial. When a capability axis is borderline (you could defensibly call it Med or High) on an SR = Med task, score it High and take the lift — this is the bounded-but-real case P3 says to deliberate over.

## Derived outputs

The score produces three things — review load is an *output* of the axes, never an input:

1. **Model tier** — Fast / Balanced / Frontier, from the routing rule above.
2. **Review-attention flag** — `elevated` when **SR = High** *or* **HS = High**; otherwise `standard`. This tells review where to spend the asymmetric second-pass attention (eng-agentic Part 2: review matters more under agents).
3. **Companion-skill triggers** — fired by a single High axis:
   - **HS = High** → run `source-driven-development` on the task: verify every API and signature against current docs before relying on it (eng-agentic P2 — hallucination is the default, sources are the brake).
   - **SR = High** → run a `code-review-and-quality` pass before merge (escalate to `security-and-hardening` when the one-way door is auth, secrets, or a destructive/PII data operation — a schema migration or backfill is the ordinary `code-review-and-quality` case).

## Annotation one-liner format

Every task in a filed task list carries one routing line. It **must begin with `Model:`** (the conformance check is `grep -L 'Model:' docs/tasks/*.md` returning nothing). The axis vector is positional and fixed-order so two independent applications diff cleanly: `RC · SC · HS · SR · OR`.

```
Model: <Fast|Balanced|Frontier> · risk <reversible|one-way> · review <standard|elevated> · axes RC·SC·HS·SR·OR = <L|M|H>·<L|M|H>·<L|M|H>·<L|M|H>·<L|M|H>[ · companions <skill[, skill]>]
```

The `companions` segment is omitted when no companion trigger fires.

## Worked example

**Task:** "Write a function that deduplicates overlapping calendar events, merging adjacent ones."

| Axis | Score | Rationale |
|---|---|---|
| Reasoning complexity | **High** | interval-merge logic with non-obvious edge cases (touching vs overlapping, zero-length) — subtle algorithmic correctness |
| Specification completeness | Med | behaviour described; the adjacency rule and tie-handling need inference |
| Hallucination sensitivity | Low | pure logic, no external API surface |
| Stakes / reversibility | Low | one pure function, covered by unit tests, trivially reverted — two-way door |
| Orchestration role | Low | leaf worker |

**Derivation.** SR = Low → floor **Fast**. One capability axis at High (reasoning complexity) lifts one step → **Balanced**. No orchestrator pin. Review flag: SR and HS both not High → `standard`. No companion trigger.

```
Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·M·L·L·L
```

**Contrast — same rubric, different tiers** (shows the gate discriminates):

| Task | RC·SC·HS·SR·OR | Tier | Review | Why |
|---|---|---|---|---|
| Rename a column reference across the codebase | L·L·L·L·L | **Fast** | standard | all low pressure; mechanical, reversible |
| Add a migration renaming `users.email` and backfilling it | M·M·M·H·L | **Frontier** | elevated | SR = High one-way door sets the Frontier floor; `companions code-review-and-quality` |

## Common miscalibrations

**Scoring spec completeness like the others.** It is inverted. A fully-specified task is *Low* pressure; marking "well-specified = High" routes trivial tasks to Frontier. Read the column header, not the word.

**Routing on effort instead of risk.** "This is a big task, give it Opus." Size is verification granularity — a big task is split into slices (Step 5), and each slice is routed on its own axes. Effort is never an input here.

**Escalating on suspicion.** For reversible tasks the default is down. "Might be tricky" is not a demonstrated capability gap. Start at the floor; escalate when the cheaper tier actually fails the task, not when it might.

**Letting stakes touch only the review flag.** A one-way door sets *both* the tier floor (Frontier) and the review flag (elevated). Routing a risky task to Fast "because review will catch it" inverts the rule — the model that opens the door should be the capable one.

**Scoring an orchestrator as a worker.** If the task decomposes and delegates, orchestration role is High → Frontier, however simple any single sub-task looks. The orchestrator's errors propagate to every worker downstream.

## What this is not for

- **Not effort or time estimation.** The output is a tier and a flag — never hours, days, or story points (eng-agentic P8). Reaching for "this'll take a while" means you are in the wrong rubric.
- **Not a runtime cascade.** This is planning-time routing: one model chosen per task before it runs. Mid-execution escalation to a bigger model is a separate, named, out-of-scope layer.
- **Not a replacement for the verification-granularity Size check.** The at-pickup task breakdown phase sizes each task by whether it is one verifiable slice. This rubric is a second lens applied *after* that check passes — it routes the already-sized slice. A task that is too big is split first, then each slice is routed.

## Sources

- Anthropic — "Models overview" and "Choosing the right model" (capabilities / speed / cost triad; tier selection)
- Anthropic — "Building a multi-agent research system" (orchestrator/worker pattern)
- Augment — "AI model routing guide"; TianPan — "LLM routing vs model cascades" (routing vs cascading distinction)
- `rules/eng-principles-universal.md` — P3 (architecture is the expensive-to-change decisions; one-way vs two-way doors; reversibility-gated deliberation)
- `rules/eng-principles-agentic.md` — P2 (hallucination is the default, sources are the brake), P8 (effort is measured in slices and gates, not calendar time)
- `skills/delivery-shape/SKILL.md` — at-pickup task breakdown (verification granularity), the discipline this rubric routes to
