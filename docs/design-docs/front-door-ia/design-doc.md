---
name: front-door-ia
status: accepted
authors: Anton Babushkin
created: 2026-06-12
last_updated: 2026-06-12
supersedes: the prior never-accepted shaping-pipeline IA (since deleted; surviving decisions live in delivery-shape + ADR 0002)
consumes: ADR 0004 (verb namespace table) + docs/design-docs/execution-workflow/design-doc.md (A/N04)
naming_record: this doc + docs/adr/0005-shaping-door-leaf-names.md record the shaping door names; ADR 0004 remains the record of the shape:/exec: prefix split.
linear: ABA-375 (N01 — Establish the Information Architecture)
---

# Front-door IA — absorption map, survivor manifest, naming schema, gate inventory

**Trigger (Rule A1).** Three triggers hold; any one suffices. The deliverable breaks into six nodes (N01–N06, > ~5). The absorption map is a **one-way door**: the door builds delete the folded skills, and `install.sh` publishes the door namespace into every install through wrapper generation and `shape-*` symlinks. The work touches **shared infrastructure**: command wrappers, skill symlinks, `using-this-pack` routing, and the plugin manifest.

**Scope boundary.** This doc fixes maps, manifests, and naming rules only. Door prose is N02–N05's work at pickup. Any sentence here that drafts a door's actual wording is scope creep — reject it at review.

## Problem

The shaping pack contains twelve skills (2,599 lines at the 2026-06-12 baseline), and it fails its own authoring standards: three skills exceed the 300-line cap (`delivery-shape` 381, `plan-review` 369, `roadmap-shape` 303), and overlapping When-to-use instructions force a routing guess at the start of every session — `using-this-pack` papers over the ambiguity instead of removing it.

We are holding five updates (N02–N06) because we have not yet decided how to merge the legacy content, what everything is named, or where every `[GATE]` lands. If the door authors make these choices independently, the logic drifts, risking silent gate losses like the one already found in delivery-shape (see Context). The delay prevents the authors from writing their task breakdowns, leaves the N08 sweep without a single deletion list, costs every session a routing guess and extra context, and blocks initiative C, whose supervisor prompts will cite the door verbs literally.

This document provides the consolidation maps and naming specs required to unblock those updates. We reach the success state (KR1) when the measured set totals 2,200 lines or fewer and every update passes its automated line-count, gate-header, and `install.sh` resolution checks.

## Context

We are consolidating the shaping lifecycle based on the confirmed pruning from the lifecycle-expansion analysis: delete roadmap-shape, backlog-manage, and app-calibrate; fold idea-triage into `shape:idea` and the spikes into `shape:design`; keep plan-review as the design/delivery exit gate and render-html as a utility. This document defines the section-level mechanics for that consolidation; it inherits those decisions and does not re-litigate the namespace ADR 0004 already established (`shape:*` / `exec:*` in one table, the shaping-half consolidation left to this initiative). To keep the decision record clear, the shaping leaf names decided here will be filed as **ADR 0005 at acceptance**, mirroring the ADR 0004 pattern — and this document supersedes the prior never-accepted shaping-pipeline architecture (2026-06-03; delivery-shape already carries its surviving decisions, and commit `2c03385` deleted its `execution-breakdown` construct).

However, the repository baseline has moved since the original cycle issues were written (they carry 2026-06-10 numbers). The anatomy reform landed: `docs/skill-anatomy.md` (revised in `e0cd32f`) now specifies the two-field frontmatter and the eleven-section body this spec binds the doors to. The anatomy-prune (`cfe42f6`) cut design-doc 243→174 and initiative-shape to 175. delivery-shape, **196 lines at `cfe42f6`**, has since grown to **381** (`ac931a7` — walking-skeleton conditionality; `372f09f`/`fc9b497` — +293/−108 overall) — but the expansion is normative contract, such as the `Done when:` discipline, the size check, dependency ordering, and the model-routing rubric that `bin/check-plan-framing` enforces, rather than unnecessary padding. The drift makes N02's premise ("no fold needed, already under cap at 266") stale; see Q1.

Furthermore, we must restore the integrity of the automated gate checks. Since commit `45b49b9`, delivery-shape has silently lost six of its seven `[GATE]` markers (2 committed-input, 3 map-to-KRs, 4 Rule A1 design-first, 6 five-section body, 7c acceptance criterion, 7d size check, 9 verify-plan; only step 2 stays marked). The substance of the six survives as unmarked steps and prose (steps 3, 4, 6, 9 and the step-7 task rules), but a fitness check that counts markers would bless their deletion. This doc recommends re-marking them; the owner confirms that, or records the demotion as deliberate, at acceptance (Q4 and the delivery-shape ledger in the inventory).

