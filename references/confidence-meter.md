---
name: confidence-meter
description: >
  Calibration scale for evidence quality, used when scoring the Confidence dimension in ICE.
  Source: Itamar Gilad.
type: reference
cited_by:
  - skills/idea-triage/SKILL.md
  - rules/PRODUCT_RULES.md
---

# Confidence Meter

The Confidence Meter is Itamar Gilad's framework for scoring the quality of evidence behind a product hypothesis. It appears in his "GIST Planning" framework and the associated "Confidence Meter" blog post. The scale measures evidence quality — not how strongly someone believes something. A team can hold a conviction at maximum certainty while the underlying evidence is still opinion-level. The distinction matters because it drives routing: low-evidence ideas warrant validation work, not build bets. High-evidence ideas have earned consideration for a build slot.

## The scale

| Level | Score | What it means | Example |
|---|---|---|---|
| Opinion | 0.1 | Assumption, gut feel, executive intuition — no external data | "Our CEO thinks customers want this" |
| Anecdote | 0.5 | One or a few informal observations; not systematically gathered | "A sales rep heard this from two customers" |
| Indirect data | 2–5 | Surveys, market research, user interviews — structured but not causal | "70% of survey respondents said this is painful" |
| Experiment | 5–8 | Smoke tests, A/B tests, prototypes with measured outcomes — causal signal | "Smoke test showed 40% click-through on the fake door" |
| Validated | 8–10 | Launched feature with sustained behavioural data; causal effect observed | "Cohort analysis shows 15% retention lift after 90 days" |

## Applying the scale to ICE

The Confidence score feeds directly into the ICE Confidence dimension. The Gilad scale maps 1:1 to the ICE 1–10 range — Gilad 0.1 becomes ICE Confidence 1; Gilad 8–10 becomes ICE Confidence 8–10. No conversion formula is needed; the ranges map naturally. Assign the score that reflects the best quality of evidence actually in hand, not the evidence the team hopes to gather.

## Common miscalibrations

**Treating strong conviction as high confidence.** Confidence is about evidence quality, not certainty of belief. A highly articulate argument backed by no data is still 0.1. The persuasiveness of the argument is irrelevant to the score.

**Treating "we've seen this pattern before" as indirect data.** Recollection of past patterns without documented evidence is an anecdote (0.5), not market data. Memory of a pattern is not a survey; recalling a past experiment is not the experiment itself.

**Averaging scores across evidence types.** If you have one user interview and one survey, the score is not an average. Take the best evidence type available — the survey sets the floor at 2–5. Blending a 0.5 anecdote with a 3 survey to get 1.75 understates the confidence you actually have.

## Routing implication

In idea-triage, the Gilad score drives the routing gate: below 5 routes to a validation slot; at or above 5 routes to the idea bank as a build candidate. This document does not encode the routing logic — see `skills/idea-triage/SKILL.md` for the full routing workflow.

## Sources

- Itamar Gilad, "Confidence Meter" (blog post)
- Itamar Gilad, "GIST Planning" framework
- `references/ice-scoring.md` — ICE scoring mechanics and worked examples
