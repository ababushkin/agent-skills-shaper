---
name: prototype-to-validate
description: >
  Build a throwaway artefact that answers one specific product question before committing
  engineering time to a design. Use when anyone wants to test an interaction, flow, or
  concept before building it for real — regardless of whether idea-triage ran first.
  Trigger phrases: "let's prototype this", "build a quick mockup", "can we test this
  flow first", "let's validate the UX before building", "quick demo to see if it
  works", "does this interaction make sense", "let's see what it feels like". Also
  use when a design-doc stalls because the team disagrees about which approach will
  feel right and opinion-based argument isn't resolving it.
pack: engineering
lifecycle_stage: define (discovery)
principles_implemented:
  - source: eng-universal
    id: P4
    bucket: embedded
  - source: eng-universal
    id: Rule B3
    bucket: embedded
  - source: eng-universal
    id: Rule C5
    bucket: adapted
  - source: eng-universal
    id: Rule D5
    bucket: embedded
  - source: eng-agentic
    id: P8
    bucket: embedded
length_target: 180–240
author: Anton Babushkin
predecessor:
  repo: none
  skill: none
  relation: new
kept_from_predecessor: "n/a"
changed_from_predecessor: "n/a"
---

# Prototype to validate

## Purpose

A prototype-to-validate is a throwaway artefact built to answer one specific question before engineering time is committed to a design. The question is always a product question — how the feature will feel, whether users will understand an interaction, whether a proposed flow creates or removes confusion. Technical unknowns belong in a spike (Rule C5). The output is a written finding, not a deliverable artefact.

This skill sits between `idea-triage` and `design-doc`. Idea-triage confirms a problem is real and worth pursuing. That is not enough to know how to solve it. When the gap between "this is worth building" and "this is how we'll build it" is a product question, a prototype answers it cheaply. A design-doc started from an unclear product direction will be redesigned; a prototype started from an unclear product direction will be thrown away. Throwaways are cheaper.

The risk this skill guards against is the prototype that becomes an implementation. A prototype built with production-quality code, extended beyond its original question, and shipped to users has become a real release — without tests, without a design review, without operability planning. Prototypes must be throwaway by policy: the question is the constraint, the code is the instrument, the finding is the output.

## When to use

- An idea has cleared idea-triage and the dominant remaining unknown is product feel — how the interaction works, whether the flow makes sense, what the experience is like for a user.
- A design-doc has stalled because the team disagrees about which approach will feel right and opinion-level argument is not resolving it.
- Before committing to a design-doc for a significant UX-touching change where intuition about user response is low.

## When not to use

- **The dominant unknown is technical** — run a spike instead. Spikes answer: can we do this, at what cost, with what constraints? Prototypes answer: does this feel right, will users understand this?
- **The idea hasn't been triaged** — run `idea-triage` first. A prototype is not a substitute for problem validation; it is a tool for solution exploration after the problem is confirmed.
- **The interaction is known and the task is to design the system** — go directly to `design-doc`. Prototype-to-validate is discovery work; design-doc is commitment work.
- **Multiple questions need answering** — triage the questions first. One prototype answers one question. Run prototypes sequentially, not simultaneously.

## Inputs

- An idea-triage output: validated hypothesis, ICE score, confidence rating.
- A single, specific question the prototype will answer (one sentence, written before building begins).
- A time box (set before the prototype begins; not extended after starting).

## Outputs

A written finding at `docs/prototypes/<slug>/finding.md`. The finding contains: the question, the prototype approach, the observations, and a recommendation: proceed / reshape / kill. The prototype code, if any, is either deleted or explicitly marked non-production in the finding.

## Workflow

**1. Write the question.**
Before building anything, write the question in one sentence. The question must be specific (one thing, not a cluster), answerable by observation, and bounded (there is a signal that means "yes" or "no"). If the question cannot be written in one sentence, it is not well-defined. Resolve it first.

Good questions:
- "Will a user who has not seen this flow understand that step 2 must complete before step 3 unlocks?"
- "Does inline editing feel faster than a modal for this data type, based on a walkthrough with one internal user?"
- "Is the proposed navigation structure legible — does a new user land in the right section?"

Questions too vague to drive a prototype:
- "How should the onboarding flow work?" — a design brief, not a question
- "Will users like this?" — not specific enough to be answerable
- "Is this the right approach?" — too broad; which aspect of the approach?

**2. Set the time box and the kill condition.**
Name both before writing a line. Default appetite: 1–3 build-observe iterations on the single question. Each iteration is a slice (build → put it in front of an observer → record what was seen). Anything beyond ~3 iterations means the question is too broad or the answer is already "reshape" — stop and write the finding (see Agentic P8: appetite is a cap expressed in slices, not in days). The kill condition is the signal that ends the prototype early — the question is answered in the first iteration, or the approach clearly fails in a way that needs no further exploration. Stopping early is not a failure; it is the skill working as intended.

