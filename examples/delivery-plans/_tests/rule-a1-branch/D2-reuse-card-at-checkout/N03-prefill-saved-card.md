---
layer: node
id: N03
type: story
title: Pre-fill the saved card at checkout
parent: D2
serves_kr: KR2
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
delegates_to: execution-breakdown (per-node task breakdown)
---

# N03 — Pre-fill the saved card at checkout

> **As** a returning shopper, **I want** my saved card shown pre-filled at checkout, **so that**
> I do not re-enter details I have already stored.

> **▶ On pickup — before coding:** expand this node via `execution-breakdown`.

## Acceptance criteria

- **Done when:** a shopper with a saved card sees it pre-selected at checkout and can complete the
  order without re-entering card details — verified in the checkout flow.
- **Done when:** a shopper with no saved card sees the unchanged manual-entry checkout (no
  regression).

## Tasks

- [ ] Render the saved-card option pre-selected when a token exists for the shopper.
- [ ] Fall back to manual entry when no token exists.
