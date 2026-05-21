---
name: initiative-types
description: >
  Six-type taxonomy for classifying a Linear initiative by what success means for it.
  Used by /initiative-shape to set the Objective shape and the rubric the KRs are judged
  against. Per-type playbooks (default KR mix, anti-patterns, verification rubric) are
  filled in below the corresponding type entry as the skill matures.
type: reference
cited_by:
  - skills/initiative-shape/SKILL.md
---

# Initiative types (6)

The `/initiative-shape` skill probes the project type before shaping KRs. The type determines what "success" means for the initiative: a methodology skill pack and a personal product can both pass cycle close, but they pass on different KRs, because their theories of success are different. Naming the type up front lets the skill load the right Objective shape and verification rubric — and lets a downstream agent reading the Linear project description apply the right rubric without re-deriving the taxonomy.

The six types below are the ones actually observed across this portfolio (`pde-skills`, `nestl`, `agent-skills`, paused `em-os`, `stock-review`) plus one anticipated type (production / customer-facing). If a new initiative doesn't fit any of the six, the taxonomy needs updating — flag rather than force-fit.

## Type 1 — Methodology skill pack

*Examples: `pde-skills`, `agent-skills`.* Markdown-encoded decision rules invoked by humans or agents at decision moments. The consumer is the author plus any agent that loads the pack. The theory of success is that the skill fires at the right decision moment, and when it fires, decision quality improves. Authoring more skills is output, not outcome — invocation accuracy at the right moment, and the downstream quality of decisions made under the skill's guidance, are what count. Leading-indicator KRs measure invocation rate; lagging-indicator KRs measure decision quality when invoked.

**Objective shape.** "For [agent or human invoker], make [decision moment] happen correctly without prompting." The Objective sentence names the *decision moment*, not the artefact. Authoring is implementation; what the OKR scores is whether the decision moment is now handled.

**Default KR mix (3 KRs).** One leading + one lagging + one anti-output guard. Pair as two committed + one aspirational, or one committed + two aspirational, depending on which dimensions are inspectable today.

- **Invocation-rate KR (leading)** — does the skill fire at the right moment? Form: "[skill] fires (or is offered) in ≥X% of [decision-moment] across the next N cycles." Data sources: transcript history (`rtk discover`), Linear project list, sampled session logs. This is the leading indicator that the trigger description is well-targeted.
- **Decision-quality KR (lagging)** — when it fires, does the outcome improve? Form: "in ≥X of last N sampled invocations, [skill] surfaced an issue or produced an artefact that would otherwise not have appeared." This is the lagging indicator that the skill body itself is well-authored.
- **Anti-output guard KR (committed)** — the discipline holds at the bottleneck. Form: "zero [historically-common output failure] across [window]" (e.g., zero repo-aliased Linear projects, zero KRs without sub-fields). Catches drift between intent and practice.

Adoption KRs ("skill installed in N repos") are output unless cross-repo adoption is itself the named goal — usually leave them out.

**Worked example — `/initiative-shape` itself.**

```
Goal:           For Anton (and any agent invoking pde-skills), make
                initiatives properly shaped before they enter a cycle —
                so cycle planning works against goals and KRs rather than
                repo-aliased backlogs.

KR1 [committed] — initiative-shape fires (or is offered) in ≥80% of
                  new-initiative moments across the next 4 cycles
  baseline: unknown — first cycle of measurement
  target:   ≥80% offered at new-initiative moments
  window:   next 4 cycles
  source:   transcript history (rtk discover), sampled

KR2 [committed] — in ≥4 of last 5 created initiatives, all six fields
                  pass the verification rubric
  baseline: 0/5 pass full rubric today
  target:   4/5 pass full rubric
  window:   next 4 cycles
  source:   Linear project descriptions, manual audit

KR3 [aspirational] — zero Linear projects created in the next 4 cycles
                  that are repo-aliased rather than outcome-named
  baseline: majority of historical projects repo-aliased
  target:   0 repo-aliased in window
  window:   next 4 cycles
  source:   Linear project list

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

- **Correctness KR (lagging)** — does the system get the right answer when it runs? Form: "≤X false negatives / missed events / wrong outputs across [N] runs in window" or "[result] matches [reference source] in ≥X% of [N] sampled runs." Data sources: production logs, sampled outputs against ground truth, the system's own audit trail. This is the lagging indicator that the implementation is sound.
- **No-silent-failure KR (committed)** — when a failure happens, do you find out? Form: "every error surfaces in [alert channel] within [bounded time] of failure" or "zero silent failures across [N] runs in window — every job either completes or fires an alert." Data sources: alert history, log diff between job runs and alert firings. This is the committed operability brake: a Type 2 system that fails silently is worse than one that doesn't run at all, because you're now trusting an output that isn't there.
- **Maintenance-burden KR (committed)** — does the human have to intervene to keep it running? Form: "zero manual restarts / redeploys / production-data hotfixes over [N-day window]" or "≤X manual interventions per [window]." Data sources: deploy history, ssh/console session log, on-call notes. This is the committed brake against the slow-leak failure mode where the product technically runs but consumes the operator's attention.
- **Availability KR (optional, committed when central)** — do the scheduled jobs complete? Form: "scheduled job [name] completes within [time budget] in ≥X% of runs across [window]." Data sources: job scheduler logs, completion timestamps. Use when scheduled-job completion is the central guarantee; otherwise rolled into maintenance-burden.

Feature-shipping KRs ("add [feature]", "build [integration]") are output. Growth KRs (DAU, MAU, retention, signups) are categorically inapplicable — there is one user.

**Worked example — `nestl`-shaped personal Rails app, scheduled-job product.**

```
Goal:           For Anton (single user), make the daily [recurring job]
                run reliably without manual intervention — so the output
                arrives on time without nagging the operator.

