---
layer: deliverable
id: D1
title: Review gate proven on seeded defects
parent: ..
serves_kr: KR2
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR2 holds — bin/grade-execution-review fixtures/execution-review/ reports the
    persona set surfacing ≥9 of 10 seeded Critical/Required findings, with run logs
    cached under fixtures/execution-review/_runs/.
---

# D1 — Review gate proven on seeded defects

**Serves:** KR2 *(foundation)* — "The review/verify skills surface ≥9 of 10 seeded
Critical/Required findings when run against fixture diffs with known defects."

This deliverable is the foundation the whole initiative stands on: a review gate whose quality is
*measured against a known answer key*, not asserted. It lands first because everything downstream
trusts it — the entry skill (N05) delegates its review step to the fan-out skill built here, and
the uninstall (N11) is only safe once the first-party replacement for `/code-review-and-quality`
demonstrably catches what the third-party skill caught. KR2's own baseline names the fixture set +
grader as the first issue.

Its three nodes carry the proof end-to-end: **N01** (story, the initiative's walking skeleton)
builds the fixture corpus and the grader and proves the grading seam with a stub persona; **N02**
(ADR) pins the persona contract — file format, structured finding format, dispatch protocol with
non-Claude fallback; **N03** (story) authors the three personas and the review fan-out skill and
iterates them to the ≥9/10 target.

## Nodes

- [N01 — Fixture corpus + review grader](N01-fixture-corpus-and-grader.md) · `story` · `skeleton`
- [N02 — ADR: persona contract + dispatch protocol](N02-adr-persona-contract.md) · `adr`
- [N03 — Personas + review fan-out skill](N03-personas-and-review-fan-out.md) · `story`

## Done when

KR2 is observed: `bin/grade-execution-review fixtures/execution-review/` runs each persona
against each fixture diff, diffs surfaced findings against the seeded manifest, and reports
≥9/10 — reducible to its children's criteria (N03's last task *is* the KR observation), so no
acceptance node exists here.
