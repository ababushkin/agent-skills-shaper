# Engineering principles — universal (tier 1)

These are the universal engineering principles for the pde-skills pack. "Universal" means: a senior engineer in 2010 would have agreed with them. They predate AI agents and apply equally whether the implementer is a human or an agent.

The companion document `eng-principles-agentic.md` covers tier-2 principles — those specific to AI-agent failure modes (context-as-asset, hallucination-as-default, evidence-beats-vibes, and others). Skills, hooks, and sub-agent personas trace to principles in either tier; some trace to both.

When the two tiers overlap (e.g. small batches matter universally; the AI-coding batch-size finding is tier-2 amplification), the universal principle is stated here, and the agent-specific texture is in the agentic file.

---

## Part 1 — Guiding principles

These are the ten beliefs that inform every engineering decision. If a decision conflicts with a principle, the principle wins by default — and the burden of justification sits with the person arguing to deviate.

### 1. Shipped is not done; observed is done

Deployed code is necessary but not sufficient. A change is only "done" when it is running in production, instrumented, and the thing it was meant to move has been observed moving — or decisively not moving. This is the engineering translation of the roadmap's "outcome achieved, not feature shipped." A decade of DORA research makes the evidence overwhelming: high-performing teams deploy small changes often and see the effect quickly; low-performing teams ship occasionally, discover problems weeks later, and spend their lives in firefighting. Deployment without observation is theatre.

**Implication:** Definition-of-done includes production telemetry in place, rollback tested, and the primary metric observed. If those aren't in place, the work isn't finished — regardless of what the PR status says.

### 2. Design starts with the problem, not with the stack

A technical design document begins with the problem, the users it affects, the constraints (functional and non-functional), and the alternatives considered — and only then describes the proposed solution. When an engineer opens a doc with "we'll build a Kafka consumer that…" they've pre-committed to a solution before the problem is understood. Will Larson's rule for when to write a design doc is well calibrated: any project taking more than a month, any capability that will be reused, or any change that meaningfully affects users. Michael Nygard's ADR format — Context, Decision, Consequences — embeds the same discipline at the decision level. Mark Richards calls this the "second law of software architecture": why is more important than how.

**Implication:** Every non-trivial spec has a Problem, Context, Constraints, Alternatives, Decision, and Consequences structure. Solution-first specs are sent back for rewriting.

### 3. Architecture is the set of decisions that are expensive to change — minimise that set

Martin Fowler's definition of architecture is the cleanest one available: the decisions that are hard to change later. A good architecture does not try to get every decision right; it tries to keep the set of hard-to-change decisions small. Bezos's framing of one-way doors versus two-way doors captures this operationally: two-way doors can be walked through quickly and reversed if wrong, so decide fast; one-way doors demand deliberate, evidence-based deliberation. Mary and Tom Poppendieck call this the Last Responsible Moment: make the decision when not deciding costs more than the information you'd gain by waiting. This is the engineering analogue of the roadmap's "every item is a bet" — and reversibility is how we keep the portfolio survivable.

**Implication:** When evaluating an architectural choice, name (a) whether it's reversible and (b) how expensive the reversal is. Deliberation budget scales with cost-of-reversal, not with emotional attachment to the choice.

### 4. Assumptions must be named; risky ones must be tested before committing

Every design contains implicit bets — about load patterns, failure modes, third-party SLAs, data shape, schema stability, team capacity, adoption rates. Hunt & Thomas's *The Pragmatic Programmer* prescribes tracer bullets: real code that exercises the riskiest path early. Alistair Cockburn's walking skeleton makes the same point — a minimal end-to-end implementation that touches every real component is more valuable than a detailed plan that assumes them away. This is the direct engineering analogue of the roadmap's Confidence Meter: a design whose assumptions are unverified is a low-confidence design, no matter how senior the person proposing it.

**Implication:** Before committing engineering time to a large build, identify the three riskiest assumptions and test them with a time-boxed spike. If the spike invalidates them, reshape or kill — don't proceed on hope.

### 5. Code is a liability; the best change is often the one you don't make

