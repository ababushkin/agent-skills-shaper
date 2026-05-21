# KR quality templates — personal-project Layer 1 / Layer 2

Reference cited by `skills/initiative-shape/SKILL.md` Step 6.5 rules 5b and 5d. Use it when drafting key results to (a) pick a Layer 1 dimension and (b) shape the KR to its Layer 2 template.

## Scope — personal projects only

Every initiative in this workspace is a personal project: no production traffic, no real-user funnel, no on-call rotation. The vocabulary below is calibrated for that scale. Frameworks deliberately not imported as defaults:

- **SRE SLO machinery** (availability / latency / error-budget). Assumes user traffic and an on-call team.
- **DORA four keys** (deployment frequency / lead time / change failure rate / MTTR). Assumes a deployment pipeline serving customers.
- **AARRR product funnels** (acquisition / activation / retention / referral / revenue). Assumes a multi-user product.

A single initiative can still cite one of these — but only when the initiative genuinely has that property. They are not the default Layer 1 vocabulary, and a KR drawn from them must justify why the default four don't fit.

## Layer 1 — the four dimensions

| Dimension | What it answers | When it's load-bearing |
| -- | -- | -- |
| **Correctness** | does the thing produce the intended output on the cases I care about | always, for any build |
| **Outcome / behaviour change** | does the thing I built actually change what I do or how I work | most product-shaped initiatives (Types 2, 4, 5, 6 from `references/initiative-types.md`) |
| **Maintenance / future-me cost** | can I come back in 30 days and still navigate this | always — solo means future-me pays the whole tax |
| **Discipline / completion** | did the artefacts get finished, or did this half-ship | always — solo means nobody else will finish it |

The four are deliberately distinct: correctness is about the artefact's output on inputs; outcome is about whether the artefact changes operator behaviour downstream; maintenance is about cost-of-future-edit; discipline is about whether the build actually completed. A KR that conflates two of them (e.g. "the skill works and I've used it 5 times") is a filler signal — pick one dimension per KR.

## Layer 2 — measurement templates

One template per Layer 1 dimension. Every template is verifiable by one person, locally, without instrumentation.

### Correctness — Golden-path test

**When it applies:** any initiative that produces a concrete artefact (skill, script, report, doc, configured tool) with verifiable output for known inputs.

**Required fields:**
- named input(s) — specific fixtures, sample tickers, sample prompts, etc.
- named expected output — what "correct" looks like for each input
- verification method — script run, snapshot diff, eyeball check against a checked-in reference
- judged-by date — when the check is run

