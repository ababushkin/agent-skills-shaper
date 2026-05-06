---
name: backlog-manage
description: >
  Lifecycle skill for the idea bank. Use when the idea bank needs review or curation,
  a validation-slot item needs promoting or killing, KTLO items need tracking, or
  post-launch evidence needs feeding back into confidence scores.
  Trigger phrases: "review the backlog", "manage the idea bank", "clean up the backlog",
  "add to KTLO", "what's ready for roadmap?", "promote this idea", "kill this idea".
pack: product
lifecycle_stage: define
principles_implemented:
  - source: product
    id: A5
    bucket: embedded
  - source: product
    id: A6
    bucket: embedded
  - source: product
    id: B6
    bucket: embedded
  - source: product
    id: D1
    bucket: adjacent
  - source: product
    id: D2
    bucket: embedded
  - source: product
    id: D5
    bucket: embedded
length_target: 150–220
author: Anton Babushkin
predecessor:
  repo: none
  skill: none
  relation: new
kept_from_predecessor: "n/a"
changed_from_predecessor: "n/a"
---

# Backlog manage

## Purpose

backlog-manage is the maintenance skill for the idea bank. It reads the `## Routing` section of every triage record as the live status field, and updates it when items are promoted, killed, or have their confidence revised. It also maintains `docs/ktlo.md` as the trackable home for KTLO items that bypass triage under Rule A5.

Without this skill, the idea bank accumulates zombie records, validation slots never get closed, and roadmap-shape has no clean input to work from. The `roadmap-shape` skill reads from the idea bank expecting items marked ready — this skill is what maintains that marking.

## When to use

- Before running `roadmap-shape`, to clean the idea bank and surface what is genuinely ready.
- When a validation result arrives and a slot decision (promote or kill) must be recorded.
- When a KTLO item needs adding to `docs/ktlo.md`.
- When post-launch evidence should update a related item's confidence score (Rule D5).
- As a periodic check to surface stale items and flags, even if no action is taken.

## When not to use

- **Triaging a new incoming idea** → `idea-triage`
- **Building the roadmap from a cleaned idea bank** → `roadmap-shape` (run backlog-manage first)
- **Post-launch review of shipped work** → `post-launch-impact-review` (not yet authored); feeding evidence back into confidence uses this skill's `update-confidence` operation

## Inputs

- All files in `docs/idea-bank/*.md` (triage records produced by `idea-triage`)
- `docs/ktlo.md` (KTLO list — may not exist yet; create it on first `add-ktlo` operation)
- Optional: a slug and operation name for targeted updates vs. full review

## Outputs

- Updated triage records (`## Routing` section updated to reflect current status)
- Updated `docs/ktlo.md`
- Inline session summary (not filed — a snapshot, not a permanent artefact)

## Workflow

**Status convention.** The `## Routing` section of each triage record is the live status field. Allowed values are written as a comment on the last line of that section:

```
<!-- status: idea bank — ready for roadmap-shape -->
<!-- status: validation slot — [method] in progress -->
<!-- status: validation slot — [method] complete; confidence updated to X; promote or kill pending -->
<!-- status: killed — [YYYY-MM-DD] — [one-line reason] -->
<!-- status: on roadmap — [Now/Next/Later] — placed YYYY-MM-DD -->
```

When a record has no status comment, treat it as `validation slot — method in progress` and flag it.

---

**Step 1. Load the backlog.**
List all files in `docs/idea-bank/`. Read the `## Routing` section of each. Read `docs/ktlo.md` if it exists.

**Step 2. Produce current state summary.**
Group triage records by status:
- _On roadmap_: count + list with horizon (Now/Next/Later) and date placed
- _Idea bank (ready for roadmap-shape)_: count + list with ICE totals
- _Validation slot (active)_: count + list with method and age in days since file creation date
- _Validation slot (pending decision)_: flag explicitly — these need a promote or kill call
- _Killed_: count only

Also list open KTLO items (where Done = `—`).

**Step 3. [GATE] Identify session intent.**
One of:
- `review` — read-only audit; surface flags from Step 6 only
- `add-ktlo` — append one or more items to `docs/ktlo.md`
- `promote` — move a named validation-slot item to idea bank with updated evidence
- `kill` — mark a named item killed with documented reason
- `update-confidence` — revise confidence score on a named item with new evidence (Rule D5)
- `mark-placed` — record that `roadmap-shape` has placed a named item on the roadmap (horizon + date)

