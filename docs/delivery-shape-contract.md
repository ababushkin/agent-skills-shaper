# delivery-shape — plan-artefact contract

The schema for a **delivery plan**: the set of cross-referenced markdown files that turn one
committed initiative into an ordered, verifiable delivery hierarchy — deliverable → node → task —
that a human reads top-down and a deterministic reader walks bottom-up into a tracker manifest.

This contract was **read off a worked example**, not designed in the abstract:
[`examples/delivery-plans/top-down-delivery-planning/`](../examples/delivery-plans/top-down-delivery-planning/).
Read that example alongside this spec — every rule here points at a node that demonstrates it.

> **Tool-agnostic by rule.** This contract names no tracker, language, or runtime. It describes
> *file-set structure* and *tracker-artefact classes* (milestone-class / issue-class /
> sub-issue-class). Binding those classes to a concrete tracker is the **adapter's** job and lives
> in another repo. Emitted plans (the example) may name concrete tools; this contract may not.

---

## The three layers

| Layer | Lives as | Tracker-artefact class | Completion criterion |
|-------|----------|------------------------|----------------------|
| **Deliverable** | a directory `D*/` with `_deliverable.md` | milestone-class | its served KR is observed |
| **Node** | a file `N*.md` | issue-class | **type-dependent** (see vocabulary) |
| **Task** | a `- [ ]` / `- [x]` line inside a node | sub-issue-class | the checkbox + its description |

A node is **polymorphic**: it is not always a user story. It carries whichever completion
criterion its work calls for — a story carries acceptance criteria, a spike carries a decision and
a stop condition, a capability carries its own spec, and so on. This is the central claim the
example exists to prove. (A capability is one of these node types, not a separate structural
layer — see *Design notes* for why the earlier four-layer model was collapsed.)

---

## Schema element 1 — Directory layout

Directory nesting **is** the hierarchy. Depth encodes layer; nothing else needs to:

```
<initiative-slug>/
├── README.md                  initiative root: goal + KRs + how-to-read + tree + hand-count manifest
├── D<n>-<slug>/               deliverable      → milestone-class
│   ├── _deliverable.md        the deliverable's own front-matter + statement
│   ├── N<nn>-<slug>.md        node             → issue-class
│   └── …
└── …
```

Rules:

- **Numeric prefixes** (`D1`, `N03`) give a deterministic reading and walking order. Pad node
  numbers (`N01`) so lexical sort = intended sort past nine nodes.
- **Layer-header files** are underscore-prefixed (`_deliverable.md`) so they sort
  first within their directory and are unambiguously the layer object, not a node.
- **Node files** are the only `N*.md` files; one node per file.
- The **root `README.md`** is the single top-down entry point: it carries the goal + KRs verbatim
  (read top-down starts at the outcome, not at task 1), the rendered tree, and the **hand-count
  manifest** the walk-script must reproduce.

## Schema element 2 — Cross-reference convention

**Relative paths + directory hierarchy + front-matter back-links.** Three reinforcing signals, no
hand-maintained index:

- **Down** — a parent links to each child by relative path (`_deliverable.md` lists its
  nodes; `README.md` renders the whole tree).
- **Up** — every file's front-matter carries `parent:` (the enclosing layer) so a reader that
  starts at any node can climb without scanning directories.
- **To the bet** — every deliverable and node carries `serves_kr:` naming the KR it serves, so the
  outcome trace is explicit at every layer, not inferred from position.
- **Ordering within a deliverable** — numeric `N*` prefixes give the default reading/working order.
  A hard dependency beyond that order is named in prose as a `> **Blocked by:** <node-id>` callout
  in the dependent node's body — e.g. the build nodes of a Rule A1 deliverable are *blocked by* its
  `design-doc` node. This is **intentionally prose-only**: it is a human-read sequencing signal, not
  a structured front-matter key, and the walk-script does not parse or enforce it (the manifest is
  order-independent). If inter-node dependencies ever need machine enforcement, that is the trigger
  to add a structured key — until then, the prose callout is the convention.

The **manifest is derived, never authored**: a walk-script reconstructs milestone/issue/sub-issue
counts from the directory structure + front-matter. The hand-count in the README exists only as
the oracle the derived manifest is checked against. (A hand-maintained manifest file was
considered and rejected — it is a second source of truth that drifts; see *Design notes*.)

## Schema element 3 — Per-node tags (front-matter)

Every layer file opens with YAML front-matter. The load-bearing tags:

