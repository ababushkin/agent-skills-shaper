# Product rules

These are the product principles and operational rules for the pde-skills pack. They cover roadmap structure, prioritisation, commitment, and learning. The companion skill `idea-triage` handles problem-framing at the point of intake. `roadmap-shape` (Next) covers the mechanics of building and maintaining the roadmap itself.

---

## Part 1 — Guiding principles

These are the ten beliefs that inform every roadmap decision. If a decision conflicts with a principle, the principle wins by default — and the burden of justification sits with the person arguing to deviate.

### 1. Outcomes, not outputs

Every item on the roadmap exists to produce a change in the world — a shift in a customer behaviour or a business metric — not to ship a feature. A team that celebrates shipping without measuring impact is a feature factory, and feature factories lose to teams that ship fewer things that work. Melissa Perri calls this trap the reason organisations "live and die by outputs" rather than customer value. Marty Cagan's formulation is stronger: roadmaps of features are the single largest source of waste in product teams.

**Implication:** We do not judge a quarter by how many things shipped. We judge it by how many of the shipped things moved the metric they were meant to move.

### 2. Roadmap items are problems to solve, not solutions to build

A roadmap item is framed as a problem with a desired outcome, not a feature. "Integrate PayPal" is not a roadmap item; "reduce checkout abandonment for international users" is. The team then has the freedom — and responsibility — to find the best solution. Cagan's SVPG work is built on this distinction: when you hand a team a feature, you've already decided most of the thinking for them, and you've lost access to the better solutions they would have found.

**Implication:** If a proposed roadmap item starts with a verb like "build," "add," or "integrate," rewrite it before it goes any further.

### 3. Every roadmap item is a bet, not a promise

Most product ideas don't work on the first try. Cagan estimates that "many of the ideas won't actually work as we hope, and those that could work will typically take several iterations to get to the point where they move the needle." A roadmap is therefore a portfolio of bets — some will pay off, some won't, and the job is to learn fast enough to adjust. Ryan Singer codifies this in Shape Up by explicitly calling the planning meeting the "betting table" — the word is chosen to make the probabilistic nature of the work honest.

**Implication:** Expect some roadmap items to be killed mid-flight. That is a sign of health, not failure.

### 4. Evidence beats opinion — but confidence must be made explicit

Ideas are cheap and abundant; the scarce asset is evidence that the idea will work. Itamar Gilad's Confidence Meter makes the point numerically: an opinion from the CEO carries roughly 0.1 out of 10 confidence; anecdotal data is 0.5; data from surveys, smoke tests or experiments is substantially higher. Without a confidence score, "high impact" is a claim, not a number. The Impact × Confidence × Ease score (ICE, via Sean Ellis and Gilad) gives the team a shared, auditable way to argue about priorities without devolving into HIPPO (Highest-Paid Person's Opinion) decisions.

**Implication:** A roadmap item's priority is a function of expected impact and the strength of evidence behind that expectation.

### 5. Focus is the multiplier — saying "no" is the core act

Cagan, quoting Steve Jobs, reframes focus: "Focus means saying no to the hundred other good ideas." Most companies do too many things at once and make too little progress on any of them. Shreyas Doshi's LNO framework formalises this at the task level: leverage tasks return 10–100× the effort put in, while overhead returns almost nothing. The same logic applies at the roadmap level: a handful of bets pursued with full weight will outperform a dozen pursued half-heartedly.

**Implication:** Every "yes" must be accompanied by an explicit "no." A full roadmap is a failing roadmap.

### 6. Value flows both ways — customer and business

Cagan originally framed product success as valuable, usable, feasible. He later split "valuable" into customer value and business viability because teams were gravitating toward customer value and ignoring the business side (or vice versa). A roadmap item that delights customers but has no monetisation path, channel fit, legal clearance, or brand consistency will fail just as surely as one customers don't want. Perri's "value exchange" makes the same point: customers only realise value when their problem is solved; the business only realises value (revenue, data, loyalty) when that happens.

**Implication:** No roadmap item is approved until we can articulate the customer value and the business value it's expected to produce.

### 7. Certainty decays with time horizon — plan accordingly

