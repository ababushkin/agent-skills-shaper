---
name: incremental-implementation
description: >
  Implement work in thin vertical slices, walking skeleton first, with a test-verify
  gate before each slice is committed. Use when implementation is ready to begin —
  whether that's a new feature, a significant change, or a KTLO bug fix. Trigger
  phrases: "let's build this", "start implementing", "code this up", "write the
  code for", "implement the", "let's start coding", "begin the implementation".
  Also use for bug fixes — no design doc required for KTLO path.
pack: engineering
lifecycle_stage: build
principles_implemented:
  - source: eng-universal
    id: P4
    bucket: embedded
  - source: eng-universal
    id: P5
    bucket: embedded
  - source: eng-universal
    id: P8
    bucket: standalone
  - source: eng-universal
    id: Rule B1
    bucket: embedded
  - source: eng-universal
    id: Rule B2
    bucket: standalone
  - source: eng-universal
    id: Rule B3
    bucket: embedded
  - source: eng-universal
    id: Rule C1
    bucket: embedded
  - source: eng-universal
    id: Rule C4
    bucket: embedded
  - source: eng-universal
    id: Rule C8
    bucket: embedded
  - source: eng-agentic
    id: P1
    bucket: embedded
  - source: eng-agentic
    id: P3
    bucket: embedded
  - source: eng-agentic
    id: P6
    bucket: embedded
length_target: 200-250
author: Anton Babushkin
predecessor:
  repo: https://github.com/addyosmani/agent-skills
  skill: incremental-implementation
  relation: derivative
kept_from_predecessor:
  - Slice-by-slice delivery discipline
  - Each increment independently verifiable
  - Test-implement-verify as the per-slice unit of work
changed_from_predecessor:
  - Walking skeleton is a mandatory first gate, not an optional recommendation
  - Failing build or test is a hard stop; agent must investigate before continuing
  - Accepted design doc is a required input; drift from it is an explicit failure mode
  - Per-slice open question surfacing is a named step
  - YAGNI (Rule B1) applied within each slice
  - KTLO bug fix sub-workflow added as a named path
---

# Incremental implementation

## Purpose

This skill takes an accepted design doc and builds it in thin vertical slices, starting with a walking skeleton. It is the operational form of Rule B2 (walking skeleton first) and Principle 8 (small batches beat big batches): the walking skeleton is a hard prerequisite for any feature slice, and each slice must be tested and verified before the next begins. The accepted design doc is the spec that holds the work throughout — drift from it is an explicit failure mode, not a stylistic concern (Agentic P3). When a failing build or test appears, work stops; the stop-the-line hook enforces this at the PR level (Agentic P6). The skill covers all implementation work: design-doc-backed features via Path 1, and KTLO bug fixes via Path 2.

## When to use

- Any implementation work backed by an accepted design doc — run Path 1.
- KTLO bug fixes with no design doc — run Path 2 (bug fix sub-workflow).
- Any size of implementation: walking skeleton discipline and per-slice verification are not optional for large projects only.

## When not to use

- **No accepted design doc and the work exceeds a Rule A1 trigger** — run `design-doc` first. A draft or in-review doc does not count as accepted.
- **The problem involves unresolved technical unknowns** — run a spike first, then return to `design-doc`, then here.
- **Work is already in progress without a walking skeleton** — this skill does not backfill mid-implementation. It governs from the start.

## Inputs

- Accepted design doc at `docs/design-docs/<name>/design-doc.md`
- Relevant ADRs referenced by the design doc
- `rules/eng-principles-universal.md` (Rules B1, B2, B3, C1, C4, C8)
- `rules/eng-principles-agentic.md` (P1, P3, P6)
- A working build environment

## Outputs

Code and commits — one commit for the walking skeleton, one commit per verified slice. No standalone artefact.

## Workflow

### Path 1 — Design-doc-backed implementation

**Step 1 — Context load [GATE]**

Load the accepted design doc, relevant ADRs, and this skill's referenced principles. Name each artefact loaded. If no accepted design doc exists — or if the doc's status is `draft` or `in-review` — stop. Run `design-doc` first and return here once the doc is accepted. Do not begin implementation against an unaccepted doc.

**Step 2 — Walking skeleton [GATE]**

Implement the minimal end-to-end path: one request wired through every real component in the real deployment environment. No feature logic yet. The skeleton is done when it deploys and the key path works end-to-end. Commit it.

Any estimate made before this point is uncalibrated. Revise scope and timeline after the skeleton is in — not before.

*Escape hatch:* If the implementation is a single function or method with no integration surface — touches no external system, no deployment, no shared interface — the skeleton may be degenerate: the function itself is the skeleton. State this explicitly rather than silently skipping the gate. The judgment criterion: would a failing integration surprise wreck this work? If no, the gate is trivially satisfied. If yes, build the skeleton. The default is: build it.

**Step 3 — Slice identification**

