---
name: task-annotation-check
description: >
  Flags task list files in docs/tasks/ where one or more task blocks lack a
  model-tier + risk routing annotation (the Model: field from
  references/task-sizing.md). Deterministic count comparison: task headers vs
  valid Model: lines. Traces to Eng Agentic P8.
category: hook
pack: engineering
trigger_event: commit
principles_implemented:
  - source: eng-agentic
    id: P8
    bucket: hook
  - source: eng-universal
    id: Rule A3
    bucket: embedded
length_target: 60–90
author: Anton Babushkin
predecessor:
  repo: none
  skill: none
  relation: new
kept_from_predecessor: n/a
changed_from_predecessor: n/a
---

# Task annotation check

## Purpose

The `Model:` routing annotation on each task is the durable planning-time record that routes a slice to the right model tier and review-attention level. Without it, the five-axis rubric from `references/task-sizing.md` may have been applied during `planning-and-task-breakdown` but leave no trace in the filed task list, making the routing invisible to the agent that picks up the work. Agents will silently omit the field when a template placeholder goes unfilled. Human reviewers miss it reliably across long task lists. This hook catches it mechanically: it counts task headers and valid `Model:` lines, compares the two, and fails the commit when they diverge. No prose interpretation is required.

## Trigger event

Fires on commit. Input: the set of files in the committed diff whose path matches `docs/tasks/*.md`. If no such file is in the diff, the hook exits silently.

## Check

For each `docs/tasks/*.md` file in the commit:

1. **Task-header count (H):** count lines matching the pattern `^### Task ` — each represents one task block.
2. **Annotation count (A):** count lines matching `Model:` AND containing `risk reversible` or `risk one-way` anywhere on the same line — each represents one filled annotation.

Compare: `A == H`.

The template placeholder (`[routing annotation per references/task-sizing.md — Fast|Balanced|Frontier · risk · review · axes]`) contains neither `risk reversible` nor `risk one-way`, so it does not count as a filled annotation. Unfilled templates fail.

Patterns:
- Task header: `^### Task `
- Valid annotation: `Model:.*risk (reversible|one-way)`

## Fail criteria

- **`A < H`** in any checked file: fewer valid annotations than task headers. Report: file path, H, A, and the task-header line numbers with no matching annotation.
- **`A > H`** in any checked file: more annotations than task headers — misplaced or duplicate annotation. Report: file path, H, A, and the extra annotation line numbers.

## Pass criteria

`A == H` for every `docs/tasks/*.md` file in the commit. Files where `H == 0` (no task headers yet) pass automatically.

## On fail

For each failing file:

1. List the task-header line numbers missing a valid `Model:` annotation.
2. Open `references/task-sizing.md` and score the five axes for each flagged task.
3. Add the annotation directly below the `**Done when:**` line using the format:
   `Model: <Fast|Balanced|Frontier> · risk <reversible|one-way> · review <standard|elevated> · axes RC·SC·HS·SR·OR = <L|M|H>·<L|M|H>·<L|M|H>·<L|M|H>·<L|M|H>`
4. Re-commit. The hook re-runs on the new commit.

Unfilled template placeholders must be replaced with a real scored annotation — they are not counted as present.

## Out of scope

- **Annotation correctness** — whether tier or axes are scored accurately. The hook checks presence, not scoring fidelity; that is a judgement call for `code-review-and-quality`.
- **Task files outside `docs/tasks/`** — only canonical task list locations are checked.
- **Axes vector and companions segment** — format completeness beyond tier name is not validated here.
- **Non-task `###` headings** — lines not matching `^### Task ` are not counted as task headers.

## References

- `references/task-sizing.md` — defines the `Model:` line format this hook enforces
- `skills/planning-and-task-breakdown/SKILL.md` — verification criterion 9 (every task has a Model: field)
- `rules/eng-principles-agentic.md` — P8 (effort is measured in slices and gates; annotation is the gate record)
- `rules/eng-principles-universal.md` — Rule A3 (every architecturally significant decision produces an ADR / durable record)
