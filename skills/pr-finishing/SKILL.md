---
name: pr-finishing
description: >
  Decomposes a verified, slice-committed diff into a stack of small PRs — one per
  commit slice — using Graphite (with plain-git fallback), each carrying a
  What/Why/Focus body; posts a review-summary trail to the Linear issue.
  Trigger phrases: "finish this branch", "submit the stack", "create stacked PRs",
  "finish the PR", "submit my work".
pack: engineering
lifecycle_stage: ship
principles_implemented:
  - source: eng-agentic
    id: P2
    bucket: embedded
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
    id: P7
    bucket: embedded
  - source: eng-universal
    id: P1
    bucket: embedded
  - source: eng-universal
    id: P3
    bucket: embedded
  - source: eng-universal
    id: P8
    bucket: embedded
length_target: 220–280
author: Anton Babushkin
predecessor:
  repo: https://github.com/obra/superpowers
  skill: finishing-a-development-branch
  relation: derivative
kept_from_predecessor: "verify-then-finish flow; worktree environment detection; worktree cleanup rules"
changed_from_predecessor: "slice-during-build commit discipline; commit→stacked-PR decomposition via Graphite; gt recovery loop; What/Why/Focus body contract (ported from pr-prepare); Linear trail step; plain-git fallback with artefact parity"
---

# PR finishing

## Purpose

pr-finishing lands a coarse Linear issue as a **stack of small, independently-reviewable PRs** —
one per commit slice — rather than one fat PR that obscures the logic of each change.
The decomposition is decided during the build, not after: the worker commits in reviewable slices
(one logical change per commit, each independently green), and pr-finishing maps those commits
mechanically to stacked PRs without re-slicing a flattened diff.

The skill ports the verify-then-finish discipline from `finishing-a-development-branch` and adds
three new parts: a Graphite-first stacked-submit path with a recovery loop that retries transient
failures and halts on genuine precondition failures; a plain-git fallback that produces the same
PR body and Linear trail when `gt` is absent; and a review-summary comment posted to the Linear
issue at the end. The PR body — What/Why/Focus — is the persistent context artefact that survives
after the ticket is closed (agentic P7: memory lives in artefacts).

## When to use

- A build is complete: tests pass, all changes are committed in independently-green slices on a
  feature branch.
- The issue is ready to transition from In Progress to Done or review, and the exit sequence
  requires PR submission.
- Triggered by the drain orchestrator's completion sequence or by the operator directly.
- Trigger phrases: "finish this branch", "submit the stack", "create stacked PRs", "submit my work".

## When not to use

- **Tests are failing.** Fix tests first; this skill does not mask a broken state.
- **Work is committed as one squash with multiple independent changes.** Advise the worker to
  re-slice before finishing — post-hoc re-slicing of a squashed commit is the hard, error-prone
  path. The skill logs a warning if the manifest is absent but continues on best-effort for a
  single-commit, single-change case.
- **The PR already exists.** Use `pr-prepare` to write or rewrite a body on an existing PR.
- **`gt auth` or `gt repo init` fails.** These are precondition failures, not transient errors.
  The skill surfaces a clear halt; it does not silently degrade to git on a misconfigured Graphite
  setup.

## Inputs

- A feature branch with independently-green commits — one logical change per commit.
- Optional: `.drain-handoff.json` in the worktree root with a `slices` array (SHA, title, why).
  If absent, the skill derives slices from `git log main..HEAD --reverse`.
- `gt` CLI (Graphite): if present and preconditions pass, the Graphite path runs; otherwise,
  the plain-git path applies.
- Push policy from repo instructions (e.g. this repo: push directly to main; PR only on request).
  The skill honours the policy it reads.
- Linear issue ID (required for the review-summary trail step).

## Outputs

- A stack of PRs — one per slice — each carrying the What/Why/Focus body.
- Graphite path: a `gt stack` submitted with `--no-interactive`.
- Plain-git path: one branch + PR per slice, branches named `<issue>/<slug>-<n>`.
- `.drain-handoff.json` updated with a `pr_urls` array.
- A review-summary comment posted to the Linear issue.

