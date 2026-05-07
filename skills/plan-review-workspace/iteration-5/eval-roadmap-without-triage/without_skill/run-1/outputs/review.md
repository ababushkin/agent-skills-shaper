# Plan Review: Next-Quarter Roadmap

## Summary verdict

Not ready to approve. The framing is directional but the three themes lack the specification needed to commit to them responsibly. The rationale for each is a symptom, not a validated problem statement, and the allocation percentages are asserted rather than derived. Below is a breakdown of what's missing and what should happen before approval.

---

## Theme-by-theme assessment

### Shareable shortlist (60%)

**Stated rationale:** "we keep getting requests"

This is a demand signal, not a validated problem. Request volume is a starting point, not a prioritisation argument. Before committing 60% of a quarter to this:

- Who is requesting it? New users, power users, a handful of vocal accounts? The answer changes what "shareable" should mean.
- What outcome does shipping it move? Retention? Acquisition? Referral rate? Without a target metric, there's no way to know whether the bet paid off.
- What's the simplest version that tests the hypothesis? Sixty percent of a quarter is a large appetite for something justified by unquantified inbound.

The "highest priority" designation appears to flow from request frequency, which is a common and expensive mistake. Popular ≠ high-impact.

### Push notifications (30%)

**Stated rationale:** "re-engagement is flat"

This is closer to a metric observation, which is better. But "flat" is not a diagnosis. Push notifications are one of many levers for re-engagement, and they carry significant risk of accelerating churn if mis-calibrated. Missing here:

- What is the baseline re-engagement rate, and what's the target?
- Has the team ruled out that re-engagement is flat because the core product isn't delivering enough value to return to? Notifications layered on top of a weak value proposition produce unsubscribes and negative sentiment, not re-engagement.
- What's the hypothesis about which user segment, which trigger, and which message cadence would move the metric? "Push notifications" is a solution. "Users who complete onboarding but don't return within 7 days" is a problem.

### Onboarding rewrite (10%)

**Stated rationale:** "the funnel is leaky"

This is the most concrete diagnostic of the three, and the allocation is the smallest. That's backwards if it's true. A leaky funnel means every user acquired at the top is being lost at a known, fixable point. The expected value of fixing this typically outweighs re-engagement or virality work — new users who convert properly become the audience for both notifications and sharing.

Questions:
- Where specifically does the funnel leak? Drop at step 1, step 3, day 7? This should be known before sizing the work.
- Is 10% of a quarter enough to fix the leak, or is it enough to start a rewrite that won't ship until Q3?
- A "rewrite" is a solution. The problem might be solvable with a much smaller intervention once the drop-off point is identified.

---

## Structural concerns

**The allocation percentages are outputs, not inputs.** Sixty/thirty/ten is presented as a given, but there's no visible reasoning about why the problem with the highest evidence weight (funnel leakage, which has a metric) gets the smallest slice. The allocation appears to reflect stakeholder pressure or gut feel rather than expected impact × confidence.

**None of the three items have a measurable success criterion.** After the quarter ends, how will the team know whether any of these bets paid off? Without a specific metric target per theme, the post-quarter review will produce a features-shipped count, not a learning.

**No sequencing rationale.** Onboarding quality directly affects the audience size and quality for both sharing and re-engagement. A case can be made that onboarding should come first (or be much larger), not last. That case should be made explicitly and either accepted or rejected with reasoning.

**No mention of capacity constraints, cross-team dependencies, or risks.** Three themes in one quarter is achievable only if the team has headroom for all three. If push notifications require platform work, or onboarding rewrite requires design, those dependencies should be surfaced before the plan is locked.

---

## What should happen before approval

1. For each theme, write one sentence in the form: "We believe [problem] is causing [metric] to underperform. If we solve it, we expect [metric] to move by [target] within [timeframe]." If any of the three can't be written this way, that theme isn't ready.

2. Confirm the funnel drop-off point for onboarding with data before deciding whether a rewrite is warranted or whether a targeted fix would do.

3. Revisit the 60/30/10 split after step 1. If onboarding leak is the highest-confidence, highest-impact problem, it should not get 10%.

4. Define a time budget (appetite) per theme, not just a percentage — "30% of the quarter" is ambiguous about team size and scope.

5. Name the metric that will be checked at the end of the quarter for each theme. This is the only thing that separates a bet from a feature factory.

---

## Bottom line

The plan has the right instinct — three focused themes is better than ten scattered ones — but the rationale for each is a sentence of symptoms, not a validated problem statement with a measurable target. Approve the direction; don't approve the plan until the three questions per theme above are answered.