Kent Beck's *Tidy First* frames software design explicitly as economics: the asset is behaviour (what the system does); the cost is structure (the code that produces the behaviour). Every line of code is a tax on every future change — read, understand, test, refactor, migrate, delete. YAGNI ("you aren't gonna need it," Beck, via XP) is the practical corollary: don't build capability for a future you haven't confirmed will happen. John Gall's Law comes at the same insight from the other direction: "a complex system that works is invariably found to have evolved from a simple system that worked." You cannot skip to the complex system; you have to build your way there.

**Implication:** Default to the smallest solution that solves the present problem. Speculative flexibility is speculative debt. When in doubt, delete.

### 6. Operability, observability, and security are functional requirements, not "non-functional" ones

Michael Nygard's *Release It!* is the canonical text: a system that can't be operated, diagnosed, or recovered is not production-ready, regardless of whether the feature logic is correct. Google's SRE practice codifies this as "operational maturity is a feature" — SLOs, error budgets, structured logs, metrics, traces, and graceful degradation are not polish, they are preconditions for release. The same logic applies to security, accessibility, and privacy: shifted left, they are design concerns; shifted right, they are crises. The word "non-functional" has done more damage to engineering than almost any other term in the field by implying these concerns are optional.

**Implication:** Every design doc has an Operability section — SLOs, alerts, metrics, failure modes, rollback plan, capacity headroom, security posture. Absence of this section is a reason to reject, not a reason to proceed "and add it later."

### 7. Design for change; the system will outlive the requirements that motivated it

Ford, Parsons, and Kua's *Building Evolutionary Architectures* makes the strongest modern case: the one guaranteed fact about any system we build is that the world around it — requirements, load, team, regulations, dependencies — will change. An architecture optimised for today's requirements loses to one optimised for cheap change. Their mechanism is the fitness function: an automated, continuous check that the architecture is holding the characteristics we care about (performance, modularity, coupling, security, cost). This is the engineering equivalent of the roadmap's "certainty decays with time horizon" — the longer the timescale, the more the architecture needs to bend rather than resist.

**Implication:** When designing, name the architectural characteristics you most need to protect, and write a fitness function — a test, a metric, an alarm, a chaos experiment — that fails loudly when they drift. Without the fitness function, "we'll watch out for that" is not a plan; it is a hope.

### 8. Small batches beat big batches — every time

This is the most empirically supported principle in modern engineering. Don Reinertsen proved it economically in *The Principles of Product Development Flow*; Humble and Farley proved it operationally in *Continuous Delivery*; a decade of DORA research has proven it across industries, stacks, and company sizes. Batch size is the single most reliable predictor of delivery performance. Small batches catch bugs sooner, are safer to roll back, shorten the feedback loop, and produce more learning per unit of calendar time.

**Implication:** Trunk-based development, short-lived branches, feature flags, and continuous deployment are defaults. A PR exceeding roughly 400 lines, or sitting open more than a few days, is a warning signal — not a feature.

### 9. Conway's Law is a law, not a suggestion

Systems come to mirror the communication structure of the organisations that build them (Conway, 1968). Skelton and Pais's *Team Topologies* is the most useful modern application: four team types (stream-aligned, platform, enabling, complicated-subsystem) and three interaction modes (collaboration, X-as-a-service, facilitating), with team cognitive load treated as a first-class design constraint. Eric Evans's Domain-Driven Design provides the technical counterpart: bounded contexts are the seams along which both systems and teams should split. The implication most teams miss is the Inverse Conway Maneuver — if the architecture we want doesn't match the team structure we have, one of them must change, and it is often cheaper to change the teams.

**Implication:** Team boundaries and system boundaries are designed together, not independently. When a service has four teams contributing to it, or a team owns eight unrelated services, the topology is broken — expect quality and velocity to reflect it, because they will.

### 10. Prefer boring technology; innovation tokens are a scarce resource

Dan McKinley's "Choose Boring Technology" essay crystallised a principle that runs under the rest: every new database, language, framework, or paradigm is a budget you spend on that technology instead of on the problem. You get a finite number of innovation tokens per project and per team; spend them where they create customer value, not where they're fun. Will Larson's engineering strategy work gives the same advice from the leadership angle: the default answer to "should we adopt X new thing?" is no, and the burden of justification sits with the proposer. This is the direct engineering parallel to the roadmap's saying-no-is-the-core-act — focus compounds; fragmentation is the slow killer.

