---
layer: node
id: N04
type: story
title: Supervisor records verdicts on every exit
parent: D2
serves_kr: KR2
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    The orchestrator populates flow, outcome_verdict, and prep_verdict from the
    handoff on every exit path (Done, halted, errored), halted entries carry
    halt_reason, and the KR2 schema check distinguishes inspectable from
    uninspectable entries — pytest green.
delegates_to: at-pickup task breakdown (story); change lands in the drain-cycle repo
---

# N04 — Supervisor records verdicts on every exit

**Type:** `story` · lands in the **drain-cycle** repo.

> **Blocked by:** [N01](../D1-supervisor-sheds-workflow-prose/N01-thin-supervisor-contract-design-doc.md) —
> task breakdown waits until the handoff schema v2 is accepted. Buildable in parallel with
> [N03](N03-pack-skills-emit-verdicts.md): the read side tests against fixture handoffs written
> from the schema table, not against N03's live output.

> **▶ On pickup:** break into build tasks per the at-pickup breakdown.

## What

As the operator grading cycles, I want every worker exit — Done, halted, errored — to land a
run-log entry with verdicts and halt_reason, so that no drain is uninspectable. The run-log
schema already has the fields; nothing populates them: `outcome_verdict` and `prep_verdict` are
initialised to `None` at `orchestrator.py:647-649` and never assigned. This node has
`handoff.py` parse the schema-v2 verdict fields and the orchestrator land them on every
`append_entry` path.

## Why

The bet: reading verdicts from the handoff closes KR2 with a bounded diff on a file the
orchestrator already reads at every Done exit — no new I/O, no new failure mode. Rejected
alternative: the supervisor re-derives verdicts by inspecting PRs and Linear comments —
re-creates workflow knowledge inside the supervisor, violating the boundary this initiative
draws. Unblocks N05's grading (the schema check is one of its three measurements).

## Completion

- **Done when:** a stubbed Done-path drain writes a run-log entry with `flow`,
  `outcome_verdict`, and `prep_verdict` populated from the handoff, pytest green.
- **Done when:** a forced-halt test writes an entry carrying `halt_reason` plus whatever
  verdicts the partial handoff held.
- **Done when:** the KR2 schema check exits 0 over a compliant run log and non-zero when a Done
  entry lacks verdicts.

## Assumptions

- Every exit path flows through `runlog.append_entry`, so populating at that seam covers Done, halted, and errored exits alike. *(verified — Done and halt paths both call `log.append_entry` in orchestrator.py; the run-log docstring documents the halt-entry contract)*

## Key Risks

- **Risk:** a worker that crashes before writing the handoff leaves verdicts null, and the
  schema check reads the drain as a KR2 failure when it is actually inspectable via halt_reason.
  *Mitigation:* the schema check encodes "inspectable", not "non-null": null verdicts are
  compliant when `halt_reason` (or a non-Done exit state) explains them; a null on a Done entry
  is the violation.

## Tasks

- [ ] `skeleton` — Parse schema-v2 verdict fields in `handoff.py` and populate Done-path run-log entries (fixture-handoff test folded in) · Done when: a stubbed drain writes an entry with flow, outcome_verdict, and prep_verdict populated and pytest is green · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·L·L·L·L
- [ ] Populate halt/error exits with halt_reason plus any partial-handoff verdicts · Done when: a forced-halt test writes an entry where halt_reason is non-null and available verdicts are carried · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·L·L·L·L
- [ ] Add the KR2 schema check (one-liner or small script beside the run logs) · Done when: the check exits 0 over a compliant run log and non-zero when a Done entry lacks verdicts · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
