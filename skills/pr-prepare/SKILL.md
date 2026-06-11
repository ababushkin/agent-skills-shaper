---
name: pr-prepare
description: >
  Prepares stack PRs for review or merge: reads each PR diff, writes a structured
  What/Why/Focus body, routes each PR to auto-merge or human review using the
  carve-out rule, and records the decision in prep_verdict. Trigger phrases:
  "prepare my PR", "write a PR body", "prep the stack", "fill in the PR description",
  "should this auto-merge", "route this PR".
---

# PR prepare

## Purpose

Prepare one or more PRs for review or merge by reading the actual diff, writing a reviewer-facing What / Why / Focus body, deciding whether the PR qualifies for auto-merge, and recording the routing decision in prep_verdict.

The PR body must describe what the diff actually does, not just repeat the ticket. It is the durable review and history artefact after the ticket is closed.

## When to use

- A PR or stack is open and needs a structured description.
- An informal PR body needs to be rewritten before review.
- The operator needs a routing verdict: human review or auto-merge.

## Do not use when

- The PR does not exist yet.
- The PR is still draft by team convention.
- The goal is full code review. Use code-review-and-quality instead.

## Inputs

- One or more PR identifiers: numbers, URLs, or current branch
- Access to read PR diffs and CI status
- Write access to PR bodies
- Optional linked issue or initiative context

## Outputs

- A What / Why / Focus body written to each PR
- A prep_verdict per PR:

```json
{
  "result": "structured | auto-merge",
  "route": "human-review | auto-merge",
  "reasoning": "one sentence naming the deciding condition"
}
```

## Workflow

### 1. Restate the change

Before writing, state in one sentence what changed in this PR and what it is meant to achieve.

For stacks, read and prepare each PR independently. Do not let stack-level context replace diff-level detail.

### 2. Gate: verify diff access

Read the PR through the platform API. Stop and report the exact error if:

- The API fails
- The response is empty
- The diff cannot be parsed into changed files

Do not fabricate or infer a diff.

### 3. Read the diff and collect signals

Record:

- **Scope:** changed files and affected systems
- **Scale:** net line count, excluding generated files
- **Critical signals:** schema migration, auth-path change, breaking API change, new external dependency, production-data touch, or one-way-door decision

Generated files include lock files, generated schema snapshots, and automatically generated migration files.

### 4. Write the PR body

```markdown
## What

<One to three sentences describing changed code, behaviour, or interfaces.
Include diff-level detail, not just the ticket title.>

## Why

<Motivation, linked issue or initiative if present, and the problem solved.>

## Focus

<Specific files, patterns, or decisions reviewers should inspect.
If none: No critical review areas — safe for auto-merge.>
```

The body is for a reviewer with no prior context.

### 5. Gate: apply the auto-merge carve-out

Auto-merge only if **all four** conditions hold:

1. Net diff is ≤ 200 lines, excluding generated files.
2. No critical signals were found.
3. Focus contains only: No critical review areas — safe for auto-merge.
4. CI is confirmed green from platform status.

If all four hold:

```json
{
  "result": "auto-merge",
  "route": "auto-merge",
  "reasoning": "all carve-out conditions held: small diff, no critical signals, empty focus, CI green"
}
```

If any condition fails:

```json
{
  "result": "structured",
  "route": "human-review",
  "reasoning": "human review required because <specific failed condition>"
}
```

### 6. Write and confirm

Write the body through the platform API, then re-read the PR body and verify it matches.

If confirmation fails, stop. Do not mark the PR prepared and do not trigger auto-merge.

### 7. After the body is confirmed:

- For auto-merge PRs, trigger the platform’s native auto-merge mechanism.
- For human-review PRs, assign reviewers or mark ready according to team convention.
- Record prep_verdict for each PR.

## Red flags

- What only repeats the ticket title.
- Focus says “see diff” without naming files or decisions.
- Auto-merge is selected despite migrations, auth changes, breaking APIs, new dependencies, production-data touches, or one-way-door decisions.
- prep_verdict.reasoning is missing or vague.
- CI was not confirmed green before auto-merge.
- The body was written before reading the diff.
- The body was not re-read after writing.

## Exit criteria

The skill is complete when each PR has:

1. A confirmed What / Why / Focus body based on the actual diff.
2. Diff-level detail in What.
3. Specific review focus, or the exact safe auto-merge line.
4. A populated prep_verdict.
5. Auto-merge only when all four carve-out conditions held.
6. A confirmed platform write before routing.

## Related

- code-review-and-quality: performs the actual review verdict after preparation.
