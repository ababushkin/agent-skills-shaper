---
name: build
description: >
  Gated RED/GREEN/commit loop for a single broken-down task. Use when picking up any
  build task from a delivery plan or issue — whether the repo has a test runner or only
  a deterministic verification script. Every increment lands verified, smallest-first, with
  a commit trail a reviewer can replay. Trigger phrases: "build this task", "implement this
  story", "work on this issue", "pick up this task", "start building", "implement the slice".
pack: engineering
lifecycle_stage: build
principles_implemented:
  - source: eng-agentic
    id: P3
    bucket: embedded
  - source: eng-agentic
    id: P4
    bucket: embedded
  - source: eng-agentic
    id: P6
    bucket: embedded
  - source: eng-agentic
    id: P8
    bucket: embedded
  - source: eng-universal
    id: Rule B2
    bucket: embedded
  - source: eng-universal
    id: Rule C8
    bucket: embedded
length_target: 200–270
author: Anton Babushkin
predecessor:
  repo: https://github.com/obra/superpowers
  skill: test-driven-development
  relation: derivative
kept_from_predecessor: "RED/GREEN/REFACTOR cycle structure; iron-law framing; common rationalisations table (superpowers); Prove-It pattern and verification checklist (agent-skills/test-driven-development, MIT)"
changed_from_predecessor: "[GATE] markers on every loop step; verification-form fallback for repos with no test runner; per-slice commit convention; named escalation path to debugging skill; anatomy-compliant section order"
---

# Build

## Purpose

build is the gated implementation loop for a single task. It enforces the RED/GREEN/commit
discipline — a failing check before any implementation, the minimal change that clears the
check, then a commit — and repeats per slice. The gates are non-optional: a cycle without a
failing check first is not a cycle, it is implementation with no proof. A cycle that flails
through three consecutive reds without naming the blocker is not stuck, it is the signal to
escalate to `debugging`.

The dominant failure it guards against: skipping the failing check ("I know what to write")
produces code that compiles but does not satisfy the AC — agentic P4: "seems right" is not done.

## When to use

- Picking up any build task from a delivery plan, issue, or node task list.
- Implementing a story, a feature slice, a bug fix, or any change with an observable
  acceptance criterion.
- Repos with a test runner and repos without one — the verification-form fallback (step 1)
  covers the latter.

## When not to use

- **No task, no criterion** — if there is no acceptance criterion to turn RED, there is no loop
  to run. Stop: run `delivery-shape` or write the AC first.
- **Greenfield scaffolding with no verifiable behaviour yet** — generating a project skeleton
  with no testable surface is setup, not a build task. Fold it into the skeleton task
  description and pick up the loop at the first verifiable slice.
- **Debugging a failing system you did not build** — open `debugging` directly; the RED/GREEN
  loop does not apply when the objective is diagnosis, not increment.
- **Design decisions** — open `design-doc` or `adr`. Building before the design gate passes
  is a one-way door without a key.

## Inputs

- The task to build: the `- [ ]` line from the delivery plan, or the issue body. Must carry a
  `Done when:` acceptance criterion — that criterion is what becomes RED.
- The verification command: how to run the check (test runner, lint gate, grader script, link
  checker). Discoverable from repo instructions (`README`, `AGENTS.md`, `CLAUDE.md`, `Makefile`,
  `package.json`). If not discoverable, fallback applies (step 1).

## Outputs

- Working-tree changes that satisfy the task's `Done when:` criterion.
- One commit per slice, each passing the verification command.
- `.drain-handoff.json` in the worktree root — accumulated slice manifest (sha, title, why per slice), consumed by `pr-finishing`.
- If three consecutive implementation attempts fail without narrowing the error: an escalation note
  naming the blocker, ready to hand off to `debugging`.
- After all slices are green and committed: ready for optional `simplify` pass to reduce accidental
  complexity before review.

## Workflow

**1. [GATE] Select the verification form — before writing any code.**

