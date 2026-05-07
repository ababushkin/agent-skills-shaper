---
name: planning-and-task-breakdown
description: >
  Decomposes a design or spec into small, verifiable tasks with acceptance criteria
  and dependency ordering — so implementation can proceed one confirmed slice at a
  time. Use before starting any non-trivial implementation. Trigger phrases: "break
  this down into tasks", "what do we need to build", "give me a task list", "sequence
  the work", "plan the implementation", "what order should we build this in",
  "decompose this into steps". Use this skill whenever the sequence of work isn't
  obvious before implementation begins.
pack: engineering
lifecycle_stage: plan
principles_implemented:
  - source: eng-universal
    id: Rule A1
    bucket: embedded
  - source: eng-universal
    id: Rule B1
    bucket: embedded
  - source: eng-universal
    id: Rule B2
    bucket: embedded
  - source: eng-universal
    id: Rule C4
    bucket: embedded
  - source: eng-agentic
    id: P3
    bucket: embedded
length_target: 200–260
author: Anton Babushkin
predecessor:
  repo: https://github.com/addyosmani/agent-skills
  skill: planning-and-task-breakdown
  relation: derivative
kept_from_predecessor:
  - Decompose into small, verifiable tasks
  - Acceptance criteria per task
  - Dependency ordering before sequencing
changed_from_predecessor:
  - Accepted design doc is a required input; the skill does not accept vague specs
  - Walking skeleton is the mandatory first task, not an optional starting point
  - Task size is bounded: any task that can't be described in one sentence is too big
  - Drift from design doc is an explicit failure mode
---

# Planning and task breakdown

## Purpose

This skill takes an accepted design doc and produces an ordered task list where each task is small enough to complete and verify independently. It bridges the gap between "we have an accepted design" and "we know exactly what to build in what order." The output is a sequence of well-scoped tasks, each with acceptance criteria, that whichever build skill the team uses will pick up one at a time.

The goal is not comprehensiveness — it is clarity and verifiability. A task list that looks thorough but whose tasks are too big to verify will not survive contact with implementation. Every task must answer: "how do I know this is done?"

## When to use

- A design doc has been accepted and implementation is ready to begin.
- A well-scoped spec exists for a change that doesn't meet the Rule A1 design-doc trigger, but is complex enough that sequencing and acceptance criteria are non-obvious.

## When not to use

- **No accepted design doc and the work exceeds a Rule A1 trigger** — run `design-doc` first. A draft or in-flight doc does not count as accepted.
- **The scope is unclear or contested** — resolve scope ambiguity in the design doc before breaking down tasks. Task breakdown from a vague spec produces tasks nobody believes in.

## Inputs

An accepted design doc covering at minimum: the problem being solved, the chosen approach, the components being changed or created, and the constraints. The design doc does not need to be perfect; it needs to be stable enough that the approach won't change during implementation.

## Outputs

