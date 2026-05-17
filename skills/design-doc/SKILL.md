---
name: design-doc
description: >
  Produce a structured design document before any non-trivial implementation begins.
  Use when someone asks "how should we build X", "what's the architecture for Y",
  "should we build or buy Z", or when work breaks into more than ~5 verifiable
  slices, contains a one-way-door decision, touches shared infrastructure, or
  meaningfully affects users, cost, or compliance. Also use when
  an engineer is about to start a significant project with no written design —
  even if they haven't asked for a doc explicitly. Trigger phrases: "how do we
  build", "design this", "architecture for", "technical approach to", "what's the
  plan for building", "let's spec this out".
pack: engineering
lifecycle_stage: define
principles_implemented:
  - source: eng-universal
    id: P2
    bucket: standalone
  - source: eng-universal
    id: Rule A1
    bucket: embedded
  - source: eng-universal
    id: Rule A2
    bucket: standalone
  - source: eng-universal
    id: Rule A4
    bucket: embedded
  - source: eng-universal
    id: Rule A5
    bucket: embedded
  - source: eng-universal
    id: Rule A6
    bucket: embedded
  - source: eng-universal
    id: Rule B2
    bucket: embedded
  - source: eng-universal
    id: Rule B3
    bucket: embedded
  - source: eng-agentic
    id: P1
    bucket: embedded
  - source: eng-agentic
    id: P3
    bucket: embedded
  - source: eng-agentic
    id: P5
    bucket: embedded
  - source: eng-agentic
    id: P8
    bucket: embedded
length_target: 250-300
author: Anton Babushkin
predecessor:
  repo: https://github.com/addyosmani/agent-skills
  skill: spec-driven-development
  relation: derivative
kept_from_predecessor:
  - Premise that a written spec must precede implementation
  - Structured intake discipline — problem before solution language
  - Principle that reviewing a document is cheaper than reviewing code built on a misunderstood problem
changed_from_predecessor:
  - Structure anchored to Rule A2 (seven mandatory sections), not left to author discretion
  - Rule A1 supplies three explicit trigger conditions governing when a design doc is required
  - Walking skeleton (Rule B2) is a required named gate before implementation detail is filled in
  - Operability section (Rule A6) is a hard reject condition, not an optional section
  - Common rationalisations section required by Agentic P5
  - When not to use explicitly names right alternatives: ADR for sub-threshold, spike for unknowns
---

# Design doc

## Purpose

This skill produces a structured design document before any non-trivial implementation begins. It is the operational form of universal Principle 2 (design starts with the problem, not the stack): the seven-section structure mandated by Rule A2 makes solution-first approaches structurally incomplete. An agent or engineer cannot finish the artefact without working through Problem, Context, Constraints, Alternatives, and Operability in that order. The skill governs when a design doc is required (Rule A1), what structure it must follow (Rule A2), and which sections are hard rejections when absent (Rule A6). The deliverable is the document reviewers evaluate before any code is written — not the code itself.

## When to use

At least one Rule A1 trigger must fire. Any single trigger is sufficient:

1. The work breaks into more than roughly five independently verifiable slices, or contains any one-way-door decision (schema migration, public API, vendor lock-in, auth boundary, production-data touch). This is the agentic translation of universal Rule A1's "more than four weeks" trigger (see `eng-principles-agentic.md` P8: effort in slices and gates, not calendar time).
2. The capability will be used by parties outside the team building it.
3. The change has meaningful impact on users, operational cost, or compliance posture.

If a trigger is ambiguous, default to writing the doc. A short, fast doc costs less than a build that starts on a misunderstood problem.

## When not to use

- **None of the three triggers fire** — write a short ADR instead (Rule A3). A design doc for sub-threshold work is overhead; an ADR is the right fit.
- **The problem is not yet understood** — run a `spike` first, then return here. Writing a design doc for an undefined problem produces a document about the solution you assumed, not the problem you have.
- **Change is purely additive, clearly reversible, and has no shared-interface surface** — proceed directly to implementation. Not every shipped line needs a design doc.

## Inputs

