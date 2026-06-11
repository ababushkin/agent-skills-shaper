---
name: verify-implementation
description: Outcome verifier — reads the ticket AC checklist and the working-tree diff, then produces a structured pass/fail verdict with one finding per unmet AC item. Use after an implementation is claimed complete and before an issue is transitioned to Done. Trigger phrases: "verify this is done", "check the implementation against AC", "is this ready to close", "did the diff satisfy the ticket", "run the outcome verifier", "verify implementation", "check AC before marking Done".
---

# Verify implementation

## Purpose

Map every AC item in a ticket against observable diff evidence — a named file, a changed block, a new function — and emit a binary verdict: pass (all AC met) or fail (at least one unmet, one finding per gap).

A fail verdict is a halt, not a suggestion: the issue does not transition to Done until each finding is resolved or explicitly accepted by the operator with a written reason. Err toward precision over recall — only call an item unmet when there is a specific, nameable gap. A false fail on AC that is actually met is the failure mode to avoid.

## When to use

- An implementation is claimed complete and the issue is about to transition to Done.
- A diff exists — working-tree, PR, or commit range — and the ticket has AC.
- You are walking a completion sequence that requires a verdict before Done.

## Do not use when

- No diff exists yet — there is nothing to verify. Use planning-and-task-breakdown to identify what remains.
- The ticket has no AC — halt, name the gap, and ask the operator to add Completion criteria first.
- KTLO work carrying `completion: none (roadmap A5 carve-out)` — the skill is inapplicable.
- Re-verifying after a fix — run from scratch; do not re-use a prior verdict.

## Inputs

1. **AC list** (required) — the delivery-shape Completion section (`## Completion`, `Done when:` list) or, if absent, any bullet list under a heading containing "acceptance criteria", "AC", "done when", or "definition of done". No AC list → a structural fail verdict.
2. **Diff** (required) — `git diff HEAD`, a PR diff, or a commit range. An empty diff means the implementation is absent.
3. **Run log entry** (optional) — if present, the verdict is appended to its `outcome_verdict` field; otherwise emitted standalone.

## Outputs

A verdict object as a fenced JSON block in the conversation:

```json
{
  "result": "pass | fail",
  "invoked_at": "<ISO 8601 timestamp>",
  "findings": [
    {
      "ac_item": "<verbatim AC item text>",
      "gap": "<one-sentence description of what the diff does not provide>",
      "evidence": "<diff file path and line range, or 'absent'>"
    }
  ]
}
```

A pass verdict has `"findings": []`. On fail, a human-readable bullet list of findings follows the block.

## Workflow

### 1. Extract the AC list

Read the ticket. Prefer the delivery-shape Completion section. If absent, fall back to any heading containing "acceptance criteria", "AC", "done when", or "definition of done" and extract its bullet items verbatim.

If no AC list is found, stop and emit a fail verdict with one finding. Do not invent AC items to continue.

```
ac_item: "(none found)"
gap: "No AC checklist located in ticket body — cannot verify without criteria."
evidence: "absent"
```

### 2. Read the diff

Load the supplied diff, or run `git diff HEAD`. If the diff is empty, stop and emit a fail verdict with one finding:

```
ac_item: "(all items)"
gap: "Diff is empty — no implementation changes present."
evidence: "absent"
```

### 3. Gate: map each AC item to diff evidence

For each AC item, find concrete evidence in the diff: a file path with changed lines, a new file, a removed block, a configuration update, a test name. "The PR looks complete" is not evidence.

Only mark an item unmet when there is a specific, nameable absence — a required capability that appears nowhere in the diff. If a changed file plausibly satisfies the criterion, mark it met. Reserve fail for diffs that are clearly insufficient.

### 4. Collect findings

For each AC item lacking concrete evidence, create one finding with `ac_item` (verbatim AC text), `gap` (one sentence on what is missing), and `evidence` (a specific diff reference, or `"absent"`).

### 5. Gate: compute verdict

- `findings` empty → `result: "pass"`.
- `findings` non-empty → `result: "fail"`.

There is no partial-pass state. Every unmet AC item is a finding; every finding makes the verdict fail. The operator may accept a finding explicitly with a written reason and issue comment, but the verdict itself carries no "pass with caveats" mode.

### 6. Emit the verdict

Write the verdict as a fenced JSON block. Set `invoked_at` to the current ISO 8601 timestamp. If a run log entry was provided, note that its `outcome_verdict` field should be updated with this object. On fail, follow with the human-readable findings list.

## Red flags

- A pass verdict with no diff evidence named for any AC item.
- AC items reworded or summarised instead of quoted verbatim in findings.
- A fail downgraded to pass by reinterpreting an AC item to fit the diff.
- `invoked_at` absent or a placeholder.
- A `gap` field that is vague ("doesn't seem complete") rather than specific.
- The skill skipped because the implementer "felt confident".
- A verdict re-used from a prior run without re-reading the current diff.

## Exit criteria

The skill is complete when:

1. The AC list was extracted verbatim (delivery-shape Completion preferred, raw ticket fallback); a missing AC produced a structural fail and a stop.
2. Every AC item was checked against the diff; none skipped.
3. The verdict JSON is valid: `result`, `invoked_at`, `findings`.
4. A pass verdict has `"findings": []`.
5. A fail verdict has one finding per unmet AC item, each with `ac_item`, `gap`, `evidence`.
6. The verdict was emitted as a fenced JSON block; on fail, a findings list followed.
7. If a run log entry was provided, the verdict was noted for appending to `outcome_verdict`.

## Related

- delivery-shape: produces the Completion section (`Done when:` list) this skill reads as its preferred AC source.
- planning-and-task-breakdown: produces the AC checklist this skill verifies against when no delivery-shape Completion section exists.