Break the remaining design doc scope into thin vertical slices. Each slice must deliver observable behaviour — something the system can do after the slice that it could not do before. Horizontal layers ("add all the database models") are not slices. Write the slice list. This becomes the per-slice checklist.

**Step 4 — Per-slice loop (repeat for each slice)**

a. Write the test(s) specifying this slice's acceptance criterion. Tests first (Rule C8).

b. Implement the minimum code that makes those tests pass. No speculative additions (Rule B1).

c. **[GATE]** Verify: tests green, CI green. If anything fails, stop. Investigate the root cause (Agentic P6). Do not continue to the next sub-step while CI is red.

d. Commit the slice. Each slice commit is short-lived; do not accumulate uncommitted slice work across sessions (Rule C1).

e. Surface any open questions raised by this slice. If the slice invalidates a design assumption, pause, document the question, and resolve it before continuing. Building past an invalidated assumption without surfacing it is a violation of Agentic P3.

**Step 5 — Completion check**

Verify all design doc requirements are covered. Confirm open questions are resolved or explicitly deferred with a named owner. Confirm fitness functions named in the design doc are passing. Flag any delta between the accepted design and what was built — do not silently reconcile them.

---

### Path 2 — Bug fix sub-workflow (KTLO; no design doc required)

This path covers all KTLO bug fixes. No design doc, no walking skeleton gate, no slice list.

**Step 1** — Write a failing test that reproduces the bug. The test is the spec.

**Step 2** — Fix the minimum code required to make the test pass (Rule B1).

**Step 3 [GATE]** — Verify: test green, CI green. If any other test broke, stop and investigate before continuing (Agentic P6; stop-the-line hook applies).

**Step 4** — Commit.

The TDD loop is the entire workflow. Do not extend Path 2 into Path 1 without writing a design doc.

## Artefact template

Not applicable. The skill's output is code and commits.

Optional: at Step 3 of Path 1, the implementer may record the slice list as a checklist in the design doc's open questions section or in a working notes file. This is not required but helps tracking on multi-day implementations.

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "We'll do the walking skeleton after we understand the codebase better." | Rule B2: pre-skeleton estimates are uncalibrated. The skeleton is how you understand the codebase — it flushes out the integration surprises that wreck schedules. Deferring it means deferring the only reliable source of ground truth. |
| "This slice is too big to split." | It is not a vertical slice; it is a horizontal layer (Rule B2: slices must deliver observable behaviour end-to-end). Break it into observable states: what can the system do after each step that it could not do before? If you cannot answer that question for a sub-piece, the boundary is wrong, not the approach. |
| "I'll write the tests after I understand the code better." | Rule C8: tests are specification of behaviour, not coverage. Writing them first forces you to define the acceptance criterion before implementing it. Tests written after describe what you built; they do not constrain what you should have built. |
| "The CI is failing but it's just a flaky test — I'll keep going." | Rule C4 and Agentic P6: flaky tests are bugs, not background noise. A failing build is a stop signal. Proceeding past it is the specific failure mode the stop-the-line hook guards against. Stop and fix the flaky test first. |
| "The design doc changed while I was implementing — I'll just go with what I have." | Agentic P3: the spec holds the work. If the accepted design doc has changed, or if your implementation has diverged from it, surface the delta explicitly, document it, and get it accepted. Silently building something different from the accepted doc is invisible scope drift. |

## Red flags

- Feature slices merged before a walking skeleton commit exists
- Slice produces no observable behaviour (implementation without a test boundary)
- Test added after implementation to match code that was already written
- CI red for more than one commit
- Build failure noted in a commit message as "known issue" and work continued
- Implementation references capabilities not in the accepted design doc with no change to the doc's status
- Path 2 (bug fix) used for work that would trigger a Rule A1 condition

## Verification / exit criteria

Path 1 is complete when:

- Walking skeleton commit exists and deployed before any feature slice began
- Each slice has a corresponding test written before implementation
- All tests green, CI green at every slice boundary
- All design doc requirements are covered or explicitly deferred
- Any delta between accepted design and what was built is documented

Path 2 is complete when:

- A failing test reproducing the bug exists before the fix
- Test is green, CI is green
- No other tests were broken by the fix (or breakage was investigated and resolved)

## References

- `rules/eng-principles-universal.md` — P4, P5, P8, Rule B1, B2, B3, C1, C4, C8
- `rules/eng-principles-agentic.md` — P1, P3, P6
- `hooks/stop-the-line/HOOK.md` — fires on PR open/update; catches signal-suppression moves (type suppressions, test skips, lint suppressions, deleted assertions) that agents reach for when a build or test is failing (Agentic P6)
- `skills/design-doc/SKILL.md` — required input for Path 1
- Cockburn, Alistair — walking skeleton (Rule B2 source)
- Humble & Farley — "Continuous Delivery" (small batches, trunk-based development)
- Reinertsen, Don — "Principles of Product Development Flow" (P8 source)
- Beck, Kent — "Tidy First" (P5 source; YAGNI via XP)
