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
- grader — one-sentence describable command that runs the inputs and diffs against expected output (exit code + diff summary)
- judged-by date — when the check is run

**Good example:**
> "Run `/initiative-shape` against the 5 fixture inputs in `fixtures/initiative-drafts/`; all 5 produce the 6-field structure verified by `diff` against checked-in expected outputs in `fixtures/initiative-drafts/expected/`; judged at cycle close."
> - baseline: `0/5` pass (fixtures don't exist yet — first issue creates them)
> - target: `5/5` pass
> - measured over: cycle close
> - how we'll know: `bin/grade-initiative-shape fixtures/initiative-drafts/` runs each fixture, diffs against `fixtures/initiative-drafts/expected/<name>.md`, exits 0 only if all pass; exit code + diff output cached at `fixtures/initiative-drafts/_runs/<cycle-id>.log`

**Bad example:**
> "The skill works well."
> *(no named inputs, no named outputs, no verification method, no date — not gradable.)*

### Outcome / behaviour change — Self-trial protocol

**When it applies:** any initiative whose success is "this changes what I do or how I work" — methodology skills, productivity changes, decision-support tooling.

**Required fields:**
- the situation (X) where the behaviour change should occur
- the next N occurrences over which it's judged (N is small — typically 3–10 — so the cycle window can contain it)
- the observable behaviour (Y) that confirms or denies the change
- grader — one-sentence describable command that scans the artefacts produced across N occurrences and emits a numeric grade or pass/fail

**Good example:**
> "Next 5 initiatives shaped with `/initiative-shape` after this lands: zero filler KRs in the created Linear projects, graded by `bin/grade-kr-quality` against rules 5a–5f."
> - baseline: filler-KR rate is `~1 in 3` historically (eyeball estimate from past 9 projects)
> - target: `0/5` filler KRs
> - measured over: next 5 invocations
> - how we'll know: `bin/grade-kr-quality $(linear-project-list --since=cycle-start)` reads each project description and emits a per-project pass/fail across 5a–5f; the KR passes if total filler-KR count is 0; output cached at `~/.initiative-shape/grades/cycle-<id>.log`

**Bad example:**
> "Initiatives will be better shaped."
> *(no situation, no N, no observable behaviour, no inspection method.)*

### Maintenance / future-me cost — Structural cap + revisit gate

**When it applies:** any initiative producing artefacts that will be edited or re-read after a delay — skills, references, code, docs.

**Required fields:**
- size/shape cap — a stated bound: LOC, line count, section count, file count, function count
- revisit gate — a check at N days that the artefact is still navigable (typical: "I can answer question X from memory" or "I can find section Y without re-reading the whole file")
- grader — one-sentence describable structural-cap check using shell primitives (`wc -l`, `grep -c`, file count); the navigation gate is the manual half and is captured in a retro note
- judged-by date — when the revisit check is run

**Good example:**
> "`skills/initiative-shape/SKILL.md` stays ≤ 320 lines; in 30 days from cycle close I can locate where rule 5c lives without grepping."
> - baseline: 281 lines today
> - target: ≤ 320 lines, navigation check passes
> - measured over: 30 days from cycle close
> - how we'll know: `wc -l skills/initiative-shape/SKILL.md` returns ≤ 320 (cap check, automated); the 30-day navigation check is the manual half — captured in a one-paragraph retro note in `retros/<cycle-id>.md`

**Bad example:**
> "The skill stays maintainable."
> *(no cap, no revisit gate, no date — vibe.)*

### Discipline / completion — Artefact-exists + sections-complete

**When it applies:** any initiative whose risk is half-shipping — the build started but the doc / test / reference / cleanup didn't land.

**Required fields:**
- named artefact (file path)
- named sections within the artefact (e.g. "rule 5 has 5a/5b/5c/5d/5e populated", "rationalisations table has the new row")
- grader — one-sentence describable existence + section-count + no-placeholder check (chained shell primitives: `test -f`, `grep -c '^### '`, `! grep -E 'TBD|unknown'`)
- zero placeholders — no `TBD`, no `unknown`, no `we'll figure it out`
- predecessor / supersedes declaration if the artefact replaces an earlier one

**Good example:**
> "ABA-191 closes only after `skills/initiative-shape/SKILL.md` has rule 5 enumerated as 5a/5b/5c/5d/5e each with a 1-line pass condition, rule 6 has the extended placeholder ban list and concrete-artefact requirement, the rationalisations table has the 'padding to 3' row, and `references/kr-quality-templates.md` exists with all four templates."
> - baseline: rule 5 is one row, rule 6 has the short ban list, no kr-quality-templates reference
> - target: all four artefact changes landed
> - measured over: cycle close
> - how we'll know: `test -f references/kr-quality-templates.md && [ $(grep -cE '^\| 5[a-f] \|' skills/initiative-shape/SKILL.md) -ge 5 ] && ! grep -nE 'TBD|currently unknown|the logs|the system' skills/initiative-shape/SKILL.md references/kr-quality-templates.md` — exit code + matched-line output

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

## Roles within an initiative

Layer 1 says what a KR *measures* (correctness / outcome / maintenance / discipline). The **role** says what a KR *does for the bet* — and the two are orthogonal. Every KR carries exactly one role:

| Role | What it is | Target shape |
| -- | -- | -- |
| **bet** | what the initiative is actually pushing forward this cycle | a delta or a new state ("p95 drops to ≤ X", "first-shot correctness ≥ 8/10") |
| **brake** | catches regression in something that already works today | "don't drop below baseline" / "stay at 0" — paired with a bet to make the trade-off visible |
| **foundation** | makes the bet and brakes measurable — instrumentation, telemetry, tracking, schema work | "the record exists at `<path>` for every run" — without it the lagging KRs are ungradable by construction |

The role tag is orthogonal to the `(commit)` / `(stretch)` tag. A brake can be either: a strict brake ("stay at 0 silent failures") is usually `(commit)`; a soft brake ("stay within 5% of baseline") may be `(stretch)`. The two tags answer different questions — `(commit|stretch)` sets the grading bar at cycle close (Wodtke); the role says which way the KR points in the initiative's theory of change.

**Most initiatives have at most 1–2 bets.** A draft where every KR is a `bet` usually means the brakes were silently omitted — the initiative is pushing on three fronts at once with nothing named as load-bearing-to-protect. When you see an all-bet draft, ask: what already works that this push could break? That's a brake. What has to exist before the bet is even measurable? That's the foundation. (This is the soft check behind Step 6.5 rule 11 in `skills/initiative-shape/SKILL.md`.) The roles are not a quota — some honest shapes are 2 bets + 1 foundation, or 1 bet + 2 brakes; the rubric does not force one of each.

The bet/brake split generalises Type 6's quality-pair pattern (`references/initiative-types.md`) to all six types: a bet paired with a brake is the same move as a value KR paired with a quality KR — name the thing you're pushing and the thing you must not break in the process. Per-type role defaults are suggestions, not mandates; each type's playbook in `references/initiative-types.md` annotates its default KR mix with the usual bet / brake / foundation split.

## The grader-backed KR pattern

Every KR in this workspace is **grader-backed** by default: its `how we'll know:` field points at a command (script, query, one-liner) that reads the write-side artefacts and emits a verdict. Manual cycle-close inspection is the carve-out, not the default. This is the load-bearing sub-check at rule 5f in `skills/initiative-shape/SKILL.md` Step 6.5 — sharper than 5b / 5c / 5d combined, because a KR that cannot name a one-sentence grader is filler regardless of how well it satisfies the other sub-rules.

### Two-part shape

The pattern has two halves, both scoped *into* the initiative as user stories on its issue list:

| Part | What it is |
| -- | -- |
| **Write-side artefact** | Every relevant event / run / state-change emits a structured record at a known location with a known schema |
| **Read-side grader** | A command reads the write-side records and emits a verdict — numeric grade, OK / WATCH / KILL, or pass / fail |

### Worked example — drain-cycle

The drain-cycle initiative shaped both halves explicitly. Two user stories from its issue list:

> *As the operator, I want each drain run to write a structured log (issue order, spawn timestamps, exit codes, final Linear state) to* `~/.drain-cycle/runs/<cycle-id>.json` *— so KR1 (completion %) is gradable from the file alone, and KR2's time_spent block has a known home to be appended to at cycle close.*

> *As the operator, I want to run a command that reads the run logs across recent cycles and prints a grade — per-cycle completion %, trend across the last N cycles, recurrent failure-mode tuples, and a verdict against the kill condition (OK / WATCH / KILL) — so I can decide whether to ship-as-is, iterate, or walk away, without re-reading JSON by hand.*

The first story is the write-side schema; the second is the read-side grader. Together they make the lagging KRs gradable in one command at cycle close.

### The one-sentence-grader test

If you cannot describe the grader command in one sentence at draft time, the KR is filler. This is the sharpest filler-KR filter the rubric has:

- "We will document this initiative" — no grader. Fail.
- "Skill exists and has all anatomy sections" — grader is `grep -c '^## ' skills/<name>/SKILL.md` returns ≥ 11. Pass.
- "Decision quality improves" — no grader. Fail.
- "0/5 filler KRs in next 5 shaped initiatives, graded by `bin/grade-kr-quality`" — grader names the command. Pass.

A draft KR that survives 5a–5e but cannot name a one-sentence grader still fails 5f.

### Grader shapes by Layer 1 dimension

| Layer 1 | Grader shape | Typical primitives |
| -- | -- | -- |
| **Correctness** | runs the named inputs, diffs against expected output → exit code + diff summary | `diff`, snapshot tests, `pytest`, exit code |
| **Outcome** | scans resulting artefacts, counts observable behaviour → numeric grade | `linear-project-list`, file globs, `grep`, simple counters |
| **Maintenance** | checks structural caps → pass/fail (navigation gate stays manual) | `wc -l`, `grep -c`, `find … \| wc -l` |
| **Discipline** | asserts artefact existence + section count + no-TBD → pass/fail | `test -f`, `grep -c '^## '`, `! grep -E 'TBD\|unknown'` |

See the Layer 2 templates above for one full example per dimension.

### Manual-grading carve-out

A KR may be manually graded only when one of these holds:

- The initiative is genuinely one-shot or throwaway (and the project type field reflects that — e.g. a Type 4 thesis essay whose review is irreducibly a reader's verdict).
- The verdict is irreducibly qualitative ("the prose reads naturally", "the diagram is legible") and no honest automatable proxy exists.

The carve-out must be stated alongside the KR — drafts that lean on it without explicit justification fail rule 5f. "It's too much work to write a grader for this personal project" is not a valid justification: the grader shapes above are all one-line shell commands.

### Building the grader is part of the initiative

The write-side schema and read-side grader are scoped *into* the initiative as one or two user stories — they are not bolted on after. Before the initiative enters Active, its issue list must include:

- a write-side story: "every <event> logs <fields> to <location> with <schema>"
- a read-side story: "command <name> reads <location> and emits <verdict>"

If those stories are absent at cycle planning, the grader-backed KR is aspirational decoration and the KR is ungradable by construction. The grader is the work, not the overhead — without it, the lagging KRs collapse into a vibe check at cycle close.

## Out of scope for personal projects — when not to use the defaults

Categorically inappropriate as defaults at personal-project scale:

- **Performance / latency SLOs** — no user traffic to budget against. Re-enter only if the initiative genuinely runs a job whose runtime gates further work.
- **Operability as availability SLO** — no on-call. Re-enter as "the scheduled job didn't silently fail" via the discipline template, not as 99.X%.
- **Adoption / growth / retention funnels** — single user. Re-enter only if the initiative is Type 6 with a real user cohort.

If the initiative genuinely needs one of these, name it explicitly as the reason the default vocabulary doesn't cover it — and write the KR against the actual property, not against a copied SRE/DORA/AARRR template.
