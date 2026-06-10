---
layer: node
id: N03
type: story
title: "shape:idea front door"
parent: D1
serves_kr: KR1
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    The shape:idea door exists ≤300 lines with every [GATE] the IA maps into it present,
    /shape:idea resolves, and the idea-triage and app-calibrate skill dirs and wrappers
    are deleted.
delegates_to: at-pickup task breakdown (story); change lands in the agent-skills-shaper repo
---

# N03 — shape:idea front door

**Type:** `story` · lands in the **agent-skills-shaper** repo.

> **Blocked by:** [N01](N01-front-door-ia-design-doc.md) — the absorption map (which
> idea-triage sections fold in, which app-calibrate content is absorbed vs deleted) is decided
> there; task breakdown waits until the doc is accepted.

> **▶ On pickup:** break into build tasks per the at-pickup breakdown.

## What

As a Shaper invoker, I want a single `shape:idea` door that carries idea-triage's discipline —
folded per the IA's absorption map, with app-calibrate's content absorbed where the map says
so and deleted with rationale where it doesn't — so that the first shaping step is one
invocation, not a routing decision between three overlapping skills. The folded source dirs
and their command wrappers are deleted in the same change.

## Why

The bet: triage is a phase of idea-shaping, not a sibling skill — folding it removes the
routing ambiguity `using-this-pack` currently papers over. Rejected alternative: keep
idea-triage as a thin alias door — an alias preserves the line-count problem KR1 exists to
kill and leaves two names for one discipline. Unblocks N08's sweep for these two skill names.

## Completion

- **Done when:** the `shape:idea` door is ≤300 lines, every `[GATE]` the IA maps into it is
  present, and `/shape:idea` resolves after a fresh `install.sh` run.
- **Done when:** the idea-triage and app-calibrate dirs and their command wrappers are gone,
  and `install.sh`'s prune removes their stale `shape-*` symlinks on a re-install.

## Assumptions

- idea-triage's fold target is shape:idea and app-calibrate is delete-with-absorption. *(verified — the confirmed pruning list at `docs/ideas/lifecycle-expansion.md:40`; not re-litigated here)*
- The combined fold fits under 300 (idea-triage 220 + app-calibrate's absorbed remainder compressing into one door). *(to-verify — the IA's absorption map sizes the fold; if it lands 300–350 the door ships at the hard cap with the overage flagged, and over 350 without dropping a [GATE] fires the kill condition)*

## Key Risks

- **Risk:** app-calibrate content that looked deletable was load-bearing for
  `references/app-context-schema.md` consumers.
  *Mitigation:* the IA's deletion rationale names each dropped section and its dependents;
  N08's sweep catches any reference left pointing at deleted content.

## Tasks

- [ ] `skeleton` — Author the shape:idea door folding idea-triage per the IA's absorption map (app-calibrate's absorbed sections folded in) · Done when: the door is ≤300 lines with every mapped [GATE] present and /shape:idea resolves after a fresh install.sh run · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·M·L·M·L
- [ ] Delete the idea-triage and app-calibrate dirs and wrappers · Done when: both dirs and wrappers are gone and a re-install prunes their stale shape-* symlinks · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
