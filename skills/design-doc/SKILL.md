---
name: design-doc
description: Produce a structured design document before any non-trivial implementation begins. Use when someone asks "how should we build X", "what's the architecture for Y", "should we build or buy Z", or when work breaks into more than ~5 verifiable slices, contains a one-way-door decision, touches shared infrastructure, or meaningfully affects users, cost, or compliance — even if no doc was explicitly requested. Trigger phrases: "how do we build", "design this", "architecture for", "technical approach to", "what's the plan for building", "let's spec this out".
---

# Design doc

## Purpose

Produce a structured design document — Problem, Context, Constraints, Alternatives, Recommended approach, Consequences, Operability, Open questions — before any non-trivial implementation begins.

The structure forces problem-first reasoning: the doc cannot be finished without working through the problem, the alternatives, and the operability plan in order. The deliverable is the document reviewers evaluate before any code is written, not the code itself.

## When to use

At least one trigger must fire; any single one is sufficient:

1. The work breaks into more than roughly five independently verifiable slices, or contains a one-way-door decision (schema migration, public API, vendor lock-in, auth boundary, production-data touch).
2. The capability will be used by parties outside the team building it.
3. The change has meaningful impact on users, operational cost, or compliance posture.

If a trigger is ambiguous, default to writing the doc. A short, fast doc costs less than a build that starts on a misunderstood problem.

## Do not use when

- No trigger fires — write a short ADR instead. A design doc for sub-threshold work is overhead.
- The problem is not yet understood — run a spike first, then return. A design doc for an undefined problem describes the solution you assumed, not the problem you have.
- The change is purely additive, clearly reversible, and has no shared-interface surface — proceed directly to implementation.

## Inputs

- A problem description or feature request, however rough
- Named stakeholders and affected users
- Known constraints — functional and non-functional
- A rough slice count or one-way-door flag suggesting at least one trigger fires
- Prior design docs and ADRs for related capabilities

## Outputs

Artefact path: `docs/design-docs/<kebab-case-name>/design-doc.md`

A complete design doc with every section present, the Operability section fully populated, ready for review before implementation begins.

## Workflow

### 1. Gate: trigger check

Verify at least one trigger holds and state which one. If none holds, stop and recommend an ADR. If the problem itself is not yet understood, stop and recommend a spike. Do not proceed without naming the trigger.

### 2. Context load

Load prior design docs and ADRs for related work, and name each artefact loaded. State what has been tried and which constraints are inherited.

### 3. Gate: problem section

Draft the Problem section first — no solution language until it is complete. It must name the affected users, current behaviour, and desired behaviour. A statement that slides into solution language ("users can't do X, so we should build Y") is sent back for rewrite. Proceed only when the problem is stated in problem terms.

### 4. Context and constraints

Document background, history, and related prior decisions; link relevant ADRs. List non-functional requirements with numbers and units: latency at p95, availability SLO, throughput target, cost envelope, error budget, security posture. For each NFR, name its fitness function — the automated check that verifies it continuously. "Fast", "reliable", and "scalable" are not NFRs.

### 5. Alternatives

List at least two alternatives, including "do nothing". For each: a description, the blast radius if it turns out wrong, and the reversal cost. One approach listed is an incomplete doc. If you cannot say what is wrong with the alternatives, you cannot explain why the recommendation is right.

### 6. Recommended approach

State the recommendation and why it beats the named alternatives on the named constraints. This comes after alternatives because the problem shapes the recommendation, not the reverse.

### 7. Consequences

Name positive and negative consequences. State explicitly whether a walking skeleton should precede the full build — the minimal end-to-end implementation, one request path wired through every real component in the real deployment environment. Pre-skeleton estimates are uncalibrated. If the path to production is already clear and integration risks are fully known, say so.

### 8. Gate: operability plan

Complete every sub-field: metrics, structured logs, traces, alerts (thresholds and on-call routing), rollback plan (ordered steps with a verification gate per step), capacity headroom, known failure modes with mitigations, and upstream/downstream dependency failure modes. A skeletal or absent Operability section means the doc is not ready for review. Author it with the people who will operate the system, not in isolation.

### 9. Open questions

List every unresolved question. Each carries an owner and a resolution gate — the slice or milestone blocked until it is answered. Questions without owners or gates are known unknowns being politely ignored. Use calendar dates only when resolution depends on an external human commitment (vendor reply, legal review).

### 10. Review hand-off

Before sharing, dispatch the `writing-editor` persona (`agents/writing-editor/AGENT.md`) over the completed document, per the dispatch protocol in `docs/adr/0003-persona-contract-and-dispatch-protocol.md` — the `Agent` tool on Claude Code, inline self-review on a non-Claude worker. Apply its line-level rewrites. On `reject`, repair and re-run once; if it still rejects, carry the remaining notes forward as `accept with notes` rather than blocking. The persona edits prose only; the section set and order remain this skill's gates.

Then share the completed document for review before any implementation begins. Implementation starts only after acceptance. Sharing a draft with known incomplete sections is not a hand-off.

## Artefact template

Write the prose in every section against `references/writing-rules.md` — the Core rules and Design docs sections. Those rules govern how each section reads; the section set and order below are this skill's own gates, not the rules file's.

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

## Red flags

- Problem section contains solution language ("we will build…", "using X we can…").
- NFRs use adjectives instead of numbers ("fast", "highly available", "scalable").
- Alternatives section lists only the chosen approach.
- Operability section is absent, placeholder, or a stub.
- No fitness function named for any NFR.
- Walking skeleton not addressed in Consequences.
- Open questions have no owners or no resolution gates.
- Effort or scope expressed in days/weeks/months rather than slices or gates.
- Document shared for review while known sections are incomplete.
- Implementation started before acceptance.

## Exit criteria

The design doc passes review when:

1. At least one trigger is named and confirmed.
2. All sections are present and populated.
3. Every NFR has a number, a unit, and a named fitness function.
4. Alternatives contains at least two options including "do nothing", each with blast radius and reversal cost.
5. The Operability plan covers all required sub-fields.
6. The walking-skeleton recommendation is addressed in Consequences.
7. Every open question has an owner and a resolution gate.
8. No implementation work started before acceptance.
9. The Step 10 writing-editor pass returned `accept` or `accept with notes`.

## Related

- ADR — the right artefact when no trigger fires.
- spike — run first when the problem itself is not yet understood.
- delivery-shape: a design-doc-worthy deliverable emits a `design-doc` node that delegates here before its build nodes' task breakdown.
- `references/nfr-categories.md` — NFR taxonomy.
- `references/writing-rules.md` — prose ruleset every section is written against.
- `agents/writing-editor/AGENT.md` — the writing-editor persona dispatched at Step 10.
