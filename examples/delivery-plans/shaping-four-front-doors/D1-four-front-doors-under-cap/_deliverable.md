---
layer: deliverable
id: D1
title: Four front doors under the cap
parent: ..
serves_kr: KR1
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR1 holds — four front doors ≤300 lines each, zero skills in the measured set over
    300, total shaping footprint ≤2,200 lines, proven by the wc -l cap check over the
    survivor manifest the N01 design doc pins.
---

# D1 — Four front doors under the cap

**Serves:** KR1 *(bet)* — "4 front doors ≤300 lines each, zero skills over 300, total shaping
footprint ≤2,200 lines" (baseline 14 skills / 3,086 lines; over-cap: plan-review 369,
initiative-shape 310, roadmap-shape 303 — all verified against `wc -l skills/*/SKILL.md`
2026-06-10).

**Rule A1 trips** — three triggers hold, any one suffices: the deliverable breaks into 6 nodes
(> ~5); the absorption map is a **one-way door** (folded skills are deleted, and the door
namespace publishes into every install via `install.sh`'s wrapper generation and `shape-*`
symlinks); and it touches **shared infrastructure** (the command wrappers, the skill symlinks,
`using-this-pack` routing, and the plugin manifest every session resolves through). So the
first node is **N01**, a `design-doc` node; N02–N06's task breakdowns wait until that doc is
accepted, and each is `> **Blocked by:**` N01.

## Nodes

- [N01 — Front-door IA design doc](N01-front-door-ia-design-doc.md) · `design-doc`
- [N02 — shape:delivery front door](N02-shape-delivery-front-door.md) · `story` · `skeleton`
- [N03 — shape:idea front door](N03-shape-idea-front-door.md) · `story`
- [N04 — shape:project front door](N04-shape-project-front-door.md) · `story`
- [N05 — shape:design front door](N05-shape-design-front-door.md) · `story`
- [N06 — Utilities under the cap](N06-utilities-under-cap.md) · `story`

## Done when

KR1 is observed: the cap check exits clean over the measured set — four doors present, each
≤300 lines, no survivor over 300, total ≤2,200. Reducible to N01–N06 done (N06's final task is
the footprint check itself); no acceptance node needed.