Read the repo's instructions (`README`, `AGENTS.md`, `CLAUDE.md`, `Makefile`, `package.json
scripts`) to find the runnable verification command. Record it explicitly — this command is
what "RED" and "GREEN" mean for this task.

If no test runner is present, select a deterministic fallback from this priority list:
- A grader script named in the delivery plan (`Done when: bin/grader exits 0`).
- A lint or format check (`make lint`, `npm run lint`).
- A link or reference checker (`bin/check-plan-framing`, `bin/walk-delivery-plan`).
- A shell assertion (`grep -q 'expected string' file && echo PASS || echo FAIL`).

The fallback must be deterministic (same input → same exit code) and must be selectable
*before* the first slice, not improvised mid-build. A fallback that cannot be expressed as
a command with a non-zero/zero exit convention is not a fallback — it is a vibe. Stop and
clarify before building.

Record the chosen form inline: `Verification: <command>`.

**2. [GATE] RED — write the failing check first.**

Turn the task's `Done when:` criterion into a failing check: a test, a grader invocation,
or a shell assertion that exercises the criterion and fails because the implementation does
not yet exist. Run the verification command. Confirm:
- The command exits non-zero (RED). A check that passes immediately proves nothing about
  the implementation — it tests existing behaviour, not missing behaviour.
- The failure message names the missing behaviour, not a syntax error or import problem.
  A failure caused by a typo is not RED; it is a broken harness. Fix the harness, then
  confirm RED again before writing any implementation.

**Write code before the check? Delete it. Start over at step 2.**

**3. [GATE] GREEN — write the minimal implementation.**

Write the smallest change that makes the verification command exit zero. "Smallest" means:
- No features, refactors, or improvements beyond what the failing check requires.
- No speculative generalisations — one use case in the check, one use case in the code.
- No cleanup of surrounding code unless it is necessary to make the check pass.

Run the verification command. Confirm all checks pass. If not, fix the implementation (not
the check). If the check itself is wrong — it is testing a different behaviour than the AC
names — stop: revise the check to match the AC, re-confirm RED (step 2), then return here.

**4. REFACTOR — clean up without changing behaviour.** *(no gate — optional step)*

With all checks green, improve readability: remove duplication, rename, extract helpers.
Run the verification command after every refactor step. If any check goes red, revert the
last change. Add no new behaviour here.

**5. [GATE] Commit — one commit per slice.**

Commit the slice before starting the next. The commit message names the slice outcome, not
the implementation detail: `feat: add <observable outcome>`, not `feat: implement helper`.
Each commit must leave the verification command green — a commit that breaks the check is
not a slice, it is a fragment.

Commit format: conventional-commit prefix + one-line subject ≤ 70 chars. No co-author
trailers.

After committing, append this slice's record to `.drain-handoff.json` in the worktree root
(create the file if absent). The file accumulates one entry per slice:

```json
{
  "issue": "<issue-id from branch name or delivery plan>",
  "slices": [
    { "sha": "<40-char SHA of this commit>", "title": "<commit subject>", "why": "<commit body, or empty if no body>" }
  ]
}
```

This file is the input contract for `pr-finishing`. Without it, pr-finishing falls back to
`git log` and loses commit-body context for the Why field in each PR body.

**6. Repeat for remaining slices.**

Return to step 2 for the next slice. Each slice extends the task in exactly one direction
and is independently verifiable. A slice that requires the next slice to pass its own check
is a fragment — merge the two, then split at a verifiable boundary.

When all slices are complete and all tests pass, open `simplify` for an optional post-green
clarity pass before review.

**7. [GATE] Consecutive-failure escalation — three reds, name the blocker.**

If the verification command fails across three consecutive implementation attempts (RED results)
without progress — same error output, no narrowing toward green — stop the loop. Do not retry. Record:
- The check command and its output verbatim.
- The three implementation attempts and why each failed.
- The hypothesis about what is blocking (dependency, missing context, wrong assumption).

Hand off to `debugging` with this record as context. Flailing through a fourth attempt
without the blocker named is not persistence — it is noise that contaminates the commit trail.

## Artefact template

The skill produces one file artefact (`.drain-handoff.json`, grown one entry per commit) and an inline run log:

```
Verification: <command>          # step 1 — recorded before any code

