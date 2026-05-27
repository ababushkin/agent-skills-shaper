# Trial plan — Pipeline recovery without the database console

> **Trial fixture, not the operative plan.** Produced by `delivery-shape` in the N07 self-trial
> (ABA-288) to grade the D2 bet: does the skill bake framing in — acceptance criteria on every
> story, ≥1 walking-skeleton task — when fed only an initiative's goal + KRs? This file-set is the
> instrument, not a commitment to build nestl work now. See [`../FINDING.md`](../FINDING.md) for
> the experiment finding and per-trial re-prompt count.

**Source initiative:** [Pipeline recovery without the database
console](https://linear.app/ababushkin/project/pipeline-recovery-without-the-database-console-628d938363fa)
· Linear `ABA` · repo `nestl` · Type 2 (personal product). Fed to `delivery-shape` as **goal +
KRs only** — a deliberately out-of-domain initiative (production software, not a skill pack) to
test that the framing comes from the skill, not from domain familiarity.

---

## The bet (read this first — top-down starts at the outcome)

**Goal:** For the Nestl operator, trigger and recover all pipeline jobs from the admin dashboard,
on a laptop that regularly sleeps — without dropping to the database console.

| KR | Claim | Role | Served by |
|----|-------|------|-----------|
| **KR1** *(commit)* | **Recovery path** — any stuck `PipelineRun` state clears from the admin dashboard in one action. | recovery | **D1** |
| **KR2** *(commit)* | **Prevention** — every manual trigger of a scrape, enrichment, or status-check job produces a terminal `PipelineRun` result (`completed` or `failed`). | prevention | **D2** |

**Appetite:** ~6 nodes (the source initiative's `~10 issues`, regrouped — see shaping note below).
**Kill condition (from the initiative):** if orphaned `"running"` rows persist after one full
remediation cycle, accept console intervention as the operational model and cancel.

---

## How to read this plan top-down

```
initiative (this README)            ← goal + KRs
└── deliverable  D*/_deliverable.md  → milestone   (tagged serves_kr)
    └── node  N*.md                   → issue        (polymorphic: design-doc / story / …)
        └── task  - [ ] in node        → sub-issue    (`skeleton` opens the path; `acceptance` closes it)
```

Schema: [`docs/delivery-shape-contract.md`](../../../../docs/delivery-shape-contract.md).

## Tree

```
pipeline-recovery/
├── README.md                                       ← you are here (initiative root)
├── D1-recovery-action-in-the-dashboard/            → milestone · serves KR1 · Rule A1 TRIGGERED
│   ├── _deliverable.md
│   ├── N01 … recovery-semantics design doc            · design-doc        ← the branch
│   ├── N02 … clear a stuck run from the dashboard      · story · skeleton
│   └── N03 … action surfaces only when safe            · story
└── D2-manual-triggers-reach-a-terminal-state/      → milestone · serves KR2
    ├── _deliverable.md
    ├── N04 … scrape job always reaches terminal        · story · skeleton
    ├── N05 … extend the guarantee to enrich + status   · story
    └── N06 … soak: zero orphaned runs over the window  · story · [acceptance]
```

## Shaping note — appetite regrouped, not cut

The source initiative set an appetite of `~10 issues`; this plan shapes 6 nodes. No scope was
dropped — `delivery-shape` regroups the work by outcome rather than mirroring the initiative's
issue count. The prevention work (KR2) collapses from a per-category issue spread into two build
nodes (one category proven end-to-end, the guarantee extended to the other two) plus a soak
`acceptance` node, and the recovery work (KR1) folds its design decision into one `design-doc` node
ahead of two build nodes. The appetite is the cap; the node count is delivery-shape's regrouping
under it.

## Rule A1 branch + acceptance flag (what this trial exercises)

| Deliverable | Rule A1 trigger | First node | Flag exercised |
|-------------|-----------------|-----------|----------------|
| **D1** | met (shared `PipelineRun` state machine · one-way-door cancellation semantics · production-data mutation) | `design-doc` node, `delegates_to: design-doc` | — |
| **D2** | none (per-category guarantees are reversible, additive) | `story` node | **`acceptance`** on N06 — KR2's "zero orphans over the window" is a production soak observation no single child owns; `external_window` carries the 30-day soak |

## Hand-count manifest

| Tracker artefact | Source layer | Count |
|------------------|--------------|------:|
| Milestones | deliverables (`D*`) | **2** |
| Issues | nodes (`N*`) | **6** |
| Sub-issues | tasks (`- [ ]` lines) | **12** |
