---
name: delivery-shape
description: Decomposes a committed initiative (goal + key results) into an ordered, verifiable delivery hierarchy — deliverables → nodes → tasks — that a human reads top-down and a deterministic reader walks bottom-up into a tracker manifest. Use after an initiative is shaped and before any node is picked up to build. Trigger phrases: "turn this initiative into a delivery plan", "decompose this initiative", "break the initiative into deliverables", "plan the delivery for this", "shape the delivery", "what are the deliverables for this initiative".
---

# Delivery shape

## Purpose

Take a committed initiative — its goal and key results — and emit the full delivery hierarchy that sits between "we have an initiative" and "we know what to build, in what order, and how we'll know each piece is done."

The hierarchy has three layers: deliverables (each serving one KR), nodes (polymorphic units of work — a story, a spike, an ADR, an experiment, …), and tasks (the checklist inside a node). A human reads it top-down from the outcome; a deterministic reader walks it bottom-up into a tracker manifest. Every deliverable traces to a KR, every node names its completion form, and every node carries a uniform five-section body. The skill selects and delegates to the disciplines it points at; it does not re-author them inline.

## When to use

- A committed initiative exists (goal + 3–5 KRs) and you need the deliverable → node → task hierarchy before work starts.
- You are about to write a flat task list from an initiative and want the outcome trace (deliverable ↔ KR) and per-node completion framing baked in instead.

## Do not use when

- No committed initiative yet — the input is a vague idea or a problem with no goal/KRs. Run initiative-shape first; delivery-shape consumes its output.
- A single node is ready to build — you have one issue and need its task breakdown. Use the at-pickup breakdown phase of your build agent or hand the node to your build skill.
- Single-issue, bug, or KTLO work — create the issue directly in the ops slot. A bug fix does not need a deliverable hierarchy.

## Inputs

A committed initiative as text: the goal sentence and 3–5 key results (the six-field shape initiative-shape produces is ideal; goal + KRs as plain text is the minimum). The KRs are the spine every deliverable traces to. If the input has no KRs, stop — there is nothing for deliverables to serve.

## Outputs

A delivery-plan file-set under `examples/delivery-plans/<initiative-slug>/` (or the path the caller names), laid out per `docs/delivery-shape-contract.md`: a root `README.md` (goal + KRs + tree + hand-count manifest), one `D<n>-<slug>/` directory per deliverable with a `_deliverable.md`, and one `N<nn>-<slug>.md` per node. The file-set walks cleanly under `bin/walk-delivery-plan` and passes `bin/check-plan-framing`.

## Workflow

### 1. Restate the problem

Write one sentence: "This initiative wants [outcome] for [who]." Anchor to the stated outcome, not to "what would make a plausible plan."

### 2. Gate: scale — full hierarchy or lite tier

Before checking whether KRs are present, triage scale. Two output shapes share one body
discipline; the input picks the tier:

- **Lite tier** — a single outcome with no KR worth tracking and ≤~3 distinct changes (a small
  task, a tuning job, a behaviour-preserving sweep). Emit `Context` + `Goal` + one
  `N<nn>-*.md` node per change at the plan root, each with the five-section body. **No** `D*`
  deliverable directories, **no** KR/deliverable tagging, **no** task breakdown, **no** walking
  skeleton, **no** manifest table. The lite plan still walks under `bin/walk-delivery-plan` and
  passes `bin/check-plan-framing` — the gates detect the lite shape automatically.
- **Full hierarchy** — anything that produces or maps to a committed initiative (goal + 3–5
  KRs). Proceed through steps 3–9 as the full deliverable → node → task hierarchy.

When in doubt, prefer lite: an under-shaped lite plan converts up to full cheaply, whereas a
full plan emitted for a single task is pure ceremony. If you pick full, you owe an initiative;
read the goal and KRs next and, if there is no goal sentence or fewer KRs than the initiative
was shaped with, stop and route to initiative-shape. Do not invent KRs to proceed.

The remaining workflow steps (3–9) describe the **full** path. Lite emits steps 5 (node body)
and 9 (gate verification) only — KR mapping, design-doc triggering, task breakdown, and the
file-set layout collapse to a flat `N*.md` set at the plan root.