An ordered task list at `docs/tasks/<feature-slug>.md`. Each task has: a one-sentence description, acceptance criteria (how you know it's done), and any upstream dependencies called out. The list begins with the walking skeleton as task 1.

## Workflow

**1. Read the design doc end-to-end.**
Do not start decomposing until you have read the full document. The most common task breakdown error is starting with the first section and ignoring the constraints and operability sections at the end. Those sections often constrain the sequencing.

**2. Identify the walking skeleton.**
The walking skeleton is the thinnest possible slice that exercises the full path end-to-end — from input to output — without filling in the real functionality. It is always task 1. If you cannot identify a walking skeleton (a slice that makes the system run, however crudely), the design doc is missing something. Stop and resolve it before proceeding.

Examples:
- API endpoint: a handler that accepts the request, returns a hardcoded response, passes a smoke test — no real logic yet.
- UI feature: a route that renders the page with static content — no data binding yet.
- Pipeline stage: a step that accepts the input format and emits the output format with placeholder data — no processing yet.

**3. Identify the feature slices.**
Starting from the walking skeleton, list the increments that build toward the full design. Each increment should:
- Extend functionality in one direction (add real logic, add a field, add an error path)
- Be independently testable
- Leave the system in a working, deployable state

Do not batch unrelated concerns into one slice. If a task touches the data layer AND the API AND the UI, it is three tasks.

**4. [GATE] Write acceptance criteria for each task.**
Before ordering tasks, write the "done" check for each one. An acceptance criterion is a test, an assertion, or a measurable condition — not a description of what to build. If you cannot write the acceptance criterion, the task is not well enough understood to schedule.

Format: `Task is done when: [specific, verifiable condition]`

- Bad: "Task is done when the search feature is implemented."
- Good: "Task is done when: a query against the `/search` endpoint returns a 200 with the correct result shape for a known test input, covered by an automated integration test."

**5. [GATE] Size check.**
Review every task. Any task that:
- Cannot be described in one sentence
- Has more than one acceptance criterion that requires a separate deployment to verify
- Would take more than one working session (~4–6 hours) to implement and verify

is too big. Split it. Size is not about effort estimation; it is about verification granularity. Small tasks surface problems early.

Example — too big:
> "Implement user authentication, including sign-up, login, password reset, and session management."

Split into verifiable tasks:
> Task A: POST /auth/signup creates a user and returns a JWT — covered by an integration test.
> Task B: POST /auth/login returns a JWT for valid credentials, 401 for invalid — covered by tests.
> Task C: POST /auth/password-reset sends a reset email — covered by a test mocking the mailer.
> Task D: Session expiry revokes access on subsequent requests — covered by a test advancing time.

Each task has one observable outcome, one test, and one commit boundary. That is a correctly sized task.

**6. Order by dependency.**
Sequence tasks so that each one's dependencies are complete before it starts. Call out explicit dependencies (on other tasks in this list, on external work, on platform capabilities). If a task depends on work from another team, flag it immediately — Rule C4: dependencies are surfaced before commitment.

**7. Write and file the task list.**
Use the template below. File at `docs/tasks/<feature-slug>.md`.

## Task list template

```markdown
# Tasks: <feature-slug>

Design doc: docs/designs/<feature-slug>.md
Last updated: <date>

## Task list

### Task 1 — Walking skeleton
**Description:** [one sentence — what does the skeleton do?]
**Done when:** [acceptance criterion]
**Dependencies:** none

### Task 2 — [name]
**Description:** [one sentence]
**Done when:** [acceptance criterion]
**Dependencies:** Task 1

### Task N — [name]
**Description:** [one sentence]
**Done when:** [acceptance criterion]
**Dependencies:** [list, or "none"]

## Open questions
<!-- Anything blocking or uncertain that was surfaced during breakdown.
     Do not start implementation until these are resolved. -->
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "The tasks are obvious from the design doc — no need to write them out." | If they're obvious, writing them out takes 15 minutes. If it takes more, they weren't as obvious as assumed. The acceptance criteria are worth the time even if the tasks aren't. |
| "We'll figure out the order as we go." | Unordered tasks produce surprise dependencies mid-implementation. Dependency discovery during a build is expensive; discovery before the build is cheap. |
| "This task is a bit big but we know what we're doing." | Task size is not a trust issue — it is a verification issue. Big tasks fail silently. Small tasks fail loudly and early. |
| "The design doc isn't fully accepted but it's close enough." | An almost-accepted design doc means the approach is still negotiable. Tasks broken down from a negotiable design are likely to be redone. |
| "We don't need a walking skeleton — we'll integrate at the end." | Integration at the end is the most expensive integration there is. The walking skeleton exists to find integration problems on day 1, not day 29. |
| "We already know the dependencies — no need to list them." | Dependencies change during implementation; listing them before forces you to verify each one rather than discover them when they block you. A listed dependency that turns out not to exist costs nothing. An unlisted dependency that surfaces mid-sprint costs days. |
| "I'll write acceptance criteria after I implement so I know what 'done' looks like." | By then you've already built the wrong thing. Acceptance criteria written before implementation are a spec — they constrain what you build. Criteria written after implementation describe what you built. The goal is the former. |
| "The task list will need to change anyway, so there's no point spending time on it." | The value is not the list surviving implementation intact. It is the thinking done while creating it — discovering the dependencies, sizing the slices, identifying the walking skeleton. A plan that gets revised is still better than no plan. |

## Red flags

- The walking skeleton is missing or is listed as something other than task 1.
- Any task has more than one independent acceptance criterion.
- Acceptance criteria say "feature is implemented" or "code is written" rather than describing a verifiable condition.
- Acceptance criteria reference implementation details ("the function is written") rather than observable behaviour ("the endpoint returns X for input Y").
- The task list was written before reading the constraints section of the design doc.
- A task depends on unresolved external work that hasn't been flagged.
- The list was generated from the design doc introduction without reading the full document.
- A "setup" or "scaffolding" task appears before the walking skeleton, deferring integration discovery.

## Verification / exit criteria

The skill has run correctly when:

1. A task list exists at `docs/tasks/<feature-slug>.md`.
2. Task 1 is the walking skeleton, with an acceptance criterion that can be checked independently of downstream tasks.
3. Every task has a single, concrete acceptance criterion stating a verifiable condition.
4. Every task can be described in one sentence.
5. Dependencies are listed for every task that has them.
6. Any external or cross-team dependency has been surfaced explicitly in the open questions section.
7. No "setup" or "scaffolding" task precedes the walking skeleton — if infrastructure is needed before the skeleton, the skeleton task encompasses it.
8. The open questions section is either populated with owners and resolution dates, or explicitly marked empty because no unresolved questions remain.

## References

- `rules/eng-principles-universal.md` — Rule A1 (design doc trigger), Rule B1 (YAGNI per slice), Rule B2 (walking skeleton first), Rule C4 (dependencies before commitment)
- `rules/eng-principles-agentic.md` — P3 (no drift from design doc)
- `skills/design-doc/SKILL.md` — the upstream output that this skill consumes
- Ryan Singer — "Shape Up" (appetite and scope as planning primitives)
