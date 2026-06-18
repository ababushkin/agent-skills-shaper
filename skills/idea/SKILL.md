---
name: idea
description: 'Intake gate for new ideas: elicit and refine the idea, take evidence, and route. Comparative scoring runs only when asked. Use when an idea arrives in any form — request, observation, suggestion, feedback — and needs a triage record. Trigger phrases: "we should build", "a customer asked for", "I had an idea", "can we add", "what if we", "competitor just launched".'
---

# Shape: idea

## Purpose

shape:idea is the intake gate for the product system. It fires when an idea arrives in any form — verbal, written, issue, customer request, competitive observation — and answers three questions before that idea goes anywhere: What does the person actually mean? Is it framed as a problem or a solution? Does the evidence warrant a build slot or a validation slot? The skill leads with a short elicitation loop that sharpens the idea, then takes evidence, names the problem (A2), and routes to either the idea bank or a validation slot based on Confidence. Comparative scoring (ICE, Kano) runs only if the person asks to rank this idea against others.

## When to use

Run when an idea arrives from outside the existing roadmap and backlog: a user request, a stakeholder suggestion, customer feedback, a competitive observation, an internal brainstorm output, or an analytics anomaly. The intake step is cheap; the cost of skipping it is not.

If the idea targets a measurable improvement and `docs/app-context.md` is missing or stale (last measured >90 days), populate or refresh that file per `references/app-context-schema.md` before assessing evidence — an ungrounded judgement is an assertion, not data.

## Do not use when

- **KTLO work** — bug fixes, compliance items, partner obligations, minor maintenance go straight to the backlog without triage (Rule A5). Do not wrap these in outcome hypotheses.
- **Ideas already on the roadmap being refined or scoped** — use `shape:design` instead.
- **Ideas that already hold a triage record with a confirmed restate** — re-triage only if material new evidence or a real change of intent arrives.
- **Non-interactive contexts (CI, scheduled jobs, drain workers)** — the elicitation loop needs a live, responsive human. Flag the ask as a blocker rather than guess.

## Inputs

The raw idea in whatever form it arrived: a sentence, a Slack message, a customer quote, a feature request, a competitor announcement, an analytics anomaly. No special format required. A live person available to answer questions.

Optional: `docs/app-context.md` at the current project root. When present, the skill uses baseline metrics to ground the evidence interrogation. When absent and the idea is improvement-type, flag the absence and note that grounding is missing.

## Outputs

A triage record at `docs/idea-bank/<idea-slug>.md`. The record leads with **Raw intake → Refined intent** (the confirmed restate, surfaced assumptions, open questions) before Evidence and Routing. The Confidence score is mandatory; the ICE table is optional and appears only when the comparative-scoring step ran.

## Workflow

### 1. Capture the idea verbatim

Write the idea exactly as received. Do not interpret, reframe, or improve it. The verbatim capture is the first field of the triage record.

### 2. Elicit and refine the idea

Run the elicitation loop in `references/idea-elicitation.md`: lead with a one-sentence hypothesis and a confidence number; ask one question at a time, each carrying its own best guess; listen for want-vs-should-want and probe with "if you didn't have to justify this, what would you actually want?"; restate intent in a six-line block (Outcome / User / Why now / Success / Constraint / Out of scope); loop until the person says an explicit yes. The 95% stop applies — done when you can predict reactions to the next three questions.

Record the confirmed restate in the Refined intent section along with the assumptions the loop surfaced and any open questions it could not close. Do not proceed without the explicit yes.

### 3. Gate: problem or solution?

Is the confirmed restate framed as a solution ("we should build X") or a problem ("users can't do Y")? The elicitation loop will usually have surfaced the underlying problem already; this gate verifies the framing made it into the restate. If you cannot articulate a problem — no answer to "what goes wrong for which customer if we don't build this?" — return to the submitter for clarification. Do not proceed.

### 4. Interrogate the evidence

Who is affected? How often? What is the observable negative outcome? What evidence exists? Assign a Confidence score using Gilad's Confidence Meter:

- Opinion, assertion, assumption: 0.1
- Anecdote, one-off observation: 0.5
- Survey data, market research: 2–5
- Experiment, smoke test, prototype test: 5–8
- Validated launch, sustained behavioural data: 8–10

Name the specific evidence and its type. "Our sales team hears this a lot" is an anecdote (0.5), not data.

**Baseline check.** If `docs/app-context.md` exists: read it, identify the 1–2 metrics most relevant to this idea's domain, and record their Current values, Targets, and Sources in the Evidence section. Apply the data-source calibration from `references/app-context-schema.md`: manually entered metrics count as Gilad 2–3; live MCP sources count as Gilad 4–6; metrics with Last measured >90 days are treated as Gilad 1–2. If the file exists but fewer than 2 metric rows have Current values, note that grounding remains incomplete — the baseline does not meet the minimum validity threshold.

If `docs/app-context.md` does not exist: note the absence and proceed with a gut-estimated assessment, flagging it as ungrounded.

### 5. Write the problem statement

Apply the A2 template: "For [customer segment], we believe [problem] is causing [negative outcome]." If baseline data is available, include a measurable target: "...causing [negative outcome] — currently at [baseline value], targeting [target]."

### 6. Gate: does the problem statement hold?

Can you name the customer segment, the problem, and the negative outcome clearly and specifically? If any blank contains hedges like "various users" or "some friction," return for clarification or discard. Do not proceed.

### 7. Gate: route the idea

Check the Confidence score:

