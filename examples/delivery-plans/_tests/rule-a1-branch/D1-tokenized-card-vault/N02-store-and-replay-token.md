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
delegates_to: execution-breakdown (per-node task breakdown)
---

# N02 — Store and replay a card token

> **As** a returning shopper, **I want** my saved card replayed from a stored token, **so that**
> I complete checkout without re-entering card details.

> **▶ On pickup — before coding:** expand this node via `execution-breakdown`.
> **Blocked by:** N01 (the card-vault design doc must be accepted first).

## Acceptance criteria

- **Done when:** a stored token is exchanged for a charge and the order completes — observed in
  logs with the token reference and order id.
- **Done when:** no raw card number is persisted outside the vault (PCI scope held).

## Tasks

- [ ] `skeleton` — store one token and replay it through to a completed test charge end-to-end (vault client + checkout call stubbed where external, folded in).
- [ ] Hold PCI scope: assert no raw PAN is written outside the vault.
