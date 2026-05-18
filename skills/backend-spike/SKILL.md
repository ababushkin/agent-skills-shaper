---
name: backend-spike
description: >
  Investigate a backend correctness question — detection threshold, substitution strategy,
  algorithmic safeguard — and produce a written recommendation with rejected alternatives
  before committing to an implementation. Use when a backend problem has at least two
  plausible approaches and picking the obvious one without comparison carries silent
  correctness risk. Trigger phrases: "what's the right threshold for", "how should we
  detect", "what's the best way to handle", "what guard should we add", "spike on",
  "investigate the approach for", "is there a better way to handle", "what does the data
  say about". Also use when a design-doc stalls on a correctness sub-question that is not
  yet understood well enough to commit to an approach.
pack: engineering
lifecycle_stage: define (discovery)
principles_implemented:
  - source: eng-universal
    id: P4
    bucket: embedded
  - source: eng-universal
    id: Rule C5
    bucket: adapted
  - source: eng-universal
    id: Rule D5
    bucket: embedded
  - source: eng-agentic
    id: P4
    bucket: embedded
  - source: eng-agentic
    id: P8
    bucket: embedded
length_target: 200–270
author: Anton Babushkin
predecessor:
  repo: none
  skill: none
  relation: new
kept_from_predecessor: "n/a"
changed_from_predecessor: "n/a"
---

# Backend spike

## Purpose

A backend spike is a time-boxed investigation that answers one backend correctness question — what detection threshold is right, which substitution strategy handles the edge cases, what algorithmic safeguard prevents the distortion — before any implementation is committed. The question is always analytical: it has a right answer that depends on data, edge cases, and trade-offs between precision and robustness. Preference, feel, and user response are not the criteria; correctness and reliability are.

This skill sits between a stalled design-doc sub-question and the implementation ticket that follows. When a backend problem has at least two plausible approaches and picking one without comparing them carries silent correctness risk, this skill is the right intervention. The failure mode it guards against is the rejected-alternatives skip: choosing the obvious option, shipping it, and discovering the correctness gap later when the edge case the alternatives table would have caught is now in production data.

The output is a written recommendation with a rejected-alternatives table — not code, not a prototype. The code belongs in the follow-up implementation ticket.

## When to use

- A backend problem has at least two plausible approaches that differ in edge-case behaviour, precision, or robustness.
- A design-doc has stalled because a sub-question about detection logic, substitution rules, or algorithmic safeguards is not yet understood well enough to pick an approach.
- You have identified a correctness failure in existing behaviour and the right fix is not obvious.
- The question involves a threshold, classification rule, or fallback strategy where the "obvious" choice carries hidden assumptions about input shape or volatility.

Size the work: if you can answer the question in one paragraph from memory with no alternatives worth comparing, a spike is unnecessary — write the decision inline and proceed. If the answer requires evaluating ≥2 options against concrete examples, run this skill.

## When not to use

- **The dominant unknown is product feel** — run `prototype-to-validate` instead (becomes `product-spike` when ABA-129 lands). That skill answers: does this interaction feel right, will users understand this? This skill answers: is this approach correct, does it handle the edge cases?
- **The problem is not yet framed** — run `idea-triage` or `design-doc` first. A spike on an undefined problem produces an answer to the wrong question.
- **The answer is well-established and unambiguous** — document the choice in the design-doc or an ADR and proceed. No spike needed.
- **The spike requires building and running code to verify** — that is a proof-of-concept, not a spike. Size accordingly and route to a build task, not this skill.

## Inputs

- A problem statement (one sentence): what correctness failure or open question are we investigating?
- A failure example: one concrete case where the current approach fails or the question is unresolved.
- Existing behaviour: what does the system currently do in this case?
- A time-box: set before the investigation begins, expressed in investigation steps (per Agentic P8 — slices, not calendar time). Default: 3–5 steps.

## Outputs

A written recommendation at `docs/spikes/<slug>/recommendation.md`. The recommendation contains: the question, the alternatives table, the recommended approach with rationale, and the next step — always a named follow-up implementation ticket.

## Workflow

**1. [GATE] Write the question.**
Before investigating, write the question in one sentence. It must be specific (one correctness property, not a cluster), answerable by reasoning over data or examples, and bounded (there is a signal that means "this approach handles it" or "this approach fails here"). If the question cannot be written in one sentence, decompose it and run one spike per sub-question.

Good questions:
- "What TTM window detects FCF base-year distortion reliably without over-triggering on normal volatility?"
- "Which WACC derivation rule produces values within 1% of analyst consensus across the most common input shapes?"
- "What guard prevents trailing-1Y FCF from being silently promoted to a normalised-FCF proxy?"

Questions too vague to drive a backend spike:
- "How should the stock model work?" — a design brief, not a correctness question
- "What's the right architecture?" — not a correctness question; route to design-doc
- "Should we fix this?" — the decision to fix belongs upstream of the spike

