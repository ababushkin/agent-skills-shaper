---
name: ice-scoring
description: >
  ICE scoring mechanics — Impact, Confidence, Ease dimensions and worked example.
  Used for prioritising validated hypotheses.
type: reference
cited_by:
  - skills/idea-triage/SKILL.md
  - rules/PRODUCT_RULES.md
---

# ICE scoring

ICE is a lightweight scoring method for comparing product hypotheses against each other. The formula is Impact × Confidence × Ease. Sean Ellis coined it; Itamar Gilad incorporated it into the GIST framework. It produces a relative priority number, not an absolute measure of value — a score of 200 in one team's backlog tells you nothing about a 200 in another team's. The Confidence dimension is the most important of the three because it is the hardest to inflate unconsciously: it requires naming actual evidence, not just asserting that the problem matters.

## Dimensions

| Dimension | Question it answers | Score (1–10) |
|---|---|---|
| Impact | If this works, how much does it move the metric that matters? | 1 = negligible, 10 = transformative |
| Confidence | How strong is the evidence that the problem is real and the solution will work? | Calibrated using the Confidence Meter (see `references/confidence-meter.md`) |
| Ease | How hard is this to build and ship? | 1 = very hard, 10 = trivial |

## Formula and score interpretation

**ICE = I × C × E**

Maximum possible score: 1000. That number is not meaningful on its own.

Use ICE to compare options within the same context — same team, same planning cycle, same outcome focus. Do not compare scores across teams or product areas; the inputs are too context-dependent.

Ease is the least reliable dimension at triage stage. Treat it as a rough proxy, not a real estimate. It can be sharpened later with a walking skeleton or technical spike (see `eng-principles-universal.md` Rule B2), but at triage the number is a direction, not a commitment.

## Worked example

**Idea:** Add an in-app onboarding checklist for new users.

| Dimension | Score | Rationale |
|---|---|---|
| Impact | 7 | New user activation is a top-of-funnel metric with direct revenue link; meaningful if it works |
| Confidence | 3 | Indirect data — user research shows confusion during onboarding, but no experiment has been run |
| Ease | 5 | Moderate — checklist UI exists in the component library; backend state management is needed |
| **ICE** | **105** | 7 × 3 × 5 |

Routing: Confidence 3 is below the threshold of 5, so this idea goes to a validation slot, not a build slot. The next step is a targeted experiment or smoke test to raise confidence before any build commitment is made.

## What ICE is not for

**Replacing judgment.** ICE surfaces what deserves discussion; it does not replace the discussion. Two ideas with scores of 200 and 210 are not meaningfully different — argue about the underlying assumptions, not the decimal.

**Comparing fundamentally different bet types.** A growth experiment and a platform investment both get ICE scores, but those scores do not belong on the same scale. Apples-to-oranges comparisons belong in a portfolio allocation conversation (Rule B3), not an ICE sort.

**Validating the idea.** A high ICE score on an opinion-level hypothesis is a high-confidence guess. It does not mean the idea is good; it means someone scored their own assumptions generously. Score the Confidence dimension honestly against actual evidence, using the Confidence Meter. If the evidence is thin, the Confidence score is low — and that is the right answer.

## Sources

- Sean Ellis — coined ICE scoring
- Itamar Gilad — incorporated into GIST Planning; Confidence Meter integration
- `references/confidence-meter.md` — Confidence dimension calibration
