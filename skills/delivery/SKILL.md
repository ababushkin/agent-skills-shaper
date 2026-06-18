---
name: delivery
description: 'Decompose committed work into a verifiable delivery hierarchy. Trigger phrases: "plan this project", "breakdown the design into tasks", "plan this initiative"'
---

# Delivery shape

## Purpose

Take committed work and create a delivery plan that's easy for humans to review and for agents to action.

The input may be an initiative, a single task, or an accepted design doc. The hierarchy has three layers: deliverables, nodes, and tasks. Deliverables serve a stated outcome source. Nodes are typed units of work such as stories, spikes, ADRs, experiments, design docs, or KTLO work. Tasks are the verifiable checklist inside a node.

## When to use

- Committed work exists and the desired outcome is known.
- You need a deliverable → node → task hierarchy before build pickup.
- You want traceability from each deliverable back to the relevant outcome source.
- You are shaping work from one of these sources:
  - an initiative with a goal and KRs
  - a single task with acceptance criteria or a clear desired outcome
  - an accepted design doc with decisions, constraints, and rollout target

## Do not use when

- The input is only a vague idea or problem with no committed outcome. Route to the appropriate shaping skill first.
- The work is already fully decomposed and ready to execute.
- The request is just to implement one issue now, with no need for an intermediate delivery plan.

## Inputs

Committed work as text.

Supported input shapes:

| Source | Minimum input | Traceability spine |
|---|---|---|
| Initiative | Goal plus KRs | KRs |
| Single task | Task statement plus outcome or acceptance criteria | Acceptance criteria or stated outcome |
| Accepted design doc | Accepted design, decisions, constraints, and rollout target | Design decisions, requirements, or rollout outcomes |

If the input has no committed outcome source, stop. Do not invent outcomes, KRs, acceptance criteria, or design decisions to proceed.

## Outputs

Emit a delivery-plan file-set matching `docs/delivery-shape-contract.md`.

By default, write it under:

```text
examples/delivery-plans/<work-slug>/
```

unless the caller names another path.

The file-set contains:

- Root `README.md` with the source summary, traceability spine, rendered tree, and hand-count manifest.
- One `D<n>-<slug>/` directory per deliverable.
- One `_deliverable.md` per deliverable.
- One `N<nn>-<slug>.md` file per node.

The emitted plan must pass:

```bash
bin/walk-delivery-plan <plan>
bin/check-plan-framing <plan>
```

## Workflow

### 1. Restate the work

Write one sentence:

```text
This work wants [outcome] for [who or what].
```

Anchor to the stated outcome, not to a plausible implementation.

### 2. Gate: confirm the input is committed work

Identify the source type:

```text
initiative | single-task | accepted-design-doc
```

Then identify the traceability spine.

For an initiative, use the KRs.

For a single task, use the acceptance criteria or stated outcome.

For an accepted design doc, use the accepted decisions, requirements, constraints, or rollout outcomes.

If no traceability spine exists, stop and route back to shaping. Do not fabricate one.

### 3. Gate: map deliverables to the traceability spine

Group the work into milestone-class deliverables. Each deliverable must serve exactly one item from the traceability spine. Use the trace field defined by `docs/delivery-shape-contract.md`.

Two checks must hold:

- Every deliverable serves exactly one outcome item.
- Every outcome item is served by at least one deliverable.

An outcome item with no deliverable is unplanned. A deliverable with no outcome source is output without a bet.

### 4. Gate: decide whether a deliverable needs design first

For each deliverable, check whether any design-doc trigger applies:

- It breaks into more than about five nodes.
- It contains a one-way-door decision.
- It touches shared infrastructure.
- It carries meaningful user, cost, compliance, or operational impact.

If any trigger applies, the deliverable's first node is:

```yaml
type: design-doc
```

Build nodes under it are blocked by that design-doc node. Their detailed build task breakdown waits until the design doc is accepted.

If the input itself is an accepted design doc, do not create another design-doc node unless a later deliverable introduces a new design question.

If no design-doc trigger applies, proceed straight to nodes.

If a smaller architectural decision matters but does not need a full design doc, create an `adr` node.

Delegate discipline-specific structures to their source skills or references. Do not inline spike protocols, ADR templates, design-doc templates, or sizing rubrics.

### 5. Decompose deliverables into nodes

For each unit of work, select a node `type` from `docs/delivery-shape-contract.md`. Every node must carry `type`, trace field, and `maps_to`.

If the current contract has not yet migrated from `serves_kr`, use the contract's required trace field consistently.

### 6. Gate: write the five-section node body

Every node must use the same five body sections:

```markdown
## What
## Why
## Completion
## Assumptions
## Key Risks
```

Write the body against the `writing-refinement` skill (`skills/writing-refinement/references/style-rules.md`, `plans-okrs.md`). Phrase the node as a summary achievement; keep the actor in the subject and use concrete verbs.

Completion form varies by node type — see `docs/delivery-shape-contract.md`.

For story nodes, the first sentence of `## What` uses the following form:

```text
As <role>, I want <capability>, so that <benefit>.
```

Every assumption must be tagged:

```text
*(verified)*
*(to-verify)*
```

