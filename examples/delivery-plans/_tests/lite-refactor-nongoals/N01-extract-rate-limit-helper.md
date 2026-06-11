---
layer: node
id: N01
type: refactor
title: Extract rate-limit helper
parent: lite-refactor-nongoals
maps_to: linear-issue
completion:
  form: invariant
delegates_to: at-pickup task breakdown (refactor — invariant-preserving)
---

# N01 — Extract rate-limit helper

## What

Extract the inline rate-limit accounting in `request_handler.process` into a
standalone helper. Behaviour observable to callers does not change; only the
location of the logic moves.

## Why

The accounting is duplicated between two callers and the duplication has
already drifted once. The bet: one helper with a single test is cheaper to
keep correct than two inline copies. Rejected: inlining the second caller's
copy back into the first — easier short-term but ratchets the duplication
problem forward.

## Completion

**Invariant:** for any sequence of requests, the number of rate-limit
rejections observed by clients before and after the change is identical.
**Verified by:** the existing `request_handler` suite, run at the same count
and with the same skips as before the change.
**Out of scope:** the rate-limit *policy* itself — thresholds, windows, and
back-off curves are not touched.

## Non-goals

- Changing rate-limit thresholds or window size.
- Adding new instrumentation around rate-limit events.
- Renaming the public `process` entry point.

## Assumptions

- The existing test suite covers both callers' rate-limit paths *(verified)*.
- No external consumer reaches into the inline accounting via reflection *(to-verify)*.

## Key Risks

- **Risk:** the second caller's copy has drifted from the first in a way no
  test catches, so unifying them silently changes behaviour. *Mitigation:*
  diff the two copies before unifying; document any reconciliation in the
  commit message.

## Tasks

- [ ] `skeleton` — move the first caller's accounting block to a helper and route the caller through it (toolchain + import wiring folded in) · Done when: the existing suite passes unchanged · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·L·L·L·L
- [ ] Route the second caller through the helper and remove its inline copy · Done when: both callers share one accounting path and the suite passes unchanged · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·L·L·L·L
