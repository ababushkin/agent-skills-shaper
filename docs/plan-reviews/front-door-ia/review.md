# Plan review: front-door-ia

## Plan reference

`docs/designs/front-door-ia.md` — IA design doc for ABA-375 (N01): absorption map, survivor manifest + measured set, frontmatter-cut spec, naming schema, gate-preservation inventory for the four-phase-skill consolidation.

Review method: structured buckets in main context **plus a fresh-context adversarial sub-agent pass** (mitigation for the known limit "review runs in main context — same blindspots"; the doc author and reviewer were the same session). The sub-agent fact-checked every line count, gate line number, and citation claim against the repo and attacked scope, assumptions, and internal consistency.

## Inputs

- **Appetite**: 1 slice (one reviewed document); fixed.
- **Cynefin domain**: Complicated — knowable with expertise; emphasis on dependencies and the one-way doors.
- **Tier**: Full — auto-selected (≥1 one-way-door decision: door naming + irreversible skill deletions; also feeds >5 downstream nodes).
- **Trigger**: a design doc is about to be approved (trigger 1) + auto-fire on one-way doors (trigger 4). Fast-track gate: does not fire (not KTLO, not single-consumer, one-way doors present).

## B1 — Problem framing

Opens with the problem (routing ambiguity, over-cap skills, four builds blocked on undecidable-per-node decisions) before any naming/solution content. **OVERTURNED** (no defect). Falsifying condition: a reader can state the doc's purpose without reading past §Problem — holds.

