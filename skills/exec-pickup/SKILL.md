---
name: exec:pickup
description: >
  Front-door skill for draining a Linear issue end-to-end — from pickup through breakdown,
  build, review, verify, and PR finishing. Every step is a named delegation to its owning
  skill; this skill is the supervisor pointer, not the procedure. Use when a drain-cycle
  worker or supervisor prompt picks up a Linear issue and needs a single entry point for
  the full execution workflow.
  Trigger phrases: "pick up this issue", "start working on this ticket", "drain this issue",
  "exec:pickup", "begin issue execution", "work on ABA-NNN".
pack: engineering
lifecycle_stage: build
principles_implemented:
  - source: eng-agentic
    id: P7
    bucket: embedded
  - source: eng-agentic
    id: P3
    bucket: embedded
  - source: eng-universal
    id: B2
    bucket: embedded
length_target: 120–180
author: Anton Babushkin
predecessor:
  repo: obra/superpowers
  skill: subagent-driven-development (MIT)
  relation: adjacent
kept_from_predecessor: >
  Pickup → breakdown → build → review → finish loop shape; the principle that breakdown
  happens at pickup time (fresh context) rather than plan time.
changed_from_predecessor: >
  Every step is a named delegation to a specific `exec:*` skill (no inlined procedure).
  Handoff contract (`pickup-envelope.json`) carries the issue AC checklist end-to-end so
  the spec-compliance persona can grade built-the-wrong-thing. Blocked/halt path is
  explicit. Tracker-bound: reads issue from Linear, writes status on finish.
---

# Exec: Pickup (Front Door)

## Purpose

A drain-cycle worker picks up a Linear issue and must reach a merged PR with a full review trail. This skill is the single entry point: it reads the issue, writes the handoff envelope, invokes `exec:breakdown` to produce the ordered task list, then delegates each remaining step — build, review, verify, and finish — by name. It does not inline any procedure; every named delegation is the whole description of that step.

The acceptance criteria on the issue travel inside `pickup-envelope.json` from this step through to the spec-compliance persona in `exec:review`. Nothing is re-typed; nothing is lost in transit.

## When to use

- A Linear issue has been assigned and a worktree is open.
- A drain-cycle supervisor prompt points here as its single execution pointer.
- Any worker picking up an issue fresh and wanting the complete execution path without improvising.

## When not to use

- **Only reviewing a diff** — use `exec:review` directly.
- **Only finishing an already-built PR** — use `exec:finish` directly.
- **Shaping or planning work** — use `shape:delivery`, `shape:initiative`, or `shape:plan-review`; this skill is execution-only.
- **Exploratory spikes** — use `shape:backend-spike` or `shape:product-spike`; `exec:pickup` assumes the work is broken down and ready to build.

## Inputs

- **Issue ID** — a Linear issue identifier (e.g. `ABA-363`), provided by the supervisor prompt or the user
- **Worktree path** — the local path where the issue branch is checked out
- **Branch name** — the git branch for this issue

## Outputs

- **`pickup-envelope.json`** at the worktree root — the handoff carrier for all downstream steps
- An ordered task list from `exec:breakdown`, each task with a `done_when` clause
- A series of delegations to `exec:build`, `exec:review`, `exec:verify`, and `exec:finish`
- On blocked: a Linear comment naming the blocker; issue status left In Progress

## Workflow

**1. Read the issue. [GATE]**

Load the issue body from Linear (via `mcp__claude_ai_Linear__get_issue`). Extract:
- `issue_id` — the identifier
- `body_md` — full body text
- `ac_checklist[]` — every Done-when / acceptance-criteria line, verbatim
- `labels[]` — issue labels
- `blocked_by[]` — any issues listed in a "Blocked by" section

If the issue cannot be read, halt with a comment naming the failure and do not proceed.

**2. Check for blockers. [GATE]**

If `blocked_by[]` is non-empty, invoke `shape:stop-the-line`:
- Post a comment on the issue naming each blocker explicitly.
- Leave the issue status as In Progress.
- Halt. Do not proceed to breakdown.

**3. Write `pickup-envelope.json`.**

Write the envelope to the worktree root:

```json
{
  "issue_id": "<id>",
  "branch": "<branch>",
  "worktree_path": "<path>",
  "ac_checklist": ["<verbatim AC item>", "…"],
  "body_md": "<full issue body>",
  "labels": ["<label>", "…"],
  "blocked_by": []
}
```

This file is the contract. All downstream skills read it; none re-read the Linear issue.

