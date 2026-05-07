# Authoring learnings

Calibration guidance and failure modes for authors and editors. Surfaced during v0.1 scoping; encoded here so the authoring cycle reflects them. Authors and editors load this directly.

## 1. New artefacts enter only with personal-usage evidence or principle-derived justification

Anything that fails both bars goes to the idea bank to await trial. This rule, written down up-front, would have saved four rounds of scope churn during v0.1 planning.

## 2. Confidence scoring drifts toward generous unless calibrated against personal usage

First triage entries scored 6-8 on principle-only evidence; later entries correctly scored those same skills at 1.5-2. **Editors flag confidence claims that don't cite specific personal-usage evidence.** See `references/confidence-meter.md` for the calibration warning.

## 3. Recency and specificity of evidence matter, not just data type

"I've been using this lately" is materially higher confidence than "I've used this at some point." The Confidence Meter as written treats both as anecdote (~0.5). The reference file distinguishes.

## 4. Jargon-as-rigor is the v0.1 voice failure mode

Phrases like "structured placement act" or "accepted candidates accumulate" sound rigorous but obscure simple ideas. **Editor reject trigger:** any prose where a simpler phrasing exists and the formal one is doing rhetorical work rather than conceptual work.

Examples to recognise:
- "Structured placement act" → "putting things on the roadmap"
- "Accepted candidates accumulate" → "approved items pile up"
- "Discharge the assumption" → "test the assumption"
- "Operationalise" → "use" or "do"
- "Leverage X to do Y" → "use X to do Y"

## 5. The pack scopes correctly, not comprehensively

v0.1 is Define/Plan/Build heavy and right-side-of-lifecycle light because that's where the owner's current practice is. The shape is honest. Comprehensiveness comes from v0.2 trial surfacing real needs, not from front-loading skills the owner has never run.

## 6. Most principles are embedded, not standalone

The reflexive move to "one skill per principle" inflates the pack. The right move is many-to-many: a principle appears as red-flag bullets, rationalisation rebuttals, or gates inside skills the agent is already running. A principle earns a standalone artefact only when it has:

- a workflow (skill)
- a mechanically-verifiable failure mode (hook)
- a structural reason the agent won't catch its own failure (sub-agent)

Reviewers check this during PR review: a proposed standalone artefact must satisfy all three.

## See also

- `references/confidence-meter.md` for calibration scale
- `docs/skill-anatomy.md`, `docs/hook-anatomy.md`, `docs/sub-agent-anatomy.md` for artefact shapes