One factual defect found and fixed: the draft said "two skills over the cap"; the repo and the doc's own cited source count three (delivery-shape 381, plan-review 369, roadmap-shape 303). Corrected.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| `bin/eval-triggers` hardcodes `delivery-shape` + `initiative-shape` (:32–35) and reads `eval/delivery-shape-triggers.md`; no node owned the retarget | **SUSTAINED** → fixed: added to Constraints, N02/N04 dispositions, NFR grep scope | `bin/eval-triggers` exits non-zero after the renames with no owning node |
| `install.sh:161–173` hardcodes a help-text block printing 8 legacy verbs; "install.sh derives everything else" was false | **SUSTAINED** → fixed: claim corrected, help-text named a hand-owned seam, per-node edit + N08 grep | a fresh install after N02 prints dead commands |
| `.claude-plugin/plugin.json` description names deleted capabilities; absent from sweep scope | **SUSTAINED** → fixed: N06 rewrites it; added to NFR grep scope | post-N08 grep finds legacy capability names in the manifest |
| `docs/designs/shaping-pipeline.md` is the prior IA (14 legacy-name citations) and was never disposed; frontmatter said `supersedes: none` | **SUSTAINED** → fixed: superseded by this doc; historical-record exemption stated | two live IA docs disagree about the pipeline shape |
| "fragments are clauses, not sections" (shape:project) and "load-bearing rows merge into Red flags" are judgement-sized | PARTIAL — accepted residual: clause-level mapping is door-author work by design (scope boundary); the gate inventory bounds the risk | a door ships a roadmap/backlog *section* rather than a clause |
| CHANGELOG / `examples/delivery-plans/` carry legacy names | OVERTURNED as defect → exemption now explicit (historical record) | the sweep "passes" while a *live* surface still cites a deleted skill |

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| delivery-shape 381→300 is a "density pass" (draft's framing) | 0.5 → **refuted**: file was 196 at `cfe42f6`; +293/−108 of deliberate contract content since (`ac931a7`, `372f09f`); `bin/check-plan-framing` enforces parts of it | `git diff cfe42f6..HEAD --stat` (run) | **SUSTAINED** → fixed: reframed as contract-aware compression with `docs/delivery-shape-contract.md` overflow; protected-content list added; Q1 rewritten |
| Gate-marker counting protects delivery-shape semantics | 0.1 → **refuted**: `45b49b9` had 7 `[GATE]` markers; current file has 1; six de-marked with substance intact | `git show 45b49b9:… \| grep GATE` (run) | **SUSTAINED** → fixed: seven-gate ledger (D1–D7) added; Q4 decides re-mark vs recorded demotion; N02 fitness binds to the ledger |
| render-html's two reference citations are dangling | 0 → **false fact**: both files exist at `skills/render-html/references/` (bundled, `<skill-base>/…` paths); the draft's default would have stripped load-bearing citations | `ls skills/render-html/references/` (run) | **SUSTAINED** → fixed: claim corrected; bundled refs excluded from measured set explicitly; Q2 narrowed to true orphans |
| shape:design fold 568→≤350 closes without dropping a gate | 2 (precedent: anatomy-prune compressions ~1.4:1; needed ~1.6:1) | N05 pickup: compute the verbatim floor (gates + templates) before writing prose; kill condition is the documented exit | PARTIAL — accepted with named kill condition (was already in the doc) |
| using-this-pack rewrite stays small | 0.5 → bounded instead of assumed | pinned ≤150 in the manifest; N06 Done-when | OVERTURNED after fix |
| Naming convention is mechanically derivable | 8 (verified by reading `install.sh` generation + prune paths) | already run | OVERTURNED |

## B4 — Dependencies (Full only)

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| ADR 0004 namespace table (upstream) | accepted, on main | n/a | OVERTURNED |
| `docs/skill-anatomy.md` spec of record | revised on main (`e0cd32f`) | n/a | OVERTURNED |
| N02–N06 consume this doc | same owner (Anton); blockedBy edges exist in Linear | cycle-planned | OVERTURNED |
| Initiative C binds door verbs later | named in doc; binds only post-acceptance | out of window | OVERTURNED |
| Initiative A churn in `skills/` | measured set pinned by filename | n/a | OVERTURNED |

## B5 — Reversibility + ADR pairing (Full only)

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Shaping door leaf names | yes — Alts 1–4 with blast radius + reversal cost | **committed: ADR 0005 at acceptance** (added in revision; draft had no ADR pairing) | SUSTAINED → fixed |
| Deletion of 7 skill dirs + wrappers | inherited decision (lifecycle-expansion confirmed intent), recoverability via git named | recorded in this doc + the absorption map | OVERTURNED |
| Measured-set definition (KR1 semantics) | yes — Q3 routes to owner at acceptance instead of silent KR rewrite | this doc is the record | OVERTURNED |

## B6 — Operability + success metrics (Full only)

- Metrics: named (per-node line/gate/install checks; initiative-level footprint, benchmark, citation grep).
- Alerts: named as kill conditions with owner routing (>350-without-gate-drop; benchmark <80% after two attempts).
- Rollback path: ordered steps with verification gate per step (revert unit → re-install prune → resolution check).
- Runbook equivalent: each node's Done-when; N08 sweep list.
- Capacity headroom: corrected in revision — draft's arithmetic was wrong twice (1,951/249 → **1,781 base / 1,831 with shape:design at 350 / ≥369 headroom**).
- User-visible outcome metric: routing without guesswork is proxied by KR2's benchmark ≥90% and the single-router rewrite; KR1 footprint is the delivery metric. Acceptable for a methodology pack.

## B7 — Sequencing + capacity (Full only)

Critical path surfaced: N01 (this doc) → N02 skeleton → N03–N05 folds → N06 closing check; N07/N08 follow. Walking skeleton declared (N02) and now carries its true scope (help-text seam, eval retarget, Q1/Q4 corrections) rather than the stale "no-risk re-house" framing. Appetite fixed by the issue set; single owner. No defect.

## B8 — Pre-mortem

Ranked, specific:

1. **shape:design cannot close ≤350 with all 7 mapped gates** (likeliest). Kill-switch: N05's first task computes the verbatim floor (gates + merged spike template) *before* prose; floor >350 → surface the kill condition, ship style reforms only.
2. **shape:delivery compression deletes normative contract** that only manifests when a future drain emits a malformed plan. Kill-switch: protected-content list + `bin/check-plan-framing` and `bin/walk-delivery-plan` exit-0 in N02's Done-when + the D1–D7 ledger check; overflow to `docs/delivery-shape-contract.md` instead of deletion.
3. **A live surface keeps a dead verb** (install help text, plugin manifest, eval harness) and headless workers follow it. Kill-switch: N08's grep scope now enumerates the live surfaces explicitly; fresh `install.sh` run is in every door node's Done-when.

## Recommendation

**REVISE → conditions cleared → APPROVE** (post-revision), with acceptance conditions routed to the owner.

### Conditions

Cleared in the same session (doc revised in place):

1. False repo fact removed (render-html references exist as bundled files; destructive Q2 default dropped). ✔
2. Density-pass premise replaced with contract-aware compression + protected-content constraint + rewritten Q1. ✔
3. delivery-shape's de-marked gates surfaced as ledger D1–D7 with Q4; gate fitness re-anchored to 7, not 1. ✔
4. `bin/eval-triggers` / `eval/`, install.sh help text, plugin.json, and shaping-pipeline.md brought into scope (constraints, dispositions, sweep list, supersedes). ✔
5. Arithmetic corrected (1,781 / 1,831 / ≥369 headroom); using-this-pack bounded ≤150. ✔
6. ADR pairing committed for the naming one-way door (ADR 0005 at acceptance). ✔

Remaining for the owner at acceptance (not blockers to handing the doc over, blockers to *acceptance*): answer Q1 (delivery sizing route), Q3 (measured-set confirmation), Q4 (re-mark vs recorded demotion); file ADR 0005; flip status to accepted.

## Acceptance addendum (2026-06-12)

All owner conditions cleared. The owner additionally reviewed the doc's prose through two crit rounds (full rewrite against his writing guidelines; his Problem/Context/Constraints section drafts fact-checked and adopted with corrections — R2→KR1, ADR 0005 vs supersedes conflation, Q4 pre-decision softened) before resolving:

1. **Q1 → Route A**: contract-aware compression to ≤300, grounded in the usage model (humans run shape:delivery interactively; drain workers never do). Compression order recorded in the doc.
2. **Q3 → confirmed**: seven-file measured set incl. the router; 2,200 kept; citation guardrail added to Constraints II (reference files uncounted only when cited at the using workflow step).
3. **Q4 → re-mark all six** de-marked delivery gates at N02 before compression; fitness count binds to 7. Owner confirmed the demotion was editorial collateral.
4. **ADR 0005 filed**: `docs/adr/0005-shaping-door-leaf-names.md`. Doc status → accepted.
