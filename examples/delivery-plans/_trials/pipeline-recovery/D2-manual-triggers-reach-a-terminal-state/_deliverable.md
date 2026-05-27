---
layer: deliverable
id: D2
title: Manual triggers reach a terminal state
parent: ..
serves_kr: KR2
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR2 holds — every manual trigger of a scrape, enrichment, or status-check job
    produces a terminal PipelineRun result; zero "running" rows older than the
    longest expected job duration over the soak window.
---

# D2 — Manual triggers reach a terminal state

**Serves:** KR2 *(prevention)* — "Every manual trigger of a scrape, enrichment, or status-check job
produces a terminal `PipelineRun` result (`completed` or `failed`)."

Recovery (D1) clears the symptom; prevention stops orphaned rows arising. A manually triggered job
whose worker dies must still resolve to `completed` or `failed`. The work proves the guarantee for
one category end-to-end (**N04**), extends it to the other two (**N05**), then **observes the
aggregate in production over the soak window** (**N06**, the acceptance node).

Rule A1 not triggered for D2: each per-category guarantee is an additive, reversible change behind
the state machine D1's design doc already settled — no new one-way-door decision here.

## Nodes

- [N04 — Scrape job always reaches terminal](N04-scrape-job-always-terminal.md) · `story` · `skeleton`
- [N05 — Extend the guarantee to enrichment + status-check](N05-extend-to-enrich-and-status.md) · `story`
- [N06 — Soak: zero orphaned runs over the window](N06-soak-zero-orphaned-runs.md) · `story` · `acceptance`

## Done when

KR2 is observed: over the soak window, the admin Pipeline Runs table shows zero `"running"` rows
older than the longest expected job duration, across all three job categories. **N06** carries this
observation as the acceptance node — it closes last, so D2 reaching 100% coincides with KR2 being
observed.
