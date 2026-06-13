---
name: idea
description: >
  Intake gate for new ideas. Interrogates, scores, and routes an idea before any action
  is taken. Use when an idea arrives in any form — request, observation, suggestion,
  feedback — and needs a triage record. Trigger phrases: "we should build",
  "a customer asked for", "I had an idea", "can we add", "what if we",
  "competitor just launched".
---

# Shape: idea

## Purpose

shape:idea is the intake gate for the product system. It fires when an idea arrives in any form — verbal, written, issue, customer request, competitive observation — and answers three questions before that idea goes anywhere: Is it framed as a problem or a solution? Is there evidence, and how much? Is the problem worth pursuing? The skill produces a triage record — not a spec, not a decision — and routes it to either the idea bank or a validation slot based on confidence. This is how Rules P2, P3, P4, A2, A6, B2, and B6 get applied at the moment an idea enters the system, before any solution thinking begins.

## When to use

Run when an idea arrives from outside the existing roadmap and backlog: a user request, a stakeholder suggestion, customer feedback, a competitive observation, an internal brainstorm output, or an anomaly spotted in analytics. The triage step is cheap; the cost of skipping it is not.

If the idea targets a measurable improvement and `docs/app-context.md` is missing or stale (last measured >90 days), populate or refresh that file per `references/app-context-schema.md` before scoring — an ungrounded Impact score is an assertion, not evidence.

## Do not use when

- **KTLO work** — bug fixes, compliance items, partner obligations, minor maintenance go straight to the backlog without triage (Rule A5). Do not wrap these in outcome hypotheses.
- **Ideas already on the roadmap being refined or scoped** — use `shape:design` instead.
- **Ideas that already hold a triage record and confidence score** — re-triage only if material new evidence arrives.
- **Multi-round, open-ended refinement** — use the `idea-refine` skill (addy/agent-skills).

## Inputs

The raw idea in whatever form it arrived: a sentence, a Slack message, a customer quote, a feature request, a competitor announcement, an analytics anomaly. No special format required.

Optional: `docs/app-context.md` at the current project root. When present, the skill uses baseline metrics to ground Impact scoring. When absent and the idea is improvement-type, flag the absence and note that Impact is ungrounded.

## Outputs

A triage record at `docs/idea-bank/<idea-slug>.md`. The record conforms to the A2 template (problem / customer / outcome) and carries a mandatory ICE score and routing decision.

## Workflow

**1. Capture the idea verbatim.**
Write it down exactly as received. Do not interpret, reframe, or improve it yet. The verbatim capture is the first field of the triage record.

**2. [GATE] Diagnose: problem or solution?**
Is the idea framed as a solution ("we should build X") or a problem ("users can't do Y")? If it is a solution, restate the underlying problem before proceeding. If you cannot articulate a problem — no answer to "what goes wrong for which customer if we don't build this?" — return to the submitter for clarification. Do not proceed.

**3. Interrogate the evidence.**
Who is affected? How often? What is the observable negative outcome? What evidence exists? Assign a Confidence score using Gilad's Confidence Meter:
- Opinion, assertion, assumption: 0.1
- Anecdote, one-off observation: 0.5
- Survey data, market research: 2–5
- Experiment, smoke test, prototype test: 5–8
- Validated launch, sustained behavioural data: 8–10

Name the specific evidence and its type. "Our sales team hears this a lot" is an anecdote (0.5), not data.

**Baseline check.** If `docs/app-context.md` exists: read it, identify the 1–2 metrics most relevant to this idea's domain, and record their Current values, Targets, and Sources in the Evidence section. Apply the data-source calibration from `references/app-context-schema.md`: manually entered metrics count as Gilad 2–3; live MCP sources count as Gilad 4–6; metrics with Last measured >90 days are treated as Gilad 1–2. If the file exists but fewer than 2 metric rows have Current values, note that Impact scoring remains ungrounded — the baseline does not meet the minimum validity threshold.

If `docs/app-context.md` does not exist: note the absence and proceed with gut-estimated Impact, flagging it as ungrounded.

**4. Write the problem statement.**
Apply the A2 template: "For [customer segment], we believe [problem] is causing [negative outcome]." If baseline data is available, include a measurable target: "...causing [negative outcome] — currently at [baseline value], targeting [target]."

**5. [GATE] Does the problem statement hold?**
Can you name the customer segment, the problem, and the negative outcome clearly and specifically? If any blank contains hedges like "various users" or "some friction," return for clarification or discard. Do not proceed.

