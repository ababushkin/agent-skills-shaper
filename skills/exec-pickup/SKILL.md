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

Take a freshly-picked Linear issue all the way to a finished PR with a full review trail. This skill reads the issue, writes the `pickup` section of `exec-state.json`, and then delegates each step — breakdown, build, review, verify, finish — to its owning `exec:*` skill by name. It inlines no procedure; the named delegation is the whole of each step. The issue's acceptance criteria travel inside `exec-state.json` (pickup section) from pickup to the spec-compliance persona in `exec:review`, re-typed by no one and lost by no one.

## When to use

- A Linear issue is assigned and a worktree is open.
- A drain-cycle supervisor prompt points here as its single execution pointer.
- A worker picking up an issue fresh wants the complete execution path without improvising.

## Do not use when

- **Only reviewing a diff** — use `exec:review` directly.
- **Only finishing an already-built PR** — use `exec:finish` directly.
- **Shaping or planning** — use `shape:delivery`, `shape:initiative`, or `shape:plan-review`.
- **Exploratory spikes or design work** — use `shape:design`; this skill assumes the work is broken down and ready to build.
- **Non-build node** (`experiment`, `design-doc`, `spike`, `adr`, `incident`, `slo`, `compliance`) — these produce a finding, design doc, decision, or obligation artefact, not a PR; run via the delegate skill named in the issue body.

## Inputs

- **Issue ID** — a Linear issue identifier (e.g. `ABA-363`)
- **Worktree path** — where the issue branch is checked out
- **Branch name** — the git branch for this issue
- **Parent branch** — `main`, or the parent branch in the stack if this work stacks on another issue

## Outputs

- **`exec-state.json`** at the worktree root — the handoff carrier; the `pickup` section is written by this skill and read by every downstream step
- An ordered task list from `exec:breakdown`, each task carrying a `done_when` clause
- Delegations to `exec:build`, `exec:review`, `exec:verify`, and `exec:finish`
- On non-build node: a Linear comment naming the node type and delegate skill; issue left In Progress
- On blocked: a Linear comment naming the blocker; issue left In Progress

## Workflow

### 1. Gate: read the issue

Load the issue from Linear (`mcp__claude_ai_Linear__get_issue`) and extract `issue_id`, `body_md`, `ac_checklist[]` (every Done-when / acceptance line, verbatim), `labels[]`, and `blocked_by[]`. Then scan `body_md` for delivery task lines — any `- [ ]` or `- [x]` line that also contains `Done when:` and `Model:`. Capture those lines verbatim into `plan_tasks[]` and set `has_plan_tasks: true`; if none exist, set `plan_tasks: []` and `has_plan_tasks: false`. If the issue cannot be read, halt with a comment naming the failure.

### 2. Gate: check for non-build node type

