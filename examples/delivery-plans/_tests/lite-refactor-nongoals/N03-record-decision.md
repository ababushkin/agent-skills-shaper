---
layer: node
id: N03
type: adr
title: Record helper-vs-inline decision in an ADR
parent: lite-refactor-nongoals
maps_to: linear-issue
completion:
  form: decision-record
delegates_to: eng-principles-universal.md Rule A3 (ADR)
---

# N03 — Record helper-vs-inline decision in an ADR

## What

Write a short ADR capturing the decision to extract the rate-limit accounting
into a helper rather than inline the duplication, including the rejected
alternative and the maintenance argument.

## Why

The next time accounting drift surfaces, the reader needs to know why the
helper exists and what the inline alternative cost. The bet: a one-page ADR
costs less now than the recurring "why is this here?" round-trip. Rejected:
relying on the commit message — commits scroll out of working memory; ADRs
are searchable.

## Completion

**Decision:** the rate-limit accounting is centralised in a single helper.
The ADR records context (drift incident), the rejected alternative
(inline-and-monitor), and the consequences (one place to change, one place
to break) — written and linked from the module README.

## Assumptions

- The repo's ADR convention is already established (Rule A3) *(verified)*.

## Key Risks

*(none)*