Do not proceed until intent is named. If the owner says "just check the backlog," that is `review`.

**Step 4. Execute the operation.**

- **add-ktlo**: Append row to the `docs/ktlo.md` table (item, date added, owner, done). Create the file from the artefact template if it does not yet exist.
- **promote**: Require: item slug, updated Confidence score, evidence that changed it, new ICE total. Update `## Routing` status comment to `idea bank — ready for roadmap-shape`. Update `## ICE score` and `## Evidence` sections with the new values.
- **kill**: Require: item slug and a one-line reason naming what evidence or circumstance drove the kill (Rule D2). Update `## Routing` status comment to `killed — [YYYY-MM-DD] — [reason]`.
- **update-confidence**: Revise `## Evidence` section with new evidence. Recalculate ICE. Update `## Routing` status if the new Confidence score crosses 5 in either direction.
- **mark-placed**: Require: item slug, horizon (Now/Next/Later), date placed. Update `## Routing` status comment to `on roadmap — [horizon] — placed YYYY-MM-DD`. This operation is normally called by `roadmap-shape` at the end of shaping, not manually.
- **review**: No writes. Output the summary from Step 2 plus all flags from Step 6.

**Step 5. [GATE] Confirm writes.**
Before modifying any file, state exactly what will change and in which file. Get explicit confirmation. Do not proceed until confirmed.

**Step 6. Surface flags (every session).**
Always report, regardless of intent:
- Validation slots with no status comment, or open > 30 days with no progress note
- Items marked "idea bank" with Confidence < 5 (miscategorised — should be in validation slot)
- Items marked "on roadmap" that do not appear in `docs/roadmap.md` (orphaned — either roadmap was edited without updating the idea bank, or the item was removed from the roadmap and needs a new status)
- KTLO list exceeding 10 open items (signals under-resourcing or scope stretch)
- Any triage record with no ICE score (incomplete triage — return to `idea-triage`)

## Artefact template

KTLO list at `docs/ktlo.md`:

```markdown
# KTLO backlog

| Item | Added | Owner | Done |
|------|-------|-------|------|
| <!-- description of the work --> | <!-- YYYY-MM-DD --> | <!-- name --> | — |
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "The validation slot has been open a while but we're still working on it." | A slot open > 30 days without a progress note is stale, not active. Document what is happening or kill it. |
| "I know this idea should be promoted — the confidence score doesn't need updating." | The whole point of promotion is to record why confidence changed. Skipping the evidence update breaks the Rule D5 feedback loop. |
| "This KTLO item is significant enough to need an outcome hypothesis." | If it needs outcome framing, it goes through `idea-triage`, not KTLO. Rule A5 is a carve-out, not a back door. |
| "Killing ideas feels negative. Let's just leave it in the bank." | Rule D2: killing is celebrated, not penalised. A graveyard of honestly killed ideas is a sign the system works. A bank full of zombie ideas is a sign it does not. |
| "I can tell roadmap-shape which items are ready without updating the status comment." | The status comment is the contract between this skill and roadmap-shape. Verbal overrides break the feedback loop for the next session. |

## Red flags

- `## Routing` says "idea bank" but Confidence score is below 5
- Validation slot open > 30 days with no update and no flag raised
- A `promote` operation is run without new evidence being named
- KTLO list contains items with outcome hypotheses or ICE scores
- Any write executed without the Step 5 confirmation gate

## Verification / exit criteria

The skill has run correctly when:

1. Every file in `docs/idea-bank/` has a `## Routing` section with a valid status comment in one of the five allowed forms.
2. Every `promote` operation records an updated Confidence score and names the evidence that changed it.
3. Every `kill` operation records a date and a one-line reason.
4. `docs/ktlo.md` exists and follows the table format if any KTLO items have been added.
5. All flags from Step 6 are surfaced in the session summary, even if no action is taken on them.

## References

- `rules/PRODUCT_RULES.md` — A5 (KTLO carve-out), A6 (no parking lot), B6 (validation slot lifecycle), D2 (killing is normal), D5 (learning fed back to idea bank)
- `references/confidence-meter.md` — Gilad's scale for evidence quality scoring
- `references/ice-scoring.md` — ICE = Impact × Confidence × Ease mechanics
