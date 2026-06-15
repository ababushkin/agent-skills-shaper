---
name: design
description: >
  Single entry point for working through a technical or product unknown before
  committing to a build. Routes to one of three tracks — design document,
  backend spike, or product spike — based on the dominant unknown. Use whenever
  the question is "how should we build X", "what's the right approach for Y",
  "investigate this correctness question", or "validate this interaction before
  designing it". Trigger phrases: "how do we build", "design this", "spike on",
  "what's the right threshold for", "let's prototype this", "investigate the
  approach for", "what's the architecture for", "validate the UX before
  building".
---

# Shape: design

## Purpose

This skill is the entry point for any pre-implementation shaping work. It routes to three tracks:

- **Design document** — structure a significant engineering decision into a reviewable doc before any code begins.
- **Backend spike** — answer one backend correctness question (threshold, substitution strategy, algorithmic safeguard) with a written recommendation and a rejected-alternatives table.
- **Product spike** — answer one product question (does this interaction feel right? will users understand this flow?) with a throwaway artefact and a written finding.

The tracks share a discipline: produce a written artefact before implementation begins. The track selection depends on the dominant unknown.

## When to use

Use this skill when one of these conditions holds:

| Dominant unknown | Track |
|---|---|
| Architecture, system design, one-way-door decision, or work spanning ≥5 independently verifiable slices | Design document |
| Backend correctness: threshold, detection logic, substitution rule, algorithmic safeguard — ≥2 plausible approaches, picking one without comparing carries silent risk | Backend spike |
| Product feel: interaction sequencing, user comprehension, flow legibility — opinion-based argument has not resolved the question | Product spike |

If the problem itself is not yet framed, run `shape:idea-triage` first. A design or spike on an undefined problem produces an answer to the wrong question.

## Do not use when

- No trigger fires — write a short ADR instead.
- The change is purely additive, clearly reversible, and has no shared-interface surface — proceed directly to implementation.
- The answer is well-established and unambiguous — document it in the design-doc or ADR and proceed.
- A spike requires building and running code to verify — that is a proof-of-concept; route to a build task.

## Inputs

- A problem description or question, however rough.
- The dominant unknown (correctness, architecture, or product feel).
- Named stakeholders and known constraints (for design-doc track).
- A failure example and time-box (for backend-spike track).
- A single specific question and time-box (for product-spike track).

## Outputs

One of:
- `docs/design-docs/<name>/design-doc.md` — complete design doc, accepted before implementation.
- `docs/spikes/<slug>/recommendation.md` — spike recommendation with rejected-alternatives table.
- `docs/prototypes/<slug>/finding.md` — prototype finding with proceed / reshape / kill recommendation.

Artefact templates: `references/design-spike-templates.md`.

## Workflow

### 1. Gate: route selection

Name the dominant unknown and the track it selects. If the dominant unknown is ambiguous, default to **design document** — a short, fast doc costs less than a build that starts on a misunderstood problem. Do not proceed without naming the track.

---

### Track A — Design document

#### A2. Context load

Load prior design docs and ADRs for related work; name each artefact loaded. State what has been tried and which constraints are inherited.

#### A3. Gate: problem section

Draft the Problem section first — no solution language until it is complete. It must name the affected users, current behaviour, and desired behaviour. A statement that slides into solution language ("users can't do X, so we should build Y") is sent back for rewrite. Proceed only when the problem is stated in problem terms.

#### A4. Context and constraints

Document background, history, and related prior decisions; link relevant ADRs. List non-functional requirements with numbers and units: latency at p95, availability SLO, throughput target, cost envelope. For each NFR, name its fitness function — the automated check that verifies it continuously. "Fast", "reliable", and "scalable" are not NFRs.

#### A5. Alternatives

List at least two alternatives, including "do nothing". For each: description, blast radius if wrong, reversal cost. One approach listed is an incomplete doc.

#### A6. Recommended approach

State the recommendation and why it beats the named alternatives on the named constraints. This comes after alternatives — the problem shapes the recommendation, not the reverse.