### 3. Gate: map deliverables to KRs

Group the work into deliverables, each a milestone-class chunk serving **exactly one KR**. Tag every `_deliverable.md` with `serves_kr:`. Two checks must hold: every deliverable serves one KR, and every KR is served by at least one deliverable. A KR with no deliverable is an unplanned outcome; a deliverable serving no KR is output without a bet.

### 4. Gate: design-doc-worthy deliverables get a design doc before build

For each deliverable, test the triggers: does it break into **more than ~5 nodes**, contain a **one-way-door** decision, touch **shared infrastructure**, or carry **meaningful user / cost / compliance** impact? If any holds, the deliverable's **first** node is a `design-doc` node (`type: design-doc`); the build nodes under it are **blocked by** that node and their task breakdown waits until the design doc is accepted. If none holds, proceed straight to nodes. A smaller architecturally-significant decision that is not design-doc-worthy takes an `adr` node instead. Delegate the design-doc discipline to the design-doc skill; do not re-author its structure inline.

### 5. Decompose each deliverable into nodes; select the type

A node is polymorphic — not always a story. For each unit of work, select the node `type` from the vocabulary in `docs/delivery-shape-contract.md` (`story`, `spike`, `adr`, `experiment`, `refactor`, `ktlo`, …), which fixes its completion form. **`refactor`** is the type for behaviour-preserving change — its `## Completion` is an invariant (`**Invariant:** … **Verified by:** … **Out of scope:** …`), not a Cohn story or `Done when:` list. Tag every node with `type`, `serves_kr`, and `maps_to`. Do not copy a spike protocol or ADR template into the node — link to the source instead.

### 6. Gate: five-section body on every node, with type-appropriate Completion

Emit all five body sections — **What / Why / Completion / Assumptions / Key Risks** — on every node, regardless of type or tier (lite and full share one body definition). The Cohn story form ("As <role>, I want…, so that…") is the first sentence of `## What` on story nodes. Completion content is type-dependent (story → `Done when:` list; spike → decision + stop condition; experiment → hypothesis + success metric; adr → decision record; design-doc → what the accepted doc covers; **refactor → `Invariant:` + `Verified by:` + `Out of scope:`**; ktlo → none). Every Assumptions item carries a `(verified)` or `(to-verify)` tag; `(to-verify)` items block pickup. Every Key Risk carries a mitigation step or a falsifier.

An optional sixth section, **`## Non-goals`**, names scope the node deliberately excludes — work tempting to absorb but being declined, so the exclusion survives into pickup rather than being rediscovered there. Add it only when such tempting-but-excluded scope exists; do not pad. When the heading is present, the section must carry at least one list item. `## Non-goals` is distinct from `refactor`'s `**Out of scope:**` line inside `## Completion` (which names what the invariant protects); `## Non-goals` names excluded **work**.

Enforced mechanically by `bin/check-plan-framing`.

### 7. Break each node into tasks

Work through six sub-steps in order. Every task ends up on a single `- [ ]` line in the format shown in the template.

**7a. Walking skeleton first, foundational work folded in (executable nodes only).** The first task is the walking skeleton: the thinnest slice that runs the node's path end-to-end, marked with a leading `` `skeleton` `` tag. Before writing it, ask: "what toolchain or setup must exist for this skeleton to run?" Fold that answer into the skeleton task's description (a parenthetical is enough); never emit it as a separate setup task *before* the skeleton — that defers the integration discovery the skeleton exists to surface on day one. The skeleton mandate applies to executable software nodes (`story`, `refactor`, `capability`, `migration`, `experiment`); a doc/spec/config node (`adr`, `design-doc`, `ktlo`, …) has no executable path to run end-to-end and carries no skeleton task — only its non-skeleton breakdown tasks (if any).

**7b. Feature slices — each extends one direction and is independently deployable.** After the skeleton, add one task per feature slice. Each extends the skeleton in exactly one direction (one capability, one layer, one error path), is independently testable, and leaves the system deployable on its own. A half-wired slice that needs the next task to compile is a fragment, not a slice. Name each as one observable outcome.