KR1 [aspirational] — ≤1 missed event / false negative per 30-day window
                  across the daily run
  baseline: unknown — first cycle of measurement
  target:   ≤1 missed event per 30 days
  window:   next 4 cycles (3 × 30-day observation windows)
  source:   production logs + sampled audit against source-of-truth

KR2 [committed] — every job failure surfaces in [alert channel] within
                  5 minutes; zero silent failures in window
  baseline: unknown — first cycle of measurement
  target:   0 silent failures across 90 days
  window:   next 4 cycles
  source:   alert history vs job scheduler log diff

KR3 [committed] — zero manual restarts, redeploys, or production-data
                  hotfixes across the 90-day window
  baseline: estimate ~1 manual intervention/week today; first cycle
            instruments the counter
  target:   0 manual interventions across 90 days
  window:   next 4 cycles
  source:   deploy history + ssh/console session log

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

## Type 4 — Research / thesis-driven

*Example: `em-os` (paused).* Work whose primary output is knowledge — a defended thesis, a resolved open question, or a published position. The consumer is the intended audience for the thesis (engineering leaders, in `em-os`'s case). The theory of success is that the thesis is clear, survives critique, and — at later stages — is adopted by the intended audience. Knowledge KRs (what we will be able to assert, with sourced evidence and stated confidence) sit above artefact-clarity KRs (what we will publish); adoption KRs sit above both but are usually later-stage. Pre-registration of predictions matters where the work is forecasting-shaped.

## Type 5 — Equity research tooling

*Examples: `stock-screen`, `stock-signal`, `stock-model`, `stock-timing`, `stock-portfolio`.* Tools that produce structured forecasts and decisions about specific tickers, with a durable artefact (cached `reports/TICKER_YYYYMMDD.json`) per call. The consumer is the author plus any downstream reader of cached reports. The theory of success is forecast calibration improving over time — the Tetlock standard — not throughput of analyses. Per Tetlock, calibration over a portfolio of dated, pre-registered calls matters more than accuracy on any single name; the Brier-score view forces forecasts to be dated, immutable, and graded against outcomes. Pre-registration is what makes the discipline honest — it removes the option to rationalise a wrong call after the fact, and it is the single feature that separates equity research from horoscope. Every KR points at the structured outputs the equity skills already produce.

**Objective shape.** "For [analyst plus downstream reader of cached reports], make [BUY/WATCH/AVOID calls] calibrated and pre-registered, with hit-rate and calibration graded post-hoc." The Objective names the *calibration discipline*, not the per-call analysis throughput. Running more screens, signals, or models is implementation; what the OKR scores is whether the calls made under this initiative grade well 12 months out — and whether the calling discipline was honest enough to be gradable at all.

**Default KR mix (3 KRs).** One pre-registration (committed) + one calibration (aspirational, lagging) + one hit-rate (aspirational, lagging). Pre-registration is non-negotiable for Type 5 — without it, the lagging KRs are ungradable, because there is no immutable record of what was actually claimed before outcomes were visible. A decision-quality KR (per-call postmortem) is an optional 4th when the cycle window already covers prior 12-month outcomes.

- **Pre-registration KR (committed)** — every BUY/WATCH/AVOID call written to a dated, immutable artefact before 12-month outcomes are visible. Form: "every BUY/WATCH/AVOID call from [skill] this window is logged to `reports/TICKER_YYYYMMDD.json` with timestamp; zero retroactive edits detected via git history across [window]." Data sources: the `reports/` directory git history (the immutability check) and the cached report files themselves. This is the committed brake against post-hoc rationalisation — a Type 5 initiative without it is producing horoscopes, not forecasts.
- **Calibration KR (aspirational, lagging)** — does the model's stated range bracket reality? Form: "for ≥X of N tickers whose 12-month window has closed, the bear–bull range from `/stock-model` bracketed the actual price at window close." Data sources: cached `reports/TICKER_YYYYMMDD.json` for the original call + current price at window close. This is the lagging indicator that the model's uncertainty bands are honest — wider isn't better, narrower isn't better, calibrated is what counts.
- **Hit-rate KR (aspirational, lagging)** — directional calls graded against the market. Form: "of BUY calls made ≥12 months ago, ≥X% are above entry by ≥Y%; of AVOID calls, ≥Z% are flat or down vs entry." Data sources: original call timestamps + current/window-close prices, both derivable from the cached reports. This is the lagging indicator that the calling discipline produces positive expected value, not just well-reasoned losses.
- **Decision-quality KR (optional 4th, aspirational)** — per-call postmortem. Form: "for ≥X tickers whose 12-month window has closed, a written postmortem exists in `reports/postmortems/` comparing model output, action taken, and observed outcome." Use when the cycle window already covers closed 12-month windows from prior calls; otherwise the 3-KR default is sufficient.

Throughput KRs ("run `/stock-screen` on N tickers", "produce N reports") are categorically the wrong shape for Type 5 — more analyses is output, and Type 5 grades on calibration of the analyses you already made.

**Worked example — equity skill pack cycle, calibrated-calls initiative.**

```
Goal:           For Anton (and any downstream reader of cached reports),
                make BUY/WATCH/AVOID calls from /stock-signal calibrated
                and pre-registered — so 12-month outcomes can be graded
                against immutable claims rather than rationalised after.

KR1 [committed] — every BUY/WATCH/AVOID call this cycle is logged to a
                  dated, immutable file before the next earnings release
                  for each ticker; zero retroactive edits detected via
                  git history across the window
  baseline: pre-registration discipline not enforced; 0/7 calls dated
  target:   7 calls timestamped + immutable across the window
  window:   this cycle + 90-day no-edit period
  source:   reports/TICKER_YYYYMMDD.json + git history (immutability)

KR2 [aspirational] — for ≥5 of 7 tickers whose 12-month window has
                  closed, the bear–bull range from /stock-model
                  bracketed the actual price at window close
  baseline: unknown — first cohort with full 12-month windows
  target:   5/7 calibration hits
  window:   next 4 cycles (catches the first cohort's window closes)
  source:   reports/TICKER_YYYYMMDD.json + current price feed

KR3 [aspirational] — of BUY calls made ≥12 months ago, ≥60% are above
                  entry by ≥10%; of AVOID calls, ≥60% are flat or down
                  vs entry
  baseline: zero graded calls — first cohort
  target:   ≥60% BUY hit-rate, ≥60% AVOID hit-rate
  window:   next 4 cycles
  source:   reports/TICKER_YYYYMMDD.json + current price feed

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

*Anticipated; no example yet in this portfolio.* Live software with paying users or external business stakeholders. The consumer is the paying user (or the business). The theory of success is standard product-OKR territory: activation, retention, conversion — each paired with a quality KR (NPS, p95 latency, error rate) to prevent vanity gains. Every KR has a baseline number from production telemetry, a target, and a window, with the telemetry in place before the cycle starts. "Ship feature X to 100% of users" is the canonical output-disguised-as-outcome failure mode here (Cagan); the antidote is to name the customer behaviour the feature is supposed to change.

## Sources

- Internal research: Linear document "Research and implementation plan — OKR shapes by project type" (Section 1.1, project `Initiative quality — type-aware OKRs with KRs`)
- `rules/linear-workflow.md` — initiative format the type field is added to
- `skills/initiative-shape/SKILL.md` — invokes the type probe at Step 2.5
