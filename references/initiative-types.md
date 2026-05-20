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

## Type 2 — Personal product (single-user, running)

*Example: `nestl` (Rails app).* Complete deployed software solving a recurring problem for one user. The consumer is the author as a single user. The theory of success is that the recurring job gets done reliably without manual intervention. Growth metrics, MAU, and adoption breadth are inapplicable — the dimensions that matter are correctness (zero false negatives or missed events), no-silent-failure (every failure surfaces in a visible alert within a bounded time), availability (scheduled jobs complete to SLO), and maintenance burden (zero manual restarts/redeploys over the observation window).

## Type 3 — Utility skill pack

*Examples: `resell-au`, `garage-sale`, `codex-primary-runtime`.* Flat collection of callable skills, each solving a discrete recurring task. The consumer is the author at per-invocation use. The theory of success is first-shot correctness of the generated artefact — the next invocation produces something the user posts, prints, or hands off without editing. Authoring more skills is output; what counts is whether the next invocation needs ≤ one edit and whether the pack covers the categories the user actually encounters end-to-end. Time-to-result KRs are usually vanity here unless speed is the named bottleneck.

## Type 4 — Research / thesis-driven

*Example: `em-os` (paused).* Work whose primary output is knowledge — a defended thesis, a resolved open question, or a published position. The consumer is the intended audience for the thesis (engineering leaders, in `em-os`'s case). The theory of success is that the thesis is clear, survives critique, and — at later stages — is adopted by the intended audience. Knowledge KRs (what we will be able to assert, with sourced evidence and stated confidence) sit above artefact-clarity KRs (what we will publish); adoption KRs sit above both but are usually later-stage. Pre-registration of predictions matters where the work is forecasting-shaped.

## Type 5 — Equity research tooling

*Examples: `stock-screen`, `stock-signal`, `stock-model`, `stock-timing`, `stock-portfolio`.* Tools that produce structured forecasts and decisions about specific tickers, with a durable artefact (cached `reports/TICKER_YYYYMMDD.json`) per call. The consumer is the author plus any downstream reader of cached reports. The theory of success is forecast calibration improving over time — the Tetlock standard — not throughput of analyses. Pre-registration of BUY / WATCH / AVOID calls before outcomes are visible, and post-hoc calibration scoring across 12-month windows, matter more than per-call confidence or volume. Every KR points at the structured outputs the equity skills already produce.

## Type 6 — Production / customer-facing

*Anticipated; no example yet in this portfolio.* Live software with paying users or external business stakeholders. The consumer is the paying user (or the business). The theory of success is standard product-OKR territory: activation, retention, conversion — each paired with a quality KR (NPS, p95 latency, error rate) to prevent vanity gains. Every KR has a baseline number from production telemetry, a target, and a window, with the telemetry in place before the cycle starts. "Ship feature X to 100% of users" is the canonical output-disguised-as-outcome failure mode here (Cagan); the antidote is to name the customer behaviour the feature is supposed to change.

## Sources

- Internal research: Linear document "Research and implementation plan — OKR shapes by project type" (Section 1.1, project `Initiative quality — type-aware OKRs with KRs`)
- `rules/linear-workflow.md` — initiative format the type field is added to
- `skills/initiative-shape/SKILL.md` — invokes the type probe at Step 2.5
