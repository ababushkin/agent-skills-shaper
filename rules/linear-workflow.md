# Linear workflow — initiative model

This document is the canonical governance model for how work is tracked in Linear across all repos in this workspace. It applies to: pde-skills, stock-review, agent-skills, nestl, adyen-onboarding.

---

## The initiative model

An **initiative** is a time-bounded, goal-oriented body of work with a stated success criterion and a bounded appetite. It is not a repo alias, not a backlog, and not a feature list.

An initiative is ready to enter a cycle when it can answer all four of these fields:

```
Goal:               For [who], we want to [solve problem / achieve outcome].
Success criterion:  [observable change] — measurable by [method], within [window].
Affected repos:     [list]
Appetite:           ~[N] issues
```

If any of the four fields can't be filled, the initiative is not ready. Create it as a Draft in Linear but don't assign it to a cycle.

### Initiative size

| Size | Issue count | Notes |
|---|---|---|
| Too small | < 5 | Not an initiative — create a standalone issue or put it in the ops slot |
| Small | 5–8 | One cycle slot with room left for other initiatives |
| Medium | 9–12 | One full cycle slot |
| Large | 13–15 | Full cycle slot; very little room for anything else |
| Too large | > 15 | Split into two initiatives before committing |

### Initiative lifecycle

| State | Meaning |
|---|---|
| **Draft** | Idea exists; goal or criterion not yet written |
| **Ready** | Goal + criterion + appetite confirmed; can enter a cycle |
| **Active** | Assigned to the current cycle; work in progress |
| **Done** | Success criterion observed (or definitively ruled out) — not just issues closed |
| **Paused** | Deprioritised mid-cycle; carries over with a note on why |

**Done ≠ all issues closed.** An initiative closes when the success criterion moves — or when the evidence definitively says it won't. An initiative that shipped everything but the criterion didn't move is not Done; it is Paused for a retrospective.

### Creating an initiative

Use the `/initiative-shape` skill. Do not create Linear projects by hand for goal-directed work — the skill enforces the four-field check before creating the project.

Direct creation is permitted only for: maintenance buckets, ops slots, and one-off standalone issue groupings.

---

## Cycle model

A cycle is 3–4 working days of focused work plus 1 planning day.

### Cycle composition

Every cycle has **exactly four slots**:

| Slot | Type | Goal/criterion required? |
|---|---|---|
| Initiative 1 | Goal-oriented | Yes |
| Initiative 2 | Goal-oriented | Yes |
| Initiative 3 | Goal-oriented | Yes |
| Ops slot | Maintenance | No |

The ops slot is not an initiative. It exists for: bug fixes, compliance items, emergent issues, one-offs, and KTLO work. Ops slot issues have no project assigned — they live directly on the team backlog and are pulled into the cycle as standalone issues.

**Do not add a 4th initiative.** The ops slot is not a buffer for overflow from the three initiative slots; it is a deliberate reservation for non-initiative work that would otherwise eat into initiative time unplanned.

### Cycle planning

On planning day:
1. Confirm 3 initiatives are in Ready state (four-field check passes for each).
2. Identify the ops slot: pull 2–5 issues from the team backlog (bugs, maintenance, one-offs) into the cycle as standalone issues.
3. For each initiative, confirm which issues in its backlog will be worked this cycle. Do not try to clear the entire initiative backlog in one cycle — prioritise by what moves the success criterion.
4. Assign all confirmed issues to the cycle.

### Cycle close

At cycle end, for each initiative:
- If the success criterion moved: mark initiative Done. Write one sentence in the Linear project description noting what was observed.
- If the work shipped but criterion didn't move yet: note this; either carry the initiative into the next cycle (Active) or pause it for a retrospective.
- If the initiative is being killed: mark Cancelled with a one-sentence reason. This is a normal outcome, not a failure.

---

## Backlog

**Backlog = team issues with no project assigned.**

Issues enter the backlog when:
- They don't belong to any current initiative
- They surface mid-flight as non-initiative work (bugs, one-offs)
- An initiative is killed and its remaining issues are descoped

Issues leave the backlog at cycle planning: either assigned to an initiative project, pulled into the ops slot for the current cycle, or explicitly deferred to a future cycle.

The backlog is not the idea bank. The idea bank (from `idea-triage`) holds unvalidated product hypotheses. The backlog holds concrete issues that are ready to be worked but not yet assigned.

---

## Issue workflow

### On start

- Move to **In Progress** via `mcp__claude_ai_Linear__save_issue`.
- If the issue isn't yet in the current cycle and you intend to ship it this cycle, assign it to the current cycle.
- Every issue must be either (a) assigned to an initiative project, or (b) explicitly in the ops slot (no project). An issue with neither a project nor a cycle assignment is untracked — don't let this happen.

### On completion

- Move to **Done** only after the work is committed AND pushed. An issue isn't Done if the work only exists locally.
- Status updates happen at the moment of state change — not batched at the end of a session.

### Blocked

Leave In Progress. Add a blocker comment naming the blocker explicitly. Don't silently park work.

### New work surfaced mid-flight

Two cases:

- **Initiative-shaped** (5+ issues, clear goal): create a new Linear project via `/initiative-shape`. Slot it into the next cycle explicitly — don't silently expand the current cycle's scope.
- **Bug or one-off** (< 5 issues, no sustained goal): create the issue on the team backlog. If it's urgent, pull it into the current cycle's ops slot.

---

## Linear project conventions

- **Project name**: goal or problem name, not a solution name and not a repo name.
  - Good: "Equity analysis report — usability for non-analysts"
  - Bad: "stock-review", "stock-explain feature", "pde-skills v2"
- **Project description**: always uses the four-field initiative format (goal / success criterion / affected repos / appetite).
- **Project state**: Planned until it enters a cycle; In Progress when active; Completed or Cancelled on close.

---

## What this model replaces

The previous model used repo-named Linear projects (e.g. "PDE skill pack", "Equity skill pack") as de-facto issue containers. These were not initiatives — they had no goal sentences, no success criteria, and no appetite. Work was tracked by repo rather than by outcome, making cross-repo initiatives invisible and preventing meaningful cycle planning.

The new model uses:
- **Projects** = initiatives (goal + criterion + appetite)
- **Team backlog** = issues not yet assigned to an initiative
- **Cycles** = sprint cadence pulling 3 initiatives + 1 ops slot