**Implication:** Novel technology requires written justification — what problem does it uniquely solve, what is the total cost of ownership (training, hiring, operations, migration), which innovation token does it consume, and why is this the best use of that token. "It's the modern way" or "the team is excited about it" are not justifications.

---

## Part 2 — Laws / Rules

These are concrete, operational rules — written so that any team member can check whether the team is complying with them. They cover four areas: what we specify, how we design, how we build and ship, and how we review and learn.

### A. What we specify (design docs, ADRs, specs)

**Rule A1 — Any work meeting one of three triggers gets a written design doc.**
(Adapted from Larson.) The triggers are: (1) more than four weeks of engineering time; (2) the capability will be used by more than the team building it; (3) the change has meaningful impact on users, cost, compliance, or operational load. If none of these apply, a short ADR may suffice. If any apply, a design doc exists before implementation begins. "We'll figure it out in the code" is a symptom of the build trap, not a delivery strategy.

**Rule A2 — Every design doc follows the same structure.**
Problem → Context → Constraints (functional and non-functional, with numbers) → Alternatives considered → Recommended approach → Consequences → Operability plan → Open questions. This is Nygard's ADR shape expanded to the full design. The Alternatives section is not decorative: a design doc that lists only the chosen approach is incomplete, because it gives reviewers nothing to push back against.

**Rule A3 — Every architecturally significant decision produces an ADR.**
(Nygard.) "Architecturally significant" means it affects structure, dependencies, interfaces, non-functional characteristics, or construction techniques. ADRs are short (one page), immutable once accepted, and superseded rather than edited. They live in version control next to the code. The Context section is in facts, not opinions; the Consequences section is in both positive and negative directions.

**Rule A4 — Non-functional requirements are specified up front as measurable targets.**
Latency percentiles (p50/p95/p99), availability SLOs, throughput targets, error budgets, security posture, data residency, accessibility, cost envelope. "Fast," "reliable," and "scalable" are not specifications. A design doc that doesn't name numbers for the NFRs that matter is not complete, regardless of how polished the prose is.

**Rule A5 — Fitness functions make the targets in A4 executable.**
(Ford/Parsons/Kua.) Each architectural characteristic we care about gets an automated check — a test, a metric alarm, a CI gate, a chaos experiment. A target that isn't being continuously verified will drift; the fitness function is the seatbelt. If you cannot express a quality as a fitness function, you don't yet understand it well enough to protect it.

**Rule A6 — Every design doc has an Operability section.**
Metrics, logs, traces, alerts, on-call runbook, rollback plan, capacity headroom, known failure modes, upstream and downstream dependency failure modes. If the team building it cannot describe how on-call will debug it at 3am, it's not shippable. This section is authored with the people who will operate it — not delivered to them.

