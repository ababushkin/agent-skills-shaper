---
layer: node
id: N01
type: design-doc
title: Thin-supervisor contract design doc (before build)
parent: D1
serves_kr: KR3
maps_to: linear-issue
external_window: none
completion:
  form: the-design-doc
  criterion: >
    An accepted design doc covering the ≤15-line prompt-segment allocation, the
    .drain-handoff.json schema v2 (verdict fields, writer/reader allocation), the
    process-vs-workflow boundary chart, and vendor-agnostic prose constraints.
delegates_to: design-doc (Rule A1 design doc — produced before the build nodes are picked up)
---

# N01 — Thin-supervisor contract design doc (before build)

**Type:** `design-doc`. D1 met a Rule A1 trigger (one-way-door contract on shared
infrastructure across two repos), so the design doc comes first. This is the initiative's
flagged Frontier exception.

> **Blocked by:** initiative A's accepted execution-workflow design doc
> ([A/N04](../../issues-drain-end-to-end/D2-execution-workflow-drains-issues/N04-execution-workflow-design-doc.md)) —
> this doc *extends* A's inter-skill handoff contract to the supervisor seam; it does not
> re-decide the skill graph.

> **▶ On pickup — before any build node in this plan:** produce the design doc via the
> `design-doc` skill and accept it through the `plan-review` exit gate. Build nodes **N02, N03,
> and N04 are blocked by this node**: their task breakdown waits until this doc is accepted.

## What

The design doc for the supervisor↔worker contract: which segments the ≤15-line prompt template
carries (issue context, worktree, base branch, skill pointer — whether the resume directive
counts as process context or moves, and **how the per-issue stack/push policy reaches the
worker**: `stack` is a supervisor-resolved fact (`--no-stack`, `push_to_main_repos`,
`orchestrator.py:505`) that today selects the preamble variant, so the pointer-only template
must still transmit it as a process segment); the `.drain-handoff.json` schema v2 — the verdict fields
(`outcome_verdict`, `prep_verdict`, `flow`, halt reason on non-Done exits), who writes each and
who reads each; the boundary chart allocating every current prompt/orchestrator concern to
*process* (supervisor keeps: spawn, guardrails, halt, resume, grade) or *workflow* (pack owns:
everything else, including verify-flow routing); and the vendor-agnostic prose constraints that
let a non-Claude worker follow the same pointer. `delivery-shape` does not restate the
design-doc structure here — that discipline lives in the `design-doc` skill.

## Why

The bet: one accepted contract lets the prompt re-scope and both verdict halves build against a
stable seam instead of three locally-sensible interfaces negotiated through PRs. Rejected
alternative: re-scope the prompt ad hoc and let the handoff schema grow fields as needs appear —
schema drift across two repos with no single source, exactly the two-sources-of-truth failure
the thin-supervisor architecture exists to end. Unblocks N02–N04 and gives any future
non-Claude worker a written contract to be tested against.

## Completion

An accepted design doc covering: the prompt-segment allocation with the ≤15-line budget spent
line by line — including the per-issue stack/push-policy signal and the grep pattern that
defines "procedure verb" for KR3's check; the handoff schema v2 with writer/reader allocation
per field; the process-vs-workflow boundary chart (including where `flow.py`'s verify-label
routing and `prompt.py`'s shape-task directive go); and the vendor-agnostic constraints.
Accepted through the `plan-review` gate.

## Assumptions

- Initiative A's design doc (A/N04) is accepted before this one is drafted — this doc extends its handoff contract rather than competing with it. *(to-verify — A/N04 is planned but not yet built; if it slips, this node inherits its namespace and contract questions and grows accordingly)*
- The ≤15-line cap is measured on the worker prompt template, with process segments (worktree, base branch, resume) counted inside the budget. *(verified — KR3's own measurement clause: `wc -l` on the prompt template plus grep for procedure verbs)*

## Key Risks

- **Risk:** this contract drifts from A/N04's inter-skill handoff contract — two documents
  describing one file's schema.
  *Mitigation:* schema v2 amends A/N04's handoff table in place (one table, both initiatives
  cite it); this doc adds the supervisor-seam columns rather than copying the table.

## Tasks

- [ ] Frame the constraints and draft ≥2 alternatives for the prompt-segment allocation and handoff schema v2 · Done when: the doc presents the alternatives with trade-offs against the ≤15-line cap and vendor portability · Model: Frontier · risk one-way · review elevated · axes RC·SC·HS·SR·OR = H·H·L·H·L · companions code-review-and-quality
- [ ] Record the decision (boundary chart + schema v2 + segment allocation) and pass the plan-review exit gate · Done when: the design doc is accepted and N02–N04 can break tasks against it · Model: Frontier · risk one-way · review elevated · axes RC·SC·HS·SR·OR = H·H·L·H·L · companions code-review-and-quality
