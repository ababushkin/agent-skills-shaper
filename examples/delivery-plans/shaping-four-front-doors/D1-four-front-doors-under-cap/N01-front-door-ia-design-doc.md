---
layer: node
id: N01
type: design-doc
title: Front-door IA design doc
parent: D1
serves_kr: KR1
maps_to: linear-issue
external_window: none
completion:
  form: accepted-design-doc
  criterion: >
    The accepted doc fixes the absorption map (every one of the 14 baseline skills mapped
    to fold / delete / survive, section by section), the survivor manifest and the measured
    set for the ≤2,200 check, the frontmatter-cut spec, the door directory / wrapper /
    symlink / router naming (consuming A/N04's naming table), and the gate-preservation
    inventory.
delegates_to: design-doc (Rule A1 branch — the doc is authored via that skill at pickup)
---

# N01 — Front-door IA design doc

**Type:** `design-doc` · lands in the **agent-skills-shaper** repo. The Rule A1 node for D1:
the absorption map is a one-way door (folded skills get deleted) published through shared
install infrastructure, so it is decided once, in a reviewed doc, before any door is built.

> **Blocked by:** initiative A's
> [N04](../../issues-drain-end-to-end/D2-execution-workflow-drains-issues/N04-execution-verb-namespace-design-doc.md) —
> A's design doc decides the verb-namespace naming table; this doc consumes that table so the
> `shape:*` doors and A's execution verbs are named from one scheme, not two.

> **▶ On pickup:** author the doc via the `design-doc` skill; N02–N06's task breakdowns wait
> until it is accepted.

## What

Decide the information architecture the four doors are built against: which sections of
idea-triage, app-calibrate, initiative-shape, roadmap-shape, backlog-manage, design-doc,
backend-spike, and product-spike fold into which door, and which content is deliberately
deleted with a written rationale; the survivor manifest (4 doors + ≤3 utilities) and **the
measured set for the ≤2,200-line check** — initiative A is concurrently adding execution
skills to `skills/`, so `wc -l skills/*/SKILL.md` drifts for reasons outside this initiative
and the doc must pin which files KR1 counts; the frontmatter-cut spec (which of the current
ten fields survive, against `docs/skill-anatomy.md`); and the door directory / command-wrapper
/ `shape-*` symlink / `using-this-pack` route naming, consuming A/N04's naming table.

## Why

The bet: one reviewed IA decision makes the four door builds mechanical compression jobs
instead of four separate judgement calls that drift apart. Rejected alternative: let each door
node decide its own absorption inline — that re-decides the same one-way door four times, and
a dropped `[GATE]` in one fold surfaces only at the benchmark, not at review. Unblocks N02–N06
(their task breakdowns wait on this doc) and gives N08 the deletion list it sweeps against.

## Completion

Prose form (design-doc): the accepted doc covers the absorption map for all 14 baseline
skills, the survivor manifest plus the measured set for the cap check, the frontmatter-cut
spec, the naming scheme consumed from A/N04's table, and the gate-preservation inventory —
every `[GATE]` line in a folded skill mapped to a destination section or a written deletion
decision.

## Assumptions

- A/N04's naming table is accepted before this node is picked up. *(verified — enforced by the blockedBy edge onto ABA-361; cycle planning cannot pull this node first)*
- KR1's measured set excludes the execution skills initiative A adds to `skills/`. *(to-verify — the KR baseline counted the pre-A 14-skill set; the doc pins the measured set explicitly and the owner confirms it at doc acceptance, rather than the KR being silently rewritten)*
- `plan-review`, `render-html`, and `using-this-pack` are the ≤3 utilities. *(verified — the confirmed intent names plan-review and render-html as survivors at `docs/ideas/lifecycle-expansion.md:40`, and `using-this-pack` is the router the doors are reached through)*

## Key Risks

- **Risk:** the absorption map silently drops a `[GATE]` from a folded skill, and the loss is
  discovered only when the benchmark or a live shaping run misbehaves.
  *Mitigation:* the gate-preservation inventory is a named task with its own Done-when — every
  `[GATE]` in the eight folded/compressed skills is enumerated and mapped before the doc is
  accepted.
- **Risk:** the doc scope creeps into authoring the doors' prose inline.
  *Mitigation:* the doc fixes maps, manifests, and naming only; door prose is N02–N05's work
  at pickup — same boundary delivery-shape itself draws (agentic P7).

## Tasks

- [ ] `skeleton` — Draft the IA doc via the design-doc skill (absorption map, survivor manifest + measured set, frontmatter-cut spec, naming consumed from A/N04's table folded in) · Done when: the doc exists under docs/designs/ with all 14 baseline skills mapped to fold / delete / survive · Model: Frontier · risk one-way door · review elevated · axes RC·SC·HS·SR·OR = H·H·L·H·L · companions code-review-and-quality
- [ ] Compile the gate-preservation inventory and fold it into the doc · Done when: every `[GATE]` line in the eight folded/compressed skills appears in the doc mapped to a destination section or a written deletion rationale · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·M·L·M·L