Two facts pin the measurements. Initiative A concurrently adds execution skills to `skills/` (build, debugging, exec-pickup, execution-review, pr-finishing, simplify), so the measured set below names KR1's files explicitly instead of globbing the directory. And this doc loads its evidence from the repo: `docs/design-docs/execution-workflow/design-doc.md`, ADR 0001–0004, `docs/skill-anatomy.md`, `install.sh` (wrapper generation :20–38, symlink prune :77–84, symlink creation :86–93, hardcoded help text :161–173), `bin/eval-triggers`, the `.claude/commands/` inventory, and the N01–N06 plan sources under `examples/delivery-plans/shaping-four-front-doors/`.

## Constraints

This consolidation is not merely a file reorganisation; it is a normative contract that preserves the existing validation logic and system stability while it reduces the pack's footprint. Three groups of constraints bind the door nodes.

**I. Maintain functional continuity** — every existing executable and check keeps working across the fold.

- Map every gate in the eight folded skills to a destination section, or write a deletion rationale — the issue's mandatory Done condition.
- `bin/walk-delivery-plan` and `bin/check-plan-framing` keep exiting 0 against the existing example plans after the delivery re-house.
- `bin/eval-triggers` keeps running: N02 and N04 retarget its `CANDIDATE_SKILLS` array (it hardcodes `delivery-shape` and `initiative-shape`, `bin/eval-triggers:32–35`) and rename or re-point the `eval/` fixture files in the same changes.
- Each door's commit deletes the folded source directories and their wrappers together, so one `git revert` restores both sides.

**II. Protect the normative contract** — we compress the files; we do not delete the substance of the core logic.

- The six-field initiative description that initiative-shape emits today stays byte-stable across the fold; `shape:delivery`'s gate 2 consumes it verbatim.
- delivery-shape's protected detail survives: the step-7 contract rules (`Done when:`, size check, dependency ordering, model routing) and the six de-marked gates' substance. N02 may move this detail intact to the existing `docs/delivery-shape-contract.md` with a citation; it may not delete it.
- **Citation guardrail (Q3).** Content moved from a counted `SKILL.md` into an uncounted reference file must be cited at the exact workflow step that needs it — a real on-demand load, not an appendix. N03–N05 reviews check the citation exists; an uncited reference file is a cap dodge, not chunking.
- No stack-prescriptive content enters door prose (repo rule); the doors stay stack-agnostic.

**III. Enforce the performance limits (NFRs)** — fitness functions, not judgement, measure the reform.

