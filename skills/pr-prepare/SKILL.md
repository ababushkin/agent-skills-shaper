---
name: pr-prepare
description: >
  Prepares stack PRs for review or merge: reads each PR diff, writes a structured
  What/Why/Focus body, routes each to auto-merge or human review per the carve-out
  rule, and records the decision in `prep_verdict`.
  Trigger phrases: "prepare my PR", "write a PR body", "prep the stack",
  "fill in the PR description", "should this auto-merge", "route this PR".
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
length_target: 170–220
author: Anton Babushkin
predecessor:
  repo: none
  skill: none
  relation: new
kept_from_predecessor: "n/a"
changed_from_predecessor: "n/a"
---

# PR prepare

## Purpose

pr-prepare reads one or more stack PR diffs, writes a structured three-section body (What / Why / Focus) on each, decides whether the PR qualifies for the auto-merge carve-out, and records the routing verdict in `prep_verdict`. Without it, PRs from drained tickets carry no structured context: reviewers parse intent from the diff alone, trivially safe changes queue for unnecessary human review, and risky changes get merged without a named focus area. The PR body is the artefact reviewers carry from PR open to merge — and the artefact that survives in version history after the ticket is closed (agentic P7: memory lives in artefacts). The routing verdict is how the operator avoids over-reviewing safe changes while ensuring risky ones are seen.

## When to use

- A PR (or a stack of PRs) is open but lacks a structured description.
- A PR body exists but was written informally; a reviewer is about to be assigned.
- The operator wants a routing verdict before deciding whether to queue for human review or merge directly.
- Trigger phrases: "prepare my PR", "write a PR body", "prep the stack", "should this auto-merge", "route this PR".

## When not to use

- **The PR does not exist yet.** Write the code first; this skill reads an actual diff.
- **The PR is a draft by convention.** Mark it ready for review first, then run this skill.
- **The goal is full code review, not preparation.** Use `code-review-and-quality` to issue review verdicts — this skill writes context for the reviewer, not a review verdict.

## Inputs

- One or more PR identifiers (numbers, URLs, or "current branch") from a stack
- Access to the PR diff via the configured PR platform API
- Write access to PR bodies on the same platform
- Optional: linked issue or initiative text as context for the Why section

## Outputs

- A What/Why/Focus body written to each PR
- A `prep_verdict` record per PR: `{result: "structured"|"auto-merge", route: "human-review"|"auto-merge", reasoning: "..."}`

## Workflow

**1. Restate the change.**
Before writing, state in one sentence what changed in this PR and what it is meant to achieve. This anchors the body to the actual diff, not to what the agent assumes the PR should say (agentic P3). If the input is a stack, read each PR diff independently before writing — stack-level context leaks into individual bodies and produces descriptions that only make sense in sequence, not in isolation.

**2. [GATE] Verify platform API access and diff readability.**
Call the read API against the PR. Stop and report the exact error if: the API returns an error, the response is empty, or the diff cannot be parsed into changed files. Do not proceed and do not fabricate a diff (agentic P2: hallucination is the default). A silently-wrong diff produces a confidently-wrong body; there is no recovery from a fabricated What section that ships to reviewers.

**3. Read the diff; identify the signals.**
Read the full diff. Record:
- **Scope**: which files changed and which systems they belong to
- **Scale**: net line count, excluding generated files (lock files, generated schema snapshots, automatically generated migration files)
- **Critical signals**: any of the following make the PR non-auto-mergeable — schema migration, auth-path change, breaking API change, new external dependency, production-data touch, one-way-door decision (universal P3: decisions expensive to reverse warrant deliberate review)

**4. Write the What / Why / Focus body.**
Compose three sections:
- **What**: what changed — which code, which behaviour, which interface. One to three sentences. Do not re-state the ticket title; add the diff-level detail the title cannot carry.
- **Why**: the motivation — which issue or initiative this serves, what problem it solves for whom. Cite the linked ticket if present; derive from the diff and context if absent.
- **Focus**: where reviewers should concentrate. Name specific files, patterns, or decisions that carry risk or non-obvious logic. If no items exist, write a single line: `No critical review areas — safe for auto-merge.`

The body is written for a reviewer with no prior context on the change, not for the author who just wrote it (agentic P7).

