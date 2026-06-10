# Delivery plan — drain-cycle supervises; the pack owns the workflow

The delivery hierarchy for initiative C of the lifecycle expansion, emitted by `delivery-shape`
per [`docs/delivery-shape-contract.md`](../../../docs/delivery-shape-contract.md).

**Source initiative:** [drain-cycle supervises; the pack owns the
workflow](https://linear.app/ababushkin/project/drain-cycle-supervises-the-pack-owns-the-workflow-0f0222d99392)
· Linear `ABA` · Type 2 (personal product, single-user) · dominant model tier Balanced (the
prompt/skill contract design is the Frontier exception). Review package:
[`docs/ideas/lifecycle-expansion.md`](../../../docs/ideas/lifecycle-expansion.md) §4. Third of
three; depends on initiative A ([issues-drain-end-to-end](../issues-drain-end-to-end/README.md)).

---

## The bet (read this first — top-down starts at the outcome)

**Goal:** For Anton (single user), make unattended cycle drains run with the supervisor owning
only process concerns — spawn, guardrails, halt, resume, grade — so any vendor's worker can
follow the pack's workflow prose unchanged.

| KR | Claim | Role | Served by |
|----|-------|------|-----------|
| **KR1** *(stretch)* | A full cycle drains to completion with the worker prompt reduced to issue context + a single skill pointer (zero inlined workflow steps), at the execution initiative's quality bar (no manual fix commits). Target: ≥1 clean full-cycle drain, measured over the first 2 cycles after the re-scope lands (prompt template diff + `drain-cycle grade`). | bet | **D3** |
| **KR2** *(commit)* | Every worker exit in the window produces a run-log entry with exit state, verify/prep verdicts, and halt_reason where applicable; zero uninspectable drains (schema check one-liner over `~/.drain-cycle/runs/*.json`). | foundation | **D2** |
| **KR3** *(commit)* | The supervisor carries zero workflow prose: worker prompt template ≤15 lines, no skill-procedure steps, test suite green (`wc -l` + grep for procedure verbs + pytest exit code). | brake | **D1** |

**Appetite:** ~7 issues. This plan emits **5 nodes** — two under, deliberately: the process
concerns the supervisor keeps (spawn, guardrails, halt, resume, grade) already exist in
drain-cycle, so the re-scope is subtractive — work appears only where something is decided
(N01), removed (N02), or wired (N03–N04), plus the validation experiment (N05). Flagged here
rather than padded; if the contract design surfaces a missing process concern, that becomes a
new node, not a silent scope creep.

**Kill condition:** If pointer-only prompts cause 3 consecutive halted drains that the inlined
prompt would have completed, stop — restore the inlined tail and keep the re-scope to guardrails
and logging only.

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
Default working order is D1 → D2 → D3. **N01 blocks every build node** (D1's design doc decides
the contract D2 builds against), named as `> **Blocked by:**` callouts in the dependent nodes.
**Cross-initiative dependencies on A** are also named per node: N02 needs A's entry skill (N05)
and pointer swap (N10) landed; N03 extends A's D2 skills; N05 follows A's validation drains
(N09). Bind these as Linear blockedBy edges — drain-cycle topo-sorts a run on them, so they also
fix the Graphite stack order.

## Tree

```
drain-cycle-thin-supervisor/
├── README.md                                       ← you are here (initiative root)
├── D1-supervisor-sheds-workflow-prose/             → milestone · serves KR3
│   ├── _deliverable.md
│   ├── N01 … thin-supervisor contract design doc      · design-doc (Rule A1)
│   └── N02 … pointer-only prompt template             · story · [skeleton]
├── D2-every-drain-inspectable/                     → milestone · serves KR2
│   ├── _deliverable.md
│   ├── N03 … pack skills emit verdicts into handoff   · story
│   └── N04 … supervisor records verdicts on every exit · story
└── D3-full-cycle-on-pointer-prompt/                → milestone · serves KR1
    ├── _deliverable.md
    └── N05 … validation: 2 cycles on the pointer prompt · experiment · [acceptance]
```

## Node-type coverage

| Type | Completion-criterion form | Exercised by |
|------|---------------------------|--------------|
| `story` | acceptance criteria (Cohn form) | N02, N03, N04 |
| `design-doc` | the accepted design doc (Rule A1 branch) | N01 |
| `experiment` | hypothesis + success metric | N05 |

**Flags** (orthogonal to type): **N02** carries `skeleton: true` — the pointer-only template
smoke-drained through one issue is the initiative's walking skeleton: it proves the
prompt → entry-skill → handoff → submit seam with the thinnest possible supervisor. **N05**
carries `acceptance: true` (verifies D3) — D3's Done is irreducible to ∀child.done: the prompt
can be ≤15 lines and the verdicts wired, and a full cycle can still fail to drain. Close it last.

## Repo split

N02 and N04 land in **drain-cycle**; N03 lands in **agent-skills-shaper**; N01 (the design doc)
and N05 (the experiment finding) are authored in agent-skills-shaper with their subjects in both
repos. Same-repo issues drained in one run chain into one Graphite stack — the blockedBy edges
above keep each stack's review order sane.

## Hand-count manifest

`bin/walk-delivery-plan` must emit counts equal to these hand-counted totals:

| Tracker artefact | Source layer | Count |
|------------------|--------------|------:|
| Milestones | deliverables (`D*`) | **3** |
| Issues | nodes (`N*`) | **5** |
| Sub-issues | tasks (`- [ ]` / `- [x]` lines) | **12** |

If the walk-script prints anything other than `3 / 5 / 12`, the file-set drifted from this
count or the layout stopped walking deterministically — investigate before declaring the plan
emitted.
