---
name: verify-implementation
description: >
  Outcome verifier — reads the ticket AC checklist (from Task Shaper output or raw ticket body)
  and the working-tree diff, then produces a structured pass/fail verdict with one finding per
  unmet AC item. Use after an implementation is claimed complete and before an issue is
  transitioned to Done. A fail verdict halts progression; a pass verdict records that AC was
  observed met, not merely assumed. Trigger phrases: "verify this is done",
  "check the implementation against AC", "is this ready to close", "did the diff satisfy the
  ticket", "run the outcome verifier", "verify implementation", "check AC before marking Done".
pack: engineering
lifecycle_stage: verify
principles_implemented:
  - source: eng-agentic
    id: P3
    bucket: embedded
  - source: eng-agentic
    id: P4
    bucket: embedded
  - source: eng-agentic
    id: P6
    bucket: embedded
  - source: eng-universal
    id: P1
    bucket: embedded
  - source: eng-universal
    id: Rule D2
    bucket: adapted
length_target: 180–250
author: Anton Babushkin
predecessor:
  repo: none
  skill: none
  relation: new
kept_from_predecessor: "n/a"
changed_from_predecessor: "n/a"
---

# Verify implementation

## Purpose

verify-implementation is the brake on silent Done. It exists because agentic P4 says evidence
beats vibes, and "the diff looks right" is vibes. The skill forces a structured mapping of every
AC item in the ticket against observable diff evidence — a named file, a changed block, a new
function — and emits a binary verdict: pass (all AC met) or fail (at least one AC unmet, with
one finding per gap). A pass verdict is a record that a structured check was done; a fail verdict
is a halt signal with named gaps the implementer must address before Done.

The skill is the mechanical form of agentic P6 (stop the line): a fail verdict is not a
suggestion. It blocks the issue from transitioning to Done until each finding is resolved or
explicitly accepted by the operator with a written reason. Without a verdict in the run log,
KR2 (zero silent Dones) cannot be satisfied mechanically.

The skill errs toward **precision over recall**. Only call an AC item unmet when there is a
specific, nameable gap. If the diff could plausibly satisfy a criterion — even partially — do
not fabricate a finding. False positives (fail on AC that is actually met) are the failure
mode to avoid.

## When to use

- An implementation is claimed complete and the issue is about to transition to Done.
- A diff exists — working-tree diff, PR diff, or a commit range — and the ticket has AC.
- You are the operator walking a completion sequence and the sequence requires a verdict before
  marking Done (the most common case).

A single trigger is sufficient.

## When not to use

- **No diff exists yet** — implementation is not done. There is nothing to verify. Do not
  synthesise a verdict from partial work; use `planning-and-task-breakdown` to identify what
  remains.
- **Ticket has no AC** — the skill cannot check what was never specified. Halt, name the gap,
  and ask the operator to add Completion criteria to the ticket before running verification.
- **KTLO work with no Completion section** — delivery-shape marks ktlo nodes with
  `completion: none (roadmap A5 carve-out)`. If the ticket explicitly carries that carve-out,
  this skill is inapplicable.
- **Re-verifying after a fix** — run again from scratch; do not re-use a prior verdict.

## Inputs

1. **AC list** (required) — The Task Shaper Completion section of the issue (`## Completion`,
   `Done when:` list) or, if absent, any bullet list under a heading containing "acceptance
   criteria", "AC", "done when", or "definition of done" in the raw ticket body. Without an
   AC list, the verdict is `fail` with a single structural finding.
2. **Diff** (required) — The working-tree diff (`git diff HEAD`), a PR diff, or a commit range.
   An empty diff means the implementation is absent.
3. **Run log entry** (optional) — If the issue has an active run-log entry, the emitted verdict
   is appended to its `outcome_verdict` field. If absent, the verdict is emitted standalone.

## Outputs

A verdict object as a fenced JSON block in the conversation, conforming to the `outcome_verdict`
schema (see Artefact template). If the verdict is `fail`, the conversation also carries a
human-readable summary of findings for the operator.

## Workflow

**1. Extract the AC list.**
Read the ticket. Prefer the Task Shaper Completion section (`## Completion` with `Done when:`
items). If absent, fall back to any heading containing "acceptance criteria", "AC", "done when",
or "definition of done" and extract its bullet items verbatim.

If no AC list is found, do not proceed further. Emit a `fail` verdict with one finding:
```
ac_item: "(none found)"
gap: "No AC checklist located in ticket body — cannot verify without criteria."
evidence: "absent"
```
Return the verdict and stop. Do not invent AC items to continue.

**2. Read the diff.**
Load the diff supplied by the operator (or run `git diff HEAD` against the working tree). If
the diff is empty, emit a `fail` verdict with one finding:
```
ac_item: "(all items)"
gap: "Diff is empty — no implementation changes present."
evidence: "absent"
```
Return the verdict and stop.