#### A7. Consequences

Name positive and negative consequences. State explicitly whether a walking skeleton should precede the full build. Pre-skeleton estimates are uncalibrated. If the path to production is already clear and integration risks are fully known, say so.

#### A8. Gate: operability plan

Complete every sub-field: metrics, structured logs, traces, alerts (thresholds and on-call routing), rollback plan (ordered steps with a verification gate per step), capacity headroom, known failure modes with mitigations, upstream/downstream dependency failure modes. A skeletal or absent Operability section means the doc is not ready for review. Author it with the people who will operate the system.

#### A9. Open questions

List every unresolved question. Each carries an owner and a resolution gate — the slice or milestone blocked until it is answered. Questions without owners or gates are known unknowns being politely ignored.

#### A10. Review hand-off

Run a writing-editor pass (`agents/writing-editor/AGENT.md`) over the completed document. On `reject`, repair and re-run once, then carry remaining notes forward as `accept with notes`. Share the document for review before any implementation begins. Sharing a draft with known incomplete sections is not a hand-off.

---

### Track B — Backend spike

#### B1. Gate: write the question

Before investigating, write the question in one sentence. It must be specific (one correctness property), answerable by reasoning over data or examples, and bounded (there is a signal that means "this approach handles it" or "this approach fails here"). If the question cannot be written in one sentence, decompose and run one spike per sub-question.

Good questions: "What TTM window detects FCF base-year distortion reliably without over-triggering on normal volatility?" Bad: "How should the stock model work?" — a design brief, not a correctness question.

#### B2. Set the time-box

Name the time-box before the investigation begins: a count of investigation steps, not a duration. Default 3–5 steps. If the box expires with no clear winner, the recommendation is "more data needed; here's what we'd need to resolve it" — that is a valid exit.

#### B3. Enumerate options (minimum 3)

Generate at least three plausible approaches, including the obvious one. For each: name it, describe what it does in one sentence, apply it to the failure example, name one failure mode. Fewer than three is the rejected-alternatives-skip rationalisation — reject it.

#### B4. Gate: scope check

Before committing to an option, check whether the same correctness problem appears in adjacent code paths. Name the adjacent paths and declare them in-scope or explicitly out-of-scope. If out-of-scope, name the follow-up spike.

#### B5. Confidence and semantics impact

For the leading option: Confidence (Gilad scale — cite evidence, not assertion); Semantics delta (does this change the meaning of an output users or downstream systems already rely on?); Failure ceiling (worst-case impact if wrong).

#### B6. Gate: write the recommendation

One option, with a rejected-alternatives table. For each rejected option: why it was rejected as a specific failure mode — "seems worse" is not accepted. If two options are genuinely indistinguishable on current evidence, state that explicitly and name what additional evidence would resolve it.

Use the recommendation template in `references/design-spike-templates.md`.

#### B7. Spawn follow-up implementation ticket

Name the follow-up ticket: what it will build, what the recommended approach is, and the acceptance criterion. The spike is not done until the follow-up ticket exists.

---

### Track C — Product spike

#### C1. Write the question

Before building anything, write the question in one sentence. It must be specific, answerable by observation, and bounded. If it cannot be written in one sentence, resolve it first.

Good questions: "Will a user who has not seen this flow understand that step 2 must complete before step 3 unlocks?" Bad: "How should the onboarding flow work?" — a design brief, not a question.

#### C2. Set the time-box and kill condition

Name both before writing a line. Default: 1–3 build-observe iterations. Each iteration is a slice (build → put it in front of an observer → record what was seen). The kill condition is the signal that ends the prototype early — the question is answered, or the approach clearly fails. Stopping early is not a failure.

#### C3. Choose the mode

| Mode | Best for |
|---|---|
| Narrative | Concept-level questions — written scenario + annotated sketches; no code |
| Clickable | Interaction questions — mockup in a design tool, navigable but static |
| Throwaway code | Questions requiring live data or real interaction behaviour |

Use throwaway code only when the question cannot be answered by narrative or clickable means.