**7c. Gate: acceptance criterion on every task, written before ordering.** Write a `Done when:` clause on every task (skeleton included) before sequencing. It must be a verifiable condition, not a description of the work: "Done when: the endpoint returns 200 for a valid request" is a criterion; "Done when: the handler is wired up" is a description. A task whose criterion can't be written in one sentence is not yet well-scoped.

**7d. Gate: size check — one sentence, one verifiable outcome.** Review every task against two tests: the description fits in one sentence, and the task has exactly one `Done when:` clause. A description needing more than one sentence holds multiple concerns; more than one independent `Done when:` means multiple tasks. Split any that fail. This is verification granularity, not effort estimation.

**7e. Dependency ordering — sequence tasks; flag external blocks inline.** Sequence so each task builds only on completed prior tasks: skeleton first, then feature slices ordered by dependency, not difficulty. For any task depending on a cross-team deliverable, external credential, third-party environment, or shared-infrastructure change outside this node, flag it inline with `⚠ blocks on: <dependency>`.

**7f. Model routing — apply the 5-axis rubric and append a `Model:` annotation.** Score the five axes from `references/task-sizing.md` (RC, SC, HS, SR, OR) Low/Med/High and derive the tier and review flag using the reversibility-gated routing rule. Append the result inline; the annotation must begin with `Model:`. When SR = High, also append `companions code-review-and-quality`; when HS = High, also append `companions source-driven-development`. A task with no `Model:` annotation is not complete.

### 8. Emit the file-set

Write the directory layout from the template: the root `README.md` carrying goal + KRs verbatim, the rendered tree, and the hand-count manifest (milestones / issues / sub-issues); one `D<n>/` per deliverable; one `N<nn>.md` per node. Numeric prefixes give deterministic order; pad node numbers past nine.

### 9. Gate: verify the emitted plan

Run both gates. `bin/walk-delivery-plan <plan>` must exit 0 — the plan walks deterministically and the derived manifest equals the README oracle (also enforces `serves_kr`, `type`, `maps_to` presence). `bin/check-plan-framing <plan>` must exit 0 — every node carries the five sections, every Assumptions item is tagged, the plan has at least one `` `skeleton` `` task, no node places a setup task before its skeleton, and every task carries a `Done when:` clause and a `Model:` annotation. If either fails, fix the file-set — do not relax the gate.

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

Every node — regardless of type — uses the same five-section body. Completion content varies by `type`; the heading is required on all of them.

```markdown
---
layer: node
id: N01
type: <story | spike | adr | experiment | refactor | ktlo | design-doc>
title: <one line>
parent: D1
serves_kr: KR<n>
maps_to: <issue-class>
completion:
  form: <completion-criterion form — see vocabulary in contract>
---

# N01 — <title>

## What

<For `story`: the grounded story form (Cohn) — "As <role>, I want <capability>,
so that <benefit>" — as the first sentence, then clarifying context.>
<For other types: what this node investigates, decides, or maintains.>

## Why

<Per-node rationale beyond `serves_kr`: the bet this node makes, the rejected
alternative, what it unblocks. Do not re-state the KR.>

## Completion

<`story` → `- **Done when:** <verifiable state>` list (≥1 item).>
<`spike` → `**Decision:** <question>` + `**Stop condition:** <when to stop>`.>
<`adr` → `**Decision:** <accepted>` + context/consequences + ADR reference.>
<`design-doc` → prose naming what the accepted design doc covers.>
<`experiment` → `**Hypothesis:**` + `**Success metric:**` + falsification condition.>
<`refactor` → `**Invariant:** <what stays true>` + `**Verified by:** <existing coverage, unchanged>` + `**Out of scope:** <what the invariant protects>`.>
<`ktlo` → `None — roadmap A5 carve-out.`>

## Assumptions

<`- <assumption> *(verified)*` or `- <assumption> *(to-verify)*` items.
`(to-verify)` items block pickup. `*(none)*` is valid for ktlo and simple nodes.>

## Key Risks

<`- **Risk:** <…>` items, each carrying a `*Mitigation:*` step OR a `*Falsifier:*`
(an observable outcome that would confirm it is not actually a risk).
`*(none)*` is valid when no risks are identified.>

## Non-goals  *(optional — include only when tempting-but-excluded scope exists)*

<List items (`- <item>`) naming scope this node deliberately excludes. If the
heading is present the section must carry at least one item; an empty
Non-goals heading fails `bin/check-plan-framing`.>

## Tasks
- [ ] `skeleton` — <thinnest end-to-end slice; foundational work folded in> · Done when: <verifiable condition> · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·M·L·L·L
- [ ] <one observable outcome> · Done when: <verifiable condition> · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
```

