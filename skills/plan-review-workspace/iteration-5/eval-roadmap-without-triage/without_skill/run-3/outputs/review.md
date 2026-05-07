# Plan Review: Q3 Roadmap — Shareable Shortlist / Push Notifications / Onboarding Rewrite

## Summary verdict

Not ready to approve. The allocation rationale and evidence base are too thin to commit team capacity at these proportions. The themes are plausible; the case for each is not.

---

## What's reasonable here

- Three themes is a sensible number for a quarter. Focus is preserved.
- The 60/30/10 split is explicit, which is better than leaving capacity allocation implicit.
- Each theme has at least a one-line rationale, which is a start.

---

## What's missing or weak

### 1. "We keep getting requests" is not a prioritisation argument

Volume of requests is a signal, not a decision. It tells you something is salient; it doesn't tell you whether solving it will move a metric, which customers are asking, what they're actually trying to do, or whether the right response is a shareable shortlist feature at all. This is the HIPPO/sales-driven roadmap failure mode — urgency borrowed from volume rather than from expected impact.

Questions that need answers before this earns 60% of capacity:

- Who is requesting it? New users, power users, churned users?
- What outcome do we expect to move if we ship it? Activation? Retention? Referral rate?
- What's our best estimate of magnitude? Even a rough range matters.
- Have we tested a proxy (e.g. share via copy-link) that tells us whether people would actually use this?

### 2. "Re-engagement is flat" — flat relative to what?

Push notifications as a re-engagement lever is a reasonable hypothesis. But "flat" is not a problem statement — it's a symptom description. Before committing 30% of a quarter to this:

- What's the re-engagement metric, and what's its current value vs. target?
- Do we have evidence that push notifications specifically move it? Or are we guessing at the mechanism?
- What's the expected lift, and over what timeframe?
- Have we ruled out that the re-engagement problem is upstream — e.g. the product isn't worth returning to — making notifications a workaround rather than a solution?

Push notifications done wrong are also a churn accelerant. That risk isn't mentioned.

### 3. "The funnel is leaky" at 10% allocation is probably not worth doing

If the onboarding funnel is leaky enough to be on the roadmap, it deserves to be treated seriously. A 10% slice is enough to produce a half-finished rewrite that's worse than the original, not enough to move the funnel meaningfully, and not enough to learn anything useful.

Either:
- The funnel data shows a specific, addressable drop-off that can be fixed with a focused intervention (not a "rewrite") — in which case scope it as that, not a rewrite
- Or the rewrite is genuinely needed, in which case 10% is an honesty problem disguised as prioritisation

"Onboarding rewrite" as a solution framing is also a red flag — it's a solution, not a problem. What's the funnel drop-off? Where? By how much? What's the hypothesis for why it's happening?

### 4. No measurable success criteria for any theme

None of the three items has a target metric. This means:
- We can't tell at the end of the quarter whether the quarter worked
- We can't make a scope decision mid-quarter based on whether we're on track
- We can't run a post-launch impact review in any useful sense

For each theme, what does "success" look like in a number? Not a vague direction ("improve re-engagement") — a specific, time-bounded, measurable target.

### 5. No confidence calibration

The plan presents all three themes with the same implied confidence level. They almost certainly aren't. Push notifications as a re-engagement mechanism is an industry-tested hypothesis with a track record. Shareable shortlist driving referral/viral growth is less certain and depends heavily on the product category. Onboarding rewrite delivering funnel improvement is a high-variance bet — rewrites often don't move the funnel because the funnel problem is usually UX or value proposition, not copy.

Making the confidence levels explicit would change how you size the bets and how much validation you'd want before committing to a full build.

### 6. Appetite is unset

What does "60/30/10" mean in practice? Is this engineer-weeks? Team-weeks? The allocation is proportional but there's no absolute number. That matters for:
- Setting a circuit-breaker (what happens if shareable shortlist runs over?)
- Understanding whether 10% of onboarding is two engineer-days or two engineer-weeks — because those produce very different scopes

---

## What I'd want before approving

1. One paragraph per theme that names: the specific customer problem, the metric we expect to move, the target value, and the evidence confidence level (not just "requests" — actual data or experiment results).
2. An explicit appetite per theme in real units (engineer-weeks), not just proportions.
3. Either reframe "onboarding rewrite" as a specific, scoped intervention tied to a measured drop-off point, or give it enough capacity to actually complete — not 10%.
4. For push notifications: confirm we have a hypothesis for *why* re-engagement is flat and that notifications address the actual cause.
5. Measurable success criteria for the quarter — what does a good quarter look like in numbers we can check in 90 days?

---

## Bottom line

The themes aren't wrong. The work to justify them hasn't been done. Approving this as written means committing team capacity to three bets with undefined expected value, no measurable targets, and no way to declare the quarter a success or failure with any precision. That's a feature factory quarter dressed up as a roadmap.
