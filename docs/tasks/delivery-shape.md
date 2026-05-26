# Tasks: delivery-shape (decompose + AC-by-default slice)

Design basis: `docs/delivery-shape-contract.md` + `docs/adr/0001-delivery-shape-new-skill-vs-expand-planning-and-task-breakdown.md` (decision A — standalone skill)
Scope: the N04 node only — decompose an initiative into deliverables → nodes → tasks with acceptance criteria emitted by default on every `story` node, plus the `bin/check-plan-framing` gate. Foundational-folding prompt, the Rule A1 design-doc branch, full up/down delegation wiring, the self-trial, and README/flowchart registration are separate nodes and out of scope here.
Last updated: 2026-05-26

## Task list

### Task 1 — Walking skeleton: `bin/check-plan-framing` gate
**Description:** A dependency-free script that walks a plan dir and exits 0 iff every `type: story` node carries an Acceptance-criteria block, else exits 1 naming each offending story.
**Done when:** `bin/check-plan-framing examples/delivery-plans/top-down-delivery-planning` exits 0; a copy with one story's `## Acceptance criteria` block removed exits 1 and names that node.
**Model:** Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·L·M·L·L
**Dependencies:** none (stdlib python3, already used by `bin/walk-delivery-plan`; folded in)

### Task 2 — `delivery-shape` SKILL.md core decompose workflow
**Description:** Author `skills/delivery-shape/SKILL.md` (anatomy-conformant) whose workflow takes a committed initiative (goal + KRs as text) and emits the three-layer file-set — deliverables (`serves_kr`) → typed nodes (`type`, `delegates_to`, `maps_to`) → skeleton-first tasks → root README with hand-count manifest.
**Done when:** `skills/delivery-shape/SKILL.md` exists with all required frontmatter fields and the required sections in order (per `docs/skill-anatomy.md`), and its workflow describes emitting the contract's directory layout; length 100–300 lines.
**Model:** Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·L·M·L·L
**Dependencies:** none

### Task 3 — Bake AC-by-default gate + deferred-delegation surfacing into the workflow
**Description:** Add a `[GATE]` to the SKILL.md workflow that emits an Acceptance-criteria block on every `story` node by default and fails loudly if a story has none, and make the emitted node template carry the on-pickup instruction naming its `delegates_to` (fires at build-time, per the contract's *Delegation — timing & surfacing* §).
**Done when:** the SKILL.md workflow contains an AC-by-default `[GATE]` that names `bin/check-plan-framing` as its verification, and the node artefact template includes an on-pickup `delegates_to` line; verified by reading the section against the contract §.
**Model:** Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·L·M·L·L
**Dependencies:** Task 2

### Task 4 — End-to-end conformance verification against the worked-example oracle
**Description:** Confirm the slice holds end-to-end by running both gates against the worked example (the conformant oracle the contract was read off).
**Done when:** `bin/walk-delivery-plan <example>` exits 0 (oracle match) AND `bin/check-plan-framing <example>` exits 0, and `check-plan-framing` exits 1 on an AC-stripped copy of one story node.
**Model:** Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
**Dependencies:** Task 1, Task 3

## Open questions

<!-- None blocking. Resolved during breakdown:
 - delegates_to ENFORCEMENT (presence, exit 2) already lives in bin/walk-delivery-plan (N02, done) —
   this slice only surfaces delegates_to in emitted artefacts, it does not re-implement the check.
 - check-plan-framing scope here is AC-on-every-story only; the skeleton-task / no-pre-skeleton-setup
   checks belong to the foundational-folding node and are deliberately not implemented now. -->