The root `README.md` ends with the hand-count manifest the walk-script reproduces:

```markdown
| Tracker artefact | Source layer | Count |
|------------------|--------------|------:|
| Milestones | deliverables (`D*`) | **<n>** |
| Issues | nodes (`N*`) | **<n>** |
| Sub-issues | tasks (`- [ ]` lines) | **<n>** |
```

## Red flags

- A node is missing any of the five body sections, or Completion is absent on a story node.
- A node carries a `## Non-goals` heading with no list items underneath — an empty exclusion list is a heading that drifted away from its content.
- A `refactor` node's Completion is written as a Cohn story or a `Done when:` list instead of `**Invariant:**` + `**Verified by:**` + `**Out of scope:**`.
- The skill was run on a single task or 2–3 changes and emitted the full KR → deliverable → node → task hierarchy with walking skeletons and a manifest (should have routed to the lite tier).
- A task's `Done when:` describes the work performed rather than a verifiable outcome, or is absent.
- A task description needs more than one sentence, or carries more than one independent `Done when:` — both require a split.
- A feature slice leaves the system non-deployable, or depends on a later task to pass its own criterion — a fragment, not a slice.
- A cross-team or external dependency is not flagged inline on the task that blocks on it.
- Any task line is missing its `Model:` annotation.
- An Assumptions item lacks a `(verified)`/`(to-verify)` tag, or a Key Risk carries neither mitigation nor falsifier.
- A deliverable has no `serves_kr`, or serves more than one KR.
- A node is missing `type` or `maps_to`.
- A node re-states a spike protocol, ADR structure, design-doc structure, or test discipline inline instead of delegating.
- A deliverable that meets a design-doc trigger has no `design-doc` node before its build nodes — or a reversible, single-surface deliverable was given one it doesn't need.
- A node's fine-grained build tasks were expanded at emission time rather than deferred to pickup.
- A setup or scaffolding task precedes the walking-skeleton task in a node.
- The plan was declared done without running `bin/walk-delivery-plan` and `bin/check-plan-framing`.
- delivery-shape was run on a vague idea with no goal or KRs (should have routed to initiative-shape).

## Exit criteria

The skill is complete when:

1. A file-set exists with a root `README.md`, one `D<n>/` per deliverable, and one `N<nn>.md` per node.
2. Every deliverable carries `serves_kr`, and every KR is served by at least one deliverable.
3. Every node carries `type`, `serves_kr`, and `maps_to`.
4. Every deliverable meeting a trigger has a `design-doc` node as its first node, with build nodes blocked by it; deliverables meeting no trigger have none.
5. Every node carries the five body sections, with Completion populated per its `type`, every Assumptions item tagged, and every Key Risk carrying a mitigation or falsifier.
6. Each node's first task is the walking skeleton (no preceding setup task, foundational work folded in); remaining tasks are independently testable, deployable slices; every task carries a verifiable `Done when:` and a one-sentence/one-criterion scope; tasks are sequenced by dependency with external blocks flagged inline; every task carries a `Model:` annotation.
7. `bin/walk-delivery-plan <plan>` exits 0.
8. `bin/check-plan-framing <plan>` exits 0.

## Related

- initiative-shape: produces the committed initiative (goal + KRs) this skill consumes.
- design-doc: the delegate for a design-doc-worthy deliverable, before its build nodes' task breakdown.
- `docs/delivery-shape-contract.md` — the plan-artefact contract: layers, cross-reference convention, per-node tags, node-type vocabulary, delegation timing.
- `bin/walk-delivery-plan`, `bin/check-plan-framing` — the deterministic reader and framing gate.
- `references/task-sizing.md` — the 5-axis model-routing rubric.
