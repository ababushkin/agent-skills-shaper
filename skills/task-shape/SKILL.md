---
name: task-shape
description: >
  Shapes a single Linear issue before implementation begins: surfaces AC gaps and
  ambiguities, decides whether the work is single-stack or multi-stack, and produces
  a per-stack ordered task list with a walking skeleton as the first task.
  Use at implementation time, when a worker session picks up a ticket.
  Trigger phrases: "shape this issue", "is this ticket ready to build",
  "verify the acceptance criteria", "what's the task list for this issue",
  "single-stack or multi-stack?", "break this ticket into tasks".
pack: engineering
lifecycle_stage: plan
principles_implemented:
  - source: eng-universal
    id: Rule B2
    bucket: embedded
  - source: eng-universal
    id: Rule B7
    bucket: embedded
  - source: eng-agentic
    id: P3
    bucket: embedded
  - source: eng-agentic
    id: P4
    bucket: embedded
  - source: eng-agentic
    id: P8
    bucket: embedded
length_target: 180–220
author: Anton Babushkin
predecessor:
  repo: none
  skill: none
  relation: new
kept_from_predecessor: "n/a"
changed_from_predecessor: "n/a"
---

# Task shape

## Purpose

task-shape is the first thing that runs when a worker session picks up a ticket. It reads the Linear issue, verifies that the acceptance criteria are complete and unambiguous, decides whether the work is single-stack or spans multiple stacks, and produces a per-stack ordered task list ready for implementation. The output is appended to the issue body so the implementer and any reviewer read the same structured contract.

The skill exists because implementation commonly starts on tickets whose AC is incomplete, whose scope is ambiguous, or whose multi-stack nature wasn't visible at planning time. Surfacing these gaps before the first line is written costs minutes; discovering them mid-build costs sprints.

## When to use

- A worker session picks up a Linear issue and implementation is about to begin.
- An issue has been assigned but its AC hasn't been verified for completeness before building starts.
- You need to decide whether the ticket is self-contained (single stack) or requires coordination across services, languages, or teams (multi-stack).

## When not to use

- **You have a design doc or spec, not a Linear issue.** Use `planning-and-task-breakdown`; that skill decomposes a whole design at planning time. task-shape operates on a single ticket at implementation time. See `docs/design-decisions.md` §17.
- **The ticket is a bug or KTLO item with a clear reproduction step and no AC.** Implement directly; the AC check applies to story and feature issues.
- **No initiative or delivery plan has been shaped yet.** Run `initiative-shape` → `delivery-shape` first; task-shape consumes an already-shaped issue, it does not create one.

## Inputs

A Linear issue — provided as an issue ID, URL, or pasted body text. The issue must have a title, a description, and at least one acceptance criterion or "done when" statement. An issue with no AC at all is returned with a blocking comment; task-shape does not invent AC from the title.

## Outputs

A structured shaping block appended to the issue body (and echoed in the session):

1. **Enriched AC checklist** — each criterion annotated as complete, gap, or ambiguous; gaps listed with the resolution needed; ambiguities listed with the assumed interpretation.
2. **Sizing decision** — single-stack or multi-stack (N stacks), with one-sentence rationale and named stacks.
3. **Per-stack task list** — one ordered list per stack, walking skeleton as task 1, cross-stack dependencies called out on the tasks they affect.

If AC gaps are irresolvable without a decision the implementer cannot make, the output stops at the AC checklist with a blocking comment naming the gap and its owner. The worker session does not proceed to implementation.

## Workflow

**1. Read the issue in full.**
Fetch the complete issue via Linear MCP (or accept pasted text). Read the title, description, all AC items, any linked design doc or delivery-plan node, and any prior comments that resolve ambiguities. Do not begin the AC check until the full context is in view — a partial read produces a checklist that misses the gaps it was meant to surface.

**2. Restate the problem.**
Write one sentence: "This issue wants [outcome] for [who]." Anchoring to the stated problem — not to what would be easiest to implement — is the seatbelt against drifting into a solution that satisfies the words but misses the intent (agentic P3). If the description doesn't answer who benefits and what outcome is wanted, that is the first gap.

**3. [GATE] AC completeness check.**
Annotate every acceptance criterion:

- **✓ complete** — specific and verifiable; an implementer unfamiliar with the background could write a test for it.
- **⚠ gap** — a path the implementation must handle that the AC doesn't address, or a term or boundary left undefined.
- **? ambiguous** — interpretable in more than one way where the interpretation changes what gets built.

A criterion is not complete unless it names an observable outcome. "Works correctly" is not a criterion. "Returns 200 with the user object when the email exists" is. List every gap and ambiguity; for each gap, state what's missing and who must resolve it; for each ambiguity, state the interpretations and declare your assumed one.

**4. [GATE] Irresolvable gaps.**
If any gap requires a product decision, legal sign-off, or another team's input that the implementer cannot source from available context — stop. Append the AC checklist to the issue as a comment, name each irresolvable gap with its owner and the question that needs an answer, and halt. No task list is produced until the gaps are resolved and the skill is re-run.

**5. Sizing decision.**
Read the AC (including resolved ambiguities), the linked design doc if any, and the repositories or services the issue touches. Decide:

- **Single-stack:** all implementation, tests, and deployment touch one codebase, one language, one team's ownership. One task list suffices.
- **Multi-stack (N stacks):** the work requires changes across N repositories, languages, or team-owned services. Each stack gets its own task list; cross-stack dependencies are named on the dependent tasks.

