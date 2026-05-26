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

## Completion

An accepted design doc covering the tokenisation scheme, vault placement, the one-way-door
decision, and the PCI/latency constraints. `delivery-shape` does not restate the design-doc
structure here — that discipline lives in the `design-doc` skill.

## Tasks

- [ ] Frame the problem + constraints (PCI scope, checkout latency budget) for the `design-doc`.
- [ ] Record the tokenisation-scheme decision and its rejected alternatives in the design doc.