## Workflow

**1. Restate the issue.**
Before anything else, state one sentence: "This branch closes [issue] by delivering [summary]."
Anchoring to the issue prevents writing a body about the technical diff without connecting it to
what the user gets (agentic P3). If no issue ID is available, derive the summary from the branch
name and commit subjects.

**2. [GATE] Verify green state.**
Run the repo's test suite. If tests fail: stop, report the failures, do not submit. This gate is
identical to `finishing-a-development-branch` Step 1 — no bypass exists (agentic P6: stop the
line on the first failure).

**3. Read the slice manifest.**
Check for `.drain-handoff.json` in the worktree root. If present, read the `slices` array; each
entry carries `sha`, `title`, and optionally `why`. If absent, run
`git log main..HEAD --reverse --format=%H %s` and treat each commit as one slice, deriving
the title from the commit subject and the Why from the commit body.

Log a notice if the manifest is absent — it means the worker did not follow slice-during-build
discipline; the skill continues on best-effort and records the path taken.

**4. [GATE] Detect Graphite preconditions.**
Check in order: `which gt` exits 0; `gt auth status` exits 0; `gt repo init --check` exits 0.

- All three pass → Graphite path (Step 5).
- `gt` absent → plain-git path (Step 7). Log which path was taken.
- `gt` present but `gt auth` or `gt repo init` fails → **halt**. These are precondition failures,
  not transient errors. Degrading silently to git changes the trail and confuses the operator.
  Display the exact `stderr` and stop.

**5. Graphite path — branch, track, body, submit.**
For each slice (oldest commit first):

a. `gt branch create <issue>/<slug>` (or `gt track --branch <name>`) to associate the commit
   with a Graphite branch.
b. Write the What/Why/Focus body for this slice (see Artefact template) and set it via
   `gt pr description` or the equivalent `gh pr edit` after `gt stack submit`.
c. After all slices are tracked, run `gt stack submit --no-interactive` to submit the full stack.

**Recovery loop** — wrap every `gt` call:

- Exit 0: continue.
- Non-zero exit: classify `stderr`:
  - Stale parent / out-of-sync: run `gt repo sync`, retry once.
  - Dirty working tree: `git stash`, retry, `git stash pop`.
  - Missing precondition (`gt auth`, `gt repo init`): halt immediately — no retry.
  - Any other error after one retry: halt, show exact `stderr`, recommend the plain-git fallback.
- Bounded retries: at most one retry per `gt` call; a second failure always halts.

**6. [GATE] Confirm stack submitted.**
After `gt stack submit`, verify each PR URL is reachable (`gh pr view <url>` exits 0 or HTTP 200).
If any URL is missing or unreachable: stop, report, do not post the review-summary comment yet.
Record the confirmed URLs in `.drain-handoff.json` under `pr_urls`.

**7. Plain-git path (used when `gt` is absent).**
For each slice (oldest first):

a. `git checkout -b <issue>/<slug>-<n>` from the slice's parent commit.
b. `git cherry-pick <sha>` for this slice.
c. Write the What/Why/Focus body (same template as the Graphite path — artefact parity is the
   contract; agentic P7).
d. `git push -u origin <branch>`.
e. `gh pr create --title "<title>" --body "<body>"`.

After all slices, record PR URLs in `.drain-handoff.json` under `pr_urls`. The body and trail
artefacts must be identical to what the Graphite path would have produced.

**8. Review-summary comment and Linear status update.**
Post one comment to the Linear issue (see Artefact template). Transition the issue status per
governance at the moment of state change — not batched at session end. If the push policy does
not permit a PR (e.g. push-directly-to-main repo), note the deviation in the comment.

## Artefact template

`.drain-handoff.json` (slices written at build time; `pr_urls` added by this skill):

```json
{
  "issue": "ABA-123",
  "slices": [
    { "sha": "<40-char SHA>", "title": "<PR title ≤ 70 chars>", "why": "<optional motivation>" }
  ],
  "pr_urls": [
    { "title": "<PR title>", "url": "<https://...>" }
  ]
}
```

