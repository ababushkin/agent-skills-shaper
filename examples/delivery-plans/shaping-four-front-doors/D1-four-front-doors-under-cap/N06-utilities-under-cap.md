---
layer: node
id: N06
type: story
title: Utilities under the cap
parent: D1
serves_kr: KR1
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    plan-review is compressed 369 → ≤300 with gates and eval assertions unchanged,
    using-this-pack routes only the four doors plus utilities, the frontmatter cut is
    applied across survivors, and the full KR1 footprint check passes over the measured
    set (zero files over 300, total ≤2,200).
delegates_to: at-pickup task breakdown (story); change lands in the agent-skills-shaper repo
---

# N06 — Utilities under the cap

**Type:** `story` · lands in the **agent-skills-shaper** repo. Closes D1: its final task is
the KR1 footprint check itself.

> **Blocked by:** [N01](N01-front-door-ia-design-doc.md) — the survivor manifest, measured
> set, and frontmatter-cut spec come from the accepted doc. Also
> [N02](N02-shape-delivery-front-door.md)–[N05](N05-shape-design-front-door.md) for the final
> footprint check only — the survivor set must be in its end state before the total is
> measured.

> **▶ On pickup:** break into build tasks per the at-pickup breakdown.

## What

As a Shaper invoker, I want the surviving utilities brought to the same bar as the doors:
plan-review compressed from 369 to ≤300 (the largest over-cap survivor — density reform, not
gate removal, with its eval assertions untouched), `using-this-pack` rewritten so its routing
table names only the four doors and the utilities, and the IA's frontmatter cut applied across
every survivor — then the KR1 footprint check run over the measured set as the deliverable's
closing proof.

## Why

The bet: plan-review's 369 lines compress without behaviour change because its length is
explanatory redundancy, not gate prose — and KR2's benchmark exists precisely to catch this
bet failing. Rejected alternative: exempt plan-review from the cap as a "deep utility" —
that makes KR1's "zero skills over 300" false on day one and normalises the next exemption.
Unblocks N07 (the benchmark measures the compressed plan-review, so it cannot run before this
lands).

## Completion

- **Done when:** plan-review is ≤300 lines, its `[GATE]` count is unchanged, and
  `skills/plan-review/evals/evals.json` is byte-identical (the benchmark measures prose
  reform, not moved goalposts).
- **Done when:** `using-this-pack`'s routing table names only the four doors and the
  utilities, and every survivor's frontmatter matches the IA's cut spec.
- **Done when:** the repo's authoring contract states the new rules — `docs/skill-anatomy.md`
  and CLAUDE.md's required-frontmatter and length sections equal the IA's spec, so the pack's
  own docs don't contradict every reformed skill.
- **Done when:** the KR1 footprint check passes — `wc -l` over the measured set shows zero
  files over 300 and a total ≤2,200, recorded for the cycle retro note.

## Assumptions

- plan-review's overage is explanatory redundancy, not load-bearing gate prose. *(to-verify — the compression is attempted against the gate-preservation inventory; if a cut drops a benchmark assertion's support, N07's re-run catches it and the repair loop restores it)*
- The measured set totals ≤2,200 after all folds. *(to-verify — arithmetic only closes once the doors exist; the IA's absorption map gives the projection, this node's footprint check gives the proof)*

## Key Risks

- **Risk:** compression changes plan-review's behaviour in ways line counts and gate greps
  cannot see.
  *Mitigation:* that risk is exactly D2 — N07 re-runs the 5-scenario benchmark against the
  compressed skill with a defined repair loop; this node keeps the eval set byte-identical so
  the comparison is valid.

## Tasks

- [ ] `skeleton` — Compress plan-review 369 → ≤300 as pure density reform (gate lines and eval assertions kept verbatim) · Done when: plan-review is ≤300 lines with [GATE] count unchanged and evals.json byte-identical · Model: Balanced · risk reversible · review elevated · axes RC·SC·HS·SR·OR = H·M·L·M·L
- [ ] Rewrite using-this-pack's routing to the four doors and apply the frontmatter cut across survivors · Done when: the routing table names only doors + utilities and every survivor's frontmatter matches the IA spec · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·L·L·L·L
- [ ] Update the authoring contract to the IA spec (docs/skill-anatomy.md plus CLAUDE.md's required-frontmatter and length sections) · Done when: the documented required fields and length rules equal the IA's surviving set · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
- [ ] Run the KR1 footprint check over the measured set · Done when: zero files over 300 and total ≤2,200, with the counts recorded for the cycle retro note · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