**3. Choose the mode.**

| Mode | Best for | What it is |
|---|---|---|
| Narrative | Concept-level questions about flow and framing | Written scenario + annotated sketches; no code |
| Clickable | Interaction questions about sequencing and affordances | Mockup in a design tool, navigable but static |
| Throwaway code | Questions that require live data or real interaction behaviour | Code that runs, intentionally not production-quality |

Throwaway code is the riskiest mode: most likely to drift into a release, most expensive to build, least often necessary. Use it only when the question cannot be answered by narrative or clickable means — for example, when the answer depends on real API latency, real data shape, or real browser behaviour.

**4. Build and observe.**
Build the minimum that answers the question. Nothing beyond it. When the prototype is in the hands of an observer — a user, a teammate, yourself — record observations, not interpretations. Interpretation goes in the finding.

**5. [GATE] Write the finding.**
A prototype must exit with a finding. If the time box expires and the question is not answered, the finding is: "this prototype approach did not answer the question; the next step is X." That is a valid finding. Exiting without a finding is not valid.

The recommendation must be one of three:
- **Proceed** — the question is answered affirmatively; proceed to `design-doc`.
- **Reshape** — the question is answered but the answer is "not this way"; the idea needs revision before a design is possible.
- **Kill** — the question is answered negatively; the idea does not survive the prototype. This is a celebrated outcome (Rule D5): the prototype saved the cost of a full design and build.

**6. Dispose of the prototype.**
Throwaway code: delete it, or mark it explicitly as non-production (no test coverage, no error handling, not to be deployed) in the finding. Do not commit throwaway code to the main branch without this marking. Do not extend throwaway code toward production quality — that requires a design-doc and a clean implementation.

## Finding template

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

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "The prototype took a day to build — we should ship it instead of throwing it away." | Sunk cost. The prototype answered a question; that was its job. If the finding is proceed, build it properly from a design-doc. If reshape or kill, the day was well spent. |
| "We'll clean up the throwaway code later." | No. Throwaway code goes to production as-is or it gets deleted. "Clean it up later" produces production code with no coverage, no error handling, and no operability. |
| "We don't have time for a prototype — let's just build it." | This is never faster. A prototype is 1–3 throwaway slices; a design-doc is many more; an implementation is many more again. Skipping the prototype bets the full build on an assumption that 1–3 throwaway slices would have resolved. |
| "We already know what users want — we don't need to observe." | This is the highest-confidence claim in product development, and the most commonly wrong one. A narrative prototype takes two hours. If the answer is certain, confirm it cheaply. |
| "The prototype became the product and it works fine." | Prototype code is built to answer a question, not to survive production. "It works fine" means it hasn't failed yet under controlled conditions. It has no test coverage, no security review, and no operability plan. It will fail. |

## Red flags

- No written question exists before the prototype begins.
- Time box was not set before starting, or was extended after starting.
- The prototype became the implementation without a design-doc.
- The finding exists but contains no recommendation.
- Throwaway code was committed to main without explicit non-production marking.
- Multiple questions are being answered by one prototype.
- The recommendation is "proceed" but no design-doc is the stated next step.

## Verification / exit criteria

The skill has run correctly when:

1. A finding exists at `docs/prototypes/<slug>/finding.md`.
2. The finding contains the original question (one sentence), the approach, raw observations, an interpretation, and a recommendation of proceed / reshape / kill.
3. The prototype artefact is either deleted or explicitly marked non-production.
4. If the recommendation is proceed, the next step (`design-doc`) is named in the finding.
5. The time box was set before the prototype began and was not extended.

## References

- `rules/eng-principles-universal.md` — P4 (name assumptions; test the risky ones before committing), Rule B3 (reversibility: prototypes are throwaway by design), Rule C5 (time-box; produce a written decision at expiry; adapted for product discovery), Rule D5 (kill is a celebrated outcome)
- `rules/eng-principles-agentic.md` — P8 (effort in slices, not calendar time)
- `skills/idea-triage/SKILL.md` — upstream: produces the validated hypothesis and confidence rating that may route here
- `skills/design-doc/SKILL.md` — downstream: the target when the recommendation is proceed
- Hunt, Thomas — "The Pragmatic Programmer" (tracer bullets; test risky assumptions before committing)
- Ries, Eric — "The Lean Startup" (build-measure-learn loop; prototype as experiment)
- Cagan, Marty — "Inspired" (product discovery vs. product delivery)