Name each stack precisely — repository or service name plus language: "`api-service` (Go)," "`web-app` (TypeScript)." "Backend and frontend" is not a stack name. Unnamed stacks produce task lists that can't be routed.

**6. [GATE] Produce the task lists.**
One ordered list per stack. Within each list:

- **Task 1 is the walking skeleton:** the thinnest slice that runs end-to-end through the stack's path, exercising real code against a real claim. Foundational tooling or fixture setup is folded into the skeleton task description, never emitted as a preceding setup task (eng-universal Rule B2).
- **Subsequent tasks** add one observable behaviour each — one error path, one field, one rule, one integration point. Each task is one sentence; if it takes two sentences, split it.
- **Cross-stack dependencies** are named on the task that blocks or is blocked: "depends on: `api-service` Task 2." Do not describe dependencies only in prose.
- **External or cross-team dependencies** are flagged as blockers with the owner named (eng-universal Rule B7).

**7. Write the shaping block.**
Use the template below. Append it to the issue body, post it as a comment, and echo it in the session so the implementer can read it immediately.

## Shaping block template

```markdown
---
**Task shape** · run: <date> · issue: <ID>

## AC checklist

| # | Criterion | Status | Notes |
|---|-----------|--------|-------|
| 1 | <criterion text> | ✓ complete | |
| 2 | <criterion text> | ⚠ gap | <what's missing; who must resolve it> |
| 3 | <criterion text> | ? ambiguous | <interpretations; assumed: <X>> |

### Gaps (require resolution before build)
- **Gap 1:** <what's missing> → Owner: <name or role> · Question: <the decision needed>

### Ambiguities (resolved for this build)
- **Ambiguity 1:** <interpretations> → Assumed: <X>. Revisit if assumption is wrong.

## Sizing decision

**Decision:** Single-stack | Multi-stack (<N> stacks)
**Stacks:** <repo/service (language)> [, <repo/service (language)>]
**Rationale:** <one sentence>

## Task list — <stack name>

- [ ] `skeleton` — <walking skeleton; setup folded in>
- [ ] <one observable outcome>
- [ ] <one observable outcome — depends on: <other stack> Task M>

<!-- Repeat the task list block for each additional stack -->
---
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "The AC looks fine — let me just start." | "Looks fine" is not the same as "is verifiable." The check surfaces the gap you'll hit on day 3, not day 1. |
| "I can resolve the ambiguity as I go." | Mid-build resolution produces an implementation that satisfies the implementer's interpretation, not the user's intent. Resolve before the first commit. |
| "This is obviously single-stack." | Name the stacks regardless. The multi-stack surprises are the ones labelled obvious. |
| "The gap is small — I'll make a safe assumption." | Small gaps produce confident builds on wrong foundations. Name the gap and assumption separately; if the assumption is wrong, the cost is visible. |
| "I'll write the task list after the build to document what I did." | By then it is a changelog, not a plan. Its value is before implementation, not after. |
| "Walking skeleton isn't needed for this ticket — it's a small change." | Small changes are the ones with the most hidden integration surface. If it's truly trivial, the skeleton takes five minutes to write. |
| "I'll put all stacks in one combined task list." | A combined list makes cross-stack dependencies invisible and prevents parallel work. Separate lists with explicit dependency callouts are what make routing and parallelism possible. |

## Red flags

- Implementation started before the shaping block was produced.
- A criterion marked ✓ complete cannot be turned into a test by an implementer unfamiliar with the background.
- The sizing decision says single-stack but the AC or description references more than one service or repository.
- A setup or scaffolding task appears before the walking skeleton in any stack's list.
- Cross-stack dependencies are described only in prose, not named on the dependent tasks.
- An irresolvable AC gap was assumed away rather than surfaced with an owner.
- The shaping block was produced for an issue with no AC (title-only description).
- The skill was run as a pre-planning step on a design doc rather than at pickup time on a ticket.

## Verification / exit criteria

The skill has run correctly when:

1. The full issue (description, prior comments, linked design doc if any) was read before the AC check began.
2. Every AC criterion is annotated (✓ / ⚠ / ?); every gap and ambiguity is listed explicitly with the notes specified in the template.
3. Irresolvable gaps are surfaced with an owner before sizing begins. If any exist, no task list is produced.
4. The sizing decision names specific stacks (repository or service name + language).
5. Each stack has an ordered task list, walking skeleton as task 1, no setup task preceding it.
6. Cross-stack and external dependencies are named on the tasks that depend on them.
7. The shaping block is appended to the issue body and posted as a comment.
8. The implementer can read the shaping block and start the walking skeleton without further clarification.

## References

- `docs/design-decisions.md` §17 — decision to run task-shape at implementation time, not at planning time; full input/output contract; rejected alternative
- `rules/eng-principles-agentic.md` — P3 (spec as seatbelt), P4 (evidence beats vibes), P8 (slices and gates)
- `rules/eng-principles-universal.md` — Rule B2 (walking skeleton first), Rule B7 (cross-team dependencies before commitment)
- `skills/planning-and-task-breakdown/SKILL.md` — the planning-time counterpart: takes a design doc, not a ticket; runs once at planning time, not at pickup
- `skills/delivery-shape/SKILL.md` — upstream: produces the shaped nodes (issues) that task-shape enriches at pickup time
