# Test plan — Rule A1 design-doc branch (both branches exercised)

A **fixture**, not a real initiative. It exists to exercise both arms of `delivery-shape`'s
Rule A1 branch in one walkable file-set:

- **D1** meets a Rule A1 trigger (touches a shared payment vault, a one-way-door tokenisation
  choice, PCI compliance) → its first node is a `design-doc` node that delegates to the
  `design-doc` skill **before** the build node is picked up.
- **D2** meets no trigger (one reversible UI surface, ≤2 slices) → it proceeds straight to a
  `story` node on goal + deliverable, with **no** design-doc node.

The fixture walks under `bin/walk-delivery-plan` and passes `bin/check-plan-framing`, so the
branch is provably expressible in the artefact schema — not just described in the skill prose.

---

## The bet (fixture)

**Goal:** For returning shoppers, cut checkout abandonment by making a saved payment method
reusable across sessions.

| KR | Claim | Role | Served by |
|----|-------|------|-----------|
| **KR1** *(commit)* | A returning shopper completes checkout with a stored card — observed end-to-end in logs. | bet | **D1** |
| **KR2** *(commit)* | The saved card pre-fills at checkout with no regression in the checkout surface. | foundation | **D2** |

**Appetite:** ~3 issues. **Kill condition:** if a stored token cannot be replayed at checkout
without re-collecting card data, the reuse premise is wrong — stop and re-shape.

## Tree

```
rule-a1-branch/
├── README.md                                       ← initiative root (this file)
├── D1-tokenized-card-vault/                         → milestone · serves KR1 · Rule A1 TRIGGERED
│   ├── _deliverable.md
│   ├── N01 … card-vault design doc (before build)     · design-doc        ← the branch
│   └── N02 … store + replay a card token              · story · skeleton
└── D2-reuse-card-at-checkout/                       → milestone · serves KR2 · Rule A1 NOT triggered
    ├── _deliverable.md
    └── N03 … pre-fill the saved card at checkout      · story
```

## Branch coverage

| Deliverable | Rule A1 trigger | First node | What it proves |
|-------------|-----------------|-----------|----------------|
| **D1** | met (shared infra · one-way door · compliance) | `design-doc` node, `delegates_to: design-doc` | design-doc-worthy work gets a design doc **before** task breakdown |
| **D2** | none | `story` node | non-triggering work proceeds on goal + deliverable, no design-doc node |

## Hand-count manifest

| Tracker artefact | Source layer | Count |
|------------------|--------------|------:|
| Milestones | deliverables (`D*`) | **2** |
| Issues | nodes (`N*`) | **3** |
| Sub-issues | tasks (`- [ ]` lines) | **6** |