**5. [GATE] Apply the auto-merge carve-out.**
Auto-merge applies only when **all four** conditions hold:
1. **Small**: net diff is ≤ 200 lines excluding generated files.
2. **No critical signals**: none of the signals from Step 3 were found.
3. **Focus is empty**: the Focus section contains only `No critical review areas — safe for auto-merge.`
4. **CI is green**: the PR's tests and lint checks have passed (confirmed from CI status, not asserted).

All four hold → `prep_verdict.result: "auto-merge"`, `prep_verdict.route: "auto-merge"`.  
Any one fails → `prep_verdict.result: "structured"`, `prep_verdict.route: "human-review"`.  

Record which condition failed in `prep_verdict.reasoning` — the operator needs the reason, not just the verdict.

**6. Write the body to the PR.**
Write the composed What/Why/Focus body to the PR via the platform API.

**7. [GATE] Confirm write; then trigger routing; record verdict.**
Re-read the PR body from the platform and verify it matches what was composed. If the write failed, stop and report the error — do not mark the PR prepared and do not trigger auto-merge on a broken write. Once the body is confirmed written: for auto-merge PRs, trigger the platform's native auto-merge mechanism (the confirmed body survives as the history artefact — universal P1: the PR body is how future observers understand the merged change); for human-review PRs, assign reviewers or mark the PR ready per the team's convention. Record `prep_verdict` for each PR.

## Artefact templates

```markdown
## What

<What changed — which code, which behaviour, which interface.
One to three sentences; diff-level detail, not ticket-level summary.>

## Why

<Motivation: which issue or initiative this serves, what problem it solves, for whom.
Cite the linked ticket if present.>

## Focus

<Named review areas — specific files, patterns, or decisions requiring attention.
One item per line. If no items: "No critical review areas — safe for auto-merge.">
```

`prep_verdict` record:

```json
{
  "result": "structured | auto-merge",
  "route": "human-review | auto-merge",
  "reasoning": "one sentence naming the deciding condition"
}
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "The ticket describes it — the PR body is redundant." | The ticket describes the desired outcome; the PR body describes what the diff actually does. They are at different abstraction levels, and the PR body is what survives in `git log` after the ticket is closed. |
| "This is a tiny change, it doesn't need a body." | If it's tiny, the body takes two minutes. If the body is hard to write, the change is not as tiny as it looked — use that difficulty as a scope signal. |
| "Auto-merge is risky — I'll always route to human review." | Over-routing defeats the carve-out. The four conditions are calibrated to make auto-merge safe; forcing human review on trivially safe changes trains reviewers to ignore PR queues. |
| "I'll write the body after the review." | The body is for the reviewer, not the author. Written after the review, it serves no one — the reviewer has already formed an opinion. |
| "I know what the diff does — I'll write Focus from memory." | Write from the diff, not from memory. Memory is incomplete and partial; the diff is the source of truth. |

## Red flags

- A What section that re-states the ticket title without adding diff-level detail.
- A Focus section that says "see diff" without naming specific files or patterns.
- `prep_verdict.route: "auto-merge"` on a PR with a schema migration, auth change, or new external dependency.
- `prep_verdict.reasoning` is absent or non-specific — every routing decision has a named condition.
- The body was written before the diff was read (agentic P3 violation: the diff is the spec here).
- CI was not confirmed green before issuing `route: "auto-merge"`.
- Step 7 skipped — the body was written but never confirmed written.

## Verification / exit criteria

The skill has run correctly when:

1. A What/Why/Focus body exists on each PR in the stack, composed after reading the actual diff.
2. The What section contains diff-level detail (specific files, behaviours, or interfaces changed), not a ticket-level summary.
3. The Focus section names specific items requiring reviewer attention, or explicitly states no critical review areas.
4. `prep_verdict` is recorded for each PR with `result`, `route`, and `reasoning` populated.
5. `route: "auto-merge"` was issued only when all four carve-out conditions held (small, no critical signals, empty focus, CI green).
6. The PR body was confirmed written by re-reading from the platform after the write.

## References

- `rules/eng-principles-agentic.md` — P2 (hallucination is default: don't fabricate the diff), P3 (spec as seatbelt: restate the change before writing), P4 (evidence beats vibes: route from signals, not feel), P7 (memory lives in artefacts: PR body is the persistent context)
- `rules/eng-principles-universal.md` — P1 (observed is done: PR body is how the change is understood post-merge), P3 (reversibility: one-way-door check is a carve-out blocker), P8 (small batches: carve-out rewards ≤200-line changes)
- `code-review-and-quality` — the skill that runs after pr-prepare: pr-prepare writes reviewer context; code-review-and-quality issues verdicts
