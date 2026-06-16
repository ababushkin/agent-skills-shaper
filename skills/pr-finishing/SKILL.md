---
name: pr-finishing
description: Finish an already-green, sliced development branch by submitting one small PR per commit slice. Use when work is complete, committed in reviewable slices, and ready for PR submission through Graphite or plain git.
---

## Purpose

`pr-finishing` turns an already-green feature branch into a stack of small PRs, one per commit slice. Prefer Graphite when available and configured; otherwise use plain git. Preserve the same PR body format on both paths.

## Use when

- Work is complete and tests pass.
- Changes are committed as independently reviewable slices, one logical change per commit.
- The operator asks to finish, submit, create stacked PRs, or submit the stack.
- Optional: a drain-cycle handoff file exists at `.drain-handoff.json`.
- Optional: a Linear issue ID is available for the final trail comment.

Do not use this skill to hide failing tests, submit a known-broken branch, or re-slice a squashed multi-change commit after the fact.

## Inputs

- Feature branch with one logical change per commit.
- Optional base branch, `<base>` (default `main`). When the work is stacked on another branch rather than `main` — e.g. a drain-cycle worktree chained off a prior issue's branch — the caller passes that branch as the base. Resolution order: an explicit base in the invocation, else a `base` key in `.drain-handoff.json`, else `main`.
- Optional `.drain-handoff.json` containing an `issue` and `slices`.
- Optional Linear issue ID from the branch name, handoff file, user request, or available Linear plugin.
- Optional Graphite CLI, `gt`.
- GitHub CLI, `gh`, for PR creation and verification.

Example `.drain-handoff.json`:

```json
{
  "issue": "ABC-123",
  "slices": [
    {
      "sha": "<40-char SHA>",
      "title": "<PR title>",
      "why": "<optional motivation>"
    }
  ]
}
```

## Outputs

- One PR per slice.
- Each PR body uses the same What / Why / Focus template.
- If `.drain-handoff.json` exists, `pr_urls` and `prep_verdict` are merged into it per schema v2.
- If Linear is available and an issue ID is known, post a review-summary comment.
- If Linear is unavailable, include the review summary in the final response instead.

### 1. Restate the issue

Start with one sentence:

> This branch closes <issue> by delivering <summary>.

If no issue ID is known, derive the summary from the branch name and commit subjects.

### 2. Verify green state

Run the repo's required tests before creating any PRs.

If tests fail, stop. Report the failing command and relevant output. Do not submit PRs.

### 3. Determine slices

If .drain-handoff.json exists, read its slices array.

If it does not exist, derive slices from git, ranging from the resolved base (default `main`):

`git log <base>..HEAD --reverse --format=%H%x00%B%x00%x00`

Use each commit as one slice. The first line of the commit message is the title; the remaining body is the Why.

If multiple unrelated changes are squashed into one commit, warn that the branch was not sliced during build. Continue only if it appears to be a single logical change, or the operator explicitly accepts the risk.

### 4. Choose submission path

Check Graphite preconditions in order:

`which gt gt auth status gt repo init --check`

Use these rules:

- If all checks pass, use the Graphite path.
- If gt is absent, use the plain-git path.
- If gt exists but auth or repo initialization fails, stop and show the exact error. Do not silently fall back to git.

### 5. Graphite path

For each slice, oldest first:

- Create or track a Graphite branch at that exact commit.
- Ensure the branch points to the slice commit, not the stack tip.
- Parent the oldest slice's branch on `<base>` (e.g. `gt track --parent <base>`) so the bottom PR targets `<base>`, not `main`. Each later slice parents on the slice before it.
- Draft the PR body using the template below.

Submit the stack:

`gt stack submit --no-interactive`

After submission, set or correct each PR body with gh pr edit.

Wrap each gt call in a bounded recovery loop:

- On success: continue.
- On stale parent or out-of-sync error: run gt repo sync, retry once.
- On dirty working tree: stash, retry once, then restore the stash.
- On auth or repo initialization error: stop immediately.
- On any second failure: stop and report the exact error.

### 6. Plain-git path

Use this only when gt is absent.

For each slice, oldest first:

- Create a branch from the slice parent named <issue-or-branch>/<slug>-<n>.
- Cherry-pick the slice commit.
- Create the PR using the shared body template.
- Push the branch and create the PR with gh pr create. Target the oldest slice's PR at `<base>` (`gh pr create --base <base>`); each later slice targets the prior slice's branch.

The plain-git path must produce the same PR body and final trail as the Graphite path.

### 7. Verify PRs

Before posting any final trail, verify every PR URL is reachable:

`gh pr view <url>`

If any PR is missing or unreachable, stop and report the problem. Do not post the Linear comment yet.

If `.drain-handoff.json` exists, merge `pr_urls` and `prep_verdict` into it:

```json
{
  "pr_urls": ["<https://...>"],
  "prep_verdict": {
    "route": "auto-merge | human-review",
    "reasoning": "<one sentence: why this route>"
  }
}
```

Set `route` to `"auto-merge"` when PRs were submitted with no blocking review findings pending human resolution. Set `route` to `"human-review"` when outstanding findings require explicit sign-off before merging — this route implies `halt_reason: "human-review-requested"` on exit.

### 8. Post final trail

If Linear is available and an issue ID is known, post one review-summary comment to the issue.

If Linear is unavailable or no issue ID is known, include the same summary in the final response.

If repo policy does not permit PRs, follow the repo policy and note the deviation in the summary.

## PR body template

Use this exact structure for every PR:

`## What <One to three sentences describing what this slice changes. Keep this diff-level, not ticket-level.> ## Why <Why this slice exists, what issue it supports, and why it can be reviewed independently. For later PRs, reference the prior PR when useful.> ## Focus <Specific files, decisions, or patterns to review. If there are no critical areas, write: "No critical review areas - safe for auto-merge.">`

## Review-summary template

`PR stack submitted: <n> PR(s) <slice-1-title>: <url> <slice-2-title>: <url> Path: graphite | plain-git Pre-submission review findings: critical: N, required: N (fixed: N, deferred: N)`

## Exit criteria

The skill is complete only when:

1. Tests passed before PR creation.
2. Each slice has exactly one PR.
3. Each PR body contains What, Why, and Focus.
4. Every PR URL was verified reachable.
5. Existing `.drain-handoff.json`, if present, was updated with `pr_urls` and `prep_verdict` per schema v2 (`references/drain-handoff-schema-v2.md`).
6. Graphite precondition failures halted instead of falling back silently.
7. The final review summary was posted to Linear when available, or reported to the operator when Linear is unavailable.
