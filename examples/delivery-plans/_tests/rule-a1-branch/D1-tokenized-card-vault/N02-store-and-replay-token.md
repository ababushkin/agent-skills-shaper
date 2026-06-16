---
layer: node
id: N02
type: story
title: Store and replay a card token
parent: D1
serves_kr: KR1
maps_to: linear-issue
skeleton: true
external_window: none
completion:
  form: acceptance-criteria
delegates_to: at-pickup task breakdown (per-node task breakdown)
---

# N02 — Store and replay a card token

> **As** a returning shopper, **I want** my saved card replayed from a stored token, **so that**
> I complete checkout without re-entering card details.

> **▶ On pickup — before coding:** break this node into task-sized pieces using your build agent's at-pickup task breakdown phase.
> **Blocked by:** N01 (the card-vault design doc must be accepted first).

## What

Store a card as a vault token and replay that token through to a completed charge at checkout,
without persisting raw card data outside the vault.

## Why

The bet: a token stored once and replayed at checkout is what lets a returning shopper skip card
re-entry — the KR1 behaviour. The rejected alternative is re-collecting card data each session,
which defeats the reuse premise. This node is the walking skeleton: it exercises the real vault and
checkout seam the design doc (N01) decided.

## Completion

- **Done when:** a stored token is exchanged for a charge and the order completes — observed in
  logs with the token reference and order id.
- **Done when:** no raw card number is persisted outside the vault (PCI scope held).

## Assumptions

- N01's design doc is accepted, fixing the tokenisation scheme and vault placement. *(to-verify)*
- The vault exposes a client the checkout call can reach. *(to-verify)*

## Key Risks

- **Risk:** raw card data leaks outside the vault during the store/replay path, breaking PCI scope.
  *Falsifier:* a test asserting no raw PAN is written outside the vault must pass; if it fails, the
  path is non-compliant and must be re-shaped.

## Tasks

- [ ] `skeleton` — store one token and replay it through to a completed test charge end-to-end (vault client + checkout call stubbed where external, folded in). Done when: a stored token drives a completed test charge end-to-end. Model: Frontier · risk one-way · review elevated · axes RC·SC·HS·SR·OR = H·M·M·H·M · companions security-and-hardening
- [ ] Hold PCI scope: assert no raw PAN is written outside the vault. Done when: a test confirms no raw card number is persisted outside the vault. Model: Frontier · risk one-way · review elevated · axes RC·SC·HS·SR·OR = M·M·M·H·L · companions security-and-hardening
