---
name: file-delivery-plan-to-linear
description: 'File a delivery plan into Linear — create the project, its milestones, and one issue per node, with every field (title, milestone, labels, blocked_by) derived by plan-to-linear-manifest so nothing is hand-picked or dropped. Use after shape-delivery emits a plan and you want it in Linear. Trigger phrases: "file the delivery plan into Linear", "file this plan into Linear", "create the Linear issues from the plan", "put the delivery plan in Linear".'
---

# File delivery plan to Linear

## Purpose

Take a delivery plan that has passed its gates and file it into Linear: create the project, every milestone, and one issue per node the plan defines. Each issue's fields — title, milestone, labels, and `blocked_by` — are **derived by `bin/plan-to-linear-manifest`, not by hand**, so the filing reproduces the plan exactly. The skill then reads the project back and diffs it against the manifest to prove the whole plan landed.

Deriving the fields is what makes the filing reliable. Hand-filing a plan once dropped every `skeleton`/`acceptance`, `model`, and `repo` label, because the labels were copied by hand from a source that never listed them. The helper now derives every field, so that class of error is gone — labels included.

The skill is thin on purpose: all derivation lives in the script. The agent's only job is the tracker work a script can't do — create through the MCP, resolve `blocked_by` node-ids to the issue identifiers Linear assigns, and verify the result.

## When to use

- A delivery-plan file-set exists, passes `bin/walk-delivery-plan` and `bin/check-plan-framing`, and you want it in Linear.
- The plan is full-tier (has `D<n>-*/` deliverable directories), so it has milestones.
- The operator asks to file, create, or push a delivery plan into Linear.

## Do not use when

- The plan has not passed its gates — run `shape:delivery`'s Step 9 gates first.
- The plan is lite-tier (flat `N<nn>-*.md` nodes, no deliverables): it has no milestones to file. Create the issues directly from the node files instead.
- You only need a manifest, not the Linear writes — run `bin/plan-to-linear-manifest` on its own.

## Inputs

- Plan directory path (the file-set root).
- The repo label, passed to the helper as `--repo <repo>`.
- `.linear_config` at the repo root, for `team` (required) and `ops_project`.
- Optional `--project` / `--project-description` overrides if the README-derived name or description is not what you want in Linear.

## Outputs

A filing verdict. Report it after the finish-gate passes:

```json
{
  "project": "<project name>",
  "created": { "milestones": 3, "issues": 8 },
  "verify": "pass",
  "issues": [
    { "node": "N01", "identifier": "ABA-421", "title": "N01 — Eval scorer", "labels": ["skeleton", "high", "opus", "agent-skills-shaper"], "blocked_by": [] }
  ],
  "mismatches": []
}
```

A non-empty `mismatches` array means the finish-gate failed — the filing is wrong, not done.

## Workflow

### 1. Restate the filing

Write one sentence:

```text
Filing <plan-dir> into Linear as project "<name>" — <n> milestones, <n> issues.
```

### 2. Gate: derive the manifest

Read `.linear_config` for `team`. Then run the helper and capture its JSON:

```bash
bin/plan-to-linear-manifest <plan-dir> --repo <repo>
```

If it exits non-zero, stop. A non-zero exit means a field could not be derived — the plan is malformed, not the filing. Fix the plan and re-run; do not hand-pick the missing value.

Every field you write below comes from this manifest. Do not add, drop, or edit a value by hand at any later step — deriving a field by hand is the exact failure this skill removes.

### 3. Ensure the derived labels exist

Collect the distinct label names across all `issues[].labels`. For each, confirm it exists with `mcp__claude_ai_Linear__list_issue_labels`; create any missing one with `mcp__claude_ai_Linear__create_issue_label`. The `model` (`opus`/`sonnet`/`haiku`) and `repo` labels usually already exist; a new repo's label may not.

### 4. Create the project

Create it with `mcp__claude_ai_Linear__save_project`:

