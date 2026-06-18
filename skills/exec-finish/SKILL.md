---
name: exec:finish
description: >
  Finish an already-green, sliced development branch by submitting one small PR per
  commit slice and then delegating to `pr-prepare` to write each PR's durable
  reviewer body and routing verdict. Composition: stack creation (this skill) →
  `pr-prepare` per PR. Use when work is complete, committed in reviewable slices,
  and ready for PR submission through Graphite or plain git.
---

# Exec: finish

## Purpose

`exec:finish` is the composition that ships a green sliced branch. It does two things in sequence:

1. **Stack creation.** Turn the branch into one small PR per commit slice — Graphite when available and configured; plain git otherwise. Same PR-creation mechanics on both paths.
2. **Per-PR preparation.** Delegate each created PR to `pr-prepare`, which reads the actual diff and writes the durable What / Why / Focus body, then records the auto-merge vs human-review verdict in `prep_verdict`.

The stack-creation step writes a minimal placeholder body so the PR exists and is reachable; `pr-prepare` then overwrites it with the diff-driven body that survives after the ticket is closed. Keeping the two steps separate lets `pr-prepare` stay independently usable on a single existing PR.

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
- Each PR body, written by `pr-prepare`, follows the What / Why / Focus template with diff-level detail.
- Each PR carries a `prep_verdict` from `pr-prepare` recording the routing decision.
- Write the `finish` section of `exec-state.json` with `pr_urls` (append-section; prior sections survive).
- If the legacy `.drain-handoff.json` exists, also update it with `pr_urls` (dual-write).
- If Linear is available and an issue ID is known, post a review-summary comment.
- If Linear is unavailable, include the review summary in the final response instead.

### 1. Restate the issue

Start with one sentence:

> This branch closes <issue> by delivering <summary>.

If no issue ID is known, derive the summary from the branch name and commit subjects.

### 2. Verify green state

Run the repo's required tests before creating any PRs.

If tests fail, stop. Report the failing command and relevant output. Do not submit PRs.

### 3. Determine slices

If .drain-handoff.json exists, read its slices array.

If it does not exist, derive slices from git, ranging from the resolved base (default `main`):

`git log <base>..HEAD --reverse --format=%H%x00%B%x00%x00`

Use each commit as one slice. The first line of the commit message is the title; the remaining body is the Why.

If multiple unrelated changes are squashed into one commit, warn that the branch was not sliced during build. Continue only if it appears to be a single logical change, or the operator explicitly accepts the risk.

### 4. Choose submission path

Check Graphite preconditions in order:

`which gt gt auth status gt repo init --check`

Use these rules:

- If all checks pass, use the Graphite path.
- If gt is absent, use the plain-git path.
- If gt exists but auth or repo initialization fails, stop and show the exact error. Do not silently fall back to git.

### 5. Graphite path

For each slice, oldest first:

- Create or track a Graphite branch at that exact commit.
- Ensure the branch points to the slice commit, not the stack tip.
- Parent the oldest slice's branch on `<base>` (e.g. `gt track --parent <base>`) so the bottom PR targets `<base>`, not `main`. Each later slice parents on the slice before it.
- Set a minimal placeholder body containing the commit subject and a `<!-- pending pr-prepare -->` marker; `pr-prepare` overwrites it in step 8.

Submit the stack:

`gt stack submit --no-interactive`

Wrap each gt call in a bounded recovery loop:

- On success: continue.
- On stale parent or out-of-sync error: run gt repo sync, retry once.
- On dirty working tree: stash, retry once, then restore the stash.
- On auth or repo initialization error: stop immediately.
- On any second failure: stop and report the exact error.

### 6. Plain-git path

Use this only when gt is absent.

For each slice, oldest first:

- Create a branch from the slice parent named <issue-or-branch>/<slug>-<n>.
- Cherry-pick the slice commit.
- Push the branch and create the PR with gh pr create, using the placeholder body from step 5 (commit subject plus the `<!-- pending pr-prepare -->` marker). Target the oldest slice's PR at `<base>` (`gh pr create --base <base>`); each later slice targets the prior slice's branch.

