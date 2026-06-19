---
name: exec:breakdown
description: >
  Break a picked-up Linear issue into an ordered task list where every task carries one
  verifiable `done_when` clause and routing. Two paths: ingest delivery's task block
  verbatim when present, or derive from AC with 5-axis routing when not. Use immediately
  after `exec:pickup` and before `exec:build`. Trigger phrases: "break this issue down",
  "task breakdown", "exec:breakdown", "size and route the tasks", "turn this AC into tasks".
---

# Exec: breakdown

## Purpose

Turn the picked-up issue into the ordered task list that `exec:build` will drain. Two paths, selected on `pickup.has_plan_tasks`:

- **Ingest** (`has_plan_tasks: true`): copy each `plan_tasks[]` entry verbatim — `done_when` and `Model:` annotation come straight from delivery. Do not re-score, do not re-route.
- **Derive** (`has_plan_tasks: false`): draft tasks from `ac_checklist`, apply the 5-axis rubric from `references/task-sizing.md`, sequence by dependency.

Both paths run through the same verify gate before writing. One invariant holds on either path: every task carries exactly one verifiable `done_when` clause, traceable to at least one AC item.

## When to use

- Immediately after `exec:pickup` has written the `pickup` section of `exec-state.json` and before `exec:build` is invoked.
- An issue is in hand with a non-empty `ac_checklist` and a body describing the work — whether or not it carries a delivery task block.
- The issue is a build node — story, ktlo, fix, or refactor. Untracked node types (design-doc, spike, adr, experiment) are filtered out at pickup; they reach this skill only by accident.

## Do not use when

- **The issue has no AC** — halt at `exec:pickup`; without acceptance criteria there is nothing to make verifiable. Use `delivery` to add the Completion section first.
- **Shaping or design work** — use `shape:design` or `delivery` for that decomposition. This skill assumes the build shape is committed.
- **Free-standing diff review or AC verification** — use `exec:review` or `exec:verify`; this skill produces a plan, not a verdict.

## Inputs

- **`exec-state.json` path** — the worktree-root handoff carrier. The `pickup` section must exist with `body_md`, a non-empty `ac_checklist`, `has_plan_tasks`, and `plan_tasks[]`.
- **`references/task-sizing.md`** — the 5-axis rubric (RC·SC·HS·SR·OR). Used on the derive path only; the ingest path copies routing verbatim.

## Outputs

- The `breakdown` section of `exec-state.json`, append-only — prior sections survive:

```json
{
  "breakdown": {
    "tasks": [
      {
        "id": "T1",
        "title": "<observable outcome>",
        "done_when": "<one verifiable clause>",
        "ac_refs": ["<verbatim AC item served by this task>"],
        "model_tier": "Fast | Balanced | Frontier",
        "review_flag": "standard | elevated",
        "axes": { "RC": "L", "SC": "L", "HS": "L", "SR": "L", "OR": "L" },
        "blocks_on": []
      }
    ]
  }
}
```

- On failure: halt with a structured reason (no AC, AC item with no task, task with no `done_when`, task with multiple criteria). Do not write a partial `breakdown` section.

## Workflow

### 1. Gate: read the pickup section

Open `exec-state.json` and load the `pickup` section. Confirm `body_md` is non-empty and `ac_checklist[]` contains at least one item. If either is missing, halt.

### 2. Route on `has_plan_tasks`

If `pickup.has_plan_tasks` is `true`, follow the **Ingest path** (steps 3–5). If `false`, follow the **Derive path** (steps 6–10). Both paths converge at the shared verify gate (step 11).

---

### Ingest path — `has_plan_tasks: true`

### 3. Parse each plan task

For each line in `pickup.plan_tasks[]`, extract:

- `title` — the task description (text before `Done when:`)
- `done_when` — the clause after `Done when:`, **verbatim**
- `model_tier`, `review_flag`, `axes` — from the `Model:` annotation, **verbatim**
- `blocks_on` — any `blocks_on:` clause, or `[]` if absent

Do not re-score and do not re-route. Delivery's routing is authoritative. If a line lacks `Done when:` or `Model:`, halt — the plan task is malformed.

### 4. Map each task to `ac_refs`

Map each parsed task to at least one item in `pickup.ac_checklist`. Record the verbatim AC text in `ac_refs`. A task with no mapping is scope drift — halt; do not invent an AC item.

### 5. Preserve order

`tasks[]` follows `pickup.plan_tasks[]` order. Dependency order is already encoded in the plan; do not re-sequence.

---

### Derive path — `has_plan_tasks: false`

### 6. Gate: every AC item maps to at least one task

Walk the `ac_checklist` and draft one or more tasks per AC item. Two checks must hold and are re-enforced at step 11:

- Every AC item is served by at least one task — record the verbatim AC text in the task's `ac_refs`.
- Every task serves at least one AC item.

An AC item with no task is unplanned coverage. A task with no AC item is scope drift; delete it, do not keep it "in case we want it later."

### 7. Gate: one `done_when` per task

Every task carries exactly one `done_when` clause describing a verifiable result — a file at a path, a command exit code, a function returning a value, a UI assertion. The clause must be observable, not procedural: *"`bin/parse fixtures/sample.json` exits 0"* is observable; *"I implement the parser"* is not. If a single sentence cannot capture the result, split the task — each half gets its own `done_when`. A clause that names two unrelated checks is a hidden multi-task bundle.