- A problem description or feature request, however rough
- Named stakeholders and affected users
- Known constraints — functional and non-functional
- A rough slice count (or one-way-door flag) that suggests at least one Rule A1 trigger fires
- Prior design docs and ADRs for related capabilities (loaded per Agentic P1)
- Access to `rules/eng-principles-universal.md` (Rules A1, A2, A4, A5, A6, B2, B3)

## Outputs

Artefact path: `docs/design-docs/<kebab-case-name>/design-doc.md`

The output is a complete design doc following the Rule A2 structure. Every section is present. The Operability section is fully populated. The document is ready for review before implementation begins.

## Workflow

**Step 1 — Trigger check [GATE]**
Verify at least one Rule A1 condition holds. State which one. If none holds, stop — recommend an ADR. If the problem itself is not yet understood, stop — recommend a spike. Do not proceed past this gate without naming the trigger condition.

**Step 2 — Context load**
Load prior design docs and ADRs for related work. Load `eng-principles-universal.md` Rules A1, A2, A4, A5, A6, B2, B3. Load `eng-principles-agentic.md` P1, P3. Name each artefact loaded. This step is the operational form of Agentic P1: context is the asset; loading it is the work.

**Step 3 — Problem section [GATE]**
Draft the Problem section first. No solution language appears until this section is complete. The problem statement names the affected users, describes current behaviour, and states the desired behaviour. Each of those three elements must be present before proceeding. A problem statement that slides into solution language ("users can't do X, so we should build Y") is sent back for rewrite. Proceed only when the problem is stated in problem terms.

**Step 4 — Context and constraints**
Document background, history, and related prior decisions. Link relevant ADRs. State what has been tried before. State any inherited constraints. Then list non-functional requirements with numbers and units (Rule A4): latency at p95, availability SLO, throughput target, cost envelope, error budget, security posture. For each NFR, name its fitness function — the automated check that will verify it continuously (Rule A5). "Fast," "reliable," and "scalable" are not NFRs.

**Step 5 — Alternatives**
List at least two alternatives, including the "do nothing" option. For each: a description, the blast radius if this option turns out to be wrong, and the reversal cost (Rule B3). One approach listed is an incomplete design doc. If you cannot describe what is wrong with the alternatives, you cannot explain why the recommended approach is right.

**Step 6 — Recommended approach**
State the recommendation. Explain why it beats the named alternatives on the named constraints. This section comes after alternatives because the problem shapes the recommendation — not the reverse.

**Step 7 — Consequences**
Name positive and negative consequences. Explicitly state whether a walking skeleton should precede the full build (Rule B2). A walking skeleton is the minimal end-to-end implementation — one request path wired through every real component in the real deployment environment. Pre-skeleton estimates are uncalibrated. If the path to production is already clear and integration risks are fully known, note that explicitly.

**Step 8 — Operability plan [GATE]**
Complete every sub-field: metrics (what to graph), structured logs (what to emit), traces (spans to instrument), alerts (thresholds and on-call routing), rollback plan (ordered steps with a verification gate that confirms each step succeeded), capacity headroom, known failure modes with mitigations, upstream and downstream dependency failure modes. A skeletal or absent Operability section means the doc is not ready for review. This gate does not pass until every sub-field has content. This section is authored with the people who will operate the system — not written in isolation and delivered to them later (Rule A6).

**Step 9 — Open questions**
List every unresolved question. Each question has an owner and a resolution gate — the slice or milestone whose start is blocked until the question is answered. An open questions section without owners or gates is not an open questions section; it is a list of known unknowns being politely ignored. Calendar dates appear only when the resolution depends on an external human commitment (vendor reply, legal review).

**Step 10 — Review hand-off**
Share the completed document for review before any implementation begins. Implementation begins only after the design doc is accepted. Sharing a draft with known incomplete sections is not a hand-off; it is a draft in progress.

## Artefact template

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

<!-- What is wrong or missing? Who is affected, and how? What does current
     behaviour look like vs. desired behaviour? No solution language here. -->

## Context

