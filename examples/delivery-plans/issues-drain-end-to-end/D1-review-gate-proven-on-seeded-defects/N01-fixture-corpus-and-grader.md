---
layer: node
id: N01
type: story
title: Fixture corpus + review grader
parent: D1
serves_kr: KR2
maps_to: linear-issue
skeleton: true
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    bin/grade-execution-review runs every persona prompt file against every fixture
    diff and scores surfaced findings against a seeded manifest of 10
    Critical/Required findings across ≥3 defect classes, caching run logs.
delegates_to: at-pickup task breakdown (story); grader discipline mirrors bin/walk-delivery-plan (stdlib-only, deterministic)
---

# N01 — Fixture corpus + review grader

**Type:** `story` · **Walking skeleton of the whole initiative** (`skeleton: true`).

> **▶ On pickup:** break this node into build tasks per the at-pickup breakdown; the grader
> follows the same stdlib-only, deterministic-reader discipline as `bin/walk-delivery-plan`.

## What

As a skill author hardening the review gate, I want a fixture corpus of diffs with seeded defects
and a grader that scores any persona against them, so that review quality is measured against a
known answer key instead of eyeballed. The corpus lives at `fixtures/execution-review/` — one
fixture diff + one seeded-finding manifest per fixture — and `bin/grade-execution-review` runs
each persona over each diff, diffs surfaced findings against the manifest, and caches the run
under `fixtures/execution-review/_runs/`.

## Why

The bet: building the harness *before* the personas makes KR2 falsifiable from day one and gives
every later persona edit a regression gate instead of a vibe check. Rejected alternative: author
the personas first and grade their output by inspection — no answer key, KR2 unfalsifiable, and
persona quality drifts invisibly with each edit. This node is the initiative's walking skeleton:
it exercises the fixture → persona-run → grade seam end-to-end with a stub persona before any
real persona exists, surfacing the finding-matching problem (the riskiest part of D1) on day one.
It unlocks N03's iterate-to-≥9/10 loop.

## Completion

- **Done when:** `bin/grade-execution-review fixtures/execution-review/` runs every persona
  prompt file it finds against every fixture diff and reports surfaced vs seeded findings with a
  deterministic exit code.
- **Done when:** the corpus seeds 10 Critical/Required findings across ≥3 defect classes (type
  suppression, AC violation, security hole).
- **Done when:** each run's log is cached under `fixtures/execution-review/_runs/`.

## Assumptions

- Seeded-defect diffs can be authored as static fixture files without a live repo to apply them to. *(verified — the graded artefact is the persona's reading of a diff, not a build)*
- A stdlib-only grader can match persona findings to manifest entries deterministically. *(to-verify — matching free-prose findings to seeded entries is the spike-shaped corner of this node; the structured finding format N02 pins is the intended fix)*

## Key Risks

- **Risk:** finding-to-manifest matching is too fuzzy and the grader over- or under-credits
  personas, making the ≥9/10 gate meaningless.
  *Mitigation:* require personas to emit findings in the structured line format the N02 contract
  pins (file · defect class · severity), so matching is exact key comparison, not prose fuzzing.
- **Risk:** seeded defects are too easy, and 9/10 is reachable by a weak persona — false
  confidence in the gate.
  *Falsifier:* a deliberately weak stub persona scores ≥9/10. If it does, harden the corpus
  before grading any real persona.

## Tasks

- [ ] `skeleton` — Seed one fixture diff with a 3-finding manifest and run a stub persona through `bin/grade-execution-review` end-to-end (fixture layout, grader scaffold, and `_runs/` cache folded in) · Done when: the grader exits 0 reporting 3/3 for an oracle stub and non-zero for an empty stub · Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = H·M·L·L·L
- [ ] Grow the corpus to 10 seeded Critical/Required findings across ≥3 defect classes (type suppression, AC violation, security hole) · Done when: the manifest lists 10 findings across ≥3 classes and the weak-stub falsifier scores below 9/10 · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·M·L·L·L
- [ ] Document the grading protocol (run, cache, read results) in the fixture-set README · Done when: a fresh agent can run the grader and interpret a score from the README alone · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
