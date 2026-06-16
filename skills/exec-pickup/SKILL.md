---
name: exec:pickup
description: >
  Front door for draining a Linear issue end-to-end — pickup through breakdown,
  build, review, verify, and PR finishing. Every step is a named delegation to its
  owning skill; this is the supervisor pointer, not the procedure. Use when a
  drain-cycle worker or supervisor prompt picks up a Linear issue and needs a single
  entry point for the full execution workflow. Trigger phrases: "pick up this issue",
  "start working on this ticket", "drain this issue", "exec:pickup", "work on ABA-NNN".
---

# Exec: pickup

## Purpose

Take a freshly-picked Linear issue all the way to a finished PR with a full review trail. This skill reads the issue, writes a handoff envelope, and then delegates each step — breakdown, build, review, verify, finish — to its owning `exec:*` skill by name. It inlines no procedure; the named delegation is the whole of each step. The issue's acceptance criteria travel inside `pickup-envelope.json` from pickup to the spec-compliance persona in `exec:review`, re-typed by no one and lost by no one.

## When to use

- A Linear issue is assigned and a worktree is open.
- A drain-cycle supervisor prompt points here as its single execution pointer.
- A worker picking up an issue fresh wants the complete execution path without improvising.

## Do not use when

- **Only reviewing a diff** — use `exec:review` directly.
- **Only finishing an already-built PR** — use `exec:finish` directly.
- **Shaping or planning** — use `shape:delivery`, `shape:initiative`, or `shape:plan-review`.
- **Exploratory spikes or design work** — use `shape:design`; this skill assumes the work is broken down and ready to build.

## Inputs

- **Issue ID** — a Linear issue identifier (e.g. `ABA-363`)
- **Worktree path** — where the issue branch is checked out
- **Branch name** — the git branch for this issue
- **Parent branch** — `main`, or the parent branch in the stack if this work stacks on another issue

## Outputs

- **`pickup-envelope.json`** at the worktree root — the handoff carrier for every downstream step
- **`.drain-handoff.json`** updated at the worktree root — `flow` written on entry; `halt_reason: "blocked"` written before any blocked halt
- An ordered task list from `exec:breakdown`, each task carrying a `done_when` clause
- Delegations to `exec:build`, `exec:review`, `exec:verify`, and `exec:finish`
- On blocked: a Linear comment naming the blocker; issue left In Progress

## Workflow

### 1. Gate: read the issue

Load the issue from Linear (`mcp__claude_ai_Linear__get_issue`) and extract `issue_id`, `body_md`, `ac_checklist[]` (every Done-when / acceptance line, verbatim), `labels[]`, and `blocked_by[]`. If the issue cannot be read, halt with a comment naming the failure.

### 2. Gate: check for blockers

If `blocked_by[]` is non-empty, compute `flow` from `labels[]` using the same rule as step 4 (`"verify-only"` if `"verify"` is in labels, `"shape-task"` if a breakdown block exists in `body_md`, otherwise `"build"`). Merge `{"halt_reason": "blocked", "flow": "<computed>"}` into `.drain-handoff.json` at the worktree root (preserving any fields already present), then invoke `shape:stop-the-line`: post a comment naming each blocker, leave the status In Progress, and halt. Do not proceed to breakdown.

### 3. Rebase onto the parent branch

Determine the parent branch — `main` by default, or the parent branch in the stack if this work stacks on another issue — and rebase the worktree branch onto it before any build begins. Building on a stale base produces conflicts at finish; rebase at pickup, on fresh context, instead. Record the chosen parent in `parent_branch`.

### 4. Write the envelope and record flow

Write `pickup-envelope.json` (see Artefact template) to the worktree root. This file is the contract — every downstream skill reads it; none re-reads the Linear issue.

Determine the `flow` value from `labels[]`:

- If `labels[]` contains `"verify"` → `"verify-only"`.
- Otherwise if `body_md` contains an existing task-breakdown block → `"shape-task"`.
- Otherwise → `"build"`.

Merge `{"flow": "<value>"}` into `.drain-handoff.json` at the worktree root, preserving any fields the supervisor already wrote. This records the routing decision on entry so the supervisor can grade it without re-parsing the issue.

### 5. Gate: invoke `exec:breakdown`

Delegate to `exec:breakdown`, passing the envelope. It returns an ordered task list, each task carrying `id`, `done_when` (one verifiable clause), `model_tier`, and `axes` (RC·SC·HS·SR·OR). If it returns no tasks or any task lacks `done_when`, halt and comment naming the gap.

### 6. Build each slice with `exec:build`

For each task in order, delegate to `exec:build` with the task and the envelope path. `exec:build` owns the RED → GREEN → commit loop, including `exec:debug` on a stuck red loop and `exec:simplify` on green. Do not advance until the task's `done_when` is satisfied and a commit exists.

### 7. Gate: invoke `exec:review`

After all slices are committed, delegate to `exec:review` with the working-tree diff and the envelope path (so the spec-compliance persona reads `ac_checklist` directly). On `NO-GO`, loop back into `exec:build` on the failing findings. Do not proceed until the verdict is `GO`.

### 8. Gate: invoke `exec:verify`

Delegate to `exec:verify` with the envelope's `ac_checklist` and the diff. A fail loops back into `exec:build`; a pass is the green light for finishing.

### 9. Invoke `exec:finish`

Delegate to `exec:finish` with the envelope, the review verdict, and the verify result. `exec:finish` owns the PR body, review-summary comment, and Linear status transition.

## Artefact template

`pickup-envelope.json` (in-flight carrier between skills):

```json
{
  "issue_id": "<id>",
  "branch": "<branch>",
  "parent_branch": "<main | parent branch in the stack>",
  "worktree_path": "<path>",
  "ac_checklist": ["<verbatim AC item>", "…"],
  "body_md": "<full issue body>",
  "labels": ["<label>", "…"],
  "blocked_by": []
}
```

`.drain-handoff.json` after step 4 (exit record for the supervisor):

```json
{
  "flow": "build | verify-only | shape-task"
}
```

`.drain-handoff.json` after a blocked halt (step 2 fires):

```json
{
  "flow": "build | verify-only | shape-task",
  "halt_reason": "blocked"
}
```

## Red flags

- The workflow contains a procedure that is not a named delegation.
- `pickup-envelope.json` is missing from the worktree root before `exec:build` starts.
- `.drain-handoff.json` does not contain `flow` after step 4 completes.
- A breakdown task has no `done_when` clause.
- The issue transitions to Done before `exec:finish` is invoked.
- `exec:review` returns `NO-GO` and the next step is `exec:verify` without looping back to `exec:build`.
- `ac_checklist` is empty on an issue that has acceptance criteria.
- A blocked halt occurs without `halt_reason: "blocked"` written to `.drain-handoff.json`.

## Exit criteria

- `pickup-envelope.json` exists at the worktree root with all fields populated.
- `.drain-handoff.json` contains `flow` at the worktree root after step 4.
- On a blocked exit: `.drain-handoff.json` contains `halt_reason: "blocked"` and the issue remains In Progress.
- Every breakdown task has a `done_when` clause.
- `exec:review` returned `GO` before `exec:verify` was invoked.
- `exec:finish` was invoked and posted the review-summary comment and transitioned the issue.
- A dry run on one real issue reaches the PR step without a human re-prompt between steps.

## Related

- `skills/execution-review/SKILL.md` — `exec:review` (persona fan-out, ADR 0003 dispatch)
- `skills/verify-implementation/SKILL.md` — `exec:verify`
- `skills/pr-prepare/SKILL.md` — `exec:finish`
