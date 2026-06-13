---
name: initiative-types
description: >
  Six-type taxonomy for classifying a Linear initiative by what success means for it.
  Used by /shape:project to set the Objective shape and the rubric the KRs are judged
  against. Per-type playbooks (default KR mix, anti-patterns, verification rubric) are
  filled in below the corresponding type entry as the skill matures.
type: reference
cited_by:
  - skills/project/SKILL.md
---

# Initiative types (6)

The `/shape:project` skill probes the project type before shaping KRs. The type determines what "success" means for the initiative: a methodology skill pack and a personal product can both pass cycle close, but they pass on different KRs, because their theories of success are different. Naming the type up front lets the skill load the right Objective shape and verification rubric — and lets a downstream agent reading the Linear project description apply the right rubric without re-deriving the taxonomy.

The six types below are the ones actually observed across this portfolio (`agent-skills-shaper`, `nestl`, `agent-skills`, paused `em-os`, `stock-review`) plus one anticipated type (production / customer-facing). If a new initiative doesn't fit any of the six, the taxonomy needs updating — flag rather than force-fit.

Each type's default KR mix is annotated with a **Role split** — which KR is the **bet** (the push), which are **brakes** (don't-regress guardrails), and which is **foundation** (instrumentation that makes the bet measurable). The role tags appended to each KR bullet (e.g. `· bet`, `· brake`, `· foundation`) sit alongside the leading/lagging and committed/aspirational descriptors. Roles are defined in `references/kr-quality-templates.md` "Roles within an initiative"; the splits below are defaults, not mandates.

**Worked-example convention.** Each example below uses the PM-readable KR shape `/shape:project` emits — `(commit)` / `(stretch)` tags with `baseline` / `target` / `measured over` / `how we'll know` sub-fields. The examples model KR *content* and the per-type dimension mix; the rubric trace (the `*Layer 1 · Layer 2*` audit-footer under each KR and the `*Dimensions: …*` summary line) is added per the template in `skills/project/SKILL.md` and is left off here to keep the focus on phrasing.

## Type 1 — Methodology skill pack

*Examples: `agent-skills-shaper`, `agent-skills`.* Markdown-encoded decision rules invoked by humans or agents at decision moments. The consumer is the author plus any agent that loads the pack. The theory of success is that the skill fires at the right decision moment, and when it fires, decision quality improves. Authoring more skills is output, not outcome — invocation accuracy at the right moment, and the downstream quality of decisions made under the skill's guidance, are what count. Leading-indicator KRs measure invocation rate; lagging-indicator KRs measure decision quality when invoked.

**Objective shape.** "For [agent or human invoker], make [decision moment] happen correctly without prompting." The Objective sentence names the *decision moment*, not the artefact. Authoring is implementation; what the OKR scores is whether the decision moment is now handled.

**Default KR mix (3 KRs).** One leading + one lagging + one anti-output guard. Pair as two committed + one aspirational, or one committed + two aspirational, depending on which dimensions are inspectable today.