| NFR | Target | Fitness function |
|---|---|---|
| Per-skill cap | Each door and each survivor ≤300 lines; 350 is the hard cap and 300–350 ships only flagged | `wc -l` on the file in each node's Done-when |
| Total footprint | Measured set ≤2,200 lines | the N06 footprint check: `wc -l` over the seven manifest files below |
| Gate preservation | 19/19 fold-source gates accounted for (15 mapped, 4 deleted with rationale) **plus** delivery-shape's 7-gate ledger (Q4); zero silent losses | grep of `Gate:` headers per door diffed against the Gate inventory at N03–N05 Done-when; N08 sweeps for stragglers. Known false positive: `using-this-pack:60` explains the `[GATE]` convention in prose — N06's rewrite rephrases it or the sweep whitelists it |
| Benchmark stability | plan-review benchmark ≥90% after reform (kill condition: <80% after two repair attempts) | N07 rerun of `skills/plan-review/evals/evals.json` (kept byte-identical by N06) |
| Zero legacy citations | grep for the seven deleted/renamed skill names returns empty over the **live surfaces**: README, install.sh (including the help text), hooks, `using-this-pack`, `.claude/commands/`, `bin/`, `eval/`, `.claude-plugin/plugin.json`, `docs/delivery-shape-contract.md`. Exempt as historical record: CHANGELOG, `examples/delivery-plans/`, `docs/plan-reviews/`, superseded docs | N08's sweep task |
| Wrapper collision | No two commands share a leaf name at the slash surface | diff over `.claude/commands/` after authoring (same fitness as A/N04's NFR) |

## Alternatives considered

Context fixes the fold/delete/survive calls; the open decision this doc owns is the **naming schema** — directory names, wrapper names, and how they bind to the `shape:*` verbs.

**Alt 1 — bare phase-leaf directories (`skills/idea/`, `skills/project/`, `skills/design/`, `skills/delivery/`), wrapper leaf = directory leaf.**
*Description.* The directory, the frontmatter `name`, and the wrapper file all use the phase leaf; `install.sh` derives the installed symlink `shape-<leaf>`, and the wrapper publishes `/shape:<leaf>`. The pack already applies exactly this rule (`delivery.md` → `/shape:delivery`).
*Blast radius if wrong.* Low. Leaf names read generic out of context ("design"), but they never appear out of context — the installed surface always carries the `shape-`/`shape:` prefix.
*Reversal cost.* Low. `install.sh` already prunes stale symlinks on re-install; a rename costs a directory move plus one wrapper edit.

**Alt 2 — suffixed directories (`skills/idea-shape/`, …).**
*Description.* Keep a descriptive suffix on every directory.
*Blast radius if wrong.* The installed names stutter (`shape-idea-shape`), and the wrapper leaf no longer equals the directory leaf, so the naming rule needs a lookup table instead of a convention.
*Reversal cost.* Same mechanics as Alt 1, worse steady state. Rejected for the stutter and the rule complexity.

**Alt 3 — keep current directories, retarget wrappers only.**
*Description.* `/shape:idea` points at `skills/idea-triage/`, and so on; no directory moves.
*Blast radius if wrong.* The verb and the directory drift apart permanently. The "zero legacy citations" grep can never pass because the legacy names *are* the layout, and the router must explain the mismatch forever.
*Reversal cost.* High in practice — every doc that cites a path compounds the drift.

**Alt 4 — do nothing (no consolidation).**
*Description.* Keep the twelve shaping skills.
*Blast radius if wrong.* KR1 fails by definition; the routing ambiguity and the over-cap skills persist.
*Reversal cost.* n/a — the initiative exists to remove this state.

## Recommended approach

**Adopt Alt 1.** The pack already names one door this way — `delivery.md` publishes `/shape:delivery` because the wrapper leaf matches the directory leaf — and Alt 1 extends that working rule to all four doors. The four artefacts below are the spec the door nodes build against.

### 1. Naming schema (consumes ADR 0004's table; recorded in ADR 0005 at acceptance)

| Verb | Directory | Frontmatter `name` | Wrapper (repo) | Slash command | Installed symlink |
|---|---|---|---|---|---|
| `shape:idea` | `skills/idea/` | `idea` | `.claude/commands/idea.md` | `/shape:idea` | `~/.claude/skills/shape-idea` |
| `shape:project` | `skills/project/` | `project` | `.claude/commands/project.md` | `/shape:project` | `~/.claude/skills/shape-project` |
| `shape:design` | `skills/design/` | `design` | `.claude/commands/design.md` | `/shape:design` | `~/.claude/skills/shape-design` |
| `shape:delivery` | `skills/delivery/` | `delivery` | `.claude/commands/delivery.md` (retargeted) | `/shape:delivery` | `~/.claude/skills/shape-delivery` |
| `shape:plan-review` | `skills/plan-review/` (unchanged) | `plan-review` | `.claude/commands/plan-review.md` (unchanged) | `/shape:plan-review` | `~/.claude/skills/shape-plan-review` |
| `shape:render-html` | `skills/render-html/` (unchanged) | `render-html` | `.claude/commands/render-html.md` (unchanged) | `/shape:render-html` | `~/.claude/skills/shape-render-html` |
| — (router, model-invoked) | `skills/using-this-pack/` (unchanged) | `using-this-pack` | none (status quo) | — | `~/.claude/skills/shape-using-this-pack` |

The table encodes one convention: wrapper leaf = directory leaf = frontmatter `name`. `install.sh` derives the installed symlink (`shape-<leaf>`) and prunes stale links on re-install (verified at `install.sh:77–84`). One seam stays hand-owned: the help text at `install.sh:161–173` hardcodes the command list and currently prints eight legacy verbs. Each door node updates its own lines there (N02 proves the seam), and N08's grep catches stragglers.

**Wrapper disposition.** Each door's commit deletes the wrappers of the skills it absorbs: `idea-triage.md`, `initiative.md`, `roadmap.md`, `backlog-manage.md`, `design-doc.md`, `backend-spike.md`, `product-spike.md`. The door commits create `idea.md`, `project.md`, and `design.md`, and retarget `delivery.md` in place. Initiative A owns the execution-half wrappers (`exec/*`, `stop-the-line.md`, `task-annotation-check.md`, `pr-prepare.md`, `verify-implementation.md`); N08 sweeps only their shaping-side citations.

**Plugin manifest.** `.claude-plugin/plugin.json` still describes deleted capabilities ("idea triage, roadmap shaping, …"). N06 rewrites the description to the four-door vocabulary alongside the router rewrite.

### 2. Survivor manifest and the measured set

After consolidation the shaping library is exactly seven files — four doors and three utilities. **KR1's ≤2,200 check measures this set and nothing else**, pinned by filename so initiative A's concurrent additions to `skills/` cannot drift the count. The set counts `SKILL.md` lines only; bundled skill-local reference files (e.g. `skills/render-html/references/`) sit outside it, under the citation guardrail in Constraints II:

```
wc -l skills/idea/SKILL.md skills/project/SKILL.md skills/design/SKILL.md \
      skills/delivery/SKILL.md skills/plan-review/SKILL.md \
      skills/render-html/SKILL.md skills/using-this-pack/SKILL.md
```

| Survivor | Built from (2026-06-12 lines) | Size plan |
|---|---|---|
| `shape:idea` | idea-triage (220) + app-calibrate fragments (155) | ≤300 (1.25:1 fold) |
| `shape:project` | initiative-shape (175) + roadmap/backlog fragments | ≤300 (mostly 1:1; fragments are clauses, not sections) |
| `shape:design` | design-doc (174) + backend-spike (205) + product-spike (189) = 568 | ≤300 target, 350 hard — the kill-condition watch node (N05) |
| `shape:delivery` | delivery-shape (381) | ≤300 via contract-aware compression with the overflow route to `docs/delivery-shape-contract.md`; protected content named in Constraints (Q1) |
| `plan-review` | plan-review (369) | ≤300 — density reform only, gates and evals.json untouched (N06) |
| `render-html` | render-html (131) | unchanged bar frontmatter cut; its bundled `references/` dir travels with it |
| `using-this-pack` | using-this-pack (119) | rewritten router, **≤150** (N06) |

Worst case, every capped file lands at exactly 300 and the router at its 150 bound: 300×5 + 131 + 150 = **1,781**. Modelling `shape:design` at its flagged 350 hard cap instead gives **1,831 ≤ 2,200** — ≥369 lines (≈17%) of headroom. The measured set excludes every `exec`-half skill, including the two baseline skills that transfer to initiative A (`pr-prepare`, `verify-implementation`).

### 3. Frontmatter-cut spec

Per `docs/skill-anatomy.md` (already revised), exactly two fields survive: `name` and `description` (what the skill does, then "Use when …", then trigger phrases). The eight legacy fields die: `pack`, `lifecycle_stage`, `principles_implemented`, `length_target`, `author`, `predecessor`, `kept_from_predecessor`, `changed_from_predecessor`. README tables and git history keep the taxonomy those fields carried.

initiative-shape, design-doc, and delivery-shape are already cut. Among survivors, **plan-review (10 fields), render-html (10), and using-this-pack (6)** still carry legacy fields — N06 applies the cut. The folded sources' frontmatter dies with their files.

### 4. Absorption map — all 14 baseline skills

Disposition vocabulary: **fold** (content moves into a door section), **absorb** (a clause or fragment moves; the section dies), **delete** (dies with written rationale), **survive** (file continues, possibly re-housed), **transfer** (leaves the shaping half for initiative A's execution half).

A door's body follows the eleven-section anatomy (Title → Purpose → When to use → Do not use when → Inputs → Outputs → Workflow → Artefact template → Red flags → Exit criteria → Related). Two standing rules apply throughout, recorded once instead of per-row:

- **"Common rationalisations" sections** (idea-triage, app-calibrate, roadmap-shape, backlog-manage, backend-spike, product-spike, plan-review, render-html) have no slot in the anatomy. Rule: load-bearing rows merge into the door's **Red flags**; the rest is explanatory redundancy and dies. plan-review and render-html keep theirs until their own density passes apply the same rule.
- **"References" sections** become the door's **Related** section, citing only references the door actually uses.

**idea-triage (220) → fold into `shape:idea`** — the door's core.

| Source section | Disposition |
|---|---|
| Purpose / When to use / When not to use | fold → door Purpose / When to use / Do not use when; When-to-use gains one branch clause absorbed from app-calibrate (below) |
| Inputs / Outputs | fold → door Inputs / Outputs |
| Workflow (7 steps; gates at steps 2, 5, 7) | fold → door Workflow; all three gates carried (inventory G1–G3) |
| Artefact template (Raw intake / Problem restatement / Evidence / ICE score / Routing / Notes) | fold → door Artefact template; the Routing entry adds the parked-idea-bank entry format absorbed from backlog-manage |
| Common rationalisations / Red flags / Verification | per standing rules → Red flags / Exit criteria |
| References (ice-scoring, confidence-meter, app-context-schema) | fold → Related; add kano-classification.md (used by the ICE/Kano step; today cited only by roadmap-shape) |

**app-calibrate (155) → absorb fragments into `shape:idea`; delete the rest.**

| Source section | Disposition |
|---|---|
| Purpose / When to use / When not to use | delete — the trigger collapses to one When-to-use branch clause in the door: *idea targets a measurable improvement and `docs/app-context.md` is missing or stale (>90 days) → ground the baseline first* |
| Workflow steps 1–3, 5 (gather, probe, write) | delete — the procedure compresses to one door workflow step: populate/refresh `docs/app-context.md` per `references/app-context-schema.md` |
| Workflow step 4 `[GATE]` minimum validity | **absorb** → clause on the door's scoring gate (inventory G4) |
| Artefact template | delete — duplicate of `references/app-context-schema.md`, which survives and is the single schema of record |
| Extension: MCP data sources | delete — optional enrichment never exercised; the schema reference keeps the field list |
| Rationalisations / Red flags / Verification / References | per standing rules; `app-context-schema.md` cited from the door's Related |

**initiative-shape (175) → fold-in-full into `shape:project`** — every section survives 1:1 (it already conforms to the anatomy and sits under cap). The six-field initiative description template stays **byte-stable**: `shape:delivery` gate 2 consumes it verbatim, and N04's Done-when re-runs that gate on an existing initiative description. Gates 2, 7, 8 carried (inventory G5–G7). N04 also retargets the `initiative-shape` entry in `bin/eval-triggers`.

**roadmap-shape (303) → delete.** Rationale: it is portfolio-planning ceremony the single-user reality never exercised. Ideas route individually through `shape:idea` and become initiatives through `shape:project`; no planning-cycle ritual exists to host the Now/Next/Later board, capacity allocation, or theme distribution. Roadmap *review* keeps a home: plan-review's When-to-use already covers roadmaps.

| Source section | Disposition |
|---|---|
| Purpose / When / Inputs / Outputs / Workflow (12 steps) | delete; gates at steps 3, 6, 12 individually dispositioned in the inventory (G8–G10) |
| Roadmap template (Now/Next/Later, capacity allocation, theme distribution, validation slots) | delete — this orphans `references/portfolio-themes.md` → N08 deletion list |
| Shape review | delete — the surviving plan-review utility supersedes it |
| Rationalisations / Red flags / Verification / References | delete; survivors keep citing ice-scoring / confidence-meter / kano-classification / task-sizing |

**backlog-manage (178) → delete.** Rationale: the idea-bank curation ceremony (review sessions, promote/kill passes, evidence feedback) never ran as a session of its own. What must survive, survives elsewhere: `shape:idea`'s routing output parks an idea; re-running `shape:idea` on a parked idea promotes it; `docs/ktlo.md` already records the KTLO logging convention.

| Source section | Disposition |
|---|---|
| Purpose / When / Inputs / Outputs | delete (rationale above) |
| Workflow step 3 `[GATE]` session intent | delete (inventory G11) |
| Workflow step 5 `[GATE]` confirm writes | **absorb** → clause on `shape:idea`'s routing gate (inventory G12) |
| Remaining workflow steps | delete |
| Artefact template (bank entry / ledger) | absorb the parked-entry essentials into `shape:idea`'s Artefact template (Routing entry); the curation ledger dies |
| Rationalisations / Red flags / Verification / References | per standing rules; no orphaned references |

**design-doc (174) → fold-in-full into `shape:design`** as the doc branch. The door gains a typed branch at its trigger gate: *problem understood + trigger fires → doc branch; the open question is itself the unknown → spike branch (technical or product variant)*. design-doc's "Do not use when: problem not understood → spike first" therefore becomes internal routing instead of a cross-skill referral. Gates 1, 3, 8 carried (inventory G13–G15). The artefact template survives as the doc-branch template; Related keeps `nfr-categories.md`.

**backend-spike (205) → fold into `shape:design`** as the technical-spike variant.

| Source section | Disposition |
|---|---|
| Purpose / When / When-not | fold → the door's When-to-use spike-branch triggers |
| Workflow (gates at steps 1, 4, 6) | fold → spike-branch steps; gates carried (inventory G16–G18); steps shared with the product variant where identical (write-the-question, scope/timebox) |
| Recommendation template (Question / Failure example / Options considered / Scope / Recommended approach / Confidence and semantics impact / Follow-up) | fold → merged **spike record** template, technical-variant fields |
| Rationalisations / Red flags / Verification / References | per standing rules; confidence-meter stays cited |

**product-spike (189) → fold into `shape:design`** as the product-spike variant. Same pattern: the When-to-use triggers fold into the spike branch; the finding template (Question / Approach / Observations / Finding / Recommendation / Prototype artefact) merges into the spike record template as the product-variant fields; the gate at step 5 merges into the shared spike exit gate (inventory G19). The throwaway-artefact discipline (the prototype is disposable, the finding is the deliverable) survives as spike-branch prose.

**delivery-shape (381) → survive, re-housed as `shape:delivery`** (N02, the walking skeleton). Every section folds 1:1 into `skills/delivery/`. N02's Done-when asserts the emitted plan format and `bin/` gate compatibility, and N02 retargets the `bin/eval-triggers` entry. A density pass alone cannot reach ≤300 — the growth from 196 (`cfe42f6`) to 381 is recent, deliberate contract content. The sanctioned route is **contract-aware compression**: protected content (Constraints) stays in the skill or moves intact to `docs/delivery-shape-contract.md` with a citation; N02 deletes nothing protected. Before any compression starts, Q4 settles the six de-marked gates — re-mark them, or record the demotion as deliberate — so the gate fitness check has a true baseline.

**plan-review (369) → survive** as a utility. N06 compresses it to ≤300 as pure density reform: all six `[GATE]` steps stay verbatim, `evals/evals.json` stays byte-identical, and the tier-selection and B1–B8 axes do not change. The frontmatter cut applies.

**render-html (131) → survive** as a utility, unchanged except the frontmatter cut. Its references are **bundled skill-local files** (`skills/render-html/references/html-patterns.md`, `html-skeleton.md`) cited via `<skill-base>/references/…` — they exist, travel with the directory, and stay outside the measured set.

**using-this-pack (119) → survive** as the router. N06 rewrites it to route exactly the four doors plus the utilities, point execution work at `exec:pickup`, and stay within **≤150 lines**. The frontmatter cut applies (currently 6 fields). It carries no gates; the meta-pack anatomy exemptions apply. N06 rephrases line 60's prose explanation of the `[GATE]` convention — or the sweep whitelists it — so N08's straggler grep stays clean.

**pr-prepare (163) and verify-implementation (123) → transfer** to the execution half. ADR 0004 reserves their successors (`exec:finish`, `exec:verify`); initiative A owns the skills, their gates (2 + 2), and their wrappers. They leave the shaping measured set; N08 sweeps only their shaping-side citations.

**Reference disposition** (the map settles these too). Survive: app-context-schema, confidence-meter, ice-scoring, kano-classification, project-types, kr-quality-templates, task-sizing, nfr-categories, plus render-html's bundled pair. Orphaned, onto N08's deletion list: portfolio-themes (only roadmap-shape cites it) and dora-metrics (no skill cites it; README/CHANGELOG only).

### 5. Gate inventory — every gate in the eight folded skills

The eight folded skills carry 19 gates at the 2026-06-12 baseline (line numbers from that baseline): 15 map to destinations, 4 die with rationale. N03–N05's Done-whens check door gate headers against this table, not reviewer memory.

| # | Source gate | Destination / deletion rationale |
|---|---|---|
| G1 | idea-triage:83 — step 2 "Diagnose: problem or solution?" | `shape:idea` Workflow — early gate, carried verbatim |
| G2 | idea-triage:105 — step 5 "Does the problem statement hold?" | `shape:idea` Workflow — carried verbatim |
| G3 | idea-triage:118 — step 7 "Route the idea." | `shape:idea` Workflow — final routing gate, carried; gains two absorbed clauses (G4 grounding, G12 confirm-writes) |
| G4 | app-calibrate:79 — step 4 "Minimum validity check." | **absorbed** as a clause on `shape:idea`'s scoring/evidence gate: an ICE Impact score that cites no `app-context.md` baseline is marked ungrounded |
| G5 | initiative-shape:43 — gate 2 "problem or solution?" | `shape:project` Workflow — carried verbatim |
| G6 | initiative-shape:94 — gate 7 "user confirmation" | `shape:project` Workflow — carried verbatim (also the surviving home of tracker-write confirmation) |
| G7 | initiative-shape:100 — gate 8 "verification rubric — 11 cross-cutting rules" | `shape:project` Workflow — carried verbatim; rubric content untouched |
| G8 | roadmap-shape:108 — step 3 "Strip any solution framing." | **deleted** — duplicate: the identical check survives twice, as G1 (`shape:idea`) and G5 (`shape:project`); every path to a roadmap-shaped artefact now passes one of them |
| G9 | roadmap-shape:129 — step 6 "Confidence gate (Rule B6)." | **deleted** — G3 supersedes it: `shape:idea`'s routing gate already forces low-confidence ideas to the validate lane against `references/confidence-meter.md` (which survives); no second moment exists where the check would fire |
| G10 | roadmap-shape:175 — step 12 "Shape review." | **deleted** — review-of-a-roadmap is plan-review's When-to-use, and plan-review survives; the ceremony around it dies with the skill |
| G11 | backlog-manage:103 — step 3 "Identify session intent." | **deleted** — the gate disambiguated the multi-mode curation session; the modes die with the skill, and intake disambiguation is `shape:idea`'s When-to-use |
| G12 | backlog-manage:123 — step 5 "Confirm writes." | **absorbed** as a clause on G3: any route that mutates the idea bank or the tracker announces the write and confirms it first |
| G13 | design-doc:46 — gate 1 "trigger check" | `shape:design` Workflow — carried, extended into the typed branch point (doc vs technical spike vs product spike); the no-trigger → ADR referral is unchanged |
| G14 | design-doc:54 — gate 3 "problem section" | `shape:design` doc branch — carried verbatim |
| G15 | design-doc:74 — gate 8 "operability plan" | `shape:design` doc branch — carried verbatim |
| G16 | backend-spike:80 — gate 1 "Write the question." | `shape:design` spike branch — carried, shared across both spike variants |
| G17 | backend-spike:105 — gate 4 "Scope check." | `shape:design` spike branch — carried (throwaway scope + timebox discipline) |
| G18 | backend-spike:114 — gate 6 "Write the recommendation." | `shape:design` spike branch — exit gate, merged with G19 into one "write the finding/recommendation" gate over the merged spike record template |
| G19 | product-spike:104 — gate 5 "Write the finding." | merged into the same spike exit gate as G18; both sources share one semantic — a spike may not end without a written finding — and the merge preserves it once |

**The delivery-shape ledger — gates outside the fold but inside the risk.** The re-house must not inherit the marker count of an already-degraded baseline. From `45b49b9`, `shape:delivery`'s ledger is: D1 committed-input (still marked, line 82 — carried); D2 map-to-KRs (de-marked, substance at step 3); D3 Rule A1 design-first (de-marked, step 4); D4 five-section body (de-marked, step 6); D5 acceptance criterion on every task (de-marked, step-7 rules); D6 size check (de-marked, step-7 rules); D7 verify-plan (de-marked, step 9). Q4 decides re-mark vs recorded demotion; either way N02's Done-when checks against **this ledger of seven**, not against "count stays 1".

The gates elsewhere, listed so N08 holds the full ledger (none at risk): plan-review 6 (kept verbatim through N06's compression), render-html 3 (untouched), using-this-pack 0 (one prose mention of the convention; see the NFR note), pr-prepare 2 and verify-implementation 2 (transfer with their skills).

## Consequences

**Positive.**

- N02–N05 become mechanical compression jobs against one spec; their Done-whens check `wc -l`, gate headers against this inventory, and `install.sh` resolution — no per-door judgement calls.
- N08 reads its deletion/cleanup list from one place: 7 skill dirs, 7 wrappers, 2 orphaned references, the install.sh help-text block, the plugin-manifest description, and the `bin/eval-triggers` / `eval/` retargets.
- Gate loss becomes a review-time diff, not a benchmark-time surprise — and the one silent loss that already happened (delivery-shape) is now surfaced and tracked instead of inherited.
- The naming rule stays a convention (wrapper leaf = dir leaf = frontmatter name), not a lookup table.

**Negative / costs.**

- The door names are themselves a one-way door: once `using-this-pack`, README, and initiative C's prompts cite `/shape:idea` and friends, a rename costs a coordinated sweep. Accepted — that is exactly why this doc, not a door node, decides them, and why ADR 0005 records them at acceptance.
- Dedicated curation and portfolio ceremony dies. If a real planning-cycle need emerges, it returns as a new shaped initiative, not a resurrection of the deleted files (git history keeps them recoverable).
- `shape:design` carries fold risk (568 → ≤350 hard) — mitigated by the kill-condition watch note on N05, with this doc's inventory as the non-negotiable floor: a fold that closes under 350 only by dropping a gate is a kill, not a ship.
- `shape:delivery` is no longer the zero-risk skeleton N02 assumed: the contract-aware compression (Q1) adds real work to the walking-skeleton node. Accepted trade-off — the alternative (skeleton on a different door) couples plumbing risk to fold risk, which is worse.

**Walking skeleton (Rule B2).** Required and already scheduled: **N02 (`shape:delivery` re-house) is the skeleton.** It exercises every seam this doc decides — directory move, wrapper retarget, symlink regeneration and prune, install.sh help-text edit, `bin/eval-triggers` retarget, router route, frontmatter cut — on the one door with no *absorption* risk, before any content fold starts. N03–N05 build only after the skeleton proves the plumbing. (Q1 and Q4 record the scope corrections the skeleton inherits.)

## Operability plan

Adapted to a Markdown-only pack: "production" is every installed copy of the pack, and the fitness functions are deterministic shell checks.

- **Metrics.** Per door node at Done-when: the file's line count; its gate-header count against this inventory (including the delivery ledger); an `install.sh` re-run resolving the new verb; both `bin/` plan gates exiting 0 and `bin/eval-triggers` running (N02). Initiative-level: the measured-set total (N06); the benchmark pass rate (N07); the legacy-citation grep count over the live surfaces (N08).
- **Structured logs.** Each door PR body records the before/after line counts and the gate diff against the inventory table — the review trail KR1's drains grep for.
- **Alerts (kill conditions, owner-routed).** A door exceeds 350 lines without dropping a gate → stop, surface to the owner, ship style reforms only (project brake). The benchmark drops below 80% after two repair attempts (N07) → same brake. The project description records both; nodes cite them.
- **Rollback plan.** Each door plus its source deletions lands as one revertible unit. Steps: (1) `git revert` the door commit — restores the source skills and wrappers atomically; (2) re-run `install.sh` — regenerates wrappers and prunes the door's now-stale `shape-*` symlink (prune behaviour verified at `install.sh:77–84`); (3) verification gate: the old slash commands resolve and the door's verb is gone.
- **Capacity headroom.** The 1,831-line worst case (shape:design modelled at its flagged 350) against the 2,200 cap leaves ≥369 lines (≈17%) before the brake trips.
- **Known failure modes.** (a) A fold silently drops a gate → the inventory and the delivery ledger are Done-when inputs, and N08 sweeps stragglers. (b) A fold overruns the cap → N05's watch note plus the kill condition. (c) The baseline drifts between this doc and pickup (it already happened once: delivery-shape 196→381 between issue-writing and pickup) → every door node re-measures its sources at pickup and records a baseline-refresh note when the numbers moved. (d) Stale wrappers, symlinks, or help text outlive a deletion → the `install.sh` prune, the per-node help-text edit, and the N08 grep. (e) Initiative A churns `skills/` concurrently → the measured set is pinned by filename, immune to additions. (f) Compression deletes normative contract from shape:delivery → the protected-content list in Constraints, the `docs/delivery-shape-contract.md` overflow route, and a `bin/check-plan-framing` re-run.
- **Upstream dependencies.** `install.sh` wrapper/symlink generation and help text; `docs/skill-anatomy.md` (the frontmatter/body spec of record); ADR 0004 (verbs); `bin/eval-triggers` plus the `eval/` fixtures. A change to any of these reopens this doc by ADR.
- **Downstream dependencies.** N02–N06 Done-whens; N08's sweep list; initiative C's supervisor prompts (they will cite door verbs literally — they bind after this doc is accepted, which is what makes the naming a one-way door); `docs/delivery-shape-contract.md` and the example plans (N08 updates their path citations); `.claude-plugin/plugin.json` (N06 rewrites the description).

## Open questions

| Q | Owner | Resolution gate |
|---|---|---|
| **Q1.** shape:delivery sizing. The 381 lines include deliberate, recent contract content (196 at `cfe42f6` → 381 via `ac931a7`/`372f09f`), so a density pass alone cannot reach ≤300. **Resolved 2026-06-12 (owner): contract-aware compression to ≤300**, grounded in the usage model — humans run shape:delivery interactively (never drain workers), so cited references load on demand, and the step-9 `bin/` gates run in-session. N02 compresses in this order: (1) schema detail `docs/delivery-shape-contract.md` already owns → cite, don't restate; (2) rules `bin/check-plan-framing`/`bin/walk-delivery-plan` enforce → one-line rule + the step-9 gate, cut the elaboration; (3) judgement heuristics (7a first-task choice, the `references/task-sizing.md` routing rubric) stay in the body. The file measured 390 at resolution time — N02 re-measures at pickup (failure mode c) and still classifies the `cfe42f6..HEAD` diff first; if the protected+judgement floor exceeds 300, the kill condition routes back to the owner. | Anton — **answered** | N02's at-pickup task breakdown — unblocked |
| **Q2.** Orphaned references: delete `references/portfolio-themes.md` and `references/dora-metrics.md` once roadmap-shape dies? (Default per this doc: delete both; no skill cites dora-metrics today.) | N08 pickup | N08's sweep task Done-when |
| **Q3.** Confirm the measured set. **Resolved 2026-06-12 (owner): the seven survivor files above are confirmed as KR1's measured set, and 2,200 stays the KR number** (a brake, not a target — the per-skill ≤300 cap drives the compression; the ≈17% slack absorbs shape:design's possible flagged 350). Baseline reconciliation: the project's "11 skills / 2,357 lines" ≈ the twelve shaping skills minus the router at 2026-06-10 sizes, so the transferred pr-prepare/verify-implementation were never in the denominator (excluding them moves no goalposts), and counting using-this-pack (≤150) makes the measured set slightly harder than the original KR — accepted as the honest direction. A citation guardrail (Constraints II) closes the Route-A loophole: reference files stay uncounted only when the moved content is cited at the workflow step that uses it. | Anton — **answered** | this doc's acceptance — N06's footprint check binds to the answer |
| **Q4.** delivery-shape's six de-marked gates (ledger D2–D7). **Resolved 2026-06-12 (owner): re-mark all six as `### N. Gate:` headers at the N02 re-house, before any compression starts.** The owner confirmed the demotion was editorial collateral, not intent. The gate-count fitness for shape:delivery binds to **7**. Ordering matters: re-marking precedes the Q1 compression so the density pass sees the protected content structurally flagged — the judgement gates (D1, D3, D6) and the meta-gate D7 (the step that invokes the `bin/` checkers) have no mechanical backstop and depend entirely on header prominence. | Anton — **answered** | N02's at-pickup task breakdown — unblocked; fitness count = 7 |

## Review record

Reviewed through the `plan-review` exit gate (Full tier, fresh-context adversarial pass + structured buckets): REVISE → conditions cleared in revision. The owner then reviewed the prose through two crit rounds (rewrite against the writing guidelines; section rewrites fact-checked and adopted with corrections) and resolved Q1/Q3/Q4 on 2026-06-12. ADR 0005 is filed at `docs/adr/0005-shaping-door-leaf-names.md`; status flipped to accepted the same day.