Janna Bastow's Now-Next-Later roadmap exists because timeline roadmaps pretend to know things they can't. The future is foggier the further out you look, and a roadmap should acknowledge that honestly. "Now" is committed and concrete. "Next" is directional and validated but not scoped in detail. "Later" is a set of hypotheses about where the world is going. Pretending you know what you'll ship in Q3 of next year is the kind of false precision that produces the worst kind of roadmap: the one everyone stops believing in by month two.

**Implication:** Detail and commitment should be highest for Now, lower for Next, and deliberately sparse for Later.

### 8. Fixed time, variable scope — never the other way around

Ryan Singer's Shape Up flips the default equation: rather than starting with a solution and estimating how long it will take, start with how much time the problem is worth (the appetite) and shape a solution that fits. This matters on the roadmap because it prevents the most common failure mode — work that expands indefinitely to consume all available capacity. A roadmap item with an appetite of six weeks that isn't shipped in six weeks is not automatically extended; it is re-evaluated. The "circuit breaker" is deliberate.

**Implication:** Every roadmap item carries a time budget set at the start. When the budget runs out, the default is to ship what we have, cut scope, or kill the item — not to extend it.

### 9. Strategic context matters more than any individual item

Cagan is emphatic that product strategy — a focused set of insights about which problems matter most and why — has to precede the roadmap. Without it, the roadmap becomes a grab-bag of stakeholder requests and the appearance of progress. Pichler's GO Roadmap makes the same point through form: goals are the primary element, features are derivative. Strategy tells the team which rabbit to chase. Roman proverb via Cagan: "If you chase two rabbits, you will not catch either one."

**Implication:** If a proposed roadmap item doesn't connect to a stated strategic priority, it doesn't belong on the roadmap — no matter how attractive it looks in isolation.

### 10. "Done" means the outcome moved, not the feature shipped

Perri attributes to Jeff Gothelf the line "Version 2 is the biggest lie in software development." Most teams ship v1, declare victory, and move on — never revisiting the feature to check whether it delivered the outcome they claimed it would. That is the build trap in its purest form. The definition of done for a roadmap item is not "shipped" but "outcome achieved, or decisively proven not to be achievable with this approach."

**Implication:** Finishing a roadmap item includes measuring impact, not just deployment.

---

## Part 2 — Laws / Rules

These are concrete, operational rules — written so that any team member can check whether the team is complying with them. They cover four areas: what goes on the roadmap, how we prioritise, how we commit, and how we review and learn.

### A. What goes on the roadmap (structure and format)

**Rule A1 — Time horizons, not dates, are the default format.**
The roadmap is organised as Now / Next / Later (Bastow). Dates appear only where a high-integrity commitment has been made (see Rule C2). Quarter labels are permitted as a transitional tool but not preferred — they re-introduce the very problem Now-Next-Later was designed to solve.

**Rule A2 — Every roadmap item names the problem, the customer it affects, and the outcome we want to move.**
Format: "For [customer segment], we believe [problem] is causing [negative outcome]. If we solve it, we expect [measurable outcome] to improve by [target]." Items that can't be written in this form aren't ready to be on the roadmap.

**Rule A3 — Every roadmap item is tagged with a measurable success criterion.**
No item ships without a metric that will tell us whether it worked. If we can't name the metric, we don't understand the bet well enough to make it. This is the Pichler/Cagan consensus: goal-oriented roadmaps fail when the goal is vague ("improve engagement") rather than specific ("increase weekly active usage of feature X by 15% among new users within 60 days of launch").

**Rule A4 — Solutions are held loosely; problems are held tightly.**
The roadmap describes what problem the team will solve this quarter. It does not describe the specific feature that will solve it. Solution detail is allowed in working documents (pitches, briefs, design explorations) but is not the roadmap itself. This protects us from being locked into a solution we chose before we had the information to choose well.

**Rule A5 — "Keep-the-lights-on" work doesn't need outcome framing.**
Bug fixes, compliance items, partner obligations, and minor maintenance go straight to the backlog without needing an outcome hypothesis. This is Cagan's explicit carve-out. The point of the rule is to prevent the anti-pattern of either (a) inflating trivial work with grand outcomes, or (b) letting real product work escape outcome framing by hiding inside KTLO.

