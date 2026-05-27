---
layer: node
id: N04
type: story
title: Scrape job always reaches terminal
parent: D2
serves_kr: KR2
maps_to: linear-issue
skeleton: true
external_window: none
completion:
  form: acceptance-criteria
delegates_to: planning-and-task-breakdown (per-node task breakdown)
---

# N04 — Scrape job always reaches terminal

> **As** the Nestl operator, **I want** a manually triggered scrape job to always end in
> `completed` or `failed` even if its worker dies, **so that** it never strands a `"running"` row I
> have to clean up.

> **▶ On pickup — before coding:** expand this node via `planning-and-task-breakdown`.

## Acceptance criteria

- **Done when:** a manually triggered scrape job that completes normally writes a `completed`
  `PipelineRun` result.
- **Done when:** a scrape job whose worker is killed mid-run is reconciled to `failed` within the
  longest expected job duration — observed in the Pipeline Runs table, no orphaned `"running"` row.

## Tasks

- [ ] `skeleton` — drive one scrape trigger end-to-end to a terminal result, including a simulated worker death that reconciles to `failed` (the heartbeat/finalizer mechanism is folded into this slice).
- [ ] Assert the normal-completion path writes `completed` with the run id.