**Role split (default).** The decision-quality KR is the **bet** (does the skill improve outcomes when it fires); the anti-output guard is a **brake** (the discipline must not regress at the bottleneck); the invocation-rate KR is **foundation** (without firing data the decision-quality KR can't be sampled). If invocation is already reliable, the invocation-rate KR reads as a brake instead — split foundation/brake to taste. These are defaults, not mandates.

- **Invocation-rate KR (leading · foundation)** — does the skill fire at the right moment? Form: "[skill] fires (or is offered) in ≥X% of [decision-moment] across the next N cycles." Data sources: transcript history (`rtk discover`), Linear project list, sampled session logs. This is the leading indicator that the trigger description is well-targeted.
- **Decision-quality KR (lagging · bet)** — when it fires, does the outcome improve? Form: "in ≥X of last N sampled invocations, [skill] surfaced an issue or produced an artefact that would otherwise not have appeared." This is the lagging indicator that the skill body itself is well-authored.
- **Anti-output guard KR (committed · brake)** — the discipline holds at the bottleneck. Form: "zero [historically-common output failure] across [window]" (e.g., zero repo-aliased Linear projects, zero KRs without sub-fields). Catches drift between intent and practice.

Adoption KRs ("skill installed in N repos") are output unless cross-repo adoption is itself the named goal — usually leave them out.

**Worked example — `/shape:project` itself.**

```
Goal:           For Anton (and any agent invoking Shaper), make
                initiatives properly shaped before they enter a cycle —
                so cycle planning works against goals and KRs rather than
                repo-aliased backlogs.

KR1 (commit) — shape:project fires (or is offered) in ≥80% of
               new-initiative moments across the next 4 cycles
  baseline:        unknown — first cycle of measurement
  target:          ≥80% offered at new-initiative moments
  measured over:   next 4 cycles
  how we'll know:  transcript history (rtk discover), sampled

KR2 (commit) — in ≥4 of last 5 created initiatives, all six fields
               pass the verification rubric
  baseline:        0/5 pass full rubric today
  target:          4/5 pass full rubric
  measured over:   next 4 cycles
  how we'll know:  Linear project descriptions, manual audit

KR3 (stretch) — zero Linear projects created in the next 4 cycles
                that are repo-aliased rather than outcome-named
  baseline:        majority of historical projects repo-aliased
  target:          0 repo-aliased in window
  measured over:   next 4 cycles
  how we'll know:  Linear project list

Kill condition: if KR2 isn't hit within 2 cycles of the skill update,
                the template is wrong rather than the operator
Project type:   1 — Methodology skill pack
```

**Anti-patterns specific to Type 1.**

- **"Author N new skills"** — output. Volume of skills is not what success means for a methodology pack. Success is the existing skills firing at the right moment with the right effect.
- **"Improve skill quality"** — unmeasurable; fails Wodtke's weekly-trackable test. Reshape into invocation-rate or decision-quality KRs with sample, target, and window.
- **"Update SKILL.md for X"** — task, not KR. Belongs on the issue body, not in the OKR.
- **"Skill installed in N repos"** — output disguised as outcome unless cross-repo spread is genuinely the named goal.

**Verification rubric (Type 1).** A Type 1 KR is gradable if a fresh agent in the next session can name: (a) the data source for the sample (transcript history, Linear projects, session logs); (b) the sampling method (last-N, all-of-cycle, random); (c) the baseline — recorded, not "TBD"; (d) the target — numeric or binary, not "improved"; (e) a 0.0–1.0 grade at cycle close. If any of (a)–(e) is missing, the KR isn't gradable and cycle close degrades to a vibe check.

## Type 2 — Personal product (single-user, running)

*Example: `nestl` (Rails app).* Complete deployed software solving a recurring problem for one user. The consumer is the author as a single user. The theory of success is that the recurring job gets done reliably without manual intervention. Growth metrics, MAU, and adoption breadth are inapplicable — the dimensions that matter are correctness (zero false negatives or missed events), no-silent-failure (every failure surfaces in a visible alert within a bounded time), availability (scheduled jobs complete to SLO), and maintenance burden (zero manual restarts/redeploys over the observation window).

**Objective shape.** "For [single user — name them], make [recurring job] happen reliably without manual intervention." The Objective names the *recurring job* being automated, not the technology stack or the feature set. Shipping more features is implementation; what the OKR scores is whether the recurring job now runs without nagging you.

**Default KR mix (3 KRs).** One correctness (lagging) + one no-silent-failure (committed) + one maintenance-burden (committed). Where scheduled-job completion is the system's central guarantee, an availability KR may substitute for maintenance-burden, or sit alongside it as a 4th. Pair as one aspirational (correctness — the outcome) + two committed (operability — the brake). Adoption, retention, and growth KRs are categorically inapplicable to Type 2 — there is one user.

**Role split (default).** Correctness is the **bet** (does the system get the right answer); maintenance-burden is the **brake** (don't regress into manual intervention); no-silent-failure is **foundation** (without surfaced failures you can't even tell whether the correctness bet held). An availability KR, when present, is a brake. These are defaults, not mandates.

- **Correctness KR (lagging · bet)** — does the system get the right answer when it runs? Form: "≤X false negatives / missed events / wrong outputs across [N] runs in window" or "[result] matches [reference source] in ≥X% of [N] sampled runs." Data sources: production logs, sampled outputs against ground truth, the system's own audit trail. This is the lagging indicator that the implementation is sound.
- **No-silent-failure KR (committed · foundation)** — when a failure happens, do you find out? Form: "every error surfaces in [alert channel] within [bounded time] of failure" or "zero silent failures across [N] runs in window — every job either completes or fires an alert." Data sources: alert history, log diff between job runs and alert firings. This is the committed foundation — the observability that makes the correctness bet gradable, and a brake against silent failure: a Type 2 system that fails silently is worse than one that doesn't run at all, because you're now trusting an output that isn't there.
- **Maintenance-burden KR (committed · brake)** — does the human have to intervene to keep it running? Form: "zero manual restarts / redeploys / production-data hotfixes over [N-day window]" or "≤X manual interventions per [window]." Data sources: deploy history, ssh/console session log, on-call notes. This is the committed brake against the slow-leak failure mode where the product technically runs but consumes the operator's attention.
- **Availability KR (optional, committed when central · brake)** — do the scheduled jobs complete? Form: "scheduled job [name] completes within [time budget] in ≥X% of runs across [window]." Data sources: job scheduler logs, completion timestamps. Use when scheduled-job completion is the central guarantee; otherwise rolled into maintenance-burden.

Feature-shipping KRs ("add [feature]", "build [integration]") are output. Growth KRs (DAU, MAU, retention, signups) are categorically inapplicable — there is one user.

**Worked example — `nestl`-shaped personal Rails app, scheduled-job product.**

```
Goal:           For Anton (single user), make the daily [recurring job]
                run reliably without manual intervention — so the output
                arrives on time without nagging the operator.

KR1 (stretch) — ≤1 missed event / false negative per 30-day window
                across the daily run
  baseline:        unknown — first cycle of measurement
  target:          ≤1 missed event per 30 days
  measured over:   next 4 cycles (3 × 30-day observation windows)
  how we'll know:  production logs + sampled audit against source-of-truth

KR2 (commit) — every job failure surfaces in [alert channel] within
               5 minutes; zero silent failures in window
  baseline:        unknown — first cycle of measurement
  target:          0 silent failures across 90 days
  measured over:   next 4 cycles
  how we'll know:  alert history vs job scheduler log diff

KR3 (commit) — zero manual restarts, redeploys, or production-data
               hotfixes across the 90-day window
  baseline:        estimate ~1 manual intervention/week today; first
                   cycle instruments the counter
  target:          0 manual interventions across 90 days
  measured over:   next 4 cycles
  how we'll know:  deploy history + ssh/console session log

Kill condition: if KR2 (no-silent-failure) cannot be hit within 2
                cycles, the alerting fabric is wrong rather than the
                product — pause and address operability first
Project type:   2 — Personal product
```

**Anti-patterns specific to Type 2.**

- **"Add user registration / signup flow"** — wrong product model. Type 2 is single-user by definition; there are no users to register. If signup is genuinely needed, the initiative is Type 6 (production / customer-facing) and the type was misclassified.
- **"Increase MAU / DAU / retention / signups"** — categorically inapplicable. There is one user. Growth metrics belong to Type 6.
- **"Build feature X" / "Add integration with Y"** — output. Shipping a feature is implementation; what the OKR scores is whether the recurring job now runs reliably without manual intervention.
- **"Improve performance" / "Make it faster"** — unmeasurable as written. Reshape into a specific availability KR ("p95 job completion ≤ X minutes") or drop — speed is rarely the bottleneck on a personal product.
- **"Reduce errors"** — ambiguous. Either correctness (wrong outputs) or no-silent-failure (errors not surfacing) — name which.

**Verification rubric (Type 2).** A Type 2 KR is gradable if a fresh agent in the next session can name: (a) the data source — production logs, alert history, deploy log, audit trail — recorded as a file path, query, or log location; (b) the observation window length in days or cycles; (c) the baseline — recorded, not "TBD"; (d) the target as a numeric count or a binary state, not "improved"; (e) a 0.0–1.0 grade at cycle close. If any of (a)–(e) is missing, the KR isn't gradable and cycle close degrades to a vibe check. Additionally: at least one KR scores correctness (lagging) AND at least one KR scores operability (no-silent-failure, maintenance-burden, or availability). A Type 2 OKR with three correctness KRs and no operability brake is a feature-set, not a personal-product OKR.

## Type 3 — Utility skill pack

*Examples: `resell-au`, `garage-sale`, `codex-primary-runtime`.* Flat collection of callable skills, each solving a discrete recurring task. The consumer is the author at per-invocation use. The theory of success is first-shot correctness of the generated artefact — the next invocation produces something the user posts, prints, or hands off without editing. Authoring more skills is output; what counts is whether the next invocation needs ≤ one edit and whether the pack covers the categories the user actually encounters end-to-end. Time-to-result KRs are usually vanity here unless speed is the named bottleneck.

**Objective shape.** "For [single user — name them], when doing [recurring task], make the skill produce a correct, immediately-usable artefact." The Objective names the *artefact handoff* — the listing gets posted, the label gets printed, the deck gets presented — not the skill itself and not the volume of invocations. Authoring more skills, or running the existing skills more often, is implementation; what the OKR scores is whether the next invocation produces something the user uses without rewriting it.

**Default KR mix (3 KRs).** One first-shot correctness (aspirational, lagging) + one coverage (committed) + one use-log discipline (committed). Pair as one aspirational (the outcome — does it work first-shot) + two committed (the brakes — does it cover the cases the user actually hits, and is there an immutable record so the lagging KR is gradable). A domain-specific quality KR (pricing accuracy, print acceptance, sale outcome) is an optional 4th when the pack has a quantifiable downstream signal.

**Role split (default).** First-shot correctness is the **bet** (does the artefact get used without edits); coverage is a **brake** (don't leave categories unhandled in pursuit of the bet); use-log discipline is **foundation** (without a per-invocation record the first-shot KR is ungradable by construction). When speed is the named bottleneck — as in a faster-end-to-end listings initiative — speed becomes the **bet** and first-shot correctness drops to a **brake** ("don't regress quality while getting faster"). The role tag captures which way that's gone. These are defaults, not mandates.

- **First-shot correctness KR (aspirational, lagging · bet)** — does the generated artefact get used without edits? Form: "in next N invocations of [skill] across mixed [categories / inputs / use cases], ≥X are posted / printed / handed off without text edits beyond [acceptable carve-out — e.g. photo selection only]." Data sources: the use-log (see below) with a per-invocation edit-or-not field; the artefact itself (a diff between generated and final-posted version is the strongest evidence). This is the lagging indicator that the skill body produces immediately-usable output, not just plausible output.
- **Coverage KR (committed · brake)** — does the pack handle the categories / inputs the user actually encounters? Form: "zero invocations across [window] where the skill failed to handle the category end-to-end and the user fell back to writing the artefact manually." Data sources: the use-log with a fell-back-to-manual flag; the user's "I gave up and did it myself" sessions are the failure mode this KR catches. A pack with high first-shot correctness on the easy categories but zero coverage of the hard ones is a Type 3 failure that looks like success in aggregate metrics.
- **Use-log discipline KR (committed · foundation)** — is there an immutable per-invocation record the lagging KR can be graded against? Form: "every invocation in the window is logged to [named use-log location — e.g. `listings/`, `outputs/`, `runs/`] with input, generated artefact, final posted/printed artefact, and edit-or-not outcome; zero invocations without a use-log entry across [window]." Data sources: the use-log directory's git history (or modification timestamps if the use-log is local-only). This is the committed brake that makes the first-shot correctness KR gradable — without a per-invocation record captured at the moment of use, "≥8 of last 10 needed no edits" collapses into a vibe check on remembered sessions. Parallel to Type 5's pre-registration KR: capture discipline at call time, not narration after the fact.
- **Domain-specific quality KR (optional 4th, aspirational · bet)** — does the artefact produce the downstream outcome the user actually cares about? Form: "for ≥X of next N invocations, [downstream signal] is within [tolerance] of [reference]" — e.g. "≥9 of next 10 prices within ±10% of actual sale price"; "≥X of next N labels printed without re-running the layout"; "≥X of next N decks presented without further edits in the meeting." Use when the pack has a quantifiable downstream signal; otherwise the 3-KR default is sufficient.

Throughput KRs ("run `/resell-au` N times this cycle", "process N items") are categorically the wrong shape for Type 3 — volume is output, and Type 3 grades on the quality of each artefact, not the count of them. Volume KRs disguised as "usage drives" or "cycle activity" are the same anti-pattern, just renamed.

**Worked example — `agent-skills` (`resell-au` + `garage-sale`), Facebook Marketplace pack.**

```
Goal:           For Anton selling things on Facebook Marketplace, make the
                skill pack produce a ready-to-post listing he posts without
                editing — across the categories he actually sells.

KR1 (stretch) — in the next 10 listings from /resell-au or /garage-sale
                across mixed categories, ≥8 are posted as-is, with no text
                edits (choosing which photos to use is fine)
  baseline:        unknown — start by tracking the next 5 listings
  target:          ≥8/10 posted as-is
  measured over:   next 10 listings (rolling)
  how we'll know:  listings/<item>/listing.md + listings/use-log.md,
                   with an edited / not-edited flag per listing

KR2 (commit) — zero listings where the skill can't handle the category
               end-to-end and Anton has to write the listing by hand
  baseline:        unknown — needs first-window measurement
  target:          0 manual fallbacks across the window
  measured over:   next 10 listings
  how we'll know:  listings/use-log.md with a fell-back-to-manual flag

KR3 (commit) — every listing is tracked: each run records the input
               photos, the generated listing, the final posted listing,
               and whether it was edited; zero listings with no record
  baseline:        no tracking today; ~0/10 listings recorded
  target:          10/10 listings tracked
  measured over:   next 10 listings
  how we'll know:  listings/use-log.md + listings/<item>/ directories

Kill condition: if KR2 fails twice in a row (two consecutive manual
                fallbacks), the category-detection logic is wrong rather
                than the operator — pause and address coverage before
                producing further listings
Project type:   3 — Utility skill pack
```

**Anti-patterns specific to Type 3.**

- **"Add more skills to the pack this cycle"** — output, not outcome. Type 3 grades on first-shot correctness and coverage of the cases the user actually hits, not on skill count. Five more skills with no use-log produce no graded improvement; reshape into first-shot correctness or coverage KRs over the categories the user actually encounters.
- **"Run `/resell-au` N times this cycle"** — activity vanity. Twenty invocations with bad outputs is failure, not progress. Volume is output; the OKR scores whether each artefact was used without edits. "Usage drive" framings are this anti-pattern with a friendly name.
- **"Improve skill descriptions / trigger phrases"** — wrong type. Trigger-description quality is a Type 1 invocation-rate concern (does the skill fire at the right moment?). Type 3 assumes the skill has already fired and grades what came out.
- **"Generate prettier listings / nicer-looking labels / cleaner-formatted output"** — aesthetic, unmeasurable as written. Reshape into a domain-specific quality KR with a concrete downstream signal (posted-without-edits, sold-within-7-days, printed-without-re-running) or drop.
- **"Skip the use-log — I'll remember which invocations went well"** — same failure mode as Type 5's post-hoc rationalisation. Memory is not a use-log. Without immutable per-invocation capture, the lagging first-shot correctness KR collapses into selective recall of the wins.

**Verification rubric (Type 3).** A Type 3 KR is gradable if a fresh agent in the next session can: (a) point at the use-log location — recorded as a file path or directory, not "somewhere in the repo"; (b) read each invocation's record — input, generated artefact, final-posted/-printed artefact, edit-or-not outcome — without narration from the original operator; (c) read the baseline at first-window start and the target — both numeric (counts, ratios) or binary, not "better"; (d) confirm the observation window has closed before grading begins; (e) compute a 0.0–1.0 grade by counting use-log entries against the target. Additionally: at least one KR must be a first-shot correctness KR (lagging) AND at least one KR must be a use-log discipline KR (committed) naming the log location. A Type 3 OKR without use-log discipline is ungradable by construction — the lagging KRs become arguments about which invocations the operator remembers favourably rather than checks of what each artefact actually was.

## Type 4 — Research / thesis-driven

*Example: `em-os` (paused).* Work whose primary output is knowledge — a defended thesis, a resolved open question, or a published position. The consumer is the intended audience (engineering leaders, in `em-os`'s case). The theory of success is that the thesis is source-backed and survives expert critique. Authoring essays or building demos is implementation; what the OKR scores is whether the assertions are defensible. Adoption KRs (readers, buyer interest) are later-stage — readership of an undefended thesis is noise, not signal.

**Objective shape.** "For [audience], make [thesis / open question] defensible — internally consistent, source-backed, and survivable under expert critique." The Objective names the *defensibility outcome*, not essay count or audience size.

**Default KR mix (3 KRs).** One knowledge-claim (committed) + one critique-survivability (aspirational, lagging) + one source-discipline (committed). Adoption KRs are a later-stage 4th — defer until critique-survivability has held.

**Role split (default).** Knowledge-claim and critique-survivability are the **bet** (defensible assertions that survive expert review — the push); source-discipline is **foundation** (uncited claims are ungradable for defensibility) and doubles as a **brake** (don't let unsourced assertions creep back in) — name it once, not twice. A later-stage adoption KR, when it arrives, is a bet. These are defaults, not mandates.

- **Knowledge-claim KR (committed · bet)** — assertions the thesis defends at window close. Form: "by [date], [thesis] defends [N] claims of the form 'we can assert X with [confidence band] backed by [evidence type]', recorded in [artefact path]." Catches the failure mode where the thesis grows in length but not in defensible claims.
- **Critique-survivability KR (aspirational, lagging · bet)** — does the thesis survive expert review? Form: "in ≥X of N expert reviews, the thesis survives without a load-bearing claim being overturned." Reviews logged with reviewer, date, claims challenged, and claims that held. Lagging indicator that the thesis is right, not just well-written.
- **Source-discipline KR (committed · foundation)** — every load-bearing claim cites primary evidence. Form: "zero load-bearing claims in [thesis artefact] without an inline citation across [window]; sources file shows ≥N entries." Brake against confident, persuasive, unsourced assertions that collapse under critique.

**Worked example — `em-os` thesis arc, defensibility cycle.**

```
Goal:           For VPEs/CTOs/Eng Directors at growth-stage companies,
                make the EM OS thesis defensible — source-backed and
                survivable under expert critique.

KR1 (commit) — by end of cycle, thesis defends 8 claims of the form
               "we can assert X with [confidence] backed by [evidence
               type]", recorded in drafts/em-os-thesis.md
  baseline:        ~4 specific claims; rest is framing
  target:          8 claims with confidence band + evidence type
  measured over:   end of next active cycle
  how we'll know:  drafts/em-os-thesis.md + drafts/em-os-sources.md

KR2 (stretch) — in ≥3 of 4 expert reviews, the thesis survives
                without a load-bearing claim being overturned
  baseline:        0 external reviews completed
  target:          3/4 survive
  measured over:   next 4 active cycles
  how we'll know:  drafts/em-os-reviews.md

KR3 (commit) — zero load-bearing claims in drafts/em-os-thesis.md
               without an inline citation; sources file ≥20 entries
  baseline:        ~50% of load-bearing claims uncited; ~6 sources logged
  target:          0 uncited claims; ≥20 sources
  measured over:   end of next active cycle
  how we'll know:  drafts/em-os-thesis.md + drafts/em-os-sources.md

Kill condition: if KR2 fails — two consecutive expert reviews overturn
                a load-bearing claim — pause demo/marketing and re-shape
Project type:   4 — Research / thesis-driven
```

**Anti-patterns specific to Type 4.**

- **"Publish N essays this cycle"** — output. Volume is not defensibility. A thesis with 20 unsourced essays is weaker than one with 3 claims each holding under scrutiny. Reshape into knowledge-claim KRs that name the assertions.
- **"Get to N readers / N newsletter subscribers"** — adoption masquerading as outcome on an undefended thesis. Defer until critique-survivability has held; the wrong audience signal entrenches a wrong thesis.
- **"Build the demo / build the homepage"** — output. Demos and sites are valuable artefact-clarity *after* survivability has held; before it, they amplify the error. Pair every demo/site KR with the defensibility KR it depends on.
- **"The thesis improved this cycle"** — unmeasurable. Reshape into claim-count, source-count, or review-survivability.

**Verification rubric (Type 4).** A Type 4 KR is gradable if a fresh agent in the next session can: (a) open the thesis artefact at the file path in the KR's source field; (b) count claims, sources, or surviving reviews against the target; (c) confirm the baseline was recorded at first-cycle start, not narrated post-hoc; (d) verify the observation window has closed; (e) compute a 0.0–1.0 grade from the artefact alone. At least one KR must score claim-defensibility (committed) AND at least one must score source-discipline (committed). A Type 4 OKR scoring only essay count or reader count is measuring artefact volume or noise, not defensibility.

## Type 5 — Equity research tooling

*Examples: `stock-screen`, `stock-signal`, `stock-model`, `stock-timing`, `stock-portfolio`.* Tools that produce structured forecasts and decisions about specific tickers, with a durable artefact (cached `reports/TICKER_YYYYMMDD.json`) per call. The consumer is the author plus any downstream reader of cached reports. The theory of success is forecast calibration improving over time — the Tetlock standard — not throughput of analyses. Per Tetlock, calibration over a portfolio of dated, pre-registered calls matters more than accuracy on any single name; the Brier-score view forces forecasts to be dated, immutable, and graded against outcomes. Pre-registration is what makes the discipline honest — it removes the option to rationalise a wrong call after the fact, and it is the single feature that separates equity research from horoscope. Every KR points at the structured outputs the equity skills already produce.

**Objective shape.** "For [analyst plus downstream reader of cached reports], make [BUY/WATCH/AVOID calls] calibrated and pre-registered, with hit-rate and calibration graded post-hoc." The Objective names the *calibration discipline*, not the per-call analysis throughput. Running more screens, signals, or models is implementation; what the OKR scores is whether the calls made under this initiative grade well 12 months out — and whether the calling discipline was honest enough to be gradable at all.

**Default KR mix (3 KRs).** One pre-registration (committed) + one calibration (aspirational, lagging) + one hit-rate (aspirational, lagging). Pre-registration is non-negotiable for Type 5 — without it, the lagging KRs are ungradable, because there is no immutable record of what was actually claimed before outcomes were visible. A decision-quality KR (per-call postmortem) is an optional 4th when the cycle window already covers prior 12-month outcomes.

**Role split (default).** Calibration and hit-rate are the **bet** (do the dated calls grade well 12 months out — the push); pre-registration is **foundation** (without an immutable dated record the lagging KRs are ungradable). Type 5 carries no default **brake** — the Tetlock standard is one-or-two bets plus the pre-registration foundation, so a 2-bets + 1-foundation shape is correct here, not a missing brake. These are defaults, not mandates.

- **Pre-registration KR (committed · foundation)** — every BUY/WATCH/AVOID call written to a dated, immutable artefact before 12-month outcomes are visible. Form: "every BUY/WATCH/AVOID call from [skill] this window is logged to `reports/TICKER_YYYYMMDD.json` with timestamp; zero retroactive edits detected via git history across [window]." Data sources: the `reports/` directory git history (the immutability check) and the cached report files themselves. This is the committed foundation — the immutable record that makes the lagging KRs gradable, and the guard against post-hoc rationalisation: a Type 5 initiative without it is producing horoscopes, not forecasts.
- **Calibration KR (aspirational, lagging · bet)** — does the model's stated range bracket reality? Form: "for ≥X of N tickers whose 12-month window has closed, the bear–bull range from `/stock-model` bracketed the actual price at window close." Data sources: cached `reports/TICKER_YYYYMMDD.json` for the original call + current price at window close. This is the lagging indicator that the model's uncertainty bands are honest — wider isn't better, narrower isn't better, calibrated is what counts.
- **Hit-rate KR (aspirational, lagging · bet)** — directional calls graded against the market. Form: "of BUY calls made ≥12 months ago, ≥X% are above entry by ≥Y%; of AVOID calls, ≥Z% are flat or down vs entry." Data sources: original call timestamps + current/window-close prices, both derivable from the cached reports. This is the lagging indicator that the calling discipline produces positive expected value, not just well-reasoned losses.
- **Decision-quality KR (optional 4th, aspirational · bet)** — per-call postmortem. Form: "for ≥X tickers whose 12-month window has closed, a written postmortem exists in `reports/postmortems/` comparing model output, action taken, and observed outcome." Use when the cycle window already covers closed 12-month windows from prior calls; otherwise the 3-KR default is sufficient.

Throughput KRs ("run `/stock-screen` on N tickers", "produce N reports") are categorically the wrong shape for Type 5 — more analyses is output, and Type 5 grades on calibration of the analyses you already made.

**Worked example — equity skill pack cycle, calibrated-calls initiative.**

```
Goal:           For Anton (and any downstream reader of cached reports),
                make BUY/WATCH/AVOID calls from /stock-signal calibrated
                and pre-registered — so 12-month outcomes can be graded
                against immutable claims rather than rationalised after.

KR1 (commit) — every BUY/WATCH/AVOID call this cycle is logged to a
               dated, immutable file before the next earnings release
               for each ticker; zero retroactive edits detected via
               git history across the window
  baseline:        pre-registration discipline not enforced; 0/7 calls dated
  target:          7 calls timestamped + immutable across the window
  measured over:   this cycle + 90-day no-edit period
  how we'll know:  reports/TICKER_YYYYMMDD.json + git history (immutability)

KR2 (stretch) — for ≥5 of 7 tickers whose 12-month window has
                closed, the bear–bull range from /stock-model
                bracketed the actual price at window close
  baseline:        unknown — first cohort with full 12-month windows
  target:          5/7 calibration hits
  measured over:   next 4 cycles (catches the first cohort's window closes)
  how we'll know:  reports/TICKER_YYYYMMDD.json + current price feed

KR3 (stretch) — of BUY calls made ≥12 months ago, ≥60% are above
                entry by ≥10%; of AVOID calls, ≥60% are flat or down
                vs entry
  baseline:        zero graded calls — first cohort
  target:          ≥60% BUY hit-rate, ≥60% AVOID hit-rate
  measured over:   next 4 cycles
  how we'll know:  reports/TICKER_YYYYMMDD.json + current price feed

Kill condition: if KR1 fails — any retroactive edit detected via git
                history — the pre-registration discipline is broken
                and the lagging KRs are ungradable. Stop and rebuild
                the immutability fabric before producing further calls
Project type:   5 — Equity research tooling
```

**Anti-patterns specific to Type 5.**

- **"Run `/stock-screen` on N new tickers this cycle"** — throughput vanity. Type 5 grades on calibration, not coverage. Twenty new screens with no pre-registration produce twenty unrecorded opinions, not twenty results. Reshape into a pre-registration KR over the names you actually call.
- **"BUY calls outperform the S&P over the next year"** — un-pre-registered and cherry-pickable. Without a dated, immutable set of names locked at call time, "outperform" becomes whatever cherry-picked window the analyst chooses post-hoc. Reshape into a hit-rate KR over the explicit pre-registered cohort.
- **"Update `/stock-model` with new financial data"** — KTLO masquerading as outcome. Refreshing inputs is maintenance; the question is whether the calls the model produces grade well, not whether its inputs are current. Belongs on issues, not on KRs.
- **"Improve model accuracy"** — unmeasurable without a calibration target and a closed window. Reshape into the calibration KR (range brackets actual price) or the hit-rate KR (directional calls graded).
- **"Generate N reports across the watchlist"** — same vanity as the screen-count rationalisation. Reports are the artefact, not the outcome — a small portfolio of well-calibrated reports beats a library of unread ones.

**Verification rubric (Type 5).** A Type 5 KR is gradable if a fresh agent 12 months from now can: (a) point at the cached report files (`reports/TICKER_YYYYMMDD.json`) that constitute the pre-registered claim — file paths recorded, not "in the repo somewhere"; (b) confirm the file's git history shows no retroactive edits inside the call window; (c) read the baseline at call time and the target — both numeric or binary, not "improved"; (d) verify the observation window has closed before grading begins; (e) compute a 0.0–1.0 grade by comparing the immutable claim against the current state. This is the Tetlock standard: a KR a third party can grade from artefacts alone, without narration from the original analyst. Additionally: at least one KR must be a pre-registration KR (committed). A Type 5 OKR without pre-registration is ungradable by construction — the lagging KRs collapse into arguments about what was meant rather than checks of what was claimed.

## Type 6 — Production / customer-facing

*Anticipated; no example yet in this portfolio.* Live software with paying users or external business stakeholders. The consumer is the paying user (or the business). The theory of success is standard product-OKR territory: activation, retention, or conversion — each paired with a quality KR (NPS, p95 latency, error rate, support volume per user) to prevent vanity gains. Every KR has a baseline number from production telemetry, a target, and a window, with the telemetry in place before the cycle starts (no telemetry = no Type 6 KR). The canonical failure mode is "ship feature X to 100% of users" framing — output, not outcome (Cagan); the antidote is to name the customer behaviour the feature is supposed to change.

**Objective shape.** "For [paying user segment], make [behaviour / job-to-be-done] happen reliably — observably better than today on [value metric] without regressing [quality metric]." The Objective names the *user behaviour*, not the feature; the paired quality clause is non-negotiable.

**Default KR mix (3 KRs).** One activation/retention/conversion (aspirational, lagging) + one quality-pair (committed — the brake on vanity gains) + one telemetry-discipline (committed). Growth without a paired quality counterweight is the canonical failure mode; the paired structure (every value KR has a quality KR) is what prevents it.

**Role split (default).** The activation/retention/conversion KR is the **bet** (the customer-behaviour change you're betting on); the quality-pair KR is the **brake** (the counterweight that makes a vanity gain visible); telemetry-discipline is **foundation** (no locked cohort + metric definitions → neither the bet nor the brake is gradable). This is the canonical bet/brake/foundation shape that Types 1–5 generalise. These are defaults, not mandates.

- **Activation / retention / conversion KR (aspirational, lagging · bet)** — the user behaviour change you're betting on. Form: "[N-day retention | activation rate | conversion rate] moves from [baseline]% to [target]% across [window], measured on [cohort]." Telemetry baseline required pre-cycle — if it can't be read today, the first issue in the initiative is to instrument it.
- **Quality-pair KR (committed · brake)** — the brake. Form: "[NPS / p95 latency / error rate / refund rate / support volume per user] does not regress beyond [tolerance] across [window]." Counterweight to the value KR. A retention lift paid for by latency or support volume is a vanity gain; the pair makes that trade visible.
- **Telemetry-discipline KR (committed · foundation)** — cohort + metric definitions locked before cycle start. Form: "cohort definition, metric definitions, and baselines for KR1 and KR2 are recorded in [artefact / dashboard] before cycle start; zero retroactive metric redefinitions across the window." Catches the failure mode where the team ships, the number moves, and the definition is "clarified" post-hoc to make the number look better.

**Worked example.** None in this portfolio yet — this section will get a concrete cycle example once a Type 6 initiative enters cycle planning. For now, the canonical shape is: KR1 a value KR (activation/retention/conversion baseline → target on a named cohort) + KR2 a paired quality KR (NPS, p95 latency, error rate, or support-per-user does not regress beyond a tolerance) + KR3 a telemetry-discipline KR (cohort + metric definitions recorded in a dashboard / definitions file before cycle start, with no retroactive edits across the window).

**Anti-patterns specific to Type 6.**

- **"Ship feature X to 100% of users"** — Cagan's canonical output-disguised-as-outcome. Rollout is implementation; the OKR scores whether the customer behaviour the feature was supposed to change actually moved. Reshape into a behaviour-change KR with a quality pair.
- **"MAU / DAU growth without a retention pair"** — value KR without a quality counterweight. MAU can be inflated by re-engagement emails that crater NPS, or by registration prompts that bloat the denominator. Every growth KR is paired with retention, NPS, churn, or support-per-user — a solo growth KR is half a KR.
- **"Improve conversion"** — unmeasurable as written, missing cohort, baseline, and quality pair. Reshape: "[cohort] conversion from [baseline]% to [target]% across [window] without regressing [quality metric]."
- **"Instrument the funnel"** — task, not KR. Telemetry is a precondition (telemetry-discipline KR enforces it) — if the funnel isn't instrumented, the first issue is to instrument it, not a KR.
- **"Customer-requested feature shipped"** — output. The customer asked because they had an underlying job-to-be-done; the OKR scores whether the job is done better, not whether the artefact landed.

**Verification rubric (Type 6).** A Type 6 KR is gradable if a fresh agent in the next session can: (a) open the dashboard / telemetry source at the path or query in the KR's source field; (b) read the baseline locked at cycle start and the target; (c) confirm cohort + metric definitions were recorded before cycle start (per the telemetry-discipline KR) and that git/dashboard history shows no retroactive edits; (d) verify the observation window has closed; (e) compute a 0.0–1.0 grade from telemetry alone. At least one KR must score user behaviour (activation/retention/conversion, aspirational lagging) AND at least one must score quality as a paired brake (committed). A Type 6 OKR with a growth KR but no quality pair, or with feature-rollout language as a KR, is mis-shaped.

## Sources

- Internal research: Linear document "Research and implementation plan — OKR shapes by project type" (Section 1.1, project `Initiative quality — type-aware OKRs with KRs`)
- `skills/shape:project/SKILL.md` — the six-field initiative format the type field is added to (defined inline in the skill); tracker capture is owned by the Workflow pack when installed
- `skills/shape:project/SKILL.md` — invokes the type probe at Step 2.5