**Good example:**
> "Run `/initiative-shape` against the 5 fixture inputs in `fixtures/initiative-drafts/`; all 5 produce the 6-field structure verified by `diff` against checked-in expected outputs in `fixtures/initiative-drafts/expected/`; judged at cycle close."
> - baseline: `0/5` pass (fixtures don't exist yet — first issue creates them)
> - target: `5/5` pass
> - window: cycle close
> - source: `fixtures/initiative-drafts/` + diff output

**Bad example:**
> "The skill works well."
> *(no named inputs, no named outputs, no verification method, no date — not gradable.)*

### Outcome / behaviour change — Self-trial protocol

**When it applies:** any initiative whose success is "this changes what I do or how I work" — methodology skills, productivity changes, decision-support tooling.

**Required fields:**
- the situation (X) where the behaviour change should occur
- the next N occurrences over which it's judged (N is small — typically 3–10 — so the cycle window can contain it)
- the observable behaviour (Y) that confirms or denies the change
- inspection method — what artefact you read to grade it (cached outputs, Linear project descriptions, git logs, run logs)

**Good example:**
> "Next 5 initiatives shaped with `/initiative-shape` after this lands: zero filler KRs in the created Linear projects, judged by re-reading each project description against rule 5a–5e."
> - baseline: filler-KR rate is `~1 in 3` historically (eyeball estimate from past 9 projects)
> - target: `0/5` filler KRs
> - window: next 5 invocations
> - source: Linear projects under `Initiative quality - type-aware OKRs with KRs`

**Bad example:**
> "Initiatives will be better shaped."
> *(no situation, no N, no observable behaviour, no inspection method.)*

### Maintenance / future-me cost — Structural cap + revisit gate

**When it applies:** any initiative producing artefacts that will be edited or re-read after a delay — skills, references, code, docs.

**Required fields:**
- size/shape cap — a stated bound: LOC, line count, section count, file count, function count
- revisit gate — a check at N days that the artefact is still navigable (typical: "I can answer question X from memory" or "I can find section Y without re-reading the whole file")
- judged-by date — when the revisit check is run

**Good example:**
> "`skills/initiative-shape/SKILL.md` stays ≤ 320 lines; in 30 days from cycle close I can locate where rule 5c lives without grepping."
> - baseline: 281 lines today
> - target: ≤ 320 lines, navigation check passes
> - window: 30 days from cycle close
> - source: `wc -l skills/initiative-shape/SKILL.md` + a one-paragraph navigation note added to the cycle retro

**Bad example:**
> "The skill stays maintainable."
> *(no cap, no revisit gate, no date — vibe.)*

### Discipline / completion — Artefact-exists + sections-complete

**When it applies:** any initiative whose risk is half-shipping — the build started but the doc / test / reference / cleanup didn't land.

**Required fields:**
- named artefact (file path)
- named sections within the artefact (e.g. "rule 5 has 5a/5b/5c/5d/5e populated", "rationalisations table has the new row")
- zero placeholders — no `TBD`, no `unknown`, no `we'll figure it out`
- predecessor / supersedes declaration if the artefact replaces an earlier one

**Good example:**
> "ABA-191 closes only after `skills/initiative-shape/SKILL.md` has rule 5 enumerated as 5a/5b/5c/5d/5e each with a 1-line pass condition, rule 6 has the extended placeholder ban list and concrete-artefact requirement, the rationalisations table has the 'padding to 3' row, and `references/kr-quality-templates.md` exists with all four templates."
> - baseline: rule 5 is one row, rule 6 has the short ban list, no kr-quality-templates reference
> - target: all four artefact changes landed
> - window: cycle close
> - source: `skills/initiative-shape/SKILL.md` + `references/kr-quality-templates.md`

**Bad example:**
> "The work will be documented."
> *(no artefact path, no sections named, no completion definition.)*

## Pattern for a 3-KR draft

A clean 3-KR draft typically picks 3 of the 4 dimensions, not 3 of the same one. Some patterns by initiative type:

- **Type 1 methodology skill pack** — outcome (invocation behaviour) + correctness (per-invocation decision quality) + discipline (artefact completion).
- **Type 2 personal product** — correctness (named-fixture output) + outcome (does it change my workflow) + maintenance (future-me cost).
- **Type 3 utility skill pack** — correctness (first-shot artefact quality) + discipline (use-log exists, populated) + maintenance (size cap).
- **Type 4 research / thesis** — discipline (sources file populated, claims indexed) + outcome (next N decisions cite the thesis) + correctness (claims survive critique).
- **Type 5 equity research** — discipline (pre-registration artefact exists, immutable) + correctness (per-call structure) + outcome (calibration trend across cohort).
- **Type 6 production / customer-facing** — this is the type where SRE/DORA/AARRR vocabulary genuinely applies. Cite from there for the relevant KRs, but keep at least one Layer 1 dimension (typically discipline — telemetry exists, definitions locked).

## Out of scope for personal projects — when not to use the defaults

Categorically inappropriate as defaults at personal-project scale:

- **Performance / latency SLOs** — no user traffic to budget against. Re-enter only if the initiative genuinely runs a job whose runtime gates further work.
- **Operability as availability SLO** — no on-call. Re-enter as "the scheduled job didn't silently fail" via the discipline template, not as 99.X%.
- **Adoption / growth / retention funnels** — single user. Re-enter only if the initiative is Type 6 with a real user cohort.

If the initiative genuinely needs one of these, name it explicitly as the reason the default vocabulary doesn't cover it — and write the KR against the actual property, not against a copied SRE/DORA/AARRR template.