**2. Set the time-box.**
Name the time-box before the investigation begins: a count of investigation steps, not a duration. Default is 3–5 steps. Each step is: define the option, apply it to the failure example, evaluate the edge cases. The time-box is a cap. If the question is answered at step 2, stop and write the recommendation. If the box expires with no clear winner, the recommendation is "more data needed; here's what we'd need to resolve it" — that is a valid exit.

**3. Enumerate options (minimum 3).**
Generate at least three plausible approaches, including the obvious one. Fewer than three is the rejected-alternatives-skip rationalisation in action; reject it. For each option:
- Name it (a short label)
- Describe what it does in one sentence
- Apply it to the failure example
- Name one failure mode: a realistic input where this option produces a wrong result

If fewer than three genuine alternatives exist, name the closest approximations and document why they collapse to the same approach — but do not skip the enumeration step.

**4. [GATE] Scope check.**
Before committing to an option, check: does the same correctness problem appear in adjacent code paths? If the detection threshold for path A also affects paths B and C, and the spike only covers A, the recommendation is incomplete. Name the adjacent paths and declare them in-scope or explicitly out-of-scope. If out-of-scope, name the follow-up spike.

**5. Confidence and semantics impact.**
For the leading option:
- Confidence: how certain is this the right answer? (Gilad scale — cite evidence, not assertion)
- Semantics delta: does this option change the meaning of an output the user or downstream system already relies on? Name the delta explicitly.
- Failure ceiling: what is the worst-case impact if this option is wrong in a way not caught by the alternatives table?

**6. [GATE] Write the recommendation.**
One option, with a rejected-alternatives table. For each rejected option: why it was rejected as a specific failure mode, not a generic judgement ("seems worse" is not accepted — name the input where it fails). If two options are genuinely indistinguishable on current evidence, state that explicitly and name what additional evidence would resolve it.

**7. Spawn follow-up implementation ticket.**
A spike produces a recommendation, not code. Before closing, name the follow-up implementation ticket: what it will build, what the recommended approach is, and the acceptance criterion (the failure example should pass). The spike is not done until the follow-up ticket exists.

## Recommendation template

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

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "The obvious option is clearly right — alternatives are a waste of time." | This is what every engineer thinks before the edge case surfaces in production. The table takes minutes; the edge-case debugging takes days. Enumerate anyway. |
| "I'll ship the obvious approach and tune it later." | The first version sets the baseline, users build expectations around it, and later tuning is now a breaking change. The spike costs one investigation step. |
| "I know from experience which approach is right." | Experience is a prior, not evidence. Assign a Confidence score. If it's 8+, the spike is short. If the score drops while writing the alternatives table, the spike was necessary. |
| "The scope check is unnecessary — this is clearly isolated." | Correctness problems in detection and substitution logic almost always affect adjacent paths. The check is two minutes. If the scope is truly isolated, naming it takes ten words. |
| "A recommendation doc isn't needed — I'll put the decision in the PR description." | PR descriptions are read once. Recommendation docs are referenced when the same class of problem reappears. The artefact is the institutional memory. |
| "Fewer than three alternatives exist." | Enumerate the closest approximations and document why they collapse. The discipline of trying to find three options is half the value — it surfaces the assumption that made the "obvious" choice obvious. |

## Red flags

- No written question exists before the investigation begins.
- Fewer than three options are enumerated, with no explanation of why fewer exist.
- The rejected-alternatives table contains generic rejections ("option B is worse") without a specific failure mode.
- The recommendation is "proceed with the obvious approach" and the alternatives table was skipped.
- Scope check was not run; adjacent paths are unnamed.
- The follow-up implementation ticket does not exist at spike close.
- Confidence score is absent or stated as opinion without cited evidence.

## Verification / exit criteria

The skill has run correctly when:

1. A recommendation exists at `docs/spikes/<slug>/recommendation.md`.
2. The recommendation contains the question (one sentence), at least three options in the table, and a specific failure mode per rejected alternative.
3. The scope check is documented — adjacent paths named or explicitly ruled out of scope.
4. The recommended approach includes a Confidence score with cited evidence (Gilad scale).
5. A follow-up implementation ticket is named with an acceptance criterion referencing the failure example.
6. The time-box was set before the investigation began and was not extended.

## References

- `rules/eng-principles-universal.md` — P4 (name assumptions; test the risky ones before committing), Rule C5 (time-boxed spike → written decision at expiry), Rule D5 (kill is a celebrated outcome — applies to rejected options)
- `rules/eng-principles-agentic.md` — P4 (evidence beats vibes; "seems right" is never sufficient), P8 (effort in slices and gates, not calendar time)
- `references/confidence-meter.md` — Gilad scale used in Step 5
- `skills/prototype-to-validate/SKILL.md` — parallel skill for product/UX discovery (referenced as `product-spike` once ABA-129 lands)
- `skills/design-doc/SKILL.md` — downstream: proceeds after spike recommendation is in place
- `skills/plan-review/SKILL.md` — run on the follow-up implementation ticket before committing to the build