```yaml
layer:        deliverable | node                   # which layer this file is
id:           D1 | N03                              # stable within the plan
type:         <node-type>                          # NODE FILES ONLY — the polymorphic node discriminator (see vocabulary); `capability` is one of these types
title:        <one line>
parent:       <relative path or id of enclosing layer>
serves_kr:    KR<n>                                # deliverable↔KR and node↔KR trace
maps_to:      <tracker-artefact class>             # milestone/issue/sub-issue class
skeleton:     true | (absent)                      # NODE-LEVEL: is this the walking-skeleton node?
acceptance:   true | (absent)                      # NODE-LEVEL: does this node verify its parent's cross-seam criterion?
external_window: <external constraint> | none      # see constraints — never effort-in-days
completion:
  form:       <completion-criterion form>          # the type-appropriate form (see vocabulary)
  criterion:  <the observable criterion, by form>
  verifies_parent: <parent-layer-id> | (absent)   # when acceptance: true — which parent's criterion this node closes
delegates_to: <rule or skill that owns this node type's discipline>   # REQUIRED on every node — fires at pickup, not at emission
```

The five tags the contract is required to pin down:

1. **node `type`** — selects the completion-criterion form and the delegation target (vocabulary below).
2. **deliverable↔KR** — `serves_kr:` on each `_deliverable.md` (and echoed on nodes). Every
   deliverable serves exactly one KR; this is the outcome spine.
