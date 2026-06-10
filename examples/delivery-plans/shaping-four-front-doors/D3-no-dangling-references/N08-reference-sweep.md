---
layer: node
id: N08
type: story
title: Reference sweep + fresh-install check
parent: D3
serves_kr: KR3
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    Every tracked reference to a deleted/folded skill name is re-pointed or removed, the
    KR3 grep returns only allowlisted mentions per the sweep note, and a fresh
    install.sh / uninstall.sh round-trip yields exactly the survivor wrappers and
    symlinks.
delegates_to: at-pickup task breakdown (story); change lands in the agent-skills-shaper repo
---

# N08 — Reference sweep + fresh-install check

**Type:** `story` · lands in the **agent-skills-shaper** repo.

> **Blocked by:** [N02](../D1-four-front-doors-under-cap/N02-shape-delivery-front-door.md),
> [N03](../D1-four-front-doors-under-cap/N03-shape-idea-front-door.md),
> [N04](../D1-four-front-doors-under-cap/N04-shape-project-front-door.md),
> [N05](../D1-four-front-doors-under-cap/N05-shape-design-front-door.md), and
> [N06](../D1-four-front-doors-under-cap/N06-utilities-under-cap.md) — sweeping before the
> last deletion or the router rewrite lands would pass and then rot in the same cycle.

> **▶ On pickup:** break into build tasks per the at-pickup breakdown.

## What

As a Shaper invoker, I want every cross-cutting reference to a deleted or folded skill —
README tables, `rules/PRODUCT_RULES.md` citations, the three `references/*.md` files, the
idea-bank triage baseline, the instruction files (`AGENTS.md:19` cites `initiative-shape` by
name; CLAUDE.md's authoring sections are N06's job), `hooks/` (named by KR3; zero matches at
baseline, re-checked here), the `plugin.json` description (it names "idea triage, roadmap
shaping" and, being `.json`, is invisible to KR3's `*.md` grep — swept explicitly), and any
remaining cross-skill citation (including initiative C's
plan delegating to `product-spike` by name) — re-pointed to its door or removed, so that the
KR3 grep is the proof and not a wish. The sweep note defines the allowlist: predecessor
frontmatter, `CHANGELOG.md` history, and historical records under `docs/` (ideas,
plan-reviews, emitted delivery plans) are intentional mentions; everything else is dangling.

## Why

The bet: a deleted skill that stays referenced is worse than one that never existed — the
next agent follows the citation into a 404 and improvises. Rejected alternative: sweep
incrementally inside each door node — four partial sweeps with no single proof point is how
KR3's grep ends up "mostly clean"; one node owns the gate. Closes D3 and, with N06, leaves
the pack coherent for initiative C's pointer-only workers, who navigate by exactly these
citations.

## Completion

- **Done when:** the KR3 grep (`grep -rn 'roadmap-shape\|backlog-manage\|app-calibrate'
  --include='*.md' .` over tracked files, plus the folded names idea-triage / backend-spike /
  product-spike) returns only mentions the sweep note's allowlist names.
- **Done when:** `install.sh` on a clean target yields exactly the four door wrappers plus
  utility wrappers and `shape-*` symlinks, and `uninstall.sh` removes them all.

## Assumptions

- CHANGELOG and docs-history mentions count as "intentional" under the KR. *(to-verify — the KR text says "intentional predecessor-frontmatter mentions"; the sweep note proposes the allowlist explicitly and the owner confirms it rather than the gate being quietly widened)*
- The door nodes deleted their own dirs and wrappers, leaving only citations here. *(verified — N03, N04, and N05 each carry a deletion task with its own Done-when; this node's grep would catch any they missed)*

## Key Risks

- **Risk:** an external consumer (initiative C's plan files, drain-cycle prompts, user-level
  CLAUDE.md) still cites a folded skill name after the repo sweep.
  *Mitigation:* the sweep's scope line greps the C plan's `delegates_to` lines explicitly
  (its N05 names `product-spike`); anything outside this repo is recorded in the sweep note
  as a follow-up, not silently skipped.

## Tasks

- [ ] `skeleton` — Sweep all tracked references to deleted/folded skill names across README, rules, references/, idea-bank, AGENTS.md, hooks/, the plugin.json description, and cross-skill citations (sweep-note allowlist drafted as part of the pass) · Done when: the KR3 grep over tracked markdown returns only allowlisted mentions and the plugin.json description names no pruned skill · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·L·L·L·L
- [ ] Run the fresh install/uninstall round-trip · Done when: install.sh on a clean target yields exactly the survivor wrappers and symlinks and uninstall.sh removes them all · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