# Per slice:
[RED]   <check name/description> — exits non-zero, failure names missing behaviour
[GREEN] <check name/description> — exits zero, all checks pass
[REFACTOR] optional cleanup — checks remain green
[COMMIT] <conventional-commit subject> — exits zero post-commit

# If escalating:
[BLOCKED] <blocker hypothesis> → hand off to debugging skill

# After all slices are green:
[DONE] All slices complete, tests pass → optional: open simplify skill for post-green clarity pass
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "I know what to write — I'll write the check after." | The check written after tests what you built, not what was required. It will pass immediately and prove nothing. Write it first; watch it fail. |
| "The repo has no test runner — I'll just write the code and verify manually." | Manual verification is not a gate. Select a deterministic fallback (step 1); if none exists, write a shell assertion. A check you can't re-run is not a check. |
| "The check is passing immediately — must be a flaky test, I'll move on." | A check that passes immediately is testing existing behaviour. It is not RED. Fix the check to test the missing behaviour, or delete it and write a new one. Do not move on. |
| "Three reds in a row — I'll try a slightly different approach." | Three reds without narrowing the cause is the escalation signal, not the retry signal. Record the blocker, hand off to debugging. Another attempt without new information is noise. |
| "The check is hard to write — let me implement first and come back." | Hard to test means hard to specify. The difficulty is a signal that the AC is ambiguous or the design is tangled. Resolve the ambiguity before implementing. |
| "I'll commit everything at the end once it all works." | One end-of-task commit produces a diff no reviewer can replay. One commit per slice means the trail is the story. Each commit is a verifiable increment, not a checkpoint. |
| "This slice leaves the check red but the next slice will fix it." | A slice that requires the next slice to pass its own check is a fragment. Merge the two and re-split at a boundary that is independently verifiable. |
| "The refactor step improved things — let me add one more feature while I'm here." | Refactor means clean up, not extend. Adding behaviour in the refactor step means the next slice starts with an untested implementation already in the tree. |

## Red flags

- Implementation written before a failing check exists.
- A check passes on the first run after being written (immediate green = not testing missing behaviour).
- A failing check is deleted, skipped, or `// @ts-ignore`'d to make the build proceed.
- Three or more consecutive RED results (failed implementation attempts) without progress (same error, no narrowing), with no escalation to `debugging`.
- A commit contains multiple slices, or a commit leaves the verification command failing.
- The verification form was improvised mid-slice rather than selected at step 1.
- The refactor step added new behaviour or the commit message describes implementation, not outcome.
- A "verification" step that cannot be expressed as a command with a binary exit code.

## Verification / exit criteria

The skill has run correctly when:

1. The verification form was selected and recorded before any code was written.
2. Each slice produced a failing check first, a minimal implementation that cleared it, and
   a commit — in that order, with no skipped steps.
3. Each commit passes the verification command and its message names an observable outcome.
4. If three consecutive implementation attempts (RED results) failed without narrowing the error, a blocker record
   exists and `debugging` was invoked with it as context — no further attempts without that hand-off.
5. The final state of the working tree satisfies the task's `Done when:` criterion, confirmed
   by running the verification command and observing exit 0.

## References

- `skills/debugging/SKILL.md` — escalation target when three consecutive RED loops fail
  to narrow to green; receives the blocker record as input
- `skills/simplify/SKILL.md` — exit point for post-green clarity pass after all slices are
  complete and tests pass
- `rules/eng-principles-agentic.md` — P3 (spec as seatbelt), P4 (evidence beats vibes),
  P6 (stop the line), P8 (slices and gates, not calendar time)
- `rules/eng-principles-universal.md` — Rule B2 (walking skeleton first), Rule C8 (tests
  are a specification of behaviour)
- Predecessor: `superpowers/test-driven-development` (MIT) — RED/GREEN/REFACTOR cycle
  and iron-law framing
- Predecessor: `agent-skills/test-driven-development` (MIT) — Prove-It pattern and
  verification checklist
