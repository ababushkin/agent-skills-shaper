---
name: initiative-shape
description: >
  Shapes a vague idea into a properly formed Linear initiative — goal sentence, measurable
  success criterion, affected repos, appetite — then creates the Linear project. Use when
  starting any sustained body of work, converting a repo-aliased project into a goal-oriented
  initiative, or preparing for cycle planning. Trigger phrases: "I want to work on",
  "new initiative", "create a project", "we should tackle", "shape this for the next cycle",
  "what should the next initiative be".
pack: product
lifecycle_stage: define
principles_implemented:
  - source: product
    id: P2
    bucket: embedded
  - source: product
    id: P3
    bucket: embedded
  - source: product
    id: A2
    bucket: embedded
  - source: product
    id: A3
    bucket: embedded
  - source: product
    id: C1
    bucket: embedded
  - source: eng-agentic
    id: 3
    bucket: embedded
length_target: 200–260
author: Anton Babushkin
predecessor:
  repo: none
  skill: none
  relation: new
kept_from_predecessor: "n/a"
changed_from_predecessor: "n/a"
---

# Initiative shape

## Purpose

initiative-shape is the entry point for creating a new initiative. It takes a vague idea — a sentence, a direction, a problem — and shapes it into a properly formed Linear project with a goal sentence, measurable success criterion, affected repos, and bounded appetite. The shaped initiative is then created in Linear.

The skill exists because initiatives shaped without a success criterion become repo-aliased backlogs, and backlogs without goals don't drive decisions. Goal and criterion must be defined before the work begins — not inferred once the issues are closed (Rules P2, A3, C1, agentic Principle 3).

## When to use

- Starting any body of work that will span 5 or more issues.
- Converting an existing repo-project into a properly formed initiative.
- Preparing 3 initiatives for an upcoming cycle — run this once per initiative.
- When "I want to work on X" and X is clearly bigger than a single issue or bug fix.

## When not to use

- **Single-issue, bug, or KTLO work** — create the issue directly and put it in the ops slot. The ops slot has no goal/criterion requirement.
- **Unvalidated ideas that haven't cleared idea-triage** — run `idea-triage` first if you're unsure the problem is worth pursuing at all.
- **Scoping an already-formed initiative** — use `planning-and-task-breakdown` once goal + criterion are confirmed.

## Inputs

The vague idea in any form: a sentence, a project name, a direction, a problem statement fragment. The skill probes for everything else — do not require the user to pre-format anything.

Optional: a list of existing open issues the user expects to belong to this initiative.

## Outputs

A Linear project (via `mcp__claude_ai_Linear__save_project`) whose description follows the four-field initiative format: goal / success criterion / affected repos / appetite. The project starts in Planned state — it does not enter a cycle until cycle planning.

## Workflow

**1. Capture the raw idea.**
Write it down verbatim. Do not reframe it yet.

**2. [GATE] Problem or solution?**
Read the raw idea. Is it framed as something to build ("add X", "integrate Y") or a problem to solve ("users can't Z", "the model output isn't usable")? If solution, probe: "What goes wrong if we don't build this?" If the underlying problem can't be articulated, the initiative is not ready. Return for clarification; do not proceed.

**3. Probe — four questions.**
Ask explicitly. Do not infer. Wait for a response before synthesising.

- **Who is affected?** Which users, operators, or contexts does this problem touch?
- **What's the negative outcome if this isn't solved?** What task fails, what decision can't be made, what workflow breaks?
- **What would "done" look like?** Name the observable change — a behaviour that would be different, a metric that would move, a capability that would exist.
- **Which repos does this touch?** Name them. Cross-repo scope is allowed; name it explicitly.

**4. Probe — appetite.**
Separate question: "How big is this roughly — how many issues do you expect?" Guide: 5 issues ≈ small (1–2 days), 10 ≈ medium (full cycle slot), 15 ≈ large (fills the whole cycle). If the answer exceeds 15, the initiative needs splitting — flag this now.

**5. Synthesise into initiative format.**
Draft the four fields:

```
Goal:               For [who], we want to [solve problem / achieve outcome].
Success criterion:  [observable change] — measurable by [method], within [window].
Affected repos:     [list]
Appetite:           ~[N] issues
```

Present the draft. Do not create the Linear project yet.

**6. [GATE] User confirms the draft.**
Ask explicitly: "Does this capture the initiative correctly? Any changes before I create the project?" Do not proceed until confirmed. Fixing a wrong problem statement here takes one minute; fixing it mid-cycle costs days.

**7. Create the Linear project.**
Call `mcp__claude_ai_Linear__save_project` with:
- `name`: goal or problem label — not a solution name, not a repo name
- `description`: the four-field initiative format (see template below)
- Status: Planned

Confirm the project URL and share it.

**8. Optional: assign known issues.**
If the user listed existing issues for this initiative, list them and offer to reassign them to the new project via `mcp__claude_ai_Linear__save_issue`. Assign only the ones the user confirms.

## Initiative description template

```markdown
**Goal:** For [who], we want to [solve problem / achieve outcome].

**Success criterion:** [observable change] — measurable by [method], within [window].
When this criterion is met (or definitively ruled out), the initiative is Done.

**Affected repos:** [list]

**Appetite:** ~[N] issues
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "I know what the goal is — I don't need to write it down." | The criterion isn't for you right now; it's for the agent in the next session who has no memory of this conversation. Write it down. |
| "The success criterion will be obvious once the work is done." | Defining it after the work is done is how "shipped = done" creeps in. The criterion is what converts a list of closed issues into an achieved outcome. |
| "This is too big for 15 issues but it's one coherent thing." | Split by outcome: what's the first observable change you want to see? That's one initiative. The rest follow. |
| "I'll sort out the criterion after we create the project." | Step 6 is a gate. The project doesn't get created until the criterion is confirmed. |
| "The affected repo is obvious — we only work in one repo here." | Name it anyway. The field exists for cross-repo legibility, not to teach you something you don't know. |

## Red flags

- The success criterion says "improve X" or "better Y" with no measurement method or window.
- The initiative name describes a solution ("Build the X feature") rather than a goal or problem.
- The appetite is expressed as a time duration ("2 weeks") rather than an issue count.
- The Linear project was created before Step 6 confirmed the draft.
- An initiative with > 15 issues in appetite was created without a split decision.

## Verification / exit criteria

The skill has run correctly when:

1. A Linear project exists with a description containing all four canonical fields.
2. The goal sentence names who is affected and what the outcome is — not a solution.
3. The success criterion names the observable change, the measurement method, and the window.
4. The appetite is expressed in issues (not days or weeks).
5. The user confirmed the draft before the project was created (Step 6 gate honoured).

## References

- `rules/linear-workflow.md` — initiative definition, lifecycle, cycle model, ops slot (source of truth)
- `rules/PRODUCT_RULES.md` — P2 (problems not solutions), P3 (bets), A2 (problem format), A3 (success criteria), C1 (appetite)
- `rules/eng-principles-agentic.md` — Principle 3 (spec as seatbelt; goal must precede work)
- `skills/idea-triage/SKILL.md` — upstream: run when confidence is low before committing to an initiative
- `skills/planning-and-task-breakdown/SKILL.md` — downstream: breaks a confirmed initiative into issues