**Rule A6 — There is no "parking lot." Items are on the roadmap or they are in the idea bank.**
Gilad's distinction matters: the Idea Bank is a library of validated and unvalidated hypotheses that might become roadmap items once they earn sufficient confidence. Mixing unvalidated ideas into the roadmap makes the roadmap look more certain than it is and clogs the signal.

### B. How we prioritise (choosing what's in)

**Rule B1 — Every candidate item is evaluated against both customer value and business viability.**
Neither alone is sufficient (Cagan's four-risk framework). Customer-value-only items produce delightful products that don't make money; viability-only items produce the kind of product customers abandon the moment a competitor appears. An item that scores well on only one dimension must either be reshaped to cover both or de-prioritised.

**Rule B2 — Candidate items receive an explicit Impact × Confidence × Ease score (ICE).**
Impact is the expected magnitude of change on the target metric. Confidence is the strength of evidence behind the impact claim (use Gilad's Confidence Meter — opinion ≠ data ≠ experimental evidence). Ease is an effort estimate from engineering/design. Ideas with high impact but low confidence are not killed — they are routed to validation work before they can claim a slot on the roadmap.

**Rule B3 — We classify each item into one of our portfolio themes.**
Using Shreyas Doshi's portfolio themes, every item is one of:

- Differentiators — things competitors don't have that customers care about
- Table-stakes — things we need just to be taken seriously
- Incrementals — improvements to things we already do
- Embarrassments / "broken windows" — parts of the product we're quietly ashamed of
- Customer specials / large-customer requests — things driven by specific accounts
- Tech foundation — platform, infrastructure, technical debt
- Speculative bets — high-risk, high-upside exploration

We commit to an explicit allocation across these themes each planning cycle. A roadmap that is 90% customer specials is a sales roadmap, not a product roadmap.

**Rule B4 — Use Kano classification for customer-facing work.**
For any item aimed at improving a customer-facing experience, classify whether it is a Must-be (absence causes dissatisfaction, presence is invisible), a Performance attribute (linear more-is-better), a Delighter (unexpected, disproportionate positive effect), or Indifferent (nobody cares). Fix Must-be gaps before investing heavily elsewhere. Pick a small number of Delighters deliberately — these are what customers talk about. De-prioritise Indifferents. Remember Kano's second law: today's delighter becomes tomorrow's must-be.

**Rule B5 — Use cost of delay for sequencing, not just impact.**
Two items with equal impact are not equivalent if delaying one costs revenue, churn, or competitive position more than the other (Perri, via Reinertsen). "If we don't ship this in Q2, we lose the seasonal window" is a cost-of-delay argument. It should be made explicitly, not smuggled in as urgency.

**Rule B6 — Reject any item whose confidence is below threshold unless the only work being committed to is validation.**
Low-confidence items don't get a build slot. They get a validation slot — a time-boxed piece of discovery work whose purpose is to raise confidence high enough to warrant a build bet. This is the core move of Gilad's GIST framework and Torres' Opportunity Solution Tree: separate "the idea is worth testing" from "the idea is worth building."

**Rule B7 — "A large customer asked for it" is not a prioritisation argument by itself.**
Cutler's warning about sales-driven roadmaps: features built to close individual deals rarely account for the non-linear increase in product complexity they create. A large customer's request still has to pass B1–B6 on its merits. If it does, great. If it doesn't, it goes in the idea bank, and the commercial relationship is managed separately.

### C. How we commit (capacity, dates, scope)

**Rule C1 — Each roadmap item has an appetite set at the start.**
Singer's Shape Up principle: decide up-front how much the problem is worth in time and team size, then shape a solution that fits. The appetite is a cap, not a target. If the solution that fits the appetite isn't valuable enough, we cut scope, reshape, or kill the item — we do not quietly expand the appetite.

**Rule C2 — Date commitments are high-integrity only, and are the exception.**
Cagan's "high-integrity commitment" rule: we commit to a date only after sufficient discovery has been done to understand value, usability, feasibility, and viability well enough to commit with confidence. Low-confidence dates are worse than no dates because they train the rest of the business to ignore us. When a high-integrity commitment is made, it is tracked separately from the main roadmap, and the default is to keep it.

**Rule C3 — Capacity allocation is explicit, not implicit.**
At the start of each planning cycle, we say out loud what % of capacity goes to each portfolio theme (Rule B3), what % to KTLO, and what % is reserved for validation and discovery work. A roadmap that pretends capacity is infinite is not a roadmap.

**Rule C4 — Dependencies are surfaced before commitment, not after.**
If an item depends on work from another team, a platform capability, a legal approval, or a partner integration, that dependency is identified and de-risked before the item enters "Now." Platform and cross-team dependencies are the most common cause of high-integrity commitments being missed.

**Rule C5 — The roadmap is revisited on a fixed cadence.**
At minimum, the full roadmap is re-reviewed quarterly (Pichler). New evidence, new data, and shifts in strategic context are the inputs to that review. A roadmap that hasn't moved in six months is either (a) a miracle or (b) not being looked at.

### D. How we review and learn

**Rule D1 — Every roadmap item has a post-launch impact review.**
Cutler's diagnostic question: does the team know whether the thing it shipped worked? If the answer is "no," we are a feature factory. The post-launch review asks: (1) did we hit the outcome metric, (2) if not, why not, (3) do we iterate, kill, or redirect, and (4) what did we learn about our confidence calibration.

**Rule D2 — Killing work is a normal outcome, celebrated as much as shipping.**
Singer's point: the project is great; it's just not working, and that's fine. Cutler's point: "infrequent acknowledged failures and scrapped work" is a feature-factory smell. We explicitly celebrate items that were killed after investigation, because that's the system working. We do not punish teams for bets that didn't pay off; we punish teams for ignoring the evidence.

**Rule D3 — PMs run retros on their own product decisions, not just the team's velocity.**
Cutler: "Developers have 'passing tests,' but product managers do not." A PM retrospective reviews: items shipped vs. outcomes achieved, expected impact vs. actual, confidence scores going in vs. what we learned — and feeds the result back into how we estimate the next round.

**Rule D4 — "Done" is outcome achieved, not feature deployed.**
Perri: definition of done includes the target metric moving. If it didn't move, the work isn't finished; we iterate, pivot, or kill. We do not declare victory on ship date.

**Rule D5 — Learning gets fed back into the idea bank and the Confidence Meter.**
When a bet pays off (or doesn't), the evidence is written down and attached to related ideas in the bank. Over time this raises or lowers the confidence score on adjacent hypotheses. This is how the team gets smarter cycle over cycle rather than running the same arguments every quarter.

---

## Part 3 — Quick reference

The roadmap is: a prioritised set of problems to solve, framed by outcome, held with a time horizon appropriate to our confidence, and revisited as we learn.

The roadmap is not: a list of features with dates, a sales wishlist, a stakeholder appeasement document, or a commitment register.

A roadmap item earns its slot by demonstrating:

- A customer problem worth solving
- A measurable outcome we expect to move
- Evidence (confidence) sufficient to justify the bet
- Both customer value and business viability
- Fit with a named portfolio theme and strategic priority
- An explicit appetite (time budget)

A roadmap item loses its slot when:

- Evidence arrives that the underlying hypothesis is wrong
- Something with higher expected value × confidence displaces it
- It consistently exceeds its appetite without hitting outcomes
- Strategic context shifts in a way that changes the problem's importance

The ten principles in one line each:

1. Outcomes, not outputs — judge by what moved, not what shipped
2. Items are problems to solve, not solutions to build
3. Every item is a bet — expect some to fail, learn fast
4. Evidence beats opinion — confidence must be made explicit
5. Focus is the multiplier — every "yes" requires an explicit "no"
6. Value flows both ways — customer value and business viability
7. Certainty decays with time horizon — plan accordingly
8. Fixed time, variable scope — appetite is a cap, not a target
9. Strategic context matters more than any individual item
10. "Done" means the outcome moved, not the feature shipped
