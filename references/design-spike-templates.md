# Design and spike artefact templates

## Design document — `docs/design-docs/<name>/design-doc.md`

```markdown
---
name:
status: draft | in-review | accepted | superseded
authors:
created:
last_updated:
supersedes: <path to prior doc, or "none">
---

# <title>

## Problem

<!-- What is wrong or missing? Who is affected, and how? Current vs. desired
     behaviour. No solution language here. -->

## Context

<!-- Background, history, related prior decisions (link ADRs). What has been
     tried? Which constraints were inherited rather than chosen? -->

## Constraints

<!-- Functional and non-functional requirements. NFRs must have numbers:
     latency at p95, availability SLO, throughput, cost envelope. Each NFR
     names its fitness function — the automated check that verifies it. -->

## Alternatives considered

<!-- At least two, including "do nothing." For each: description, blast radius
     if wrong, reversal cost. Only the chosen approach = incomplete. -->

## Recommended approach

<!-- The proposed solution. Why it wins on the named constraints. -->

## Consequences

<!-- Positive and negative. Whether a walking skeleton should precede the full
     build and why. If integration risks are fully known, say so. -->

## Operability plan

<!-- Metrics, structured logs, traces, alerts (thresholds + routing), rollback
     plan (ordered steps + verification gate per step), capacity headroom,
     known failure modes with mitigations, upstream and downstream dependency
     failure modes. Required. Absent = reject. -->

## Open questions

<!-- Each has an owner and a resolution gate — the slice or milestone blocked
     until it is answered. -->
```

## Backend spike recommendation — `docs/spikes/<slug>/recommendation.md`

```markdown
# Backend spike: <slug>

Date: <date>
Steps used: <n> of <time-box cap>

## Question

[One sentence.]

## Failure example

[The concrete case that motivated the spike.]

## Options considered

| Option | What it does | Handles failure example? | Failure mode |
|---|---|---|---|
| <A> | … | Yes / Partially / No | <input where A fails> |
| <B> | … | Yes / Partially / No | <input where B fails> |
| <C> | … | Yes / Partially / No | <input where C fails> |

## Scope

[Adjacent paths checked. In-scope / out-of-scope statement. Follow-up spike named if applicable.]

## Recommended approach

**<Option name>**

[One paragraph: what it does, why it handles the failure example, why each rejected alternative was ruled out — with its specific failure mode.]

## Confidence and semantics impact

- Confidence: <Gilad score> — <evidence cited>
- Semantics delta: <how the output meaning changes, or "none">
- Failure ceiling: <worst-case impact if this recommendation is wrong>

## Follow-up

Implementation ticket: <title or link>
Acceptance criterion: the failure example produces <expected result>.
```

## Product spike finding — `docs/prototypes/<slug>/finding.md`

```markdown
# Prototype finding: <slug>

Date: <date>
Time boxed: <duration>
Time used: <actual>

## Question

[One sentence.]

## Approach

[What was built or written, and why this mode was chosen.]

## Observations

[What was seen — raw observations, not interpretations.]

## Finding

[Interpretation: what do the observations mean?]

## Recommendation

**Proceed / Reshape / Kill**

[One paragraph — why this recommendation and what the next step is.]

## Prototype artefact

[Link to mockup, or path to code with non-production marking, or "deleted".]
```