### 8. Choose the first task

The first task exercises the riskiest seam, not the easiest one. Read the issue body for the named risk locus — integration, core logic, schema — and pick accordingly:

- If the issue touches an external boundary (third-party API, cross-service call, schema migration), the first task is a thin skeleton through that boundary.
- If the risk is internal logic, the first task is the smallest probe of that logic.
- For pure-fix issues, the first task is the failing repro the fix will turn green.

Fold any toolchain or environment prerequisite into the first task — do not file a separate "setup" task before it.

### 9. Sequence by dependency

Order remaining tasks by dependency, not by perceived difficulty. Each later task must extend a prior one in one direction and be independently verifiable on its own `done_when`. Flag external blockers inline as `blocks_on: ["<dependency>"]` — a third-party credential, a cross-team merge, a shared-infrastructure change. A `blocks_on` entry that names something inside this issue is not an external blocker; resolve it by reordering instead.

### 10. Gate: route each task

For every task, apply the 5-axis rubric in `references/task-sizing.md`. Score `RC` (reasoning complexity), `SC` (specification completeness, *inverted* — fully specified is Low pressure), `HS` (hallucination sensitivity), `SR` (stakes / reversibility), and `OR` (orchestration role) as L/M/H. Derive:

- `model_tier` from the routing rule — stakes sets the floor, capability axes lift it, orchestrator role pins Frontier.
- `review_flag` — `elevated` when `SR = High` or `HS = High`; otherwise `standard`.

Do not invent a sixth axis. Do not score "effort" — this rubric is risk-weighted routing, not estimation (see `references/task-sizing.md` *"What this is not for"*).

---

### 11. Gate: verify the manifest (shared — both paths)

Before writing, run these checks. Any failure halts the skill; do not emit a partial section.

- Every task has `id`, `title`, `done_when`, `ac_refs`, `model_tier`, `review_flag`, `axes`.
- Every `ac_refs` entry matches a `pickup.ac_checklist` item verbatim.
- Every entry in `pickup.ac_checklist` appears in at least one task's `ac_refs`.
- Task IDs are unique and ordered `T1, T2, …`.
- No task carries more than one `done_when`.

### 12. Write the breakdown section

Open `exec-state.json`, set the `breakdown` key (preserving any prior sections), and write the file back. The `tasks` array is ordered — this is the order `exec:build` will pick them up in.

## Artefact template

The on-disk artefact is the `breakdown` section of `exec-state.json`:

```json
{
  "breakdown": {
    "tasks": [
      {
        "id": "T1",
        "title": "Skeleton through the parser boundary",
        "done_when": "bin/parse fixtures/sample.json exits 0",
        "ac_refs": ["The CLI accepts a JSON file path and exits 0 on valid input."],
        "model_tier": "Balanced",
        "review_flag": "standard",
        "axes": { "RC": "M", "SC": "M", "HS": "L", "SR": "L", "OR": "L" },
        "blocks_on": []
      },
      {
        "id": "T2",
        "title": "Reject malformed input with a structured error",
        "done_when": "bin/parse fixtures/malformed.json exits non-zero with a JSON error envelope",
        "ac_refs": ["Malformed input produces a structured error, not a stack trace."],
        "model_tier": "Balanced",
        "review_flag": "standard",
        "axes": { "RC": "M", "SC": "L", "HS": "L", "SR": "L", "OR": "L" },
        "blocks_on": []
      }
    ]
  }
}
```

## Red flags

- A task carries no `done_when`, or its `done_when` describes work ("implement the helper") rather than a result.
- A `done_when` clause is two clauses joined by "and" — a hidden multi-task.
- An AC item from `pickup.ac_checklist` is not referenced by any task's `ac_refs`.
- A task's `ac_refs` is empty, or contains AC text not verbatim from the pickup section.
- An ingested task's `model_tier`, `review_flag`, or `axes` differ from the delivery annotation — ingest copies verbatim; any difference is a re-score.
- The first derive-path task is setup or scaffolding instead of the riskiest seam.
- `model_tier` set by intuition on the derive path instead of derived from the 5-axis score.
- A `breakdown` section was written while any step-11 check failed.
- The `pickup` section was edited to "make the breakdown easier" — the pickup contract is immutable.

## Exit criteria

- `exec-state.json` contains a `breakdown.tasks` array of at least one task, in dependency order.
- Every task has `id`, `done_when` (one verifiable clause), `model_tier`, `axes`, and `ac_refs`.
- Every AC item from `pickup.ac_checklist` is covered by at least one task.
- On the ingest path: every task's `model_tier`, `review_flag`, and `axes` match the delivery annotation verbatim.
- On the derive path: every `model_tier` and `review_flag` is derived from a recorded axis score, not freely chosen.
- On any structural failure, the skill halted rather than emitting a partial section.

## Related

- `skills/exec-pickup/SKILL.md` — `exec:pickup` (writes the `pickup` section consumed here, including `plan_tasks` and `has_plan_tasks`).
- `skills/exec-build/SKILL.md` — `exec:build` (consumes the `breakdown.tasks` array, slice by slice).
- `skills/delivery/SKILL.md` — `delivery` (the planning-time decomposition whose task block the ingest path copies verbatim).
- `references/task-sizing.md` — the 5-axis routing rubric used on the derive path.