**Rule A7 — Interfaces are designed before implementations.**
(Parnas; Cockburn's Hexagonal Architecture / Ports & Adapters.) The contract a component exposes is the expensive-to-change thing; the implementation behind it is cheap. Design the contract first, implement second, and treat internal contract changes with the same seriousness as external API changes — because to the consumers inside your system, that's exactly what they are.

### B. How we design (choosing the approach)

**Rule B1 — Default to the smallest solution that solves the stated problem.**
(YAGNI; Gall's Law.) Complexity earns its place by demonstrating that a simpler solution fails a stated requirement. "We might need this later" is not a demonstration. Speculative generality is speculative debt, and the interest rate is compounding.

**Rule B2 — Build a walking skeleton before building features.**
(Cockburn.) The minimal end-to-end implementation — one request path wired through every real component, in the real deployment environment — flushes out the integration, deployment, and infrastructure surprises that wreck schedules. Pre-walking-skeleton estimates are uncalibrated; post-walking-skeleton estimates are usable.

**Rule B3 — Every proposed solution names its blast radius and its reversibility cost.**
How much breaks if this is wrong? How long and how expensive is it to undo? (Principle 3.) Discussion of a proposal is not complete until these two questions are answered — and the rigour of deliberation scales with them. One-way doors demand more scrutiny than two-way doors.

**Rule B4 — Boring technology is the default; novelty requires written justification.**
(McKinley; Larson.) The proposer answers: what problem does this new technology uniquely solve that our existing stack cannot; what is the total cost of adoption (training, operations, hiring, migration, integration); which innovation token does it consume and why is it best spent here. If no convincing answer exists, the default wins.

**Rule B5 — Build vs. buy vs. adopt is an explicit decision.**
For every capability: is this our differentiator (build), a solved problem others can solve for us (buy / SaaS / OSS), or available as a mature ecosystem component (adopt). Building a worse version of something that exists is a common, expensive mistake. Buying something that's actually our differentiator is the same mistake in reverse. This decision is part of the design doc, not a hallway conversation.

**Rule B6 — Generalise on the third occurrence, not the first.**
(Rule of Three; Fowler.) Platformisation, framework extraction, and internal libraries are justified by multiple concrete consumers, not one hypothetical future. Two consumers is a pattern; one is an abstraction looking for a problem. (Past three consumers, Team Topologies' platform-as-product discipline kicks in — see Rule C9.)

**Rule B7 — Cross-team dependencies are surfaced and de-risked before commitment.**
(Mirrors roadmap Rule C4.) A design that assumes work from another team, a platform capability, a legal sign-off, or a vendor commitment identifies each dependency, verifies it with the owner in writing, and stages the work so that a slip in one dependency doesn't block the whole thing. Unplanned cross-team dependencies are the single most common cause of missed commitments.

### C. How we build and ship

**Rule C1 — Trunk-based development with short-lived branches is the default.**
(Humble & Farley; DORA.) Long-lived feature branches cause merge pain, delay feedback, and obscure blast radius. Branches live hours to days, not weeks. Large changes are broken into small, independently mergeable steps, hidden from users by feature flags until ready.

**Rule C2 — Deployment is decoupled from release.**
Feature flags, dark launches, canary deploys, and progressive rollouts mean that shipping code to production is a technical decision and exposing it to users is a product decision. This halves the risk of both and makes rollback a dial instead of an emergency.

**Rule C3 — Every service has an error budget, and we enforce it.**
(Google SRE.) Each service gets an SLO; the error budget is the allowance for failures within that SLO. When the budget is burning, feature work stops and reliability work starts. This is a rule, not a discussion — the point is to make the trade-off automatic and un-arguable, so no one has to win a political fight to protect reliability.

**Rule C4 — CI stays green. A red build is the team's top priority.**
If CI is broken, no one ships anything new until it's fixed. Tolerating a persistently red or flaky CI is a signal that the team has stopped treating its feedback loop as real, and everything downstream — quality, speed, confidence — decays with it. Flaky tests are bugs, not background noise.

**Rule C5 — Time-box every spike; produce a written decision when the box expires.**
(Shape Up appetites applied to technical work.) A spike is a fixed-duration investigation, not a fixed-scope one. When time is up, the output is: what we learned, what we recommend (proceed / reshape / kill), and the evidence for the recommendation. The default at the end of a spike is to pause — never to quietly extend.

**Rule C6 — Automate on the second repetition, not the first.**
First time: do it by hand. Second time: wince, do it by hand, and write down what you did. Third time: automate it. This calibrates against both premature automation (speculative, expensive) and chronic under-automation (the slow leak that nobody notices until on-call is drowning).

**Rule C7 — Security, accessibility, and privacy are shift-left concerns.**
Threat modelling happens at design time. Accessibility is baked into components and tested in CI. Privacy (data minimisation, retention, cross-border, consent) is a design decision, not a legal review at the end. Treating these as late-stage gates creates adversarial dynamics with partner teams and slows everything down for everyone.

**Rule C8 — Tests are a specification of behaviour, not a coverage metric.**
Tests exist to describe what the system is supposed to do, catch regressions, and give us the courage to change things. Optimising for coverage percentage without optimising for the quality of the assertions produces noise, not safety. A 95%-covered test suite full of tautologies is worse than a 70%-covered suite of genuinely confirming tests, because it gives false confidence.

**Rule C9 — Platforms are products; they have customers, roadmaps, and success metrics.**
(Team Topologies: platform-as-a-product.) Internal platforms that get built and then "promoted" to teams as mandatory fail at approximately the same rate as external products that skip product management. Platforms have adoption metrics, documentation, onboarding, and a feedback loop — or they don't exist as platforms, they exist as hazards.

### D. How we review and learn

**Rule D1 — Every production incident produces a blameless postmortem.**
(Allspaw; Google SRE.) The question is what conditions made the incident possible, not who made the mistake. Postmortems identify contributing factors, remediations with owners and dates, and — critically — things we learned about our model of the system that turned out to be wrong. A postmortem that yields no system-level insights is an incomplete postmortem.

**Rule D2 — Every non-trivial project gets a post-launch impact review.**
(Engineering analogue of the roadmap's D1.) At a defined interval after launch, review: did the target metric move; did any reliability, latency, or cost indicator regress; what surprised us; what would we have designed differently. The review is attached to the original design doc and its ADRs, so future readers see the full arc from bet to outcome.

**Rule D3 — ADRs are living documents: re-read, superseded, never quietly ignored.**
When new information arrives that would change an accepted ADR, we write a superseding ADR that cites the original. Silently drifting away from an accepted ADR is worse than overturning it — it creates a gap between the stated architecture and the actual one, and that gap is where the worst bugs live.

**Rule D4 — Technical quality is measured, not discussed.**
Fitness functions (Rule A5), the four DORA metrics (deployment frequency, lead time for changes, change failure rate, failed-deployment recovery time), and code-level signals (PR cycle time, test flakiness rate, incident frequency by component) are tracked and reviewed on a fixed cadence. "Our tech debt is bad" is not a measurement; it is a feeling.

**Rule D5 — Killing a technical approach is a normal, celebrated outcome.**
(Parallels roadmap D2.) A spike or prototype that ends in "we shouldn't do this" is a success — the organisation saved the cost of the full build. The failure mode is teams that quietly continue with disproven approaches because stopping feels like losing. Leaders set the tone here: reward the team that announces "we tried it, it didn't work, here's what we learned," and punish no one for evidence-based reversals.

**Rule D6 — Documentation decay is a bug, fixed like any other bug.**
When docs and behaviour diverge, we either fix the doc or fix the code — we don't leave the divergence. Stale docs are worse than missing docs: missing docs make people cautious and ask questions; stale docs make people confidently wrong.

**Rule D7 — The team retrospects on its engineering decisions, not just its velocity.**
(Engineering version of roadmap D3.) What we estimated vs. what we hit; where architectural bets paid off and where they didn't; which ADRs are aging well and which are aging badly; calibration of our confidence over time. This is how the team gets smarter cycle over cycle, rather than repeating the same mistakes in different forms.

---

## Part 3 — Quick reference

The engineering practice is: designing, building, and operating systems as a continuous learning exercise — where the code is the cheapest artefact we produce and the understanding it embodies is the expensive one.

The engineering practice is not: producing lines of code against a spec, optimising for point-in-time correctness, or treating "shipped" as "done."

A piece of work earns its slot when:

- The problem, constraints, and desired outcome are documented
- Alternatives have been considered in writing
- Non-functional requirements have numbers, not adjectives
- Reversibility and blast radius are named
- The operability plan (metrics, alerts, rollback) exists before the build begins
- Cross-team dependencies have been surfaced and confirmed with their owners
- The boring default has been considered and, if rejected, rejected in writing

A piece of work is complete when:

- It is deployed, behind a flag, with rollback verified
- Its fitness functions are green and running continuously
- The target metric has been observed moving — or the work has been decisively proven not to move it
- The design doc and ADRs reflect what we actually built, not what we originally proposed
- The post-launch review has been written and linked to the original spec

The ten principles in one line each:

1. Shipped is not done; observed is done
2. Design starts with the problem, not the stack
3. Architecture is the set of expensive-to-change decisions — minimise it
4. Name your assumptions; test the risky ones before committing
5. Code is a liability; the best change is often the one you don't make
6. Operability, observability, and security are functional requirements
7. Design for change; the system will outlive its requirements
8. Small batches beat big batches — every time
9. Conway's Law is a law, not a suggestion
10. Prefer boring technology; innovation tokens are scarce

For agent-specific principles that amplify these — context-as-asset, hallucination-as-default, evidence-beats-vibes, stop-the-line, and others — see `eng-principles-agentic.md`.
