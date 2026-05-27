# Trial plan — Per-task model routing

> **Trial fixture, not the operative plan.** Produced by `delivery-shape` in the N07 self-trial
> (ABA-288) to grade the D2 bet: does the skill bake framing in — acceptance criteria on every
> story, ≥1 walking-skeleton task — when fed only an initiative's goal + KRs? This file-set is the
> instrument, not a commitment to build this initiative now. See
> [`../FINDING.md`](../FINDING.md) for the experiment finding and per-trial re-prompt count.

**Source initiative:** [Per-task model routing — deliberate, not
ad-hoc](https://linear.app/ababushkin/project/per-task-model-routing-deliberate-not-ad-hoc-e64047e1cdf9)
· Linear `ABA` · Type 1 (methodology skill pack). Fed to `delivery-shape` as **goal + KRs only**.

---

## The bet (read this first — top-down starts at the outcome)

**Goal:** For Anton and any agent breaking work into tasks in Shaper, assign every task a model
tier and a risk profile at breakdown time without prompting — so model choice and review attention
are deliberate and reproducible rather than ad-hoc.

| KR | Claim | Role | Served by |
|----|-------|------|-----------|
| **KR1** *(commit)* | `references/task-sizing.md` exists with all required sections, and `planning-and-task-breakdown` cites it. | foundation | **D1** |
| **KR2** *(commit)* | After the layer lands, ≥90% of task lists filed under `docs/tasks/` carry a model-tier and risk annotation per the reference. | bet | **D2** |
| **KR3** *(commit)* | The routing is reproducible and discriminating: two independent applications of the rubric agree on (tier, review-flag) across a worked example + 5 held-out tasks, spanning ≥2 tiers. | brake | **D3** |

**Appetite:** ~6 nodes. **Kill condition (from the initiative):** across 2 consecutive cycles the
rubric neither changes nor defensibly justifies the model you'd have picked anyway (no decision
value), or the annotation is routinely skipped (KR2 < 50%) — ceremony, not behaviour change.

---

## How to read this plan top-down

```
initiative (this README)            ← goal + KRs
└── deliverable  D*/_deliverable.md  → milestone   (tagged serves_kr)
    └── node  N*.md                   → issue        (polymorphic: story / adr / experiment / …)
        └── task  - [ ] in node        → sub-issue    (`skeleton` task opens the path)
```

Directory nesting **is** the hierarchy; numeric `D*/N*` prefixes give deterministic order.
Schema: [`docs/delivery-shape-contract.md`](../../../../docs/delivery-shape-contract.md).

## Tree

```
per-task-model-routing/
├── README.md                                       ← you are here (initiative root)
├── D1-task-sizing-reference-decided-and-cited/     → milestone · serves KR1
│   ├── _deliverable.md
│   ├── N01 … write references/task-sizing.md          · story · skeleton
│   ├── N02 … ADR: routing-not-cascading + 5-axis rule · adr
│   └── N03 … cite the reference from the planning skill · story
├── D2-annotation-carried-by-every-filed-list/      → milestone · serves KR2
│   ├── _deliverable.md
│   ├── N04 … model + risk fields in the task template · story · skeleton
│   └── N05 … hook flags un-annotated task lists        · story
└── D3-routing-reproducible-and-discriminating/     → milestone · serves KR3
    ├── _deliverable.md
    └── N06 … rubric reproducibility + discrimination eval · experiment
```

## Shaping note — deferred scope

The source initiative listed 7 issues; three of them (thread the tier into `initiative-shape`,
add a tier/risk column to `roadmap-shape`, the sub-agent `model:` convention) broaden the
annotation to **adjacent surfaces not measured by any of the 3 KRs**. `delivery-shape` does not
place output that serves no KR on the plan (a deliverable serving no KR is "output without a bet",
product A3) — those three are deferred to the idea bank / a later cycle, not shaped here.

## Hand-count manifest

| Tracker artefact | Source layer | Count |
|------------------|--------------|------:|
| Milestones | deliverables (`D*`) | **3** |
| Issues | nodes (`N*`) | **6** |
| Sub-issues | tasks (`- [ ]` lines) | **14** |
