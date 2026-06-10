---
layer: node
id: N02
type: adr
title: "ADR: persona contract + dispatch protocol"
parent: D1
serves_kr: KR2
maps_to: linear-issue
external_window: none
completion:
  form: decision-record
  criterion: >
    An accepted ADR exists recording Context / Decision / Consequences for the persona
    contract — prompt-file format, structured finding format, and dispatch protocol
    (Agent fan-out on Claude Code, inline-sequential fallback elsewhere).
delegates_to: eng-principles-universal.md Rule A3 (ADR) + D3 (living ADRs)
---

# N02 — ADR: persona contract + dispatch protocol

**Type:** `adr`.

> **▶ On pickup:** author the decision record per the ADR discipline (Rule A3); set
> `status: accepted` when decided. This ADR gates N03 — the personas cannot be authored until
> the contract they are written to is pinned.

## What

An ADR pinning the persona contract: where persona prompt files live and what frontmatter they
carry, the structured finding format the grader (N01) matches on, and the dispatch protocol —
Agent-tool fan-out on Claude Code, inline-sequential self-review with the same persona prompt for
non-Claude workers (codex/kimi). The choice determines how N03's personas are written and how
every execution skill invokes review.

## Why

The bet: one portable contract keeps persona prose vendor-neutral and dispatch mechanics out of
the personas, which is the premise initiative C's thin supervisor builds on. Rejected alternative:
Claude-Code-native agent definitions — richer dispatch, but they break the vendor-portability
premise and strand codex/kimi workers without a fallback. An ADR rather than a design doc: single
surface, bounded consequences, and migrating prompt files later is mechanical — Rule A1's "a
short ADR may suffice" branch, mirroring the precedent in the top-down-delivery-planning plan.

## Completion

**Decision:** open — to be recorded at pickup. The accepted record pins (a) persona file format
and location, (b) the structured finding line the grader matches on (file · defect class ·
severity), and (c) dispatch: Agent fan-out on Claude Code, inline-sequential fallback elsewhere —
with Context / Decision / Consequences and a reference to the ADR file under `docs/adr/`.

## Assumptions

- The Agent tool can dispatch a plain prompt-file persona without a pack-native agent definition. *(verified — the Agent tool takes a prompt; the persona file's content is the prompt)*
- A structured finding format does not depress persona recall versus free prose. *(to-verify — checked against the N01 harness during N03's iteration task)*

## Key Risks

- **Risk:** the contract over-fits Claude Code and the non-Claude fallback is unusable in
  practice, undermining initiative C's cross-vendor premise.
  *Mitigation:* the fallback path is written as plain prose in the same persona file and trialled
  once by running a persona inline in a single context before the ADR is accepted.

## Tasks

- [ ] Record Context: enumerate the dispatch surfaces (Claude Agent fan-out; codex/kimi inline-sequential) and ≥2 candidate contract shapes with trade-offs · Done when: the ADR's Context section names both surfaces and the candidates · Model: Frontier · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·H·L·M·L
- [ ] Record the Decision and Consequences (file format, finding format, dispatch + fallback) and set status accepted · Done when: the ADR is accepted and N03 can author against it with no open contract questions · Model: Frontier · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·H·L·M·L