If `labels[]` contains any of `node:experiment`, `node:design-doc`, `node:spike`, `node:adr`, `node:incident`, `node:slo`, or `node:compliance`, invoke `shape:stop-the-line`: post a comment naming the node type and the delegate skill (from the `🛑 Non-build node` banner in the body, or the type's known `delegates_to`; see the node-type vocabulary in `docs/delivery-shape-contract.md`), leave the status In Progress, and halt.

### 3. Gate: check for blockers

If `blocked_by[]` is non-empty, invoke `shape:stop-the-line`: post a comment naming each blocker, leave the status In Progress, and halt. Do not proceed to breakdown.

### 4. Rebase onto the parent branch

Determine the parent branch — `main` by default, or the parent branch in the stack if this work stacks on another issue — and rebase the worktree branch onto it before any build begins. Building on a stale base produces conflicts at finish; rebase at pickup, on fresh context, instead. Record the chosen parent in `parent_branch`.

### 5. Write the pickup section

Write the `pickup` section of `exec-state.json` to the worktree root (see Artefact template). If `exec-state.json` already exists, open it, set the `pickup` key, and write back — preserving any prior sections. This file is the contract — every downstream skill reads it; none re-reads the Linear issue.

### 6. Gate: invoke `exec:breakdown`

Delegate to `exec:breakdown`, passing the `exec-state.json` path. It writes the `breakdown` section back to that file containing an ordered `tasks[]` array — each task carrying `id`, `done_when` (one verifiable clause), `model_tier`, `axes` (RC·SC·HS·SR·OR), and `ac_refs` linking it back to the pickup AC items. If it writes no tasks or any task lacks `done_when`, halt and comment naming the gap.

### 7. Build each slice with `exec:build`

For each task in order, delegate to `exec:build` with the task and the `exec-state.json` path. `exec:build` owns the RED → GREEN → commit loop, including `exec:debug` on a stuck red loop and `exec:simplify` on green. Do not advance until the task's `done_when` is satisfied and a commit exists.

### 8. Gate: invoke `exec:review`

After all slices are committed, delegate to `exec:review` with the working-tree diff and the `exec-state.json` path (so the spec-compliance persona reads `ac_checklist` from the pickup section directly). On `NO-GO`, loop back into `exec:build` on the failing findings. Do not proceed until the verdict is `GO`.

### 9. Gate: invoke `exec:verify`

Delegate to `exec:verify` with the `ac_checklist` from `exec-state.json`'s pickup section and the diff. A fail loops back into `exec:build`; a pass is the green light for finishing.

### 10. Invoke `exec:finish`

Delegate to `exec:finish` with the `exec-state.json` path, the review verdict, and the verify result. `exec:finish` owns the PR body, review-summary comment, and Linear status transition.

## Artefact template

```json
{
  "pickup": {
    "issue_id": "<id>",
    "branch": "<branch>",
    "parent_branch": "<main | parent branch in the stack>",
    "worktree_path": "<path>",
    "ac_checklist": ["<verbatim AC item>", "…"],
    "body_md": "<full issue body>",
    "plan_tasks": ["<verbatim task line>", "…"],
    "has_plan_tasks": true,
    "labels": ["<label>", "…"],
    "blocked_by": []
  }
}
```

## Red flags

- The workflow contains a procedure that is not a named delegation.
- A non-build node label (`node:experiment | node:design-doc | node:spike | node:adr | node:incident | node:slo | node:compliance`) is present and exec:pickup does not halt at the node-type gate.
- `exec-state.json` is missing from the worktree root before `exec:build` starts.
- A breakdown task has no `done_when` clause.
- The issue transitions to Done before `exec:finish` is invoked.
- `exec:review` returns `NO-GO` and the next step is `exec:verify` without looping back to `exec:build`.
- `ac_checklist` is empty on an issue that has acceptance criteria.

## Exit criteria

- `exec-state.json` exists at the worktree root with a `pickup` section containing all fields populated.
- Every breakdown task has a `done_when` clause.
- `exec:review` returned `GO` before `exec:verify` was invoked.
- `exec:finish` was invoked and posted the review-summary comment and transitioned the issue.
- A dry run on one real issue reaches the PR step without a human re-prompt between steps.

## Related

- `skills/exec-breakdown/SKILL.md` — `exec:breakdown` (turns the pickup AC into the ordered task list consumed by `exec:build`)
- `skills/exec-build/SKILL.md` — `exec:build` (RED/GREEN/commit loop per slice)
- `skills/exec-debug/SKILL.md` — `exec:debug` (root-cause escalation from `exec:build`)
- `skills/exec-simplify/SKILL.md` — `exec:simplify` (post-green clarity pass)
- `skills/exec-review/SKILL.md` — `exec:review` (persona fan-out, ADR 0003 dispatch)
- `skills/exec-verify/SKILL.md` — `exec:verify` (AC verdict before Done)
- `skills/exec-finish/SKILL.md` — `exec:finish` (stack creation + `pr-prepare` per PR)
- `skills/pr-prepare/SKILL.md` — `pr-prepare` (sub-skill of `exec:finish`; also independently usable)
