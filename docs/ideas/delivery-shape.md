# delivery-shape — top-down delivery planning (tool-agnostic)

> Status: refined idea, pre-spike. Output of an `idea-refine` session.

## Problem Statement
**How might we turn a committed initiative into a complete, ordered delivery plan — deliverables → capabilities → stories → verifiable tasks — as a set of hierarchically cross-referenced markdown files, with the framing baked in and foundational work never silent, so any tracker-layer (`agent-skills-workflow` → Linear) can map it mechanically?**

Today the pack has strong point skills but no executable connective tissue between *defining the bet* and *breaking it into tasks*. The user re-prompts the framing every time, gets tasks that are too low-level or missing acceptance criteria, and forgets to plan foundational/toolchain work — because `planning-and-task-breakdown` consumes a design doc (not an initiative), is deliberately anti-user-story, and forbids pre-skeleton setup tasks.

## Where it sits in the lifecycle
The target `-shape` vocabulary (renames tracked separately — see Dependencies):

> shape the idea → shape the outcome → **shape the delivery** → shape the tasks
> `idea-triage` → `initiative-shape` → **`delivery-shape`** *(new)* → `planning-and-task-breakdown`

`delivery-shape` owns **the plan**: how a committed initiative gets delivered. It is *not* the initiative (the bet) — the plan belongs to the initiative. This is why it isn't named `project-shape`: in this workspace `linear-workflow.md` hard-codes Projects ≡ initiatives, so "project" already names the bet layer.

## Recommended Direction
A `-shape`-family skill that takes a shaped initiative (goal + KRs) and emits **a set of cross-referencing markdown files** representing the full delivery hierarchy. It delegates up and down rather than re-implementing (avoids gate-drift, agentic P7):

1. **Upstream:** `initiative-shape` provides goal + KRs (delegated; depends on `initiative-shape` being Linear-decoupled first).
2. **Rule A1 gate:** design-doc trigger met → delegate to `design-doc`; else proceed on goal + deliverables.
3. **New contribution:** decompose into deliverables (each tagged to a KR) → capabilities (headings) → user stories (with acceptance criteria by default).
4. **Foundational prompt:** ask "what toolchain/setup must exist for the skeleton to run?" → fold into the walking-skeleton task (stack-agnostic, no tool names in prose).
5. **Downstream:** delegate to `planning-and-task-breakdown` per capability → walking skeleton task 1, verifiable slices under capability headers.

**The seam to `agent-skills-workflow` is the file-set structure** (directory layout + cross-reference convention + per-node tags), not a tool API. Ports-and-adapters (eng-universal A7): shaper owns the plan artefact; the workflow repo owns the Linear adapter.

## The layers (standalone markdown file-set)

| Layer | Lives as | Adapter (other repo) maps to |
|---|---|---|
| Deliverable / milestone | A file (or top section), tagged with the KR it serves | Linear milestone |
| Capability / epic | Heading / sub-file under its deliverable | Label / parent issue |
| User story | Subsection with acceptance criteria | Linear issue |
| Task / slice | Sub-list under the story; walking skeleton first | Sub-issue / task line |

The right-hand column is **not our concern** — it documents the seam so the adapter author knows what to expect.

## Walking-skeleton spike (first slice — do this before building the skill)
By hand, take **one real, already-shaped initiative** and produce the hierarchical markdown file-set end-to-end. Deliverables:
- A concrete file-set a human can read top-down and a script could walk.
- The **schema/contract** read off that example: directory layout, cross-reference convention (front-matter links? relative paths? a manifest file?), per-node tags (deliverable↔KR, story↔AC, task↔skeleton flag).
- A **decision: (A) new skill vs (B) expand `planning-and-task-breakdown`** — based on how much unique structure the upper layers actually carried. (Signal toward B: every good name for the new skill crowds `planning-and-task-breakdown`'s territory.)
- A sanity check that the file-set converts to tracker artefacts mechanically.

## Key Assumptions to Validate
- [ ] **Hierarchy is faithfully expressible as cross-referenced markdown** and walks deterministically. *Spike proves or breaks this.*
- [ ] **The file-set is mechanically convertible to tracker artefacts.** *Trace the example against Linear milestone/issue/sub-issue shapes.*
- [ ] **Invocation reliability** — triggers on "plan a project" / "let's plan this out" without colliding with `planning-and-task-breakdown` or `initiative-shape`. *Triggering eval on 8–10 phrasings.*
- [ ] **`initiative-shape` decoupling lands first** — hard dependency; this skill stays parked until then.

## MVP Scope
**In:** the walking-skeleton schema spike (above); the documented plan-artefact contract; the skill (or the `planning-and-task-breakdown` expansion, per spike outcome) with the deliverable/capability/story decomposition + foundational prompt + Rule A1 branch + delegation; an update to `using-this-pack`'s flowchart for discoverability.

**Out:** any tracker writes (that's `agent-skills-workflow`); the `initiative-shape` decoupling itself (separate, sequenced-first); the `-shape` vocabulary renames (separate initiative).

## Not Doing (and Why)
- **Merging the bet and the plan into one skill** — violates Now-Next-Later; you'd force premature detail-planning of Later bets.
- **Any Linear/tracker coupling** — the seam is the markdown file-set.
- **Naming it `project-shape`** — collides with `initiative-shape` (Projects ≡ initiatives).
- **Deciding new-skill vs expand up front** — let the spike's evidence settle it.
- **Copying sub-skill gates into the orchestrator** — guarantees drift; delegate.
- **Referencing the future `-shape` names** — `delivery-shape` cites current names (`initiative-shape`, `planning-and-task-breakdown`) until the renames land.

## Open Questions (post-spike)
- **(A) new skill vs (B) expand `planning-and-task-breakdown`** — spike decides.
- **Cross-reference convention** for the file-set — the spike's core output.

## Dependencies / sequencing
1. `initiative-shape` Linear-decoupling lands first (separate work). This skill is parked until then.
2. Vocabulary unification (`idea-triage`→`idea-shape`, `initiative`→`outcome`, `planning-and-task-breakdown`→`task-shape`) is an **independent initiative** — does not block this; `delivery-shape` tracks current names in the interim.
