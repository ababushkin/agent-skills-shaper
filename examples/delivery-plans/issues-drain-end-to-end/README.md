# Delivery plan — Issues drain end-to-end on first-party skills

The delivery hierarchy for initiative A of the lifecycle expansion, emitted by `delivery-shape`
per [`docs/delivery-shape-contract.md`](../../../docs/delivery-shape-contract.md).

**Source initiative:** [Issues drain end-to-end on first-party
skills](https://linear.app/ababushkin/project/issues-drain-end-to-end-on-first-party-skills-be562671c8d8)
· Linear `ABA` · Type 1 (methodology skill pack) · dominant model tier Balanced. Source package:
[`docs/ideas/lifecycle-expansion.md`](../../../docs/ideas/lifecycle-expansion.md) §4.

---

## The bet (read this first — top-down starts at the outcome)

**Goal:** For drain-cycle workers (and Anton driving interactively), make every picked-up Linear
issue flow from pickup to a merged, reviewable PR on Shaper skills alone — review trail attached,
no rescue by a human and no reliance on third-party packs.

| KR | Claim | Role | Served by |
|----|-------|------|-----------|
| **KR1** *(stretch)* | ≥4 of the next 5 drained issues reach Done with a merged PR and zero manual fix commits after the worker's final push, with the full review trail present (verify verdict, What/Why/Focus PR body, review-summary comment). | bet | **D2** |
| **KR2** *(commit)* | The review/verify skills surface ≥9 of 10 seeded Critical/Required findings when run against fixture diffs with known defects, via `bin/grade-execution-review fixtures/execution-review/`. | foundation | **D1** |
| **KR3** *(commit)* | 100% of drained issues in the window invoke the new execution skills and zero invoke superpowers/agent-skills; both packs uninstalled and zero references to their skill names remain in the Shaper repo or drain-cycle prompts. | brake | **D3** |

**Appetite:** ~10 issues. This plan emits **11 nodes** — one over, carried by D3's two
deliberately thin cutover nodes (different repos, so they don't merge). Flagged here rather than
silently absorbed; if the cycle squeezes, N11's audit task folds into N09's acceptance task.

**Kill condition:** If, after the execution skills ship, 3 consecutive drained issues require
manual fix commits or fall back to third-party pack skills, stop — reinstall agent-skills, keep
Shaper shaping-only, and fold the learnings into the pack's README.

---

## How to read this plan top-down

Three layers, each mapping to one tracker artefact. Read outward from the bet above:

```
initiative (this README)            ← goal + KRs
└── deliverable  D*/_deliverable.md  → milestone   (tagged serves_kr)
    └── node  N*.md                   → issue        (polymorphic: story/adr/design-doc/experiment/…)
        └── task  - [ ] in node        → sub-issue    (`skeleton` task opens the path; `acceptance` task closes it)
```

Directory nesting **is** the hierarchy; numeric `D*/N*` prefixes give deterministic ordering.
Default working order is D1 → D2 → D3, with two cross-deliverable dependencies named as
`> **Blocked by:**` callouts in the dependent nodes: N09's validation drains need N10's prompt
pointer in place first, and N11's audit reads N09's transcripts.

## Tree

```
issues-drain-end-to-end/
├── README.md                                          ← you are here (initiative root)
├── D1-review-gate-proven-on-seeded-defects/           → milestone · serves KR2
│   ├── _deliverable.md
│   ├── N01 … fixture corpus + review grader              · story · skeleton
│   ├── N02 … ADR: persona contract + dispatch protocol   · adr
│   └── N03 … personas + review fan-out skill             · story
├── D2-execution-workflow-drains-issues/               → milestone · serves KR1
│   ├── _deliverable.md
│   ├── N04 … execution-workflow design doc (Rule A1)     · design-doc
│   ├── N05 … entry skill — the front door                · story
│   ├── N06 … build skill — RED/GREEN/commit loop         · story
│   ├── N07 … debugging + simplification skills           · story
│   ├── N08 … PR finishing — Graphite-first, git fallback · story
│   └── N09 … validation drains (5 issues, ≥4/5)          · experiment · [acceptance]
└── D3-cutover-off-third-party-packs/                  → milestone · serves KR3
    ├── _deliverable.md
    ├── N10 … drain-cycle prompt pointer                  · story
    └── N11 … uninstall both packs + purge references     · story
```

## Node-type coverage

| Type | Completion-criterion form | Exercised by |
|------|---------------------------|--------------|
| `story` | acceptance criteria (Cohn form) | N01, N03, N05, N06, N07, N08, N10, N11 |
| `adr` | accepted decision record | N02 |
| `design-doc` | the accepted design doc (Rule A1 branch) | N04 |
| `experiment` | hypothesis + success metric | N09 |

This is the first plan to exercise the `design-doc` type on real work (the Rule A1 branch was
previously grounded only by the `_tests/rule-a1-branch/` fixture).

**Flags** (orthogonal to type): **N01** carries `skeleton: true` — the initiative's walking
skeleton proves the fixture → persona-run → grade seam end-to-end before any real persona exists.
**N09** carries `acceptance: true` (verifies D2) — D2's Done is irreducible to ∀child.done:
every skill can individually pass and the workflow still fail end-to-end, so the live-drain
experiment closes the deliverable. Close it last.

## Hand-count manifest

`bin/walk-delivery-plan` must emit counts equal to these hand-counted totals:

| Tracker artefact | Source layer | Count |
|------------------|--------------|------:|
| Milestones | deliverables (`D*`) | **3** |
| Issues | nodes (`N*`) | **11** |
| Sub-issues | tasks (`- [ ]` / `- [x]` lines) | **29** |

If the walk-script prints anything other than `3 / 11 / 29`, the file-set drifted from this
count or the layout stopped walking deterministically — investigate before declaring the plan
emitted.
