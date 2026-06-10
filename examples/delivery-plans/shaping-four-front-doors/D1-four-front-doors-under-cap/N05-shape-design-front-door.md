---
layer: node
id: N05
type: story
title: "shape:design front door"
parent: D1
serves_kr: KR1
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    The shape:design door folds design-doc, backend-spike, and product-spike per the IA
    into ≤300 lines (hard 350) with every mapped [GATE] present, /shape:design resolves,
    and the two spike dirs and wrappers are deleted. This is the kill-condition watch
    node for the fold clause.
delegates_to: at-pickup task breakdown (story); change lands in the agent-skills-shaper repo
---

# N05 — shape:design front door

**Type:** `story` · lands in the **agent-skills-shaper** repo. The heaviest fold in the plan:
design-doc 243 + backend-spike 205 + product-spike 189 = **637 source lines into one ≤300-line
door** — this node is where the initiative kill condition's first clause ("a front door can't
absorb its folded skills under 350 lines without dropping a `[GATE]`") is watched.

> **Blocked by:** [N01](N01-front-door-ia-design-doc.md) — the spike-fold structure (one door
> with a spike branch vs spike protocols as door-internal sections) is decided there; task
> breakdown waits until the doc is accepted.

> **▶ On pickup:** break into build tasks per the at-pickup breakdown; if the fold cannot
> close under 350 without dropping a `[GATE]`, stop and surface the kill condition — do not
> ship a gateless door.

## What

As a Shaper invoker, I want one `shape:design` door covering both the design-doc discipline
and the spike protocols (backend and product) per the IA's absorption map, so that "I need to
de-risk or decide before building" is one entry point whether the answer is a doc, a technical
spike, or a product spike. The two spike dirs and their wrappers are deleted in the same
change; design-doc's dir follows the IA's naming decision.

## Why

The bet: spikes and design docs are the same lifecycle moment (decide/de-risk before build)
with different artefacts, so one door with a typed branch reads denser than three skills with
overlapping When-to-use sections. Rejected alternative: keep the spikes as utilities — that
blows the ≤3-utility manifest and retains the routing ambiguity. Unblocks N08's sweep for the
spike skill names. Note: initiative C's plan delegates to `product-spike` by name (its N05
experiment node) — the IA's naming decision feeds N08's citation sweep so that delegation
line is re-pointed, not left dangling.

## Completion

- **Done when:** the `shape:design` door is ≤300 lines (350 hard, overage flagged), every
  `[GATE]` the IA maps from the three sources is present, and `/shape:design` resolves after
  a fresh `install.sh` run.
- **Done when:** the backend-spike and product-spike dirs and wrappers are gone, a re-install
  prunes their stale symlinks, and the kill-condition watch note records the final line count
  against the 350 bound.

## Assumptions

- The three-way fold fits under 350 without dropping a `[GATE]`. *(to-verify — 637 → ≤300 is a 2:1 compression; the IA's absorption map sizes it first, and the kill condition is the documented exit if it doesn't hold)*
- The spike protocols' completion forms (decision + stop condition; hypothesis + metric) survive as sections, not separate skills. *(verified — `docs/delivery-shape-contract.md`'s node-type vocabulary already carries spike and experiment forms independent of which skill file hosts the protocol)*

## Key Risks

- **Risk:** the fold compresses away the spike stop-conditions — the exact discipline that
  prevents unbounded investigation.
  *Mitigation:* the gate-preservation inventory (N01) lists every `[GATE]` and stop-condition
  in the three sources; the first Done-when checks presence against that list, not against
  reviewer memory.

## Tasks

- [ ] `skeleton` — Author the shape:design door folding design-doc and both spike protocols per the IA's absorption map · Done when: the door is ≤350 lines with every mapped [GATE] present and /shape:design resolves after a fresh install.sh run · Model: Balanced · risk reversible · review elevated · axes RC·SC·HS·SR·OR = H·M·L·M·L
- [ ] Compress to ≤300 or record the flagged overage and kill-condition watch note · Done when: the door is ≤300, or 300–350 with the overage and retained gates recorded in the watch note · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·M·L·L·L
- [ ] Delete the backend-spike and product-spike dirs and wrappers · Done when: both dirs and wrappers are gone and a re-install prunes their stale shape-* symlinks · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
