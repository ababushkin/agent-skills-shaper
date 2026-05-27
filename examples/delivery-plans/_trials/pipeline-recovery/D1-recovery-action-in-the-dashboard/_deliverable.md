---
layer: deliverable
id: D1
title: Recovery action in the admin dashboard
parent: ..
serves_kr: KR1
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR1 holds — any stuck PipelineRun state clears from the admin dashboard in one
    action; no row stays in "running" longer than 30 minutes without an operator
    action being available in the UI.
---

# D1 — Recovery action in the admin dashboard

**Serves:** KR1 *(recovery)* — "Any stuck `PipelineRun` state clears from the admin dashboard in
one action."

The escape-hatch deliverable: today a stuck `"running"` row needs direct DB access. This gives the
operator a one-action recovery in the UI. Because the change mutates shared pipeline state and the
cancellation semantics are a one-way-door decision (what does "clear" do to a worker that may only
be asleep, not dead?), **Rule A1 is triggered** — the first node is a `design-doc` node, and the
build nodes are blocked by it.

## Nodes

- [N01 — Recovery-semantics design doc (before build)](N01-recovery-semantics-design-doc.md) · `design-doc`
- [N02 — Clear a stuck run from the dashboard](N02-clear-stuck-run-from-dashboard.md) · `story` · `skeleton`
- [N03 — Action surfaces only when safe](N03-action-surfaces-only-when-safe.md) · `story`

## Done when

KR1 is observed: in the admin Pipeline Runs table, no row stays in `"running"` longer than 30
minutes without an operator action available in the UI to clear it.
