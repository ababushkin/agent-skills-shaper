---
layer: node
id: N05
type: story
title: Extend the guarantee to enrichment + status-check
parent: D2
serves_kr: KR2
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
delegates_to: planning-and-task-breakdown (per-node task breakdown)
---

# N05 — Extend the guarantee to enrichment + status-check

> **As** the Nestl operator, **I want** the terminal-result guarantee to cover enrichment and
> status-check jobs too, **so that** none of the three manual job categories can strand a
> `"running"` row.

> **▶ On pickup — before coding:** expand this node via `planning-and-task-breakdown`.
> **Blocked by:** N04 (the heartbeat/finalizer mechanism is established for scrape first).

## Acceptance criteria

- **Done when:** a manually triggered enrichment job reaches `completed` or `failed`, including
  under simulated worker death — no orphaned `"running"` row.
- **Done when:** a manually triggered status-check job reaches `completed` or `failed` under the
  same conditions.

## Tasks

- [ ] `skeleton` — apply the N04 finalizer to enrichment end-to-end (normal + worker-death path), reusing the established mechanism (folded in).
- [ ] Apply the same guarantee to status-check and assert both categories under worker-death.