**3. [GATE] Map each AC item to diff evidence.**
For each AC item, examine the diff for observable evidence that the item is satisfied.
Evidence must be concrete: a file path with changed lines, a new file, a removed block, a
configuration update, a test name. "The PR looks complete" is not evidence.

Precision rule: only mark an item unmet when there is a specific, nameable absence — a
capability the AC requires that does not appear anywhere in the diff. If the diff changes a
file that plausibly satisfies the criterion, mark the item met. Reserve `fail` for the cases
where the diff is clearly insufficient.

**4. Collect findings.**
For each AC item that lacks concrete diff evidence, create one finding:
- `ac_item` — the verbatim AC text.
- `gap` — a one-sentence description of what the diff does not provide.
- `evidence` — a specific diff reference (file path, line range) or `"absent"` if the change
  is entirely missing.

**5. [GATE] Compute verdict.**
- `findings` is empty → `result: "pass"`.
- `findings` is non-empty → `result: "fail"`.

There is no partial-pass state. Every unmet AC item becomes a finding; every finding
contributes to a fail verdict. The operator may accept a finding explicitly (with a written
reason and issue comment), but the verdict itself does not carry a "pass with caveats" mode.

**6. Emit the verdict.**
Write the verdict as a fenced JSON block in the conversation (see Artefact template).
Set `invoked_at` to the current ISO 8601 timestamp. If a run log entry was provided, note
that the `outcome_verdict` field should be updated with this object.

On `fail`: follow the verdict block with a human-readable bullet list of findings for the
operator.

## Artefact template

The verdict object. A pass verdict has `"findings": []`.

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

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "I can see the diff satisfies the AC — I don't need to run this." | That is vibes. Agentic P4: evidence beats vibes. The verdict is a record that a structured check was done, not an assertion that the reviewer is confident. Run the skill. |
| "The AC is vague — I'll interpret it charitably as met." | Charitable interpretation toward pass is the false-negative failure mode this skill exists to prevent. If an AC item is genuinely ambiguous, emit a finding naming the ambiguity. AC vagueness is the ticket author's problem, not the verifier's. |
| "The tests pass, so all AC is satisfied." | Tests passing covers only AC items that are testable by the test suite. A skill registration requirement, a doc section, or a command file is not covered by tests. Check each item independently against the diff. |
| "This is a docs-only change — there is no real AC." | If the ticket has AC, run the skill. If it has no AC, halt and ask for criteria. There is no bypass for "it's just docs." |
| "One finding is minor — I'll call it pass and note the gap in a comment." | The pass/fail boundary is binary. A finding is a finding. Notes and caveats belong in issue comments; the verdict does not carry partial-pass state. A fail verdict with one minor finding is still a fail verdict. |
| "I already reviewed the diff informally — I'm confident." | Confidence is not evidence. The skill forces itemised coverage of every AC item; an informal review does not. The record that a structured check was done is the deliverable, not the conclusion. |

## Red flags

- A pass verdict is emitted without any diff evidence named for any AC item.
- AC items are reworded or summarised instead of quoted verbatim in findings.
- A fail verdict was downgraded to pass by reinterpreting an AC item to fit the diff.
- The `invoked_at` field is absent or contains a placeholder.
- The `gap` field in a finding is vague ("doesn't seem complete") rather than specific.
- The skill was skipped because the implementer "felt confident" the AC was met.
- The verdict was re-used from a prior run without re-reading the current diff.

## Verification / exit criteria

The skill has run correctly when:

1. The AC list was extracted verbatim from the ticket (Task Shaper output preferred, raw ticket
   fallback). If no AC was found, a structural fail verdict was emitted and the skill stopped.
2. Every AC item was checked against the diff; no item was skipped.
3. The verdict JSON is valid and conforms to the schema: `result`, `invoked_at`, `findings`.
4. A pass verdict has `"findings": []`.
5. A fail verdict has one finding per unmet AC item; each finding carries `ac_item`, `gap`, and
   `evidence`.
6. The verdict is emitted in the conversation as a fenced JSON block.
7. On fail: a human-readable bullet list of findings follows the JSON block.
8. If a run log entry was provided, the verdict object is noted for appending to
   `outcome_verdict`.

## References

- `rules/eng-principles-agentic.md` — P3 (spec as seatbelt), P4 (evidence beats vibes),
  P6 (stop the line on first failure)
- `rules/eng-principles-universal.md` — P1 (shipped ≠ done; observed = done), Rule D2
  (post-implementation review — adapted: the verification step is the review)
- `skills/delivery-shape/SKILL.md` — produces the Task Shaper Completion section
  (`Done when:` list) this skill reads as its preferred AC source
- `skills/planning-and-task-breakdown/SKILL.md` — produces the issue AC checklist this skill
  verifies against when the delivery-shape Completion section is unavailable