- Confidence < 5: route to **validation slot**. Name the type of validation work needed (see table below). This is a hard gate — low confidence earns a validation slot, not a build slot (Rule B6).
- Confidence ≥ 5: route to **idea bank**. File the record and stop. No further action until `shape:project` runs — the triage record is not a trigger for implementation.

Before writing the routing decision, announce the destination and the mutation to the record, and confirm before committing. There is no parking lot (Rule A6) — every triaged idea goes to exactly one of these two places.

**Choosing the validation method (validation-slot items only).** Pick by dominant unknown:

| Dominant unknown | Method |
|---|---|
| Product feel — how the interaction works, whether a flow makes sense | `shape:design` (product spike) |
| Customer reality — does this problem exist, how often, for whom | Customer interview or survey |
| Market signal — will people pay, sign up, switch | Smoke test or landing-page test |
| Technical feasibility — can we build this, at what cost | `shape:design` (technical spike) |

One method per validation slot. If multiple unknowns exist, pick the riskiest one first.

### 8. (Optional) Score ICE and Kano lens

Skip unless the person explicitly asks to rank this idea against others. Comparative scoring is a separate decision; running it by default anchors the conversation on a number instead of the problem, and rewards ideas that are easy to score over ideas that are well-understood.

When asked:

- **ICE** (`references/ice-scoring.md`): score Impact (1–10), Confidence (the Gilad score scaled to 1–10), and Ease (1–10), then compute ICE = I × C × E. Ground Impact on the expected delta from Current toward Target when baseline data is available; mark as "ungrounded" otherwise.
- **Kano lens** (`references/kano-classification.md`): name whether the idea reads as Basic, Performance, or Delighter, and what that implies for prioritisation.

Record only what actually ran. If only ICE was requested, omit the Kano line.

### 9. Write and file the triage record

Fill in the artefact template and file it at `docs/idea-bank/<idea-slug>.md`. The Score section appears only if step 8 ran; otherwise omit it entirely (do not leave a blank table).

## Artefact template

```markdown
# Triage record: <idea-slug>

## Raw intake
<!-- Verbatim capture of the idea as received. Do not edit. -->

## Refined intent
<!-- The confirmed six-line restate from the elicitation loop, in the user's own words. -->
- Outcome:
- User:
- Why now:
- Success:
- Constraint:
- Out of scope:

**Assumptions surfaced:**
<!-- One bullet per assumption the elicitation loop exposed. -->

**Open questions:**
<!-- One bullet per question the loop could not resolve. Leave empty if none. -->

## Problem restatement
<!-- "For [customer segment], we believe [problem] is causing [negative outcome]." -->
<!-- If the idea arrived as a solution, record the original solution framing here and
     explain the restatement. -->

## Evidence
<!-- What evidence exists that this problem is real and affects the named customer?
     Be specific: quote, data point, observation. Name the source. -->
<!-- Confidence score (Gilad): [0.1–10] — state the evidence type. -->

## Routing
<!-- idea bank | validation slot -->
<!-- State the routing and the reason. If validation slot: name the validation
     method and the dominant unknown it will resolve. -->

## Score (optional)
<!-- Include this section only if step 8 ran (the person asked to rank this idea). -->

| Dimension  | Score (1–10) | Rationale                  |
|------------|-------------|----------------------------|
| Impact     |             |                            |
| Confidence |             |                            |
| Ease       |             |                            |
| **ICE**    | **= I×C×E** |                            |

**Kano lens (optional):** Basic / Performance / Delighter — rationale.

## Notes
<!-- Anything a future reader needs: related items, strategic context. -->
```

## Red flags

- The triage record has no Refined intent section, or the restate was never confirmed with an explicit yes.
- The skill opened with a score before the elicitation loop ran.
- The Confidence score is blank or untied to a named evidence type.
- The problem statement contains "users," "customers," or "people" without a named segment.
- The routing decision says "parking lot," "TBD," or "revisit later."
- Evidence cites opinions or assertions at Confidence > 0.5.
- The raw intake field has been edited or paraphrased.
- A build bet is proposed for an idea with Confidence < 5.
- The idea is framed as a solution in the problem restatement field.
- An ICE table is filed even though no comparative ranking was requested.

## Exit criteria

The skill has run correctly when:

1. A triage record exists at `docs/idea-bank/<idea-slug>.md`.
2. Raw intake and Refined intent are populated; the restate was confirmed with an explicit yes.
3. The problem restatement matches the A2 format exactly: "For [customer segment], we believe [problem] is causing [negative outcome]."
4. The Confidence score is explicitly tied to a named evidence type.
5. The routing decision names exactly one destination: idea bank or validation slot (not both, not neither, not a parking lot).
6. If routed to validation slot, the record names the specific validation method and the dominant unknown it will resolve.
7. If routed to idea bank (Confidence ≥ 5), no further action is taken until `shape:project` runs.
8. The Score section is present only when step 8 ran; otherwise omitted entirely.

## Related

- `rules/PRODUCT_RULES.md` — P2, P3, P4, A2, A5, A6, B2, B6
- `references/idea-elicitation.md` — the elicitation loop run in step 2
- `references/confidence-meter.md` — Gilad's Confidence Meter calibration scale
- `references/ice-scoring.md` — ICE scoring mechanics and worked examples (optional tail step)
- `references/kano-classification.md` — idea classification by customer value type (optional tail step)
- `references/app-context-schema.md` — baseline data schema, validity rules, and sourcing calibration
