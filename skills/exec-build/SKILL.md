---
name: exec:build
description: >
  Gated RED/GREEN/commit loop for a single broken-down task. Use when picking up any
  build task from a delivery plan or issue - whether the repo has a test runner or only
  a deterministic verification script. Every increment lands verified, smallest-first, with
  a commit trail a reviewer can replay. Trigger phrases: "build this task", "implement this
  story", "work on this issue", "pick up this task", "start building", "implement the slice".
---

# Build

## Purpose

The gated implementation loop for a single task: a failing check before any code, the minimal change that clears it, then a commit - repeated per slice. The one thing that must hold: no cycle starts without a failing check first. A cycle with no RED is implementation with no proof; three consecutive reds without a named blocker is the signal to escalate to `exec:debug`.

## When to use

- Picking up any build task from a delivery plan, issue, or node task list.
- Implementing a story, feature slice, bug fix, or any change with an observable acceptance criterion.
- Repos with a test runner and repos without one - the verification-form fallback (step 1) covers the latter.

## Do not use when

- No task, no criterion - there is nothing to turn RED. Run `delivery-shape` or write the AC first.
- Greenfield scaffolding with no verifiable behaviour yet - that's setup, not a build task; pick up the loop at the first verifiable slice.
- Diagnosing a failing system you did not build - open `exec:debug`; the RED/GREEN loop is for increment, not diagnosis.
- Making a design decision - open `design-doc`; building before the design gate is a one-way door without a key.

## Inputs

- The task to build: the `- [ ]` line from the delivery plan, or the issue body. Must carry a `Done when:` acceptance criterion - that criterion is what becomes RED.
- The verification command: how to run the check (test runner, lint gate, grader script, link checker). Discoverable from repo instructions (`README`, `AGENTS.md`, `CLAUDE.md`, `Makefile`, `package.json`). If not discoverable, the fallback applies (step 1).

## Outputs

- Working-tree changes that satisfy the task's `Done when:` criterion.
- One commit per slice, each passing the verification command.
- The `build` section of `exec-state.json` in the worktree root - accumulated slice manifest (sha, title, why per slice), consumed by `exec:finish`.
- On three consecutive failures without narrowing: an escalation note naming the blocker, ready to hand off to `exec:debug`.
- After all slices are green: ready for an optional `exec:simplify` pass.

## Workflow

### 1. Gate: select the verification form

Before writing any code, find the runnable verification command in the repo's instructions (`README`, `AGENTS.md`, `CLAUDE.md`, `Makefile`, `package.json` scripts) and record it inline as `Verification: <command>`. This command is what RED and GREEN mean for this task.

If no test runner exists, select a deterministic fallback, in priority order: a grader script named in the plan (`Done when: bin/grader exits 0`), a lint/format check, a link or reference checker, or a shell assertion (`grep -q 'expected' file && echo PASS || echo FAIL`). The fallback must be deterministic (same input → same exit code) and chosen *before* the first slice. A "verification" that can't be expressed as a command with a zero/non-zero exit convention is a vibe - stop and clarify.

### 2. Gate: RED - write the failing check first

Turn the `Done when:` criterion into a check that exercises it and fails because the implementation doesn't exist yet. Run the verification command and confirm:

- It exits non-zero. A check that passes immediately tests existing behaviour, not missing behaviour.
- The failure names the missing behaviour, not a syntax or import error. A failure from a typo is a broken harness, not RED - fix the harness, then re-confirm RED.

Wrote code before the check? Delete it and restart at this step.

### 3. Gate: GREEN - write the minimal implementation

Write the smallest change that makes the command exit zero: no features, refactors, or generalisations beyond what the check requires; no cleanup of surrounding code unless needed to pass. Run the command and confirm green. If it fails, fix the implementation, not the check. If the check itself tests the wrong behaviour, stop: revise it to match the AC, re-confirm RED (step 2), then return here.

### 4. Refactor - clean up without changing behaviour *(optional, no gate)*

With all checks green, improve readability: remove duplication, rename, extract helpers. Run the command after every step; revert any change that goes red. Add no new behaviour here.

### 5. Gate: commit - one commit per slice

Commit the slice before starting the next. The message names the slice outcome, not the implementation detail: `feat: add <observable outcome>`, not `feat: implement helper`. Conventional-commit prefix, subject ≤ 70 chars, no co-author trailers. Each commit must leave the command green - a commit that breaks the check is a fragment, not a slice.

After committing, append this slice's record to the `build` section of `exec-state.json` in the worktree root. Open the file (preserving the `pickup` and `breakdown` sections earlier phases wrote), append this slice to `build.slices`, and write it back - create the `build` section on the first commit:

```json
{
  "build": {
    "slices": [
      { "sha": "<40-char SHA of this commit>", "title": "<commit subject>", "why": "<commit body, or empty>" }
    ]
  }
}
```

This section is the input contract for `exec:finish`. Without it, `exec:finish` falls back to `git log` and loses the commit-body context for each PR's Why.

### 6. Repeat for remaining slices

Return to step 2. Each slice extends the task in exactly one direction and is independently verifiable. A slice that needs the next slice to pass its own check is a fragment - merge the two and re-split at a verifiable boundary. When all slices are green, open `exec:simplify` for an optional post-green clarity pass.

### 7. Gate: three reds, name the blocker

If the command fails across three consecutive implementation attempts without progress - same error, no narrowing - stop. Do not retry. Record the check command and its output verbatim, the three attempts and why each failed, and the hypothesis about what is blocking (dependency, missing context, wrong assumption). Hand off to `exec:debug` with this record as context. A fourth attempt without the blocker named is noise that contaminates the commit trail.

## Artefact template

One file artefact (the `build` section of `exec-state.json`, grown one entry per commit) plus an inline run log:

```
Verification: <command>          # step 1 - recorded before any code

# Per slice:
[RED]   <check> - exits non-zero, failure names missing behaviour
[GREEN] <check> - exits zero, all checks pass
[REFACTOR] optional cleanup - checks remain green
[COMMIT] <conventional-commit subject> - exits zero post-commit

# If escalating:
[BLOCKED] <blocker hypothesis> → hand off to exec:debug

# After all slices are green:
[DONE] All slices complete → optional: open exec:simplify for a post-green clarity pass
```

## Red flags

- Implementation written before a failing check exists.
- A check passes on its first run (immediate green = not testing missing behaviour).
- A failing check deleted, skipped, or explicitly ignored to make the build proceed.
- Three or more consecutive reds without progress and no escalation to `exec:debug`.
- A commit containing multiple slices, or one that leaves the command failing.
- The verification form improvised mid-slice rather than selected at step 1.
- The refactor step added behaviour, or a commit message describes implementation, not outcome.
- A "verification" that can't be expressed as a command with a binary exit code.

## Exit criteria

1. The verification form was selected and recorded before any code.
2. Each slice produced a failing check, a minimal implementation that cleared it, and a commit - in that order, no skipped steps.
3. Each commit passes the command and its message names an observable outcome.
4. After three failed attempts without narrowing, a blocker record exists and `exec:debug` was invoked with it - no further attempts without that hand-off.
5. The final working tree satisfies the `Done when:` criterion, confirmed by running the command and observing exit 0.

## Related

- `skills/exec-debug/SKILL.md` - escalation target when three consecutive reds fail to narrow to green; receives the blocker record.
- `skills/exec-simplify/SKILL.md` - exit point for the post-green clarity pass after all slices are green.
