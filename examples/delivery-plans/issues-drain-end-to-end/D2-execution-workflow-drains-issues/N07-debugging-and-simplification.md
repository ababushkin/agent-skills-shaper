---
layer: node
id: N07
type: story
title: Debugging + simplification skills
parent: D2
serves_kr: KR1
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    A systematic-debugging skill (hypothesis → instrument → bisect, root-cause note
    gated) and a simplification skill (post-green pass with reviewable rationale)
    exist, both reachable by name from the build skill's escalation/exit points.
delegates_to: at-pickup task breakdown (story); authoring per docs/skill-anatomy.md
---

# N07 — Debugging + simplification skills

**Type:** `story`.

> **Blocked by:** [N04](N04-execution-workflow-design-doc.md) — task breakdown waits until the
> design doc is accepted. Also [N06](N06-build-skill-red-green-commit.md) — the wiring task edits
> the build skill's escalation/exit points, so N07's branch must chain onto N06's in the PR stack.

> **▶ On pickup:** break into build tasks per the at-pickup breakdown; author per
> `docs/skill-anatomy.md`; declare each skill's predecessor relation in frontmatter (no verbatim
> ports).

## What

As a worker stuck on a failing build or finishing a green one, I want systematic-debugging and
simplification skills, so that failures resolve by hypothesis and evidence rather than
retry-flailing, and green code sheds incidental complexity before review. These are the two
domain skills confirmed in at the interview (frontend/perf/browser explicitly out).

## Why

The bet: the two failure modes that most often force a human rescue mid-drain are undiagnosed
failures (worker loops on retries) and over-built diffs (reviewer drowns) — these skills target
exactly those, which is why they made the shortlist and the rest didn't. Rejected alternative:
keep superpowers installed for its debugging skill alone — that keeps the third-party dependency
alive and makes KR3's uninstall impossible. **Port-first:** both are straight ports —
superpowers' `systematic-debugging` and agent-skills' `code-simplification` (both MIT) — with
light modification only (anatomy frontmatter, voice, the N04 graph seams). Do not re-author
proven discipline.

## Completion

- **Done when:** the debugging skill encodes hypothesis → instrument → bisect → fix with a
  written root-cause note as a gate (no fix without a stated cause).
- **Done when:** the simplification skill runs as a post-green pass emitting a reviewable
  before/after rationale.
- **Done when:** both are reachable by name from the build skill's escalation and exit points.

## Assumptions

- Two skills (not one) is the right split — debugging fires mid-loop, simplification fires post-green. *(verified — they occupy different trigger points in the N04 graph; folding them would blur both triggers)*

## Key Risks

- **Risk:** the port mutates the source's proven discipline while adapting voice and anatomy —
  losing exactly the content that justified porting instead of re-authoring.
  *Mitigation:* frontmatter declares the predecessor relation (port); the PR notes what was
  changed against the source and why, so review checks the deltas, not the whole text.

## Tasks

- [ ] `skeleton` — Port superpowers' `systematic-debugging` (MIT) with the root-cause-note gate added (skill dir + frontmatter folded in) · Done when: the ported skill passes anatomy order and the no-fix-without-stated-cause gate is marked `[GATE]` · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·L·L·L·L
- [ ] Port agent-skills' `code-simplification` (MIT) as the post-green pass with before/after rationale · Done when: the ported skill emits a reviewable simplification note on a sample diff · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·L·L·L·L
- [ ] Wire both into the build skill's escalation and exit points by name · Done when: the build skill names both delegations and neither is inlined · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
