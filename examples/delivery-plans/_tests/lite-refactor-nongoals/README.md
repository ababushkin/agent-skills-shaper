# Test plan — lite tier with `refactor` + `## Non-goals` (doc-only path)

A **fixture**, not a real initiative. It exists to exercise three pieces of framing
added in ABA-392 in one walkable file-set:

- **lite tier** — flat `N<nn>-*.md` files at the plan root, no `D<n>-*/`
  deliverable directories, no manifest oracle. This is the small-scale path
  `delivery-shape` emits for a single outcome with no KR worth tracking.
- **`refactor` node type** — behaviour-preserving change whose `## Completion`
  is expressed as `**Invariant:**` + `**Verified by:**` + `**Out of scope:**`,
  not a Cohn story.
- **`## Non-goals` section** — optional sixth body section that names
  deliberately-excluded scope so it survives into pickup.

The fixture also covers the doc/spec/config carve-out: a node whose work has no
executable path carries no walking-skeleton task, and `bin/check-plan-framing`
passes the plan anyway.

## Context

`delivery-shape` over-produces on small inputs. The plan here is itself a small
input — three behaviour-preserving touches to one module, plus a short ADR — so
it exercises the lite path that drops the deliverable/manifest scaffolding.

## Goal

Tighten the framing of a single module — extract one helper, rename two
collaborators, and record the decision — without changing observable behaviour.

## Tree

```
lite-refactor-nongoals/
├── README.md                                 ← lite-tier root (this file; no manifest)
├── N01-extract-rate-limit-helper.md          → refactor · Non-goals present
├── N02-rename-collaborators.md               → refactor · no tasks (doc/spec path)
└── N03-record-decision.md                    → adr · no skeleton (doc work)
```