PR body (written identically on both paths):

```markdown
## What

<What this slice changes — which code, which behaviour, which interface.
One to three sentences. Diff-level detail, not ticket-level summary.>

## Why

<Motivation: which issue or initiative this serves; why this slice is independent.
Cite the linked ticket. For slice 1: full context. For subsequent slices: reference prior PR.>

## Focus

<Named review areas — specific files, patterns, or decisions requiring attention.
One item per line. If no items: "No critical review areas — safe for auto-merge.">
```

Review-summary comment posted to Linear issue:

```
PR stack submitted: <n> PR(s)
<slice-1-title>: <url>
<slice-2-title>: <url>
Path: graphite | plain-git
Pre-submission review findings: critical: N, required: N (fixed: N, deferred: N)
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "The work is one change — one PR is fine." | One commit = one PR is correct for a single logical change. If there is one commit and it is genuinely one change, pr-finishing submits one PR. The skill decomposes only when the manifest or log shows multiple slices. |
| "Re-slicing the squashed diff post-hoc is good enough." | Reconstructing independently-green boundaries from a squashed diff cannot guarantee each slice builds on its own. The contract is slice-during-build; post-hoc is a logged fallback, not the primary path. |
| "The `gt` error is minor — I'll proceed with plain-git and not say so." | Silently degrading to plain-git changes the trail. The operator must know which path ran — that is what the review-summary comment records. |
| "I'll skip the recovery loop for speed — `gt` is usually reliable." | Stale-parent and dirty-tree failures are common in long-running build sessions; an unhandled non-zero exit halts the whole drain run. The recovery loop costs nothing on clean runs. |
| "The plain-git fallback can use a simpler body format." | Artefact parity is the contract (agentic P7). A reviewer or future operator cannot tell from the PR which path ran; the Linear comment records it. Same body template on both paths is non-negotiable. |

## Red flags

- A PR body is missing any of What / Why / Focus.
- `.drain-handoff.json` was not updated with `pr_urls` after submission.
- `gt auth` or `gt repo init` was not checked before running `gt branch create`.
- A `gt` call returned non-zero but the skill continued without classifying the error.
- The review-summary comment was posted before all PR URLs were confirmed reachable.
- The plain-git path produced a different body template than the Graphite path.
- Tests were skipped before submission.
- A multi-slice diff was submitted as a single PR without logging that the manifest was absent.

## Verification / exit criteria

The skill has run correctly when:

1. Tests passed (verified, not asserted) before any PR was created.
2. Each commit slice has exactly one PR; the body carries What / Why / Focus with diff-level detail.
3. `.drain-handoff.json` exists in the worktree root with `pr_urls` listing each submitted PR.
4. The path taken (Graphite or plain-git) is recorded in the review-summary comment.
5. Graphite path: each `gt` call was wrapped in the recovery loop; at most one retry per call;
   a precondition failure produced a halt, not a degraded run.
6. Plain-git path: each slice was pushed to its own branch; body and trail artefacts are identical
   to what the Graphite path would have produced.
7. The review-summary comment is posted to the Linear issue after all PR URLs are confirmed
   reachable; issue status is updated at the moment of state change.

## References

- `skills/finishing-a-development-branch/SKILL.md` (superpowers) — ported verify-then-finish flow;
  worktree environment detection and cleanup rules
- `skills/pr-prepare/SKILL.md` — What/Why/Focus body contract; auto-merge carve-out (use when
  the PR already exists and needs a body written or rewritten)
- `rules/eng-principles-agentic.md` — P2 (don't fabricate diffs), P3 (spec as seatbelt: restate
  the issue before writing), P4 (evidence beats vibes: route from signals), P6 (stop the line on
  failure), P7 (artefacts are memory: PR body is the persistent record)
- `rules/eng-principles-universal.md` — P1 (observed is done), P3 (reversibility: one-way-door
  check), P8 (small batches: stack of small PRs over one fat PR)
- `docs/design-docs/execution-workflow/design-doc.md` — drain orchestrator context; `.drain-handoff.json` schema origin
