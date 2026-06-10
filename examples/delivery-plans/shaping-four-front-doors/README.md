# Delivery plan — Shaping consolidates to four dense front doors

The delivery hierarchy for initiative B of the lifecycle expansion, emitted by `delivery-shape`
per [`docs/delivery-shape-contract.md`](../../../docs/delivery-shape-contract.md).

**Source initiative:** [Shaping consolidates to four dense front
doors](https://linear.app/ababushkin/project/shaping-consolidates-to-four-dense-front-doors-9c8a65552b93)
· Linear `ABA` · Type 1 (methodology skill pack) · dominant model tier Balanced (the front-door
information architecture is the Frontier exception). Review package:
[`docs/ideas/lifecycle-expansion.md`](../../../docs/ideas/lifecycle-expansion.md) §3. Second of
three; follows initiative A ([issues-drain-end-to-end](../issues-drain-end-to-end/README.md)),
precedes initiative C ([drain-cycle-thin-supervisor](../drain-cycle-thin-supervisor/README.md)).

---

## The bet (read this first — top-down starts at the outcome)

**Goal:** For Shaper's invokers (Anton and agents), make the shaping half reachable through four
front doors — `shape:idea`, `shape:project`, `shape:design`, `shape:delivery` — each dense,
gate-complete, and under the length cap, with every pruned skill's content either absorbed or
deliberately deleted.

| KR | Claim | Role | Served by |
|----|-------|------|-----------|
| **KR1** *(bet)* | Every shaping skill fits the cap: 4 front doors ≤300 lines each, zero skills over 300, total shaping footprint ≤2,200 lines. Baseline (verified 2026-06-10): 14 skills / 3,086 lines; 3 over cap — plan-review 369, initiative-shape 310, roadmap-shape 303. Measured by `wc -l` over the measured set the N01 design doc pins; counts recorded in the cycle retro note. | bet | **D1** |
| **KR2** *(brake)* | The plan-review benchmark holds after reform: the 5-scenario eval set re-run scores ≥90% pass with-skill. Baseline 93% ± 2% (n=3, Sonnet 4.6, `docs/benchmarks.md`); results appended to `docs/benchmarks.md`. | brake | **D2** |
| **KR3** *(brake)* | Zero dangling references to deleted/folded skills in README, install.sh, commands, hooks, or cross-skill citations: `grep -rn 'roadmap-shape\|backlog-manage\|app-calibrate' --include='*.md' .` returns only intentional predecessor-frontmatter mentions. | brake | **D3** |

**Appetite:** ~8 issues. This plan emits **8 nodes / 19 tasks** — on appetite: one IA decision
(N01), four doors (N02–N05), the utility compression (N06), the benchmark brake (N07), and the
reference sweep (N08).

**Kill condition:** If a front door can't absorb its folded skills under 350 lines without
dropping a `[GATE]`, or the plan-review benchmark falls below 80% after two repair attempts,
stop — keep the flat 14-skill layout and ship style reform only. The first clause is watched at
N05 (the heaviest fold: 637 source lines → one door); the second at N07.

---

## How to read this plan top-down

Three layers, each mapping to one tracker artefact. Read outward from the bet above:

```
initiative (this README)            ← goal + KRs
└── deliverable  D*/_deliverable.md  → milestone   (tagged serves_kr)
    └── node  N*.md                   → issue        (polymorphic: story/design-doc/experiment)
        └── task  - [ ] in node        → sub-issue    (`skeleton` task opens the path; `acceptance` task closes it)
```

Directory nesting **is** the hierarchy; numeric `D*/N*` prefixes give deterministic ordering.
Default working order is D1 → D3 → D2 (the benchmark brake measures final state, so it closes).
**N01 blocks every other node** (D1's design doc fixes the absorption map, survivor manifest,
and measured set everything else builds against), named as `> **Blocked by:**` callouts in the
dependent nodes. **One cross-initiative dependency on A**: N01 consumes the verb-namespace
naming table A's N04 design doc decides — bind as a Linear blockedBy edge onto ABA-361.

## Tree

```
shaping-four-front-doors/
├── README.md                                  ← you are here (initiative root)
├── D1-four-front-doors-under-cap/             → milestone · serves KR1
│   ├── _deliverable.md
│   ├── N01 … front-door IA design doc            · design-doc (Rule A1)
│   ├── N02 … shape:delivery front door            · story · [skeleton]
│   ├── N03 … shape:idea front door                · story
│   ├── N04 … shape:project front door             · story
│   ├── N05 … shape:design front door              · story
│   └── N06 … utilities under the cap              · story
├── D2-benchmark-holds-after-reform/           → milestone · serves KR2
│   ├── _deliverable.md
│   └── N07 … benchmark re-run post-reform        · experiment · [acceptance]
└── D3-no-dangling-references/                 → milestone · serves KR3
    ├── _deliverable.md
    └── N08 … reference sweep + fresh-install check · story
```

## Node-type coverage

| Type | Completion-criterion form | Exercised by |
|------|---------------------------|--------------|
| `story` | acceptance criteria (Cohn form) | N02, N03, N04, N05, N06, N08 |
| `design-doc` | the accepted design doc (Rule A1 branch) | N01 |
| `experiment` | hypothesis + success metric | N07 |

**Flags** (orthogonal to type): **N02** carries `skeleton: true` — re-housing the already-compliant
`delivery-shape` (266 lines) as the first door proves the entire front-door seam (skill dir →
install.sh symlink → command wrapper → `using-this-pack` route) end-to-end before the heavy
folds start. **N07** carries `acceptance: true` (verifies D2) — every door can be under cap and
every reference clean, and the reform can still have degraded plan-review's behaviour; only the
benchmark observes that. Close it last.

## Repo split

Every node lands in **agent-skills-shaper** — this initiative touches no other repo. Issues
drained in one run chain into a single Graphite stack; the blockedBy edges below keep its review
order sane (IA doc → doors → utilities → sweep → benchmark).

## Hand-count manifest

`bin/walk-delivery-plan` must emit counts equal to these hand-counted totals:

| Tracker artefact | Source layer | Count |
|------------------|--------------|------:|
| Milestones | deliverables (`D*`) | **3** |
| Issues | nodes (`N*`) | **8** |
| Sub-issues | tasks (`- [ ]` / `- [x]` lines) | **19** |

If the walk-script prints anything other than `3 / 8 / 19`, the file-set drifted from this
count or the layout stopped walking deterministically — investigate before declaring the plan
emitted.
