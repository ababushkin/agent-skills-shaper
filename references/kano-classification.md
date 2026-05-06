---
name: kano-classification
description: >
  Five-category taxonomy for classifying feature types by user satisfaction response.
  Source: Noriaki Kano, 1984. Used in idea-triage to set scope expectations and detect delight traps.
type: reference
cited_by:
  - skills/idea-triage/SKILL.md
---

# Kano Classification

The Kano model is Noriaki Kano's 1984 framework for classifying product features by how their presence or absence affects user satisfaction. It is not a prioritisation method — it does not produce a rank order. Its purpose is to identify what category a feature belongs to so the team can set the right scope expectations, spot delight traps, and understand why adding more of something eventually stops mattering.

## The five categories

| Category | Absent | Present | Implication |
|---|---|---|---|
| Must-be | Causes strong dissatisfaction | Neutral — taken for granted | Required floor; not differentiating. Missing it causes damage; adding more does nothing. |
| Performance | Causes dissatisfaction proportional to absence | Causes satisfaction proportional to presence | Linear returns. More is better; less is worse. Benchmarkable. |
| Excitement (Delighter) | Neutral — not missed | Causes delight disproportionate to cost | Differentiating if surprising. Ignored if poorly executed. High risk of over-build. |
| Indifferent | Neutral | Neutral | No measurable satisfaction effect. Remove or deprioritise; do not invest. |
| Reverse | Causes satisfaction if absent | Causes dissatisfaction if present | Some users actively do not want this. Segment before building. |

## Using Kano at triage

At the idea-triage stage, Kano classification sets scope expectations before confidence scoring begins. The classification does not override ICE — it informs it.

**Must-be:** If the idea is restoring a missing floor, treat it as KTLO unless there is evidence the floor was never established. Confidence requirement: direct data (user complaints, churn signals). Scope the fix narrowly.

**Performance:** Standard ICE applies. Linear return means the marginal value of scope additions is predictable — size the work accordingly.

**Excitement:** High risk of over-build. Excitement features delight only when the execution is surprising and polished; a mediocre implementation produces neutral or negative response. Require experiment-level confidence before committing build resources. Smoke tests and prototypes are the right validation instrument.

**Indifferent:** Flag at triage and route to deprioritisation. Do not build unless forced by dependency.

**Reverse:** Do not proceed without segmentation. If a meaningful user segment actively does not want the feature, building it for one segment may damage another. Segmentation analysis is a prerequisite, not a post-launch discovery.

## Decay

Kano categories are not permanent. Excitement features decay to Performance as users habituate, then to Must-be as the capability becomes assumed. Features that were differentiating in one generation become table stakes in the next. A category assigned at triage reflects the current state of user expectations, not a timeless property of the idea. Revisit classification when market context shifts significantly.

## Sources

- Noriaki Kano, "Attractive Quality and Must-Be Quality" (1984)
- Marty Cagan, "Inspired: How to Create Tech Products Customers Love"
- `skills/idea-triage/SKILL.md` — routing workflow that applies Kano categories at triage
