# ADR 0001 — `delivery-shape`: a new skill, not an expansion of `planning-and-task-breakdown`

- **Status:** Accepted
- **Date:** 2026-05-25
- **Decision driver:** the walking-skeleton spike (`examples/delivery-plans/top-down-delivery-planning/`,
  `docs/delivery-shape-contract.md`, `bin/walk-delivery-plan`).

This is the gate decision for the *Top-down delivery planning* initiative: build the
delivery-planning capability as **(A) a new `delivery-shape` skill**, or **(B) an expansion of the
existing `planning-and-task-breakdown` skill**.

## Context

The spike hand-produced one real initiative's full delivery hierarchy as a cross-referenced
markdown file-set, read a tool-agnostic contract off it, and then proved the file-set converts
mechanically to a tracker manifest (`bin/walk-delivery-plan` → `3 milestones / 9 issues /
19 sub-issues`, exit 0, oracle MATCH). With the schema and a working walk in hand, the A-vs-B
question reduces to one measurable thing: **how much of the delivery plan is structure that
`planning-and-task-breakdown` (PTB) does not already carry?**

PTB's contract, read off its `SKILL.md`: an *accepted design doc for a single feature* → a *flat*
ordered task list at `docs/tasks/<slug>.md`, every task carrying acceptance criteria, walking
skeleton as task 1. One input shape, one output shape, one completion form.

Quantifying the new structure the spike's plan carries, layer by layer:

- **Upper structural layers — little unique structure.** The original four-layer model's
  `capability` layer collapsed *entirely* (see contract *Design notes* / the ABA-283 collapse): all
  five capabilities were reducible to their child nodes and absorbed into deliverable prose. The
  surviving deliverable layer adds exactly two things over PTB: milestone-grouping and a
  `serves_kr` outcome tag. That is thin — this is the real signal toward **B**.
- **The node layer — large unique structure.** Nodes are *polymorphic*: eight completion-criterion
  forms (`acceptance-criteria`, `decision+stop-condition`, `decision-record`,
  `hypothesis+success-metric`, `numeric-target`, `rollback-per-phase`, `the-capability-spec`,
  `none`), each selecting a delegation target. The worked example exercises five of them on real
  content (`spike`, `story`, `adr`, `experiment`, `ktlo`). PTB has *no* concept of node type or
  completion-form selection — it knows only "task with an acceptance criterion." This is the signal
  toward **A**, and it is the dominant one.
- **Input and output shapes differ.** DS's input is a *committed initiative* (many deliverables,
  many KRs, pre-design-doc), not a single accepted design doc. DS's output is a *hierarchical
  walkable file-set + a tracker manifest*, not a flat task file. DS also decides per node *whether a
  design doc is even needed* (the Rule A1 branch) — it runs earlier and broader than PTB.
- **They compose; they do not merge.** The contract already points each `story` node's
  `delegates_to` at `planning-and-task-breakdown`: DS selects node types and the outcome spine, then
  hands each node *down* to PTB for the per-node task breakdown. Merging the two would make a skill
  that calls itself.
- **The initiative already assumes two skills.** KR3 is literally "0 collisions against
  initiative-shape or planning-and-task-breakdown" — the project's own success metric presupposes
  `delivery-shape` is a distinct, separately-triggered skill whose triggers must be disambiguated
  from PTB's.

### Mechanical-conversion evidence (the seam to `agent-skills-workflow`)

The "converts mechanically, no hand-massaging" half of the kill condition, proven by
`bin/walk-delivery-plan` and recorded here as the seam the downstream adapter implements. **No
writes to any tracker were performed** — this documents the shape correspondence only.

| Plan layer | File-set source | Manifest class (`maps_to`) | Linear create shape | Fields the conversion needs | Hand-invention? |
|---|---|---|---|---|---|
| Deliverable `D*/_deliverable.md` | directory + front-matter | milestone-class (`linear-milestone`) | `save_milestone(name, project)` | name←`title`; project←initiative | none |
| Node `N*.md` | file + front-matter | issue-class (`linear-issue`) | `save_issue(title, team, project, milestone, labels)` | title←`title`; milestone←directory nesting; labels←`type`/`serves_kr` | none |
| Task `- [ ]`/`- [x]` line | checklist line in a node | sub-issue-class | `save_issue(title, parentId, team, project)` | title←task text; parent←file nesting; done-state←`[x]` | none |

Every field Linear needs is sourced from front-matter or directory nesting; nothing is invented at
conversion time. The `completion.form` and `serves_kr` ride along as issue description / labels —
orthogonal metadata, not load-bearing on the structural shape. The kill condition ("needs a real
schema or tool rather than files") **did not fire**: the file-set walks deterministically and
converts mechanically.

## Decision

**A — build a standalone `delivery-shape` skill.** Draw its boundary exactly where the spike says:

- **`delivery-shape` owns:** committed-initiative → deliverable/node hierarchy; the outcome spine
  (`serves_kr` at every layer); node-type selection and completion-form-by-type; the Rule A1
  design-doc branch; the walkable file-set contract; the tracker-manifest seam.
- **`delivery-shape` does *not* own:** per-node task breakdown. It delegates that *down* to
  `planning-and-task-breakdown` (already recorded in each story node's `delegates_to`), and the
  per-node-type discipline to the owning rule/skill (`select and delegate; never re-author`).

The B-signal is acknowledged and absorbed rather than ignored: the upper layers *are* thin, which
is precisely why DS delegates downward and why the fourth layer was dropped. But the upper layers
were never the justification for a new skill — the polymorphic node vocabulary is, and it is both
too large and too far from "task breakdown" to bolt onto PTB without making PTB two skills wearing
one frontmatter.

## Consequences

**Positive**

- PTB keeps its clean single-input/single-output contract; DS layers above it with low coupling
  (eng-universal P9 — module/team boundaries; agentic P1 — each skill's context stays tight).
- The polymorphic node vocabulary lives in one place with a grounding rule against fabricating
  unexercised types, instead of bloating PTB's task model.
- The DS→PTB delegation is a clean seam: DS picks node types and the outcome structure; PTB does
  what it already does well.
- The manifest seam is mechanical and tool-agnostic; the concrete Linear adapter lives in
  `agent-skills-workflow`, keeping this pack tracker-agnostic.

**Negative / costs**

- Two skills now occupy adjacent territory; their trigger descriptions must be disambiguated, which
  is why KR3 gates on 0 collisions (the cost is real and explicitly measured, not hand-waved).
- DS must be authored to the full skill-anatomy spec and registered in the README + `using-this-pack`
  flowchart (node N09) — net-new surface to maintain.
- The to-fill node-type appendix (`slo`, `migration`, `deprecation`, `incident`, `compliance`,
  `capability`) is unexercised until an initiative grounds each; the vocabulary carries a documented
  risk of looking more proven than it is, mitigated by the contract's "do not fabricate a node to
  cover a type" rule.

## Gate outcome

The gate's two acceptance criteria are met: `bin/walk-delivery-plan` emits a manifest whose shape
matches Linear milestone/issue/sub-issue (`3/9/19`, exit 0), and this decision record exists citing
the spike evidence. The kill condition did not fire → **proceed to build per decision A**, on the
downstream issues (themselves blocked on the `initiative-shape` decouple).
