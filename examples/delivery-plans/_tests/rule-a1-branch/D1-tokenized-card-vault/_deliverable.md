---
layer: deliverable
id: D1
title: Tokenized card vault
parent: ..
serves_kr: KR1
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR1 holds — a returning shopper completes checkout with a stored card, observed
    end-to-end in logs.
---

# D1 — Tokenized card vault

**Serves:** KR1 *(bet)* — a returning shopper completes checkout with a stored card token.

This deliverable **meets a Rule A1 trigger**: it stands up a shared payment vault (shared
infrastructure used beyond this team), commits to a tokenisation scheme that is expensive to
reverse (a one-way door), and carries PCI compliance impact. So its first node is a `design-doc`
node — the design doc is produced via the `design-doc` skill **before** the build node is picked
up for task breakdown. `delivery-shape` does not re-author the design-doc structure; it points
`delegates_to` at the owning skill.

## Nodes

- [N01 — Card-vault design doc (before build)](N01-card-vault-design-doc.md) · `design-doc`
- [N02 — Store and replay a card token](N02-store-and-replay-token.md) · `story` · `skeleton`

## Done when

KR1 is observed: a stored token is replayed at checkout and the order completes, confirmed in
logs.
