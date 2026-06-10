---
layer: node
id: N05
type: experiment
title: "Validation: 2 cycles on the pointer prompt"
parent: D3
serves_kr: KR1
maps_to: linear-issue
acceptance: true
external_window: none
completion:
  form: hypothesis+success-metric
  verifies_parent: D3
  hypothesis: >
    A full cycle drains to completion with the pointer-only worker prompt at the
    execution initiative's quality bar — no manual fix commits — with every worker
    exit inspectable in the run log.
  success_metric: >
    drain-cycle grade over ~/.drain-cycle/runs/*.json + the prompt-template diff +
    the KR2 schema check, over the first 2 cycles after the re-scope lands: ≥1 clean
    full-cycle drain confirms. Zero clean drains in 2 cycles falsifies the bet;
    3 consecutive halted drains the inlined prompt would have completed fires the
    initiative kill condition.
delegates_to: product-spike (experiment discipline — hypothesis, success metric, written finding)
---

# N05 — Validation: 2 cycles on the pointer prompt

**Type:** `experiment` · `acceptance: true` (verifies D3). Not a build node: its honest outcomes
are *confirmed* or *falsified*, not *shipped*. This is the node that grades the KR1 bet — and,
because the measurement window is shared, it also runs the KR2 schema check over the same logs.

> **Blocked by:** [N02](../D1-supervisor-sheds-workflow-prose/N02-pointer-only-prompt-template.md),
> [N03](../D2-every-drain-inspectable/N03-pack-skills-emit-verdicts.md), and
> [N04](../D2-every-drain-inspectable/N04-supervisor-records-verdicts.md) — everything under
> test must have landed. Also initiative A's
> [N09](../../issues-drain-end-to-end/D2-execution-workflow-drains-issues/N09-validation-drains.md) —
> the execution skills should be proven on live drains before the supervisor is thinned, so a
> failure here indicts the re-scope, not the skills.

> **▶ On pickup:** run the experiment and write the finding (confirmed / falsified) via
> `product-spike`.

## What

Drain the first 2 real cycles after the re-scope lands with the pointer-only prompt, and grade
the bet: did ≥1 cycle complete with zero manual fix commits? Each cycle's evidence is three
measurements — `drain-cycle grade` over the run logs, the prompt-template diff (the ≤15-line
template in force), and the KR2 schema check (every exit inspectable). Watch the kill condition
throughout. Write the finding.

## Why

KR1 is the stretch bet, and only live cycles can grade it — N02's smoke drain proves one issue
flows, not that a whole cycle's mess (halts, resumes, stacked PRs, mixed repos) survives a
supervisor that no longer says how to work. Rejected alternative: declare victory on the smoke
drain — the unverified-claim failure this pack exists to prevent. This node carries
`acceptance: true` because D3's Done is irreducible to its children: there is no build node
whose completion implies a cycle drains. Close it last — D3 reaching 100% coincides with the KR
observation.

## Completion

**Hypothesis:** a full cycle drains to completion with the pointer-only prompt at the execution
initiative's quality bar (no manual fix commits), with every worker exit inspectable.

**Success metric:** `drain-cycle grade` + prompt-template diff + KR2 schema check over the first
2 cycles after the re-scope lands = **≥1 clean full-cycle drain**.

Zero clean drains in the window **falsifies** the bet — the re-scope is re-shaped, not extended.
Three consecutive halted drains that the inlined prompt would have completed fires the
initiative **kill condition**: restore the inlined tail; keep the re-scope to guardrails and
logging only.

## Assumptions

- Two cycles of ordinary work are available in the measurement window. *(verified — the KR's own "measured over" clause anticipates this window, and the backlog convention keeps a cycle stream)*
- "Drains the inlined prompt would have completed" is judgeable from halt transcripts. *(to-verify — the kill condition needs a per-halt judgement note; if a halt is ambiguous, it does not count toward the 3)*

## Key Risks

- **Risk:** the 2 cycles are dominated by markdown-pack work and a clean drain overstates the
  re-scope's generality.
  *Mitigation:* include at least one drain-cycle (Python) issue across the window so both repo
  types exercise the pointer prompt.

## Tasks

- [ ] `skeleton` — Drain the first post-re-scope cycle; record grade, template line count, and schema-check result in a trial note · Done when: the run log and trial note for cycle 1 exist with all three measurements · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·M·L·L·L
- [ ] `acceptance` — Drain the second cycle; evaluate the ≥1-clean-cycle metric and the kill condition; write the finding (confirmed / falsified) — this finding is D3's Done condition · Done when: the finding is written with per-cycle evidence links · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·M·L·L·L
