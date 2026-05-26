---
name: delivery-shape
description: >
  Decomposes a committed initiative (goal + key results) into an ordered, verifiable delivery
  hierarchy — deliverables → nodes → tasks — that a human reads top-down and a deterministic
  reader walks bottom-up into a tracker manifest. Every deliverable traces to a KR; every node
  carries a type and a delegation target; every `story` node carries acceptance criteria emitted
  by default. Use after an initiative is shaped and before any node is picked up to build.
  Trigger phrases: "turn this initiative into a delivery plan", "decompose this initiative",
  "break the initiative into deliverables", "plan the delivery for this", "shape the delivery",
  "what are the deliverables for this initiative".
pack: engineering
lifecycle_stage: plan
principles_implemented:
  - source: eng-agentic
    id: P3
    bucket: embedded
  - source: eng-agentic
    id: P4
    bucket: embedded
  - source: eng-agentic
    id: P7
    bucket: embedded
  - source: eng-agentic
    id: P8
    bucket: embedded
  - source: eng-universal
    id: Rule B2
    bucket: embedded
  - source: eng-universal
    id: Rule A1
    bucket: embedded
  - source: product
    id: A3
    bucket: embedded
length_target: 190–280
author: Anton Babushkin
predecessor:
  repo: none
  skill: none
  relation: new
kept_from_predecessor: "n/a"
changed_from_predecessor: "n/a"
---

# Delivery shape

## Purpose

delivery-shape takes a committed initiative — its goal and key results — and emits the full delivery hierarchy that sits between "we have an initiative" and "we know what to build, in what order, and how we'll know each piece is done." The hierarchy has three layers: deliverables (each serving one KR), nodes (polymorphic units of work — a story, a spike, an ADR, an experiment, …), and tasks (the checklist inside a node). A human reads it top-down, starting at the outcome; a deterministic reader walks it bottom-up into a tracker manifest.

The skill exists to bake the framing in so the user never re-prompts for it. Every deliverable traces to a KR, every node names its completion form and the discipline that owns it, and **every `story` node carries acceptance criteria by default** — because a story whose "how do I know this is done?" is missing is the exact gap that produces low-level task lists nobody can verify (agentic P4). delivery-shape *selects and delegates*; it does not re-author the disciplines it points at (agentic P7).

## When to use

- A committed initiative exists (goal + 3–5 KRs) and you need to turn it into the deliverable → node → task hierarchy before work starts.
- You are about to write a flat task list straight from an initiative and want the outcome trace (deliverable ↔ KR) and the completion framing (acceptance criteria per story) baked in instead.

## When not to use

- **No committed initiative yet** — the input is a vague idea or a problem with no goal/KRs. Run `initiative-shape` first; delivery-shape consumes its output, it does not produce a goal.
- **A single node is ready to build** — you already have one issue and need its task breakdown. Use `planning-and-task-breakdown`; that is the per-node delegate delivery-shape points at, not a substitute for it.
- **Single-issue, bug, or KTLO work** — create the issue directly in the ops slot. A bug fix does not need a deliverable hierarchy.

## Inputs

A committed initiative as text: the goal sentence and 3–5 key results (the six-field shape `initiative-shape` produces is ideal, but goal + KRs as plain text is the minimum). The KRs are load-bearing — they are the spine every deliverable traces to. If the input has no KRs, stop: there is nothing for deliverables to serve.

## Outputs

A delivery-plan file-set under `examples/delivery-plans/<initiative-slug>/` (or the path the caller names), laid out per `docs/delivery-shape-contract.md`: a root `README.md` (goal + KRs + tree + hand-count manifest), one `D<n>-<slug>/` directory per deliverable with a `_deliverable.md`, and one `N<nn>-<slug>.md` per node. The file-set walks cleanly under `bin/walk-delivery-plan` and passes `bin/check-plan-framing`.

## Workflow

**1. Restate the problem.**
Before decomposing, write one sentence: "This initiative wants [outcome] for [who]." Anchoring to the stated outcome — not to "what would make a plausible plan" — is the seatbelt against drifting into a tidy-looking hierarchy that doesn't serve the bet (agentic P3).

