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
delegates_to: at-pickup task breakdown (per-node task breakdown)
---

# N03 — Pre-fill the saved card at checkout

> **As** a returning shopper, **I want** my saved card shown pre-filled at checkout, **so that**
> I do not re-enter details I have already stored.

> **▶ On pickup — before coding:** break this node into task-sized pieces using your build agent's at-pickup task breakdown phase.

## What

Show a shopper's saved card pre-selected at checkout when a token exists, and leave the manual-entry
checkout unchanged when none does.

## Why

The bet: pre-filling the stored card removes the re-entry step that drives returning-shopper
abandonment (KR2). The rejected alternative is requiring the shopper to pick the saved card
manually each time, which keeps the friction the deliverable exists to remove. This node consumes
the vault D1 designed; it adds no infrastructure of its own.

## Completion

- **Done when:** a shopper with a saved card sees it pre-selected at checkout and can complete the
  order without re-entering card details — verified in the checkout flow.
- **Done when:** a shopper with no saved card sees the unchanged manual-entry checkout (no
  regression).

## Assumptions

- A token-lookup for the current shopper is available to the checkout surface. *(to-verify)*
- The checkout surface can render a pre-selected payment option. *(verified)*

## Key Risks

- **Risk:** the pre-fill path regresses the manual-entry checkout for shoppers with no saved card.
  *Falsifier:* a no-token checkout test must show the unchanged manual flow; if it changes, the
  surface regressed.

## Tasks

- [ ] Render the saved-card option pre-selected when a token exists for the shopper. Done when: a shopper with a token sees the saved card pre-selected at checkout. Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·M·L·M·L
- [ ] Fall back to manual entry when no token exists. Done when: a shopper with no token sees the unchanged manual-entry checkout. Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