**4. Invoke `exec:breakdown`. [GATE]**

Delegate to `exec:breakdown`, passing the envelope. Receive back an ordered task list. Each task must carry:
- `id` — a short slug
- `done_when` — one verifiable clause
- `model_tier` — Balanced | Fast | Frontier
- `axes` — RC·SC·HS·SR·OR ratings

If `exec:breakdown` returns fewer than one task or any task is missing `done_when`, halt and post a comment naming the gap.

**5. Build each task slice with `exec:build`.**

For each task in the ordered list:
- Delegate to `exec:build`, passing the task and the envelope path.
- `exec:build` owns the RED → GREEN → commit loop, including `exec:debug` escalation on a stuck red loop and `exec:simplify` on green.
- Do not proceed to the next slice until the current task's `done_when` clause is satisfied and a commit exists.

**6. Invoke `exec:review`. [GATE]**

After all slices are committed, delegate to `exec:review`, passing:
- The working-tree diff
- The `pickup-envelope.json` path (so the spec-compliance persona reads `ac_checklist` directly)

If `exec:review` returns `NO-GO`, loop back into `exec:build` on the failing findings. Do not proceed to verify until the verdict is `GO`.

**7. Invoke `exec:verify`. [GATE]**

Delegate to `exec:verify`, passing the `ac_checklist` from the envelope and the diff. A fail loops back into `exec:build`. A pass is the green light for finishing.

**8. Invoke `exec:finish`.**

Delegate to `exec:finish`, passing the envelope, the review verdict, and the verify result. `exec:finish` owns the PR body, review-summary comment, and Linear status transition.

## Envelope template

```json
{
  "issue_id": "",
  "branch": "",
  "worktree_path": "",
  "ac_checklist": [],
  "body_md": "",
  "labels": [],
  "blocked_by": []
}
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "The issue is simple, I'll just start building." | Skipping breakdown means tasks have no `done_when` clause and the review step has no AC to grade against. Write the envelope; invoke breakdown. |
| "I already know the acceptance criteria, I don't need to write the envelope." | Other skills cannot read your memory. The envelope is the contract; without it, the spec-compliance persona grades blind. |
| "The blocker might resolve soon, I'll start anyway." | Partial work on a blocked issue creates a merge conflict when the blocker clears. Post the comment; halt; pick up a different issue. |
| "I'll inline the breakdown steps here to save a round-trip." | The front door ≤ 200 lines constraint exists precisely to make inlining structurally impossible. Delegate to `exec:breakdown`. |
| "exec:review and exec:verify both check the AC — I'll skip one." | They check from different angles: `exec:review` grades the diff against spec (built-the-wrong-thing); `exec:verify` checks each AC item is satisfied. One pass misses what the other catches. |

## Red flags

- The workflow section contains a procedure that is not a named delegation.
- `pickup-envelope.json` is missing from the worktree root before `exec:build` starts.
- A task in the breakdown list has no `done_when` clause.
- The issue transitions to Done before `exec:finish` is invoked.
- `exec:review` returns `NO-GO` and the next step is `exec:verify` without looping back to `exec:build`.
- The `ac_checklist` field in the envelope is empty on an issue that has acceptance criteria.

## Verification / exit criteria

- `pickup-envelope.json` exists at the worktree root with all required fields populated.
- Every task from `exec:breakdown` has a `done_when` clause.
- `exec:review` has returned `GO` before `exec:verify` is invoked.
- `exec:finish` has been invoked and has posted the review-summary comment and transitioned the issue.
- A dry run on one real issue reaches the PR step without a human being re-prompted between steps.

## References

- `docs/design-docs/execution-workflow/design-doc.md` — the accepted N04 contract; skill graph, handoff contract table, and verb namespace
- `docs/adr/0004-execution-verb-namespace.md` — decision of record for the `exec:*` prefix
- `docs/adr/0003-persona-contract-and-dispatch-protocol.md` — ADR 0003 persona dispatch (consumed by `exec:review`, not by this skill)
- `skills/execution-review/SKILL.md` — `exec:review` (persona fan-out, ADR 0003 dispatch)
- `skills/verify-implementation/SKILL.md` — `exec:verify`
- `skills/pr-prepare/SKILL.md` — `exec:finish`
- Eng-agentic principle 7: "Memory lives in artefacts, not in agents" — the envelope is the artefact
- Eng-agentic principle 3: "The shortest path is the failure mode; the spec is the seatbelt" — AC carry-through