**2. [GATE] Confirm the input is a committed initiative.**
Read the goal and KRs. This is the **up-delegation**: delivery-shape *consumes* the committed initiative `initiative-shape` produces — it does not re-run that skill's goal/KR-shaping gates (re-authoring them guarantees drift, agentic P7). If there is no goal sentence, or fewer than the KRs the initiative was shaped with, the input is an idea, not an initiative — stop and route to `initiative-shape`. Do not invent KRs to proceed; deliverables with nothing to serve are the failure this gate prevents.

**3. [GATE] Map deliverables to KRs.**
Group the work into deliverables, each a milestone-class chunk that serves **exactly one KR**. Tag every `_deliverable.md` with `serves_kr:`. Two checks must hold before continuing: every deliverable serves one KR, and every KR is served by at least one deliverable. A KR with no deliverable is an unplanned outcome; a deliverable serving no KR is output without a bet (product A3).

**4. [GATE] Rule A1 — a design-doc-worthy deliverable gets a design doc before build.**
For each deliverable, test the Rule A1 triggers (eng-universal Rule A1, with agentic P8's slice-count translation of the "four weeks" trigger): does it break into **more than ~5 nodes**, contain a **one-way-door** decision, touch **shared infrastructure**, or carry **meaningful user / cost / compliance** impact? If any holds, the deliverable's **first** node is a `design-doc` node (`type: design-doc`, `delegates_to: design-doc`); the build nodes under it are **blocked by** that node and their task breakdown waits until the design doc is accepted — the design doc comes *before* task breakdown, not alongside it. If none holds, proceed straight to nodes on goal + deliverable, with no design-doc node. delivery-shape selects the branch and delegates the design-doc discipline to the `design-doc` skill; it does not re-author the design-doc structure inline (agentic P7). A smaller architecturally-significant decision that is not design-doc-worthy takes an `adr` node instead — Rule A1's "a short ADR may suffice."

**5. Decompose each deliverable into nodes; select the type and the delegate.**
A node is polymorphic — it is not always a story. For each unit of work, select the node `type` from the vocabulary in `docs/delivery-shape-contract.md` (`story`, `spike`, `adr`, `experiment`, `ktlo`, …), which fixes its completion form. Tag every node with `type`, `serves_kr`, `maps_to`, and `delegates_to` — the rule or skill that owns that type's discipline. **Do not re-author that discipline inline.** Copying a spike protocol or an ADR template into the node guarantees drift from its source (agentic P7); link and delegate instead.

**6. [GATE] Acceptance criteria by default on every `story` node.**
For each node typed `story`, emit an `## Acceptance criteria` block — a list of `Done when:` conditions, each a verifiable state, not a description of work. This is not optional and not deferred: a story without acceptance criteria does not pass this gate. If you cannot write the "done" check, the node is not understood well enough to be a story — reshape it or change its type. This gate is enforced mechanically by `bin/check-plan-framing` (every story carries the block; an empty block fails too).

**7. Break each node into tasks — walking skeleton first, foundational work folded in.**
List the node's tasks as `- [ ]` lines. The first task is the walking skeleton: the thinnest slice that runs the node's path end-to-end, marked with a leading `` `skeleton` `` tag. Before you write it, ask explicitly: **"what toolchain or setup must exist for this skeleton to run?"** — the language, parser, scaffold, fixture, account, or environment the end-to-end slice depends on. **Fold that answer into the skeleton task's description** (a parenthetical naming the folded work is enough); never emit it as a separate setup or scaffolding task *before* the skeleton (eng-universal Rule B2). A task placed before the skeleton defers the integration discovery the skeleton exists to surface on day one — which is the exact failure this prompt prevents. Each task is one observable outcome. The skeleton-and-folding rule is enforced mechanically by `bin/check-plan-framing` (≥1 skeleton task in the plan; no node with a task before its skeleton).

**8. Surface deferred, build-time delegation on every node.**
`delegates_to` fires at **pickup**, not at emission — expanding every node's fine-grained tasks now front-loads detail that decays before the node is reached (agentic P8). So delivery-shape stops at the node; it does not run the delegate. On each emitted issue-class artefact, write an explicit on-pickup instruction naming its `delegates_to` (a `story` says "expand via `planning-and-task-breakdown` before coding"; a `ktlo` node says "no breakdown step"). The picking-up agent follows that line. This is the one delegation obligation the contract places on the emitted artefact — see `docs/delivery-shape-contract.md` § *Delegation — timing & surfacing*.

**9. Emit the file-set.**
Write the directory layout from the template below: the root `README.md` carrying goal + KRs verbatim, the rendered tree, and the **hand-count manifest** (milestones / issues / sub-issues), one `D<n>/` per deliverable, one `N<nn>.md` per node. Numeric prefixes give deterministic order; pad node numbers past nine.

**10. [GATE] Verify the emitted plan.**
Run both gates. `bin/walk-delivery-plan <plan>` must exit 0 — the plan walks deterministically and the derived manifest equals the README oracle (this also enforces `serves_kr`, `type`, and `delegates_to` presence; a missing one exits 2). `bin/check-plan-framing <plan>` must exit 0 — every story carries acceptance criteria, the plan carries at least one `` `skeleton` ``-flagged task, and no node places a setup task before its skeleton. If either fails, the plan is not done; fix the file-set, do not relax the gate.

## Artefact template

The emitted file-set (paths relative to the plan root):

```
<initiative-slug>/
├── README.md                  goal + KRs verbatim · tree · hand-count manifest table
├── D1-<slug>/
│   ├── _deliverable.md        layer: deliverable · serves_kr · maps_to: <milestone-class>
│   └── N01-<slug>.md          a node (see below)
└── …
```

A `story` node file:

```markdown
---
layer: node
id: N01
type: story
title: <one line>
parent: D1
serves_kr: KR<n>
maps_to: <issue-class>
external_window: none          # never effort-in-days (agentic P8)
completion:
  form: acceptance-criteria
delegates_to: planning-and-task-breakdown (per-node task breakdown)
---

# N01 — <title>

> **As** <role>, **I want** <capability>, **so that** <benefit>.   ← grounded story form (Cohn)

> **▶ On pickup — before coding:** expand this node via `planning-and-task-breakdown`.

## Acceptance criteria
- **Done when:** <verifiable state, checked by …>

## Tasks
- [ ] `skeleton` — <thinnest end-to-end slice; foundational work folded in>
- [ ] <one observable outcome>
```

A `design-doc` node file — emitted as the **first** node of a deliverable that met a Rule A1 trigger (step 4); the build nodes that follow it carry a `Blocked by:` line naming it:

```markdown
---
layer: node
id: N01
type: design-doc
title: <deliverable> design doc (before build)
parent: D1
serves_kr: KR<n>
maps_to: <issue-class>
external_window: none
completion:
  form: the-design-doc
delegates_to: design-doc (Rule A1 design doc — produced before the build nodes are picked up)
---

# N01 — <title>

> **▶ On pickup — before any build node here:** produce the design doc via the `design-doc`
> skill. The build nodes under this deliverable are blocked by this node.
```

The root `README.md` ends with the hand-count manifest the walk-script reproduces:

```markdown
| Tracker artefact | Source layer | Count |
|------------------|--------------|------:|
| Milestones | deliverables (`D*`) | **<n>** |
| Issues | nodes (`N*`) | **<n>** |
| Sub-issues | tasks (`- [ ]` lines) | **<n>** |
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "I'll add acceptance criteria to the stories later, once I start building them." | Later is after you've built the wrong thing. AC written before the node is picked up is a spec that constrains the build; AC written after describes what got built. The gate exists to force the former. |
| "This story is obvious — it doesn't need a 'done when'." | If it's obvious, the criterion takes one line. If the line is hard to write, the story wasn't as obvious as assumed — which is exactly when the criterion is worth most. |
| "Let me copy the spike protocol / ADR template into the node so it's self-contained." | Self-contained is drift waiting to happen: the source updates, the copy rots, and the next agent reads a stale protocol with full confidence. Point `delegates_to` at the owner and link. |
| "I'll expand every node's tasks now while I have the context." | Fine-grained tasks decay before the node is reached (agentic P8). delivery-shape emits the node and the on-pickup delegation line; the delegate runs at pickup, on fresh context, against what's actually true then. |
| "A flat task list straight from the goal is faster than a three-layer hierarchy." | Faster to write, slower to verify. A flat list has no outcome trace (which KR does this serve?) and no per-story completion check. The hierarchy is what makes the plan walkable and gradable. |
| "This deliverable serves two KRs — I'll tag both." | A deliverable serving two KRs is two deliverables. One-KR-per-deliverable is what keeps the outcome spine legible; split it. |
| "The skeleton needs a setup task before it to install the toolchain." | A setup task before the skeleton defers integration discovery — the thing the skeleton exists to surface on day one. Fold the toolchain work into the skeleton task's description instead. |
| "This deliverable is clearly design-doc-worthy — I'll sketch the design inline so the plan is complete." | That re-authors the `design-doc` skill's discipline and rots the moment it updates (agentic P7). Emit a `design-doc` node, point `delegates_to` at the skill, and let the design doc be produced at pickup — before the build nodes' task breakdown. |
| "Every deliverable should get a design-doc node, to be safe." | No — that buries the signal. The branch is conditional on a Rule A1 trigger; a reversible, single-surface deliverable proceeds straight to nodes. A design-doc node on work that doesn't need one is the same waste as skipping one on work that does. |

## Red flags

- A `story` node has no `## Acceptance criteria` block, or the block is an empty heading.
- A deliverable has no `serves_kr`, or serves more than one KR.
- A node is missing `type`, `delegates_to`, or `maps_to`.
- A node's body re-states a spike protocol, ADR structure, design-doc structure, or test discipline inline instead of delegating to its owner.
- A deliverable that meets a Rule A1 trigger has no `design-doc` node before its build nodes — or a reversible, single-surface deliverable was given one it doesn't need.
- `external_window` carries a duration in days or weeks rather than a genuine external constraint (or `none`).
- A node's fine-grained build tasks were expanded at emission time rather than left to the on-pickup delegate.
- A "setup" or "scaffolding" task precedes the walking-skeleton task in a node.
- The emitted plan was declared done without running `bin/walk-delivery-plan` and `bin/check-plan-framing`.
- delivery-shape was run on a vague idea with no goal or KRs (should have routed to `initiative-shape`).

## Verification / exit criteria

The skill has run correctly when:

1. A delivery-plan file-set exists with a root `README.md`, one `D<n>/` per deliverable, and one `N<nn>.md` per node.
2. Every deliverable carries `serves_kr`, and every KR is served by at least one deliverable.
3. Every node carries `type`, `serves_kr`, `maps_to`, and `delegates_to`.
4. Every deliverable meeting a Rule A1 trigger has a `design-doc` node (`delegates_to: design-doc`) as its first node, with build nodes blocked by it; deliverables meeting no trigger have none.
5. Every `story` node carries an `## Acceptance criteria` block with at least one `Done when:` condition.
6. Each node's first task is the walking skeleton (`` `skeleton` `` tag), with foundational work folded in and no preceding setup task.
7. Every emitted issue-class artefact carries an on-pickup instruction naming its `delegates_to` (or "no breakdown step" for `ktlo`).
8. `bin/walk-delivery-plan <plan>` exits 0 — the plan walks deterministically and the derived manifest equals the README hand-count oracle.
9. `bin/check-plan-framing <plan>` exits 0 — every story node carries acceptance criteria, the plan carries at least one `` `skeleton` ``-flagged task, and no node places a task before its skeleton.

## References

- `docs/delivery-shape-contract.md` — the plan-artefact contract: three layers, cross-reference convention, per-node tags, node-type vocabulary, and the *Delegation — timing & surfacing* section this skill implements
- `bin/walk-delivery-plan` — the deterministic reader that walks the emitted file-set into a manifest and enforces `serves_kr` / `type` / `delegates_to` presence
- `bin/check-plan-framing` — the framing gate that asserts every story node carries acceptance criteria, the plan has at least one walking-skeleton task, and no node precedes its skeleton with a setup task
- `skills/initiative-shape/SKILL.md` — **up-delegation**: produces the committed initiative (goal + KRs) this skill consumes; delivery-shape does not re-run its shaping gates
- `skills/planning-and-task-breakdown/SKILL.md` — **down-delegation**: the per-node task-breakdown delegate that fires at pickup
- `skills/design-doc/SKILL.md` — the Rule A1 branch delegate: produces the design doc a design-doc-worthy deliverable needs before its build nodes' task breakdown
- `rules/eng-principles-agentic.md` — P3 (spec as seatbelt), P4 (evidence/acceptance by default), P7 (select and delegate, never re-author), P8 (slices and gates, deferred delegation)
- `rules/eng-principles-universal.md` — Rule B2 (walking skeleton first), Rule A1 (design-doc trigger)
- `rules/PRODUCT_RULES.md` — A3 (measurable success criterion: deliverable ↔ KR trace)