#### C4. Build and observe

Build the minimum that answers the question. Nothing beyond it. Record observations — not interpretations. Interpretation goes in the finding.

#### C5. Gate: write the finding

A prototype must exit with a finding. If the time box expires and the question is not answered, the finding is: "this prototype approach did not answer the question; the next step is X." That is a valid finding.

The recommendation must be exactly one of:
- **Proceed** — answered affirmatively; proceed to design document.
- **Reshape** — answered but "not this way"; the idea needs revision before a design is possible.
- **Kill** — answered negatively; the idea does not survive the prototype.

Use the finding template in `references/design-spike-templates.md`.

#### C6. Dispose of the prototype

Throwaway code: delete it, or mark it explicitly as non-production in the finding. Do not commit throwaway code to the main branch without this marking. Do not extend throwaway code toward production quality — that requires a design-doc and a clean implementation.

---

## Red flags

- Route selection skipped; track not named before proceeding.
- Problem section (Track A) contains solution language.
- NFRs use adjectives instead of numbers ("fast", "highly available").
- Alternatives section lists only the chosen approach.
- Operability section (Track A) is absent, placeholder, or a stub.
- No fitness function named for any NFR.
- Walking skeleton not addressed in Consequences (Track A).
- Open questions have no owners or resolution gates.
- No written question before investigation begins (Tracks B, C).
- Fewer than three options enumerated in Track B, with no explanation.
- Rejected-alternatives table contains generic rejections ("option B is worse") without a specific failure mode.
- Scope check not run; adjacent paths unnamed (Track B).
- Follow-up implementation ticket does not exist at spike close (Track B).
- No finding exists when prototype ends (Track C).
- Throwaway code committed to main without non-production marking (Track C).
- Implementation started before the artefact is accepted.

## Exit criteria

**Track A** — The design doc passes review when: (1) at least one trigger is named; (2) all sections present and populated; (3) every NFR has a number, a unit, and a named fitness function; (4) Alternatives contains ≥2 options including "do nothing", each with blast radius and reversal cost; (5) Operability plan covers all required sub-fields; (6) walking-skeleton recommendation addressed in Consequences; (7) every open question has an owner and a resolution gate; (8) writing-editor pass returned `accept` or `accept with notes`; (9) no implementation started before acceptance.

**Track B** — The spike has run correctly when: (1) a recommendation exists at `docs/spikes/<slug>/recommendation.md`; (2) it contains the question (one sentence), ≥3 options with specific failure modes per rejected alternative; (3) scope check is documented; (4) recommended approach includes a Confidence score with cited evidence; (5) follow-up ticket is named with an acceptance criterion referencing the failure example; (6) time-box was set before the investigation and not extended.

**Track C** — The skill has run correctly when: (1) a finding exists at `docs/prototypes/<slug>/finding.md`; (2) it contains the original question, approach, raw observations, interpretation, and a proceed / reshape / kill recommendation; (3) prototype artefact is deleted or explicitly marked non-production; (4) if proceed, `shape:design` (Track A) is named as the next step; (5) time-box was set before the prototype began and not extended.

## Related

- `shape:idea-triage` — upstream: produces the validated hypothesis that may route here.
- `shape:delivery` — downstream: a design-doc-worthy deliverable emits a `design-doc` node that delegates here.
- `shape:plan-review` — run on the follow-up implementation ticket before committing to the build.
- `references/design-spike-templates.md` — artefact templates for all three tracks.
- `references/nfr-categories.md` — NFR taxonomy for Track A constraints.
- `references/confidence-meter.md` — Gilad scale used in Track B Step 5.
- `rules/eng-principles-universal.md` — P4 (name assumptions; test the risky ones before committing), Rule C5 (time-boxed spike → written decision at expiry), Rule D5 (kill is a celebrated outcome).
- `rules/eng-principles-agentic.md` — P4 (evidence beats vibes), P8 (effort in slices, not calendar time).
- `agents/writing-editor/AGENT.md` — writing-editor persona dispatched at Track A Step 10.