<!-- Background, history, related prior decisions (link ADRs). What has been
     tried before? What constraints exist that were inherited rather than chosen? -->

## Constraints

<!-- Functional requirements and non-functional requirements. NFRs must have
     numbers: latency at p95, availability SLO, throughput, cost envelope.
     Each NFR names its fitness function — the automated check that will
     verify it continuously. -->

## Alternatives considered

<!-- At least two alternatives, including "do nothing." For each: description,
     blast radius if wrong, reversal cost. Only the chosen approach listed = incomplete. -->

## Recommended approach

<!-- The proposed solution. Why it wins on the named constraints. Comes after
     alternatives because the problem shapes the recommendation. -->

## Consequences

<!-- Positive and negative. State whether a walking skeleton should precede
     the full build and why. If integration risks are fully known, say so explicitly. -->

## Operability plan

<!-- Metrics, structured logs, traces, alerts (thresholds and routing), rollback
     plan (ordered steps + verification gate per step), capacity headroom,
     known failure modes with mitigations, upstream and downstream dependency
     failure modes. Required. Absent = reject. -->

## Open questions

<!-- Unresolved questions. Each has an owner and a resolution gate — the slice
     or milestone whose start is blocked until the question is answered. -->
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "It's too small to need a doc — we'll figure it out in the code." | Check Rule A1. If any trigger fires, the doc comes first. "Figuring it out in the code" is the build trap the trigger conditions were designed to catch. If no trigger fires, write an ADR. |
| "We already know what to build — the doc is just overhead." | The Alternatives and Constraints sections surface what you don't know you don't know. A design doc with only the chosen solution is incomplete by Rule A2. If the outcome is truly obvious, the doc will be short and the overhead will be low. |
| "We can write the doc after we understand the design better." | The design doc is how you understand the design better. Problem-first structure means the document shapes understanding — it is not a record of understanding already achieved. Post-hoc docs rationalise; they don't evaluate. |
| "The Operability section can be filled in closer to launch." | Rule A6 is explicit: the operability plan exists before the build begins, authored with the people who will operate it. "Add it later" means it never gets the scrutiny it needs before the decisions that make it hard are already made. |
| "We don't have enough alternatives to fill that section." | "Do nothing" is always an alternative. If you cannot describe what is wrong with the alternatives, you cannot explain why the recommended approach is right. A design doc that skips alternatives is not a design doc; it is an announcement. |

## Red flags

- Problem section contains solution language ("we will build…", "using X we can…")
- NFRs use adjectives instead of numbers ("fast," "highly available," "scalable")
- Alternatives section lists only the chosen approach
- Operability section is absent, has placeholder text, or is a stub
- No fitness function named for any NFR
- Walking skeleton not addressed in the Consequences section
- Open questions have no owners or no resolution gates
- Effort or scope is expressed in days/weeks/months rather than slices or gates (Agentic P8)
- Document shared for review while known sections are incomplete
- Implementation has started before the doc is accepted

## Verification / exit criteria

The design doc passes review when:

- At least one Rule A1 trigger is named and confirmed
- All Rule A2 sections are present and populated
- Every NFR has a number, a unit, and a named fitness function (Rules A4, A5)
- Alternatives section contains at least two options including "do nothing," each with blast radius and reversal cost (Rule B3)
- Operability plan covers all required sub-fields (Rule A6)
- Walking skeleton recommendation is addressed in the Consequences section (Rule B2)
- Every open question has an owner and a resolution gate
- No implementation work has started before acceptance

## References

- `rules/eng-principles-universal.md` — P2, Rule A1, A2, A4, A5, A6, B2, B3
- `rules/eng-principles-agentic.md` — P1, P3, P5, P8
- Larson, Will — "Staff Engineer" (trigger conditions for design docs)
- Nygard, Michael — "Release It!" (operability; ADR format)
- Cockburn, Alistair — walking skeleton (Rule B2 source)
- Ford, Parsons, Kua — "Building Evolutionary Architectures" (fitness functions; Rule A5 source)
- `references/nfr-categories.md` — NFR taxonomy for Rule A4
