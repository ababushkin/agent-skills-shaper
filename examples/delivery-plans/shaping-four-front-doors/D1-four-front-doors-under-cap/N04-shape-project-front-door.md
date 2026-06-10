---
layer: node
id: N04
type: story
title: "shape:project front door"
parent: D1
serves_kr: KR1
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    The shape:project door exists ≤300 lines (initiative-shape compressed from 310) with
    every [GATE] present and the six-field initiative shape intact, /shape:project
    resolves, and the roadmap-shape and backlog-manage dirs and wrappers are deleted.
delegates_to: at-pickup task breakdown (story); change lands in the agent-skills-shaper repo
---

# N04 — shape:project front door

**Type:** `story` · lands in the **agent-skills-shaper** repo.

> **Blocked by:** [N01](N01-front-door-ia-design-doc.md) — which roadmap-shape and
> backlog-manage sections are absorbed vs deleted is decided there; task breakdown waits
> until the doc is accepted.

> **▶ On pickup:** break into build tasks per the at-pickup breakdown.

## What

As a Shaper invoker, I want `shape:project` to be initiative-shape compressed under the cap
(310 → ≤300), with roadmap-shape's and backlog-manage's content absorbed or deleted per the
IA, so that shaping a committed initiative is one door and the portfolio/backlog ceremony the
pack is shedding is gone. The two pruned dirs and their wrappers are deleted in the same
change.

## Why

The bet: initiative-shape is the only one of the three that produces an artefact downstream
skills consume (the six-field initiative `shape:delivery` decomposes); the other two are
ceremony this pack's single-user reality never exercised. Rejected alternative: compress all
three and keep them — KR1's footprint cap makes three overlapping define-stage skills
unaffordable, and the confirmed intent already decided the deletion. Unblocks N08's sweep for
these two skill names.

## Completion

- **Done when:** the `shape:project` door is ≤300 lines with every `[GATE]` present, the
  six-field initiative shape it emits is unchanged (delivery-shape's gate 2 still consumes it
  verbatim), and `/shape:project` resolves after a fresh `install.sh` run.
- **Done when:** the roadmap-shape and backlog-manage dirs and their wrappers are gone, and a
  re-install prunes their stale `shape-*` symlinks.

## Assumptions

- roadmap-shape and backlog-manage are deletions, not folds-in-full. *(verified — the confirmed pruning list at `docs/ideas/lifecycle-expansion.md:40` deletes both; the IA decides only which fragments are worth absorbing)*
- Compressing initiative-shape 310 → ≤300 costs density, not gates. *(verified — the over-cap delta is 10 lines and the skill's gate count is untouched by a density pass of that size)*

## Key Risks

- **Risk:** the compression or absorption changes the six-field initiative shape and silently
  breaks `shape:delivery`'s up-delegation contract.
  *Mitigation:* the first Done-when asserts the emitted shape is unchanged; the cheapest check
  is re-running delivery-shape's gate 2 against an existing initiative description.

## Tasks

- [ ] `skeleton` — Author the shape:project door from initiative-shape compressed under 300 per the IA (absorbed roadmap/backlog fragments folded in) · Done when: the door is ≤300 lines with every [GATE] present, the six-field shape unchanged, and /shape:project resolves after a fresh install.sh run · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·M·L·M·L
- [ ] Delete the roadmap-shape and backlog-manage dirs and wrappers · Done when: both dirs and wrappers are gone and a re-install prunes their stale shape-* symlinks · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
