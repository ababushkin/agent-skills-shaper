---
layer: node
id: N03
type: story
title: Pack skills emit verdicts into the handoff
parent: D2
serves_kr: KR2
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    The pack's verify and PR-finishing steps write outcome_verdict, prep_verdict, and
    flow into .drain-handoff.json per schema v2, and blocked/halt exits write the
    reason — proven on a toy-issue dry run and a blocked-issue dry run.
delegates_to: at-pickup task breakdown (story); change lands in the agent-skills-shaper repo
---

# N03 — Pack skills emit verdicts into the handoff

**Type:** `story` · lands in the **agent-skills-shaper** repo (extends the execution skills
initiative A authors).

> **Blocked by:** [N01](../D1-supervisor-sheds-workflow-prose/N01-thin-supervisor-contract-design-doc.md) —
> task breakdown waits until the handoff schema v2 is accepted. Also initiative A's D2 skill
> stack ([N05](../../issues-drain-end-to-end/D2-execution-workflow-drains-issues/N05-entry-skill-front-door.md)–[N08](../../issues-drain-end-to-end/D2-execution-workflow-drains-issues/N08-pr-finishing-graphite-first.md)) —
> this node edits those skills' verify and PR-finishing steps, so it cannot start before they
> exist.

> **▶ On pickup:** break into build tasks per the at-pickup breakdown; the diff extends A's
> skills at their handoff seams — it does not add new skills.

## What

As the operator inspecting a drain, I want the pack's verify and PR-preparation steps to write
their verdicts into the handoff file, so that the supervisor can record them without owning any
workflow knowledge. The handoff file already carries `pr_title`/`pr_body`/`findings`; this node
adds the schema-v2 verdict fields (`outcome_verdict`, `prep_verdict`, `flow`) at the workflow
steps that produce them, plus the halt reason on blocked/non-Done exits.

## Why

The bet: the handoff file is already the proven worker→supervisor channel, so verdicts ride the
existing seam with zero new transport. Rejected alternative: the supervisor parses worker
transcripts for verdicts — couples inspection to one vendor's transcript format, which is
exactly the coupling this initiative exists to remove. Unblocks N04's read side and is the
write-half of KR2.

## Completion

- **Done when:** a toy-issue dry run through the execution skills leaves a handoff file with
  `outcome_verdict`, `prep_verdict`, and `flow` populated per schema v2.
- **Done when:** a blocked-issue dry run leaves a handoff naming the halt reason while the issue
  stays In Progress per workflow governance.

## Assumptions

- A's execution skills have distinct verify and PR-preparation steps where verdict emission can attach. *(verified — A/N05's front door names verify and PR as named delegations, and A/N08 owns the handoff write; the seams exist by contract)*
- Verdict emission is a light extension of those steps, not a redesign. *(to-verify — if a step produces no structured verdict object at all, this node adds the object at the skill seam; the supervisor side is unaffected either way)*

## Key Risks

- **Risk:** the fields the pack writes drift from the fields the supervisor reads — two repos,
  one schema.
  *Mitigation:* schema v2 lives in one table (N01's contract, amending A/N04's); N04's tests
  parse a fixture handoff written verbatim from that table, so drift fails a test before it
  fails a drain.

## Tasks

- [ ] `skeleton` — Add verdict emission to the verify and PR-finishing steps per schema v2 (fixture handoff example folded in) · Done when: a toy-issue dry run leaves a handoff with outcome_verdict, prep_verdict, and flow populated per schema v2 · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·L·L·L·L
- [ ] Write the blocked/halt emission path · Done when: a blocked-issue dry run leaves a handoff naming the halt reason and the issue status is unchanged · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·M·L·L·L