**6. Score ICE.**
Assign three scores on a 1–10 scale:
- **Impact**: expected magnitude of change on a customer or business metric if solved. If baseline data is available, ground Impact on the expected delta from Current toward Target: a 20–30% improvement on a primary metric = 7–8; secondary metric = 4–6; marginal = 2–3. If no baseline data: estimate as usual, note "ungrounded — no app-context baseline" in the rationale.
- **Confidence**: the Gilad score scaled to 1–10.
- **Ease**: rough effort proxy — how hard is this to solve? Estimate only; do not over-invest at triage stage.

Compute ICE = Impact × Confidence × Ease.

**7. [GATE] Route the idea.**
Check the Confidence score:
- Confidence < 5: route to **validation slot**. Name the type of validation work needed (see table below). This is a hard gate — low confidence earns a validation slot, not a build slot (Rule B6).
- Confidence ≥ 5: route to **idea bank**. File the record and stop. No further action until `shape:project` runs — the triage record is not a trigger for implementation.

Before writing the routing decision, announce the destination and the mutation to the record, and confirm before committing. There is no parking lot (Rule A6) — every triaged idea goes to exactly one of these two places.

**Choosing the validation method (validation slot items only).** Pick by dominant unknown:

| Dominant unknown | Method |
|---|---|
| Product feel — how the interaction works, whether a flow makes sense | `shape:design` (product spike) |
| Customer reality — does this problem exist, how often, for whom | Customer interview or survey |
| Market signal — will people pay, sign up, switch | Smoke test or landing-page test |
| Technical feasibility — can we build this, at what cost | `shape:design` (technical spike) |

One method per validation slot. If multiple unknowns exist, pick the riskiest one first.

**8. Write and file the triage record.**
Fill in the artefact template and file it at `docs/idea-bank/<idea-slug>.md`.

## Artefact template

```markdown
# Triage record: <idea-slug>

## Raw intake
<!-- Verbatim capture of the idea as received. Do not edit. -->

## Problem restatement
<!-- "For [customer segment], we believe [problem] is causing [negative outcome]." -->
<!-- If the idea arrived as a solution, record the original solution framing here and
     explain the restatement. -->

## Evidence
<!-- What evidence exists that this problem is real and affects the named customer?
     Be specific: quote, data point, observation. Name the source. -->
<!-- Confidence score (Gilad): [0.1–10] — state the evidence type. -->

## ICE score
| Dimension  | Score (1–10) | Rationale                  |
|------------|-------------|----------------------------|
| Impact     |             | <!-- expected magnitude --> |
| Confidence |             | <!-- evidence quality -->   |
| Ease       |             | <!-- rough effort proxy --> |
| **ICE**    | **= I×C×E** |                            |

## Routing
<!-- idea bank | validation slot -->
<!-- State the routing and the reason. If validation slot: name the validation
     method and the dominant unknown it will resolve. -->

## Notes
<!-- Anything a future reader needs: related items, strategic context, assumptions. -->
```

## Red flags

- The triage record has no Confidence score, or the score is blank.
- The problem statement contains "users," "customers," or "people" without a named segment.
- The routing decision says "parking lot," "TBD," or "revisit later."
- Evidence cites opinions or assertions at Confidence > 0.5.
- The raw intake field has been edited or paraphrased.
- A build bet is proposed for an idea with Confidence < 5.
- The idea is framed as a solution in the problem restatement field.
- Impact is scored above 3 on an improvement idea with no `docs/app-context.md` baseline.

## Exit criteria

The skill has run correctly when:

1. A triage record exists at `docs/idea-bank/<idea-slug>.md`.
2. All six template sections are filled in (raw intake, problem restatement, evidence, ICE score, routing, notes).
3. The problem restatement matches the A2 format exactly: "For [customer segment], we believe [problem] is causing [negative outcome]."
4. The Confidence score is explicitly tied to a named evidence type.
5. The routing decision names exactly one destination: idea bank or validation slot (not both, not neither, not a parking lot).
6. If routed to validation slot, the record names the specific validation method and the dominant unknown it will resolve.
7. If routed to idea bank (Confidence ≥ 5), no further action is taken until `shape:project` runs.

## Related

- `rules/PRODUCT_RULES.md` — P2, P3, P4, A2, A5, A6, B2, B6
- `references/confidence-meter.md` — Gilad's Confidence Meter calibration scale
- `references/ice-scoring.md` — ICE scoring mechanics and worked examples
- `references/app-context-schema.md` — baseline data schema, validity rules, and sourcing calibration
- `references/kano-classification.md` — idea classification by customer value type
