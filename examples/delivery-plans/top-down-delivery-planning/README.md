# Delivery plan — Top-down delivery planning

A worked delivery plan for one real, already-shaped initiative, **produced by hand** in the
walking-skeleton spike. It is the evidence half of the `delivery-shape` contract: the schema in
[`docs/delivery-shape-contract.md`](../../../docs/delivery-shape-contract.md) was read off *this*
file-set. (The spike that produced it — N01 — is itself a node in the plan; the plan is
self-describing.)

**Source initiative:** [Top-down delivery planning — framing baked in, foundational work never
silent](https://linear.app/ababushkin/project/top-down-delivery-planning-framing-baked-in-foundational-work-never-352e1fe0c3b8)
· Linear `ABA` · Type 1 (methodology skill pack). Source one-pager:
[`docs/ideas/delivery-shape.md`](../../../docs/ideas/delivery-shape.md).

---

## The bet (read this first — top-down starts at the outcome)

**Goal:** For Anton and any agent invoking Shaper, make a committed initiative produce its full
delivery plan top-down — deliverables → nodes (stories, capabilities, spikes, …) → verifiable
tasks — with framing baked in and foundational work never silently dropped.

| KR | Claim | Role | Served by |
|----|-------|------|-----------|
| **KR1** *(commit)* | A documented plan-artefact contract + a worked file-set exist, and a walk-script converts the file-set into the expected tracker manifest. | foundation | **D1** |
| **KR2** *(stretch)* | On a self-trial against 2 already-shaped initiatives, the emitted plan carries AC on every story and ≥1 explicit foundational/walking-skeleton task, at 0 framing re-prompts. | bet | **D2** |
| **KR3** *(commit)* | On a fixed eval set of 8–10 "plan a project" phrasings, delivery-shape is the selected skill, with 0 collisions against initiative-shape or planning-and-task-breakdown. | brake | **D3** |

**Appetite:** ~9 issues (= 9 nodes below). **Kill condition:** if the walking-skeleton spike (KR1)
can't produce a markdown file-set that walks deterministically and converts mechanically — i.e.
the seam needs a real schema or tool, not files — the standalone-markdown premise is wrong: stop
and re-shape the seam.

---

## How to read this plan top-down

Three layers, each mapping to one tracker artefact. Read outward from the bet above:

```
initiative (this README)            ← goal + KRs
└── deliverable  D*/_deliverable.md  → milestone   (tagged serves_kr)
    └── node  N*.md                   → issue        (polymorphic: spike/story/adr/experiment/ktlo/capability/…)
        └── task  - [ ] in node        → sub-issue    (`skeleton` task opens the path; `acceptance` task closes it)
```

Directory nesting **is** the hierarchy; numeric `D*/N*` prefixes give deterministic ordering.
Cross-references are relative paths plus front-matter `parent` / `serves_kr` back-links — so a
human descends by clicking and a script walks by reading front-matter. The schema is specified in
[`docs/delivery-shape-contract.md`](../../../docs/delivery-shape-contract.md).

## Tree

```
top-down-delivery-planning/
├── README.md                                              ← you are here (initiative root)
├── D1-walking-skeleton-spike-and-conversion-proof/        → milestone · serves KR1
│   ├── _deliverable.md
│   ├── N01 … hand-produce file-set + read off contract       · spike · skeleton
│   ├── N02 … walk-script: file-set → manifest                · story
│   └── N03 … ADR: new skill vs expand task-breakdown         · adr
├── D2-delivery-shape-skill-framing-baked-in/              → milestone · serves KR2
│   ├── _deliverable.md
│   ├── N04 … decompose, AC by default                        · story
│   ├── N05 … foundational prompt folded into skeleton        · story
│   ├── N06 … Rule A1 branch + up/down delegation             · story
│   └── N07 … self-trial against 2 initiatives                · experiment · [acceptance]
└── D3-trigger-reliability-and-discoverability/           → milestone · serves KR3
    ├── _deliverable.md
    ├── N08 … trigger-eval set + harness, 0 collisions        · story
    └── N09 … register in README + flowchart                  · ktlo
```

## Node-type coverage (grounded — not fabricated)

Nodes are **polymorphic**: each carries the completion criterion its work calls for, not always a
story. This example genuinely exercises five node types. The types it does *not* exercise are not
invented here — they live in the contract's to-fill appendix, to be grounded when an initiative
that uses them is shaped.

| Type | Completion-criterion form | Exercised by |
|------|---------------------------|--------------|
| `spike` | decision + stop condition | N01 |
| `story` | acceptance criteria (Cohn form) | N02, N04, N05, N06, N08 |
| `adr` | accepted decision record | N03 |
| `experiment` | hypothesis + success metric | N07 |
| `ktlo` | none (roadmap A5 carve-out) | N09 |
| _capability, slo, migration, incident, deprecation, compliance_ | _see contract appendix_ | _not exercised by this initiative_ |

`capability` is a genuine node `type` (completion form `the-capability-spec`), but this initiative
exercises none: every capability here was reducible to its child nodes and was absorbed into the
deliverable prose (see the contract's *Design notes*). It grounds when a capability carries a spec
its children don't.

**Flags** (orthogonal to type — applied on top of any node type):

| Flag | Forms | When it applies |
|------|-------|-----------------|
| `skeleton` | front-matter `skeleton: true` + task tag `` `skeleton` `` | Opens the end-to-end path; foundational work folded in |
| `acceptance` | front-matter `acceptance: true` + task tag `` `acceptance` `` | Closes the parent's cross-seam criterion. Exists only when parent's Done is irreducible to ∀child.done. Never re-runs child criteria. |

`acceptance` in this plan: **N07** carries `acceptance: true` (verifies D2). Its experiment finding
— confirmed or falsified — is D2's aggregate Done condition (KR2 observed). The acceptance task
closes last, making D2's milestone reaching 100% coincide with the KR observation.

## Hand-count manifest

The mechanical-conversion proof (gate issue ABA-282) requires `bin/walk-delivery-plan` to emit
counts equal to these hand-counted totals:

| Tracker artefact | Source layer | Count |
|------------------|--------------|------:|
| Milestones | deliverables (`D*`) | **3** |
| Issues | nodes (`N*`) | **9** |
| Sub-issues | tasks (`- [ ]` / `- [x]` lines) | **19** |

If the walk-script prints anything other than `3 / 9 / 19`, either the file-set drifted from this
count or the schema doesn't walk deterministically — investigate before declaring the gate passed.