- `name`: `manifest.project.name`
- `description`: `manifest.project.description`
- `state`: `"planned"`
- `addTeams`: `["<team from .linear_config>"]`

### 5. Create the milestones

For each entry in `manifest.milestones`, in order, call `mcp__claude_ai_Linear__save_milestone` with `project` set to the project from step 4 and `name` set to `milestone.name` verbatim (already composed as `D<n> — <title> (<KR>)`).

### 6. Create the issues

For each entry in `manifest.issues`, in manifest order, call `mcp__claude_ai_Linear__save_issue`:

- `title`: `issue.title` verbatim
- `team`: from `.linear_config`
- `project`: the project from step 4
- `milestone`: the milestone named by `issue.milestone`'s entry in `manifest.milestones`
- `labels`: `issue.labels` **verbatim** — the whole array, unedited
- `description`: the node body read from `issue.body_path` (strip the front-matter fence)
- `state`: `"Backlog"`

Record each node-id → returned Linear identifier in a map. Do **not** set `blockedBy` yet — the blockers may not exist until every issue is created.

### 7. Resolve and wire `blocked_by`

For each issue with a non-empty `blocked_by`, map each node-id to its Linear identifier from step 6, then call `mcp__claude_ai_Linear__save_issue` with `id` set to the issue and `blockedBy` set to the resolved identifiers. If any node-id has no entry in the map, stop — the manifest references a node that was not created.

### 8. Gate: read back and diff

Read the project back and prove it matches the manifest. First check coverage: every `manifest.issues[].id` maps to exactly one created Linear identifier, and no extra issue was created (one node → one issue). Then, for each created issue, `mcp__claude_ai_Linear__get_issue` and compare:

- **Title** — the issue's title equals `issue.title`.
- **Milestone** — the issue's milestone matches `issue.milestone`.
- **Labels** — the issue's label set equals `issue.labels` as a set. Any added, missing, or altered label is a mismatch.
- **blocked_by** — the resolved blockers match.

Then compare counts: milestones created equals `len(manifest.milestones)`, issues created equals `len(manifest.issues)`.

Record every divergence in `mismatches`. If `mismatches` is non-empty, report the failure and stop — do not declare the filing done. Any divergence here means the plan did not file faithfully.

### 9. Report

Emit the verdict from **Outputs**. On `verify: "pass"` with empty `mismatches`, the plan is filed.

## Artefact template

The verdict is the only artefact. Its shape is the JSON block in **Outputs**: `project`, `created` counts, `verify` (`pass` | `fail`), the per-issue `node`/`identifier`/`title`/`labels`/`blocked_by` rows, and a `mismatches` array that is empty only when the finish-gate passes.

## Red flags

- An issue or milestone the plan defines is missing, or an extra one was created — the filing is not one-to-one with the plan.
- An issue is filed under the wrong milestone, or its title does not match the manifest.
- A label is added, dropped, or edited at any step after the manifest — derivation must stay in the script.
- `blockedBy` is set in step 6 (before all issues exist) instead of the step 7 second pass.
- The verdict reports `pass` while `mismatches` is non-empty, or the finish-gate was skipped so a divergence would go unnoticed.
- The helper exited non-zero and a field was hand-supplied to proceed anyway.

## Exit criteria

The skill is complete when:

- The project, every milestone, and one issue per node exist in Linear and match the manifest one-to-one.
- `bin/plan-to-linear-manifest` exited 0 and its manifest drove every write.
- Each issue carries its manifest title, milestone, and labels verbatim — no more, no fewer.
- Every `blocked_by` is wired to the right Linear identifiers.
- The finish-gate diff returned `verify: "pass"` with empty `mismatches`.

## Related

- `shape:delivery` — emits the plan file-set this skill files; its Step 9 gates must pass first.
- `bin/plan-to-linear-manifest` — derives the filing manifest (project, milestones, issues, labels, blocked_by).
- `bin/walk-delivery-plan` — the gate the manifest helper shares its parser with.
- `.linear_config` — supplies `team` and `ops_project`.