Any `(to-verify)` assumption blocks pickup.

Every key risk must include either a mitigation or a falsifier.

### 7. Break each node into tasks

Every task is a single unchecked Markdown task line.

Each task must include:

- One observable outcome.
- One `Done when:` clause.
- One `Model:` annotation.
- Any external block flagged inline.

Write each task against `skills/writing-refinement/references/tasks.md`: active voice, a concrete done-when state, and no blank task ("Investigate latency") unless the output is named.

#### 7a. Choose the first task

The first task depends on node type and risk locus.

| Node type / risk locus | First task |
|---|---|
| Story with integration risk | `skeleton` task exercising the real risky seam |
| Story with core-logic risk | Spike on the core logic, then skeleton after the core is proven |
| Spike | The minimal probe |
| Experiment | The minimal experiment |
| ADR | No skeleton; tasks follow the decision-record completion form |
| Design doc | No skeleton; tasks follow the accepted-design completion form |
| KTLO | No skeleton; tasks preserve existing behavior |

Before writing the first task, identify any toolchain or setup prerequisites and fold them into the first task. Do not create a separate setup task before it.

A skeleton must exercise the real risky seam: the third-party call, cross-service boundary, unproven dependency, or other integration risk. Do not create a green path that only proves mocked plumbing.

#### 7b. Add feature slices where applicable

For runnable-software story nodes, add one task per feature slice after the first task. Each slice must extend prior work in one direction, be independently testable, leave the system deployable, and name an observable outcome. Do not add slices to `adr`, `design-doc`, or `ktlo` nodes.

#### 7c. Gate: write acceptance criteria before ordering

Every task needs a `Done when:` clause before sequencing. The clause must describe a verifiable result, not the work performed. If the criterion cannot fit in one sentence, split the task.

#### 7d. Gate: check task size

Each task must have:

- One sentence of task description.
- Exactly one `Done when:` clause.
- One verifiable outcome.

Split tasks that carry multiple concerns.

#### 7e. Sequence by dependency

Order tasks by dependency, not perceived difficulty. Flag external blockers inline (`blocks on: <dependency>`): cross-team deliverables, external credentials, third-party environments, or shared-infrastructure changes outside the node.

#### 7f. Add model routing

Apply the 5-axis rubric from `references/task-sizing.md` (RC, SC, HS, SR, OR). Score each axis Low / Med / High, derive the tier and review flag, and append a `Model:` annotation. A task without `Model:` is incomplete.

### 8. Emit the file-set

Write the plan using the layout and frontmatter rules in `docs/delivery-shape-contract.md`.

Use numeric prefixes (`D1-<slug>/`, `N01-<slug>.md`); pad node numbers past nine.

The root `README.md` must include the hand-count manifest from `docs/delivery-shape-contract.md`.

### 9. Gate: verify the plan

Run `bin/walk-delivery-plan <plan>` and `bin/check-plan-framing <plan>`. Fix failures; do not relax the gate.

Then sub-agent a writing review using the `writing-editor` persona (`agents/writing-editor/AGENT.md`) over the emitted node and task bodies. Apply rewrites; on `reject`, repair and re-run once, then carry remaining notes forward as `accept with notes`. Follow all of the writing guidelines and delete anything redundant/duplicate or unnecessary.

## Red flags

- The plan invents outcomes, KRs, acceptance criteria, or design decisions.
- A deliverable serves zero outcome items or more than one outcome item.
- An outcome item has no deliverable.
- A design-doc-worthy deliverable has no first `design-doc` node.
- An accepted design doc input creates a duplicate design-doc node without a new design question.
- A reversible, single-surface deliverable was given an unnecessary design-doc node.
- A node is missing `type`, trace field, or `maps_to`.
- A node omits one of the five required body sections.
- A node inlines a delegated discipline instead of linking to its source skill or reference.
- A setup/scaffolding task appears before the first risk-facing task.
- A skeleton proves mocked plumbing instead of the real risky seam.
- A core-logic-risk story starts with a skeleton that stubs the core risk.
- A task lacks `Done when:` or `Model:`.
- A task has multiple independent completion criteria.
- A cross-team or external dependency is not flagged inline.
- The plan was declared complete without running both gates.

## Exit criteria

The skill is complete when:

- The delivery-plan file-set exists.
- `bin/walk-delivery-plan <plan>` exits 0.
- `bin/check-plan-framing <plan>` exits 0.
- The Step 9 writing-editor pass returned `accept` or `accept with notes`.

## Related

- `shape:project` — produces committed initiatives this skill can consume.
- `shape:design` — owns design-doc structure for design-doc-worthy deliverables.
- `writing-refinement` — prose skill; node and task bodies are written and reviewed against (`references/plans-okrs.md`, `references/tasks.md`, `style-rules.md`).
- `agents/writing-editor/AGENT.md` — the writing-editor persona dispatched at Step 9.
- `docs/delivery-shape-contract.md` — plan artefact contract, layers, node vocabulary, frontmatter, and cross-reference rules.
- `bin/walk-delivery-plan` — deterministic reader and manifest checker.
- `bin/check-plan-framing` — node/task framing gate.
- `references/task-sizing.md` — 5-axis model-routing rubric.
