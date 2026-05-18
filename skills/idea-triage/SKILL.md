---
name: idea-triage
description: >
  Intake gate for new ideas. Use when an idea arrives in any form — request, observation,
  suggestion, feedback — and needs to be interrogated, scored, and routed before any action
  is taken. Trigger phrases: "we should build", "a customer asked for", "I had an idea",
  "can we add", "what if we", "competitor just launched".
pack: product
lifecycle_stage: define
principles_implemented:
  - source: product
    id: P2
    bucket: embedded
  - source: product
    id: P3
    bucket: embedded
  - source: product
    id: P4
    bucket: embedded
  - source: product
    id: A2
    bucket: embedded
  - source: product
    id: A5
    bucket: embedded
  - source: product
    id: A6
    bucket: embedded
  - source: product
    id: B2
    bucket: embedded
  - source: product
    id: B6
    bucket: embedded
length_target: 200–280
author: Anton Babushkin
predecessor:
  repo: https://github.com/addyosmani/agent-skills
  skill: idea-refine
  relation: adjacent
kept_from_predecessor: >
  The instinct to slow down and interrogate an idea before acting on it. Raw ideas need
  structured questioning before they can do useful work.
changed_from_predecessor: >
  Scope is narrower: single-idea triage, not multi-round refinement. This skill is a gate —
  it runs once, produces a structured record, and routes the idea. Confidence scoring via
  Gilad's ICE is a required output, not optional enrichment. PRODUCT_RULES vocabulary
  throughout. "When not to use" explicitly names KTLO/compliance items (Rule A5 carve-out).
---

# Idea triage

## Purpose

idea-triage is the intake gate for the product system. It fires when an idea arrives in any form — verbal, written, issue, customer request, competitive observation — and its job is to answer three questions before that idea goes anywhere: Is it framed as a problem or a solution? Is there evidence, and how much? Is the problem worth pursuing at all? The skill produces a triage record — not a refined idea, not a spec, not a decision — and routes that record to either the idea bank or a validation slot based on confidence. This is the mechanism by which Rules P2, P3, P4, A2, A6, B2, and B6 get applied at the moment an idea first enters the system, before any solution thinking begins.

## When to use

Run this skill when an idea arrives from outside the existing roadmap and backlog: a user request, a stakeholder suggestion, customer feedback, a competitive observation, an internal brainstorm output, or an anomaly spotted in analytics. The triage step is cheap; the cost of skipping it is not. Run it regardless of idea size.

## When not to use

- **KTLO work** — bug fixes, compliance items, partner obligations, minor maintenance go straight to the backlog without triage (Rule A5). Do not wrap these in outcome hypotheses to justify them; do not let real product work hide inside them.
- **Ideas already on the roadmap being refined or scoped** — that is design-doc or implementation territory.
- **Ideas that already hold a triage record and confidence score** — re-triage only if material new evidence arrives that changes the score.
- **Multi-round, open-ended refinement** — use the idea-refine skill (addy/agent-skills) when the goal is iterative exploration rather than a single intake decision.

## Inputs

The raw idea in whatever form it arrived: a sentence, a Slack message, a customer quote, a feature request, a competitor announcement, an analytics anomaly. No special format required at intake. The skill works with whatever text is provided and interrogates it from there.

Optional: `docs/app-context.md` in the current project root. When present, the skill uses baseline metrics to ground Impact scoring and to add a measurable target to the problem statement. When absent, scoring proceeds without baseline data — suggest running `app-calibrate` first for improvement-type ideas (improving, reducing, increasing, or speeding up something measurable).

## Outputs

A triage record filed at `docs/idea-bank/<idea-slug>.md`. The record conforms to the A2 template (problem / customer / outcome) and carries a mandatory ICE score and routing decision.

## Workflow

**1. Capture the idea verbatim.**
Write it down exactly as received. Do not interpret, reframe, or improve it yet. The verbatim capture is the first field of the triage record.