The plain-git path produces the same set of PRs in the same order as Graphite; `pr-prepare` writes the durable body on both paths in step 8.

### 7. Verify PRs

Before proceeding, verify every PR URL is reachable:

`gh pr view <url>`

If any PR is missing or unreachable, stop and report the problem. Do not invoke `pr-prepare` and do not post the Linear comment yet.

Write the `finish` section of `exec-state.json` with the submitted PR URLs. Open `exec-state.json` if it exists (preserving any prior sections), set the `finish` key, and write the file back:

```json
{
  "finish": {
    "pr_urls": [
      { "title": "<PR title>", "url": "<https://...>" }
    ]
  }
}
```

If `exec-state.json` does not yet exist, create it with only the `finish` section.

If the legacy `.drain-handoff.json` exists, also update it with `pr_urls` (dual-write for cross-repo migration compatibility):

`{ "pr_urls": [ { "title": "<PR title>", "url": "<https://...>" } ] }`

### 8. Delegate per-PR preparation to `pr-prepare`

For each created PR, in order, invoke `pr-prepare` with the PR's URL. `pr-prepare` reads the diff, writes the diff-driven What / Why / Focus body, confirms it through a re-read, applies the auto-merge carve-out, and emits a `prep_verdict` per PR. Collect each verdict alongside the PR URL.

If `pr-prepare` halts on any PR (diff unreachable, body re-read fails, carve-out conditions break), stop here. Do not post the final trail until every PR has a confirmed body and a recorded `prep_verdict` — a stack with one un-prepared PR is not finished.

### 9. Post final trail

If Linear is available and an issue ID is known, post one review-summary comment to the issue. Include the per-PR `prep_verdict.route` so the reviewer knows which PRs were routed to auto-merge and which need human review.

If Linear is unavailable or no issue ID is known, include the same summary in the final response.

If repo policy does not permit PRs, follow the repo policy and note the deviation in the summary.

## PR body template

The durable body is written by `pr-prepare` in step 8 — `exec:finish` writes only a placeholder. The template `pr-prepare` follows is:

`## What <One to three sentences describing what this slice changes. Diff-level, not ticket-level.> ## Why <Why this slice exists, what issue it supports, why it can be reviewed independently.> ## Focus <Specific files, decisions, or patterns to review. If none: "No critical review areas — safe for auto-merge.">`

## Review-summary template

`PR stack submitted: <n> PR(s) <slice-1-title>: <url> — route: <auto-merge | human-review> <slice-2-title>: <url> — route: <auto-merge | human-review> Path: graphite | plain-git Pre-submission review findings: critical: N, required: N (fixed: N, deferred: N)`

## Red flags

- A PR exists whose body is still the placeholder from step 5/6 — `pr-prepare` was never run, or its re-read confirmation failed silently.
- A PR's `prep_verdict` is missing from the review-summary comment.
- `pr-prepare` returned `auto-merge` on a PR with a schema migration, auth change, breaking API, new dependency, production-data touch, or one-way-door decision — investigate the verdict before trusting it.
- The final trail was posted before every PR was prepared and verified.

## Exit criteria

The skill is complete only when:

1. Tests passed before PR creation.
2. Each slice has exactly one PR.
3. `pr-prepare` ran on every PR and wrote a confirmed What / Why / Focus body.
4. A `prep_verdict` is recorded for every PR; the review-summary surfaces each route.
5. Every PR URL was verified reachable.
6. `exec-state.json` exists with a `finish.pr_urls` section after finishing.
7. If the legacy `.drain-handoff.json` existed, it was also updated with `pr_urls` (dual-write).
8. Graphite precondition failures halted instead of falling back silently.
9. The final review summary was posted to Linear when available, or reported to the operator when Linear is unavailable.

## Related

- `skills/pr-prepare/SKILL.md` — the named sub-skill invoked in step 8; independently usable on a single existing PR.
- `skills/exec-pickup/SKILL.md` — the front door that delegates to this skill after review and verify pass.