3. **completion-criterion** — `completion.form` + `completion.criterion`, shaped by `type`.
4. **task↔skeleton flag** — at the **task** level, the walking-skeleton/foundational task is marked
   with a leading `` `skeleton` `` tag inside its checklist line. At the **node** level, the node
   that *is* the initiative's walking skeleton carries `skeleton: true` in front-matter. Foundational
   / toolchain work is **folded into** the skeleton task's description — never a silent setup task
   before it (mirrors `planning-and-task-breakdown`'s walking-skeleton-first rule). There is no
   `foundational` node type: foundational work is a property of the skeleton **task**, not a node.

5. **task↔acceptance flag** — at the **task** level, the aggregate/cross-seam-verification task is
   marked with a leading `` `acceptance` `` tag inside its checklist line, mirroring `` `skeleton` ``
   exactly. At the **node** level, a node that verifies its **parent's** emergent or cross-seam
   completion criterion carries `acceptance: true` in front-matter plus
   `completion.verifies_parent: <parent-id>` naming which parent layer it closes. `skeleton` opens
   the end-to-end path; `acceptance` closes it.

   **Grounding rule (reducibility-gated):** an `acceptance` node or task exists **only when the
   parent's "Done when" is irreducible to ∀child.done** — a KR moving, a journey crossing child
   seams, an integration no single child owns. When the criterion is the sum of its children, there
   is no acceptance node — the parent closing is the verification. (Same reducibility test used to
   decide when `capability` is a node vs absorbed prose, applied to the completion axis instead of
   the structure axis.) An acceptance node **never re-runs child criteria** — that is the redundancy
   guard.

   **Linear mapping:** the `acceptance` flag maps to a Linear label (orthogonal to structure, like
   `skeleton`). Close the acceptance node **last**: this makes the milestone reaching 100% coincide
   with aggregate verification passing — no special field or tooling required. See `N07` for the
   worked example.

Task lines are the sub-issue layer. A task is `- [ ] ` or `- [x] `; an optional leading code-span
flags it. `` `skeleton` `` marks the walking-skeleton/foundational task; `` `acceptance` `` marks
the aggregate-verification task (flag 5 above). Examples:
`` - [ ] `skeleton` — walk the tree, read front-matter, print counts (toolchain folded in) ``.
`` - [ ] `acceptance` — evaluate aggregate result; write finding (confirmed / falsified) ``.

---

## Node-type vocabulary

`delivery-shape` **selects** the node type and **delegates** its discipline to the rule or skill
that owns it. It does **not** re-author SLO targets, ADR structure, spike protocol, or postmortem
format — that guarantees drift (agentic P7). Each type below names its completion-criterion form
and its delegation target.

### Grounded — exercised by the worked example

Each row cites the example node that demonstrates it. These are **node `type`s** — the polymorphic
discriminator carried on `N*.md` files. A delegation target is either a **Shaper rule** (always
present in this repo) or a **skill** — skills marked *(skill where available)* are not yet
Shaper-native, so the rule beside them is the durable fallback a future agent can rely on.

| `type` | Completion-criterion form | Delegates to | Demonstrated by |
|--------|---------------------------|--------------|-----------------|
| `spike` | decision + stop condition | `eng-principles-universal.md` Rule C5 (time-box; written decision at the box) | `N01` |
| `story` | acceptance criteria, in a grounded story form | `planning-and-task-breakdown` (per-node task breakdown) | `N02`, `N04`, `N05`, `N06`, `N08` |
| `design-doc` | an accepted design doc (problem / alternatives / decision / NFRs / operability) | `design-doc`; `eng-principles-universal.md` Rule A1 (design-doc trigger) | N01 of the `_tests/rule-a1-branch/` fixture (not the worked example — see below) |
| `adr` | an accepted decision record (Context / Decision / Consequences) | `eng-principles-universal.md` Rule A3 (ADR) + D3 (living ADRs); `documentation-and-adrs` *(skill where available)* | `N03` |
| `experiment` | hypothesis + success metric (confirmed / falsified) | `product-spike` (experiment discipline) | `N07` |
| `ktlo` | **none** — carve-out | ops slot (no outcome framing; roadmap A5) | `N09` |

`design-doc` is the **Rule A1 branch**: `delivery-shape` tests each deliverable against Rule A1's
triggers (more than ~5 nodes, a one-way-door decision, shared infrastructure, or meaningful
user/cost/compliance impact — agentic P8's slice-count reading of the "four weeks" trigger) and,
when one holds, emits a `design-doc` node as the deliverable's **first** node, blocking the build
nodes' task breakdown until the design doc is accepted. It is distinct from `adr`: a full design
doc (delegated to the `design-doc` skill) versus a single accepted decision record (delegated to
the ADR discipline) — Rule A1's "a short ADR may suffice" is the lesser branch. The worked example
does not exercise it (none of its deliverables trips a Rule A1 trigger), so it is grounded by the
[`_tests/rule-a1-branch/`](../examples/delivery-plans/_tests/rule-a1-branch/) fixture, which
exercises both arms of the branch — one deliverable that triggers a design-doc node and one that
does not.

`capability` **is** a node `type` — a spec-shaped node broken into task-slices, completion form
`the-capability-spec`. This initiative exercises none: every capability in the worked example was
reducible to its child nodes and was absorbed into deliverable prose (see *Design notes*), so
`capability` sits in the to-fill appendix below rather than the grounded table. It grounds the
moment a capability carries a spec *not* reducible to its children — at which point it becomes a
node, a peer of the `story` / `spike` / … nodes under its deliverable.

### To-fill appendix — not exercised by this initiative

These types are **named, not fabricated**: this methodology-pack initiative has no runtime SLO, no
production migration, no incident, no deprecation, and no external compliance obligation, so the
worked example contains none. `capability` is here for a different reason — not domain absence but
**structural reducibility** (every capability collapsed into its child nodes, as noted above). The
completion-criterion form and delegation target are recorded so the vocabulary is ready when an
initiative that genuinely exercises them is shaped — at which point the row moves up to *Grounded*
with a citation.

| `type` | Completion-criterion form | Delegates to | Ground when… |
|--------|---------------------------|--------------|--------------|
| `capability` | `the-capability-spec` | `planning-and-task-breakdown` (slice the capability spec into tasks) | a capability carries a spec not reducible to its child nodes |
| `slo` | numeric target (latency/availability/error-budget) | `eng-principles-universal.md` Rule A4 (measurable NFR) + A5 (fitness function) | a production/observability initiative is planned |
| `migration` | rollback plan **per phase** + cutover criterion | `eng-principles-universal.md` Rule A6 (rollback); `deprecation-and-migration` *(skill where available)* | a data/system migration is planned |
| `deprecation` | removal criterion + external **notice period** | `eng-principles-universal.md` Rule A6 (rollback); `deprecation-and-migration` *(skill where available)* | an API/feature sunset is planned |
| `incident` | blameless postmortem (contributing factors, remediations) | `eng-principles-universal.md` Rule D1 | the plan absorbs incident-driven remediation |
| `compliance` | obligation met by an external **deadline** | ops slot / Rule A5 carve-out | a legal/partner obligation enters the plan |

> **Do not invent a node of an appendix type to "cover" it.** A plan exercises a type only when the
> initiative's real work calls for it. Padding the example with a fake SLO would make the schema
> look more proven than it is — the exact failure the grounding rule prevents.

### Completion-criterion forms (the menu)

`acceptance-criteria` · `decision+stop-condition` · `decision-record` · `the-design-doc` ·
`hypothesis+success-metric` · `numeric-target` · `rollback-per-phase` · `the-capability-spec` ·
`none` (carve-out). A node's `completion.form` is one of these, fixed by its `type`.

---

## Constraints on the contract

- **Grounded story form only.** A `story` node uses a recognised template — Cohn
  ("As a [role], I want [capability], so that [benefit]") or a job story
  ("When [situation], I want to [motivation], so I can [outcome]"). A custom "so… so…" chain is
  not permitted: it hides the role and the benefit, the two things acceptance criteria are checked
  against. See `N02`/`N04`/`N05`/`N06`/`N08` for the Cohn form in use.
- **External windows, never effort-in-days.** The optional `external_window` field carries *only*
  genuine external constraints — a deprecation notice period, a legal or compliance deadline, a
  canary soak time, an embargo. It must **never** carry an effort or duration estimate in
  days/weeks (agentic P8: effort is measured in slices and gates, not calendar time). Every node in
  the worked example is `external_window: none` because this initiative has no external constraint;
  the appendix types (`deprecation`, `compliance`, `slo` soak) are where the field goes non-`none`.
  Sizing lives in the **appetite** (issue count = node count) and in **task granularity**, not in a
  per-node time field.
- **Tool-agnostic templates.** This contract and any template it ships name no tracker, language, or
  runtime. An emitted plan (the example) may name concrete tools in its prose and in `maps_to`
  values; the contract describes only the artefact classes those tools implement.
- **Select and delegate; never re-author.** `delivery-shape` picks the node `type` and points
  `delegates_to` at the owning rule/skill. The discipline of each type lives at its source. If a
  node's completion criterion starts duplicating Rule C5 or the ADR template inline, that is drift —
  link instead.

---

## Delegation — timing & surfacing

`delegates_to` names the discipline that owns a node, but it fires **at issue-pickup (build time),
not during plan emission.** `delivery-shape` emits the hierarchy and stops; the delegate (e.g.
`planning-and-task-breakdown` for a `story`) runs when the issue-class artefact is picked up to be
built. Rationale: small batches + certainty-decays-with-horizon — expanding every node's
fine-grained tasks at plan time front-loads detail that decays before the node is reached
(agentic P8).

There is no programmatic skill-to-skill trigger. "Fires automatically" means the **emitted
issue-class artefact carries an explicit on-pickup instruction naming its `delegates_to`**, which
the picking-up agent follows (consumer side enforced by the Workflow pack's on-start step). The
**adapter** binding nodes to a concrete tracker therefore **must surface each node's `delegates_to`
on the emitted artefact**; a `ktlo` node surfaces "no breakdown step." `delegates_to` is **required
on every node** — the walk-script enforces presence (exit 2 if missing). This is the one delegation
obligation the contract places on the adapter, and it stays tool-agnostic: which skill, not which
tracker.

---

## Walkability contract (what a deterministic reader may rely on)

This is the half of the kill condition the gate issue tests with an actual walk-script. A reader
may assume, without parsing prose:

1. **Layers are directory depth.** `D*/` = deliverable, `D*/N*.md` = node.
2. **Front-matter is the source of structured truth.** Every layer file opens with a `---` YAML
   block carrying at least `layer`, `id`, and (for nodes) `type` + `completion.form`.
3. **The manifest is countable.** milestones = `D*` directories; issues = `N*.md` files;
   sub-issues = `- [ ]`/`- [x]` lines inside node files.
4. **The oracle is the README.** The derived manifest is correct iff its counts equal the
   hand-count manifest in the root README; a mismatch means drift or a non-deterministic layout.

If a reader cannot satisfy 1–4 mechanically, the standalone-markdown premise has failed and the
seam must be re-shaped before the skill is built (the initiative kill condition).

## Design notes / alternatives considered

- **File-per-node vs section-per-node.** Chosen: one file per node, structure carried by directory
  depth + front-matter. Rejected: nodes as `##` sections inside the `_deliverable.md` file with
  fenced metadata blocks — fewer files, but it forces the reader to parse headings and extract fenced
  blocks, which is more fragile than reading front-matter from a known file path. If a future
  walk-script finds front-matter parsing insufficient, section-per-node is the documented fallback —
  but the burden is on showing front-matter failed first.
- **Derived vs hand-maintained manifest.** Chosen: derive the manifest from structure; keep only a
  hand-count *oracle* in the README. Rejected: a checked-in manifest file enumerating every
  milestone/issue/sub-issue — a second source of truth that drifts from the files it indexes.
- **Four structural layers vs three.** Chosen: three — deliverable → node → task, mapping 1:1 to
  milestone / issue / sub-issue. Rejected: a fourth `capability` layer mapped to a label. A label is
  *stateless* (name + colour, no done-state, no target), yet a capability asserts a real completion
  criterion — a stateful claim a label can't hold or check; and the mapping was asymmetric
  (deliverables, the same kind of object, get a stateful milestone). The fix folds `capability` into
  the polymorphic node vocabulary as a node *type* (completion form `the-capability-spec`): a
  capability that carries its own irreducible spec is a node, broken into task-slices, sitting beside
  the `story` / `spike` / … nodes under its deliverable. Labels remain available for *orthogonal*
  tagging (theme / area), just not as a hierarchy layer. In this worked example every capability was
  reducible to its child nodes, so all five were absorbed into deliverable prose and no
  `capability`-type node appears — it grounds when one carries a spec its children don't.