**2. [GATE] Diagnose: problem or solution?**
Read the raw intake. Is the idea framed as a solution ("we should build X") or a problem ("users can't do Y")? If it is a solution, restate the underlying problem before proceeding. If you cannot articulate the underlying problem — if there is no answer to "what goes wrong for which customer if we don't build this?" — the idea is not ready for triage. Return it to the submitter for clarification. Do not proceed.

**3. Interrogate the evidence.**
Who is affected? How often? What is the observable negative outcome? What evidence exists that this problem is real? Assign a Confidence score using Gilad's Confidence Meter:
- Opinion, assertion, assumption: 0.1
- Anecdote, one-off observation: 0.5
- Survey data, market research: 2–5
- Experiment, smoke test, prototype test: 5–8
- Validated launch, sustained behavioural data: 8–10

Name the specific evidence and the type. "Our sales team hears this a lot" is an anecdote (0.5), not data.

**Baseline check.** If `docs/app-context.md` exists in the current project: read it. Identify the 1–2 metrics most relevant to this idea's domain. Record their Current values, Targets, and Sources in the Evidence section of the triage record. Apply the data-source calibration from `references/app-context-schema.md`: manually entered metrics count as Gilad 2–3; metrics from live MCP sources count as Gilad 4–6. Metrics with a Last measured date > 90 days old are treated as Gilad 1–2.

If `docs/app-context.md` does not exist and the idea is improvement-type: note the absence in the Evidence section and recommend `app-calibrate` before proceeding. Do not block triage — proceed with gut-estimated Impact, but flag it.

**4. Write the problem statement.**
Apply the A2 template: "For [customer segment], we believe [problem] is causing [negative outcome]." Write it out. Do not paraphrase it; fill in the three blanks.

If baseline data is available from `docs/app-context.md`: include a measurable target in the negative outcome clause. Format: "...causing [negative outcome] — currently at [baseline value], targeting [target]." If no baseline data: proceed without it; the problem statement is valid but mark it as lacking a measurable target.

**5. [GATE] Does the problem statement hold?**
Can you name the customer segment, the problem, and the negative outcome clearly and specifically? If any of the three blanks cannot be filled with something concrete — if they contain hedges like "various users" or "some friction" — the idea is not ready. Return for clarification or discard. Do not proceed.

**6. Score ICE.**
Assign three scores on a 1–10 scale:
- **Impact**: expected magnitude of change on a customer or business metric if this problem is solved.
- **Confidence**: the Gilad score from step 3, scaled to 1–10. A Gilad 0.1 maps to ICE Confidence 1; a Gilad 8–10 maps to ICE Confidence 8–10.
- **Ease**: rough effort proxy — how hard is this to solve? Ease is an estimate only; do not over-invest in it at triage stage.

**Grounding Impact on baseline data.** If app-context baseline data is available for this idea's metric: ground the Impact score on the expected delta from the Current value toward the Target. A 20–30% improvement on a primary metric = Impact 7–8; improvement on a secondary metric = 4–6; marginal improvement on any metric = 2–3. If no baseline data is present: estimate as usual, but add a note in the ICE score table rationale column: "ungrounded — no app-context baseline."

Compute ICE = Impact × Confidence × Ease.

**7. [GATE] Route the idea.**
Check the Confidence score:
- Confidence < 5: route to **validation slot**. Do not assign a build bet. Name the type of validation work needed to raise confidence. This is a hard gate — low confidence earns a validation slot, not a build slot (Rule B6).
- Confidence ≥ 5: route to **idea bank** as a candidate for roadmap consideration. File the record and stop. No further action until `roadmap-shape` runs — the triage record is not a trigger for implementation.

There is no parking lot (Rule A6). Every triaged idea goes to exactly one of these two places.

**Choosing the validation method (for validation slot items only).** Pick by dominant unknown:

| Dominant unknown | Method |
|---|---|
| Product feel — how the interaction works, whether a flow makes sense | `product-spike` |
| Customer reality — does this problem exist, how often, for whom | Customer interview or survey |
| Market signal — will people pay, sign up, switch | Smoke test or landing-page test |
| Technical feasibility — can we build this, at what cost | Spike (→ `design-doc`) |

One method per validation slot. If multiple unknowns exist, pick the riskiest one and run that method first. Prototype is not the default — it is specifically for product feel unknowns.

