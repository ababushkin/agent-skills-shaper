---
layer: node
id: N02
type: story
title: Clear a stuck run from the dashboard
parent: D1
serves_kr: KR1
maps_to: linear-issue
skeleton: true
external_window: none
completion:
  form: acceptance-criteria
delegates_to: planning-and-task-breakdown (per-node task breakdown)
---

# N02 — Clear a stuck run from the dashboard

> **As** the Nestl operator, **I want** to clear a stuck `"running"` PipelineRun from the admin
> dashboard in one action, **so that** I recover the pipeline without opening the database console.

> **▶ On pickup — before coding:** expand this node via `planning-and-task-breakdown`.
> **Blocked by:** N01 (the recovery-semantics design doc must be accepted first).

## Acceptance criteria

- **Done when:** a stuck `"running"` row, selected in the admin Pipeline Runs table, reaches a
  terminal state (`failed`, marked operator-cleared) in one action — observed in the table and in
  logs with the run id.
- **Done when:** the transition is idempotent — re-issuing the action on an already-terminal run is
  a no-op, not an error.

## Tasks

- [ ] `skeleton` — clear one seeded stuck run end-to-end: dashboard action → API → state transition → row terminal, on a seeded `"running"` fixture row (the admin route + seed fixture are folded into this slice).
- [ ] Make the transition idempotent and log the run id + operator action on clear.
