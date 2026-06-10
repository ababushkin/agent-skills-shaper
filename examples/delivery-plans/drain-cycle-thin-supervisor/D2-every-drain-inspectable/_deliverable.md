---
layer: deliverable
id: D2
title: Every drain inspectable
parent: ..
serves_kr: KR2
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR2 holds — every worker exit in the window produces a run-log entry with exit
    state, verify/prep verdicts, and halt_reason where applicable; zero uninspectable
    drains, proven by the schema check over ~/.drain-cycle/runs/*.json.
---

# D2 — Every drain inspectable

**Serves:** KR2 *(foundation)* — "every worker exit in the window produces a run-log entry with
exit state, verify/prep verdicts, and halt_reason where applicable; zero uninspectable drains."

The run-log schema already carries the verdict fields, but nothing populates them:
`outcome_verdict` and `prep_verdict` are initialised to `None` in `orchestrator.py` ("populated
by M2+ roles") and never assigned — the roles that were meant to assign them were cancelled.
Under the thin-supervisor architecture the verdicts originate in the *pack's* workflow steps, so
the channel is the handoff file, in both directions: **N03** (agent-skills-shaper) has the pack
skills write verdicts into `.drain-handoff.json` per N01's schema v2; **N04** (drain-cycle) has
the supervisor read them and land them on every exit path — Done, halted, errored — with the
KR2 schema check as the proof. No Rule A1 trigger of its own: both nodes build against the
contract N01 already decided.

## Nodes

- [N03 — Pack skills emit verdicts into the handoff](N03-pack-skills-emit-verdicts.md) · `story`
- [N04 — Supervisor records verdicts on every exit](N04-supervisor-records-verdicts.md) · `story`

## Done when

KR2 is observed: the schema check exits 0 over the validation window's run logs — every entry
carries exit state, Done entries carry verdicts, halted entries carry halt_reason. Reducible to
N03 + N04 done (the window observation itself rides on D3's validation cycles); no acceptance
node needed.