**8. Write and file the triage record.**
Fill in the artefact template below and file it at `docs/idea-bank/<idea-slug>.md`.

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
<!-- Confidence score (Gilad): [0.1–10] — state the evidence type that drives this score. -->

## ICE score
| Dimension  | Score (1–10) | Rationale                  |
|------------|-------------|----------------------------|
| Impact     |             | <!-- expected magnitude --> |
| Confidence |             | <!-- evidence quality -->   |
| Ease       |             | <!-- rough effort proxy --> |
| **ICE**    | **= I×C×E** |                            |

## Routing
<!-- idea bank | validation slot -->
<!-- Live status field — backlog-manage reads and updates this section over the idea's lifecycle. -->
<!-- State the routing and the reason. If validation slot: name the type of validation
     work needed to raise confidence (customer interview, smoke test, experiment, etc.). -->

## Notes
<!-- Anything the author needs a future reader to know: related items in the idea bank,
     strategic context that influenced the score, assumptions baked into the evidence
     assessment. -->
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "We know the customer wants this — no need to score it low." | An assertion about customer want is an anecdote (0.5) until there is data. Score it honestly and let the routing logic decide. |
| "It's a small idea, triage is overkill." | Triage is a 10-minute gate. Skipping it is how small ideas accumulate into a roadmap nobody believes in. |
| "The CEO asked for it, so the confidence is high." | CEO opinion is 0.1 on the Confidence Meter. That is the whole point of Rule B2. Route it to validation like anything else at that confidence level. |
| "We can just put it in a parking lot for now." | Rule A6: there is no parking lot. The idea bank is the only holding area for unvalidated hypotheses. |
| "It's clearly a problem framing, we don't need to write it out." | If it's clear, writing it out takes two minutes. If it takes more than two minutes, it wasn't as clear as assumed. |
| "Low confidence just means we need to build and see." | That is a build bet on an unvalidated hypothesis. Rule B6: low confidence earns a validation slot, not a build slot. |
| "This is a bug fix / compliance item — does it need triage?" | No. Rule A5 carve-out: KTLO work goes straight to backlog. This is exactly the "when not to use" case. |

## Red flags

- The triage record has no Confidence score, or the score is left blank.
- The problem statement contains "users," "customers," or "people" without a named segment.
- The routing decision says "parking lot," "TBD," or "revisit later."
- The evidence section cites opinions or assertions at Confidence > 0.5.
- The raw intake field has been edited or paraphrased.
- A build bet is being proposed for an idea with Confidence < 5.
- The idea is framed as a solution in the problem restatement field.

## Verification / exit criteria

The skill has run correctly when:

1. A triage record exists at `docs/idea-bank/<idea-slug>.md`.
2. All six template sections are filled in (raw intake, problem restatement, evidence, ICE score, routing, notes).
3. The problem restatement matches the A2 format exactly: "For [customer segment], we believe [problem] is causing [negative outcome]."
4. The Confidence score is explicitly tied to a named evidence type.
5. The routing decision names exactly one destination: idea bank or validation slot (not both, not neither, not a parking lot).
6. If routed to validation slot, the record names the specific validation method (prototype, interview, smoke test, or spike) and the dominant unknown it will resolve.
7. If routed to idea bank (Confidence ≥ 5), no further action is taken on this idea until `roadmap-shape` runs. The triage record is not a trigger for implementation.

## References

- `rules/PRODUCT_RULES.md` — P2, P3, P4, A2, A5, A6, B2, B6 (direct trace)
- `references/confidence-meter.md` — Gilad's Confidence Meter calibration scale
- `references/ice-scoring.md` — ICE scoring mechanics and worked examples
- `references/app-context-schema.md` — baseline data schema, validity rules, and sourcing calibration
- `skills/app-calibrate/SKILL.md` — app context creation and refresh
- Itamar Gilad, "GIST Planning" and "Confidence Meter" (external)
- Marty Cagan, "Inspired" — problem-vs-solution framing, SVPG
- Janna Bastow, Now-Next-Later roadmap — A6 idea bank / roadmap distinction
