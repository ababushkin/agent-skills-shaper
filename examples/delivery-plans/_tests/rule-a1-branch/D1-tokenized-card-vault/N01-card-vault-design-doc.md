---
layer: node
id: N01
type: design-doc
title: Card-vault design doc (before build)
parent: D1
serves_kr: KR1
maps_to: linear-issue
external_window: none
completion:
  form: the-design-doc
delegates_to: design-doc (Rule A1 design doc — produced before the build node is picked up)
---

# N01 — Card-vault design doc (before build)

**Type:** `design-doc`. This deliverable met a Rule A1 trigger, so the design doc comes first.

> **▶ On pickup — before any build node here:** produce the design doc via the `design-doc`
> skill — problem, alternatives (tokenisation scheme + vault placement), the one-way-door call,
> NFR constraints (PCI, latency), and the operability plan. The build node `N02` is **blocked by
> this node**: its task breakdown waits until this design doc is accepted.

## What

Produce the accepted design doc for the tokenised card vault: the tokenisation scheme, where the
vault sits, the one-way-door decision, and the PCI/latency constraints the build must hold.

## Why

The bet: deciding the tokenisation scheme and vault placement once, in a reviewed design doc,
prevents a costly reversal after the vault is storing live tokens. The rejected alternative is
designing inline during the build — Rule A1 forbids it here because the choice is shared
infrastructure, a one-way door, and PCI-scoped. Accepting this doc unblocks N02's task breakdown.

## Completion

An accepted design doc covering the tokenisation scheme, vault placement, the one-way-door
decision, and the PCI/latency constraints. `delivery-shape` does not restate the design-doc
structure here — that discipline lives in the `design-doc` skill.

## Assumptions

- The vault is shared infrastructure consumed beyond this team. *(verified)*
- PCI scope and the checkout latency budget are known inputs to the design doc. *(to-verify)*

## Key Risks

- **Risk:** the tokenisation scheme is chosen without a reversal path and proves wrong after live
  tokens exist. *Mitigation:* the design doc records the one-way-door call explicitly and its
  rejected alternatives, so the decision is reviewed before any token is stored.

## Tasks

- [ ] Frame the problem and constraints (PCI scope, checkout latency budget) for the `design-doc`. Done when: the design-doc draft states the problem and the PCI/latency constraints. Model: Frontier · risk one-way · review elevated · axes RC·SC·HS·SR·OR = H·H·M·H·L · companions code-review-and-quality, security-and-hardening
- [ ] Record the tokenisation-scheme decision and its rejected alternatives in the design doc. Done when: the accepted design doc names the chosen scheme, the rejected alternatives, and the one-way-door call. Model: Frontier · risk one-way · review elevated · axes RC·SC·HS·SR·OR = H·M·M·H·L · companions security-and-hardening
