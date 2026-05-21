# Linear workflow — initiative model

This document is the canonical governance model for how work is tracked in Linear across all repos in this workspace. It applies to: pde-skills, stock-review, agent-skills, nestl, adyen-onboarding.

---

## The initiative model

An **initiative** is a time-bounded, goal-oriented body of work with a stated success criterion and a bounded appetite. It is not a repo alias, not a backlog, and not a feature list.

An initiative is ready to enter a cycle when it can answer all six of these fields:

```
Goal:           For [who], we want to [solve problem / achieve outcome].
Key results:    1. [committed|aspirational] — [observable state — binary pass/fail,
                      fitness function firing, or measurable delta]
                   baseline: [current value/state]
                   target:   [value/state we expect at the end]
                   window:   [when this is judged — "by end of cycle", "within 30 days"]
                   source:   [where the evidence lives — file path, log, Linear query]
                2. [committed|aspirational] — [observable state]
                   baseline: ...  target: ...  window: ...  source: ...
                3. [committed|aspirational] — [observable state]
                   baseline: ...  target: ...  window: ...  source: ...
                (3–5 KRs total; each verifiable by inspecting the system —
                 no "improve X" / "better Y" / "run N times" language)
Affected repos: [list]
Appetite:       ~[N] issues  (not days or weeks)
Kill condition: [observable state that says "the bet didn't work, walk away"]
Project type:   [1: methodology | 2: personal product | 3: utility skill pack |
                 4: research/thesis | 5: equity research | 6: production]
```

The format is OKR-shaped: the Goal is the Objective (qualitative, what we want to achieve), and Key results are the 3–5 observable states that must be true for the initiative to be Done. KRs are written so a future agent (or you on a fresh session) can verify each by looking at the system — no "improve X" / "better Y" language. Each KR carries four sub-fields (baseline / target / window / source) and a `[committed|aspirational]` tag that sets the grading bar at cycle close.

If any of the six fields can't be filled, the initiative is not ready. Create it as a Draft in Linear but don't assign it to a cycle.

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
| **Ready** | All six fields confirmed — Goal + Key results (with sub-fields + tags) + Affected repos + Appetite + Kill condition + Project type; can enter a cycle |
| **Active** | Assigned to the current cycle; work in progress |
| **Done** | Success criterion observed (or definitively ruled out) — not just issues closed |
| **Paused** | Deprioritised mid-cycle; carries over with a note on why |
| **Cancelled** | Kill condition triggered, or initiative definitively ruled out mid-cycle; one-sentence reason recorded |

**Done ≠ all issues closed.** An initiative closes when the key results are observed (or definitively ruled out) — not when its issue list reaches zero. An initiative that shipped everything but the KRs didn't hold is not Done; it is Paused for a retrospective.

### Creating an initiative

Use the `/initiative-shape` skill. Do not create Linear projects by hand for goal-directed work — the skill enforces the six-field check (including the 10-rule verification rubric gate at Step 6.5) before creating the project.

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

The ops slot is not an initiative. It exists for: bug fixes, compliance items, emergent issues, one-offs, and KTLO work. Ops slot issues either have no project assigned, or live in the team's **ops container project** — a perpetual Backlog-state project named e.g. "Ops — bugs, maintenance, emergent" that holds ops work. The container project carries no Goal and no Key Results because it is not an initiative — it exists only because MCP tooling can't clear an issue's project assignment, so issues created via Claude Code need a non-initiative home.

**Do not add a 4th initiative.** The ops slot is not a buffer for overflow from the three initiative slots; it is a deliberate reservation for non-initiative work that would otherwise eat into initiative time unplanned. The ops container project is not an initiative either — it doesn't get a Goal, KRs, or appetite, and it never enters the Done state.

### Cycle planning

On planning day:
1. Confirm 3 initiatives are in Ready state (six-field check passes for each: Goal + Key results with sub-fields + Affected repos + Appetite + Kill condition + Project type).
2. Identify the ops slot: pull 2–5 issues from the team backlog (bugs, maintenance, one-offs) into the cycle as standalone issues.
3. For each initiative, confirm which issues in its backlog will be worked this cycle. Do not try to clear the entire initiative backlog in one cycle — prioritise by what moves a Key Result.
4. Assign all confirmed issues to the cycle.

### Cycle close

At cycle end, for each initiative:
- If all key results hold (or were definitively ruled out): mark initiative Done. Write one sentence in the Linear project description noting what was observed.
- If the work shipped but KRs didn't hold yet: note this; either carry the initiative into the next cycle (Active) or pause it for a retrospective.
- If the initiative is being killed: mark Cancelled with a one-sentence reason. This is a normal outcome, not a failure.

---

## Backlog

**Backlog = team issues with no project assigned, plus issues in the ops container project.**

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
- Every issue must be either (a) assigned to an initiative project, or (b) explicitly in the ops slot — meaning either no project assigned, or in the ops container project. An issue with neither an initiative nor an ops home is untracked — don't let this happen.

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
- **Project description**: always uses the six-field initiative format (goal / key results with sub-fields / affected repos / appetite / kill condition / project type).
- **Project state**: Planned until it enters a cycle; In Progress when active; Completed or Cancelled on close.

---

## What this model replaces

The previous model used repo-named Linear projects (e.g. "PDE skill pack", "Equity skill pack") as de-facto issue containers. These were not initiatives — they had no goal sentences, no key results, and no appetite. Work was tracked by repo rather than by outcome, making cross-repo initiatives invisible and preventing meaningful cycle planning.

The new model uses:
- **Projects** = initiatives (goal + key results + appetite)
- **Team backlog** = issues not yet assigned to an initiative
- **Cycles** = sprint cadence pulling 3 initiatives + 1 ops slot
