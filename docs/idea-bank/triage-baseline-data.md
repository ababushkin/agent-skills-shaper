# Triage record: triage-baseline-data

## Raw intake

> "triage skill should take into account data from the app being improved. the idea is that there is a new skill that lets you calibrate the app and subsequently you either provide data manually to the triage skill, or better yet, the triage skill can reach into other skills (that use an MCP) that can fetch the necessary data. example: improving load speed of the homepage, should probably have some stats about how long the page takes to load, what improvement we're aiming for, etc"

## Problem restatement

The idea arrived as a solution ("a new calibration skill," "triage reaches into MCP-backed skills"). Restated as a problem:

For Shaper users triaging metric-driven improvement ideas (performance, conversion, engagement, reliability), we believe the absence of app-specific baseline data in the triage context is causing ICE Impact and Confidence scores that are unsupported assertions — and problem statements without measurable targets.

## Evidence

Source: skill author (Anton), direct observed use — ran triage on improvement-type ideas and confirmed the data gap materially affects ICE scoring and problem statement quality.

Evidence type: direct observation by primary user (structured comparison). Gilad Confidence: **4**.

Update (2026-05-03): Author confirmed gap is real after running validation. ICE scores without baseline data are unsupported assertions; problem statements lack measurable targets. Routing decisions affected.

## ICE score

| Dimension  | Score (1–10) | Rationale |
|------------|-------------|------------|
| Impact     | 6           | Better-grounded ICE scores improve routing quality. Problem statements with real baselines are actionable at roadmap-shape time. Affects any metric-driven idea triaged — a significant share of the use case. |
| Confidence | 5           | Direct observation by primary user confirms the gap changes outcomes. Raised from 2. Still single-user evidence; no data on frequency across other users. |
| Ease       | 3           | Requires a new calibration skill, changes to triage skill inputs/workflow, and an MCP integration path. Two solution branches (manual input vs. MCP fetch) add design surface and decision overhead. |
| **ICE**    | **90**      |            |

## Routing

**Idea bank** — candidate for roadmap consideration.

Confidence 5 ≥ 5. No further action until `roadmap-shape` runs.

Next spike (when prioritised): determine which solution branch is lower friction — (a) manual baseline data provision at triage time, or (b) MCP-backed fetch via a new calibration skill. Time-box: ≤ 1 day.

## Notes

- Two solution branches in the original idea have different complexity profiles: (a) manual data provision is low-complexity but requires user discipline; (b) MCP-backed fetch is higher complexity but reduces user burden. Neither branch should be designed until the validation confirms the core problem is real.
- Related: the triage skill's evidence interrogation step (step 3) already asks "what evidence exists?" — this idea would extend that to include quantitative baselines, not just qualitative evidence. The change may be additive rather than restructuring.
- If validated, this may also affect `roadmap-shape` — items in the idea bank for improvement ideas would benefit from carrying baseline data alongside the ICE score.
