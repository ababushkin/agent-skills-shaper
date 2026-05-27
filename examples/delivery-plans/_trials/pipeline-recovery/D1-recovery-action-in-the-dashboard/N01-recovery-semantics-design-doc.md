---
layer: node
id: N01
type: design-doc
title: Recovery-semantics design doc (before build)
parent: D1
serves_kr: KR1
maps_to: linear-issue
external_window: none
completion:
  form: the-design-doc
delegates_to: design-doc (Rule A1 design doc — produced before the build nodes are picked up)
---

# N01 — Recovery-semantics design doc (before build)

**Type:** `design-doc`. This deliverable met a Rule A1 trigger (shared `PipelineRun` state machine,
a one-way-door cancellation decision, production-data mutation), so the design doc comes first.

> **▶ On pickup — before any build node here:** produce the design doc via the `design-doc` skill —
> problem (orphaned `"running"` rows on a sleep-prone laptop), the stuck-vs-slow detection
> threshold, the safe state transition (how a row reaches a terminal state without clobbering a
> worker that is merely asleep), the dashboard action contract, and the operability plan. The build
> nodes `N02` and `N03` are **blocked by this node**: their task breakdown waits until this design
> doc is accepted.

## Completion

An accepted design doc covering: the detection threshold that separates a genuinely-stuck run from
a slow/asleep one; the safe `running → terminal` transition and its idempotency; what the one-click
action does to an in-flight worker; and the rollback/operability plan. `delivery-shape` does not
restate the design-doc structure here — that discipline lives in the `design-doc` skill.

## Tasks

- [ ] Frame the problem and constraints (sleep/wake worker death, longest expected job duration, no-clobber requirement) for the `design-doc`.
- [ ] Record the stuck-detection threshold and the safe-transition decision, with rejected alternatives, in the design doc.
