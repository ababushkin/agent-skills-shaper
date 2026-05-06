# Roadmap Plan Review

**Recommendation: Do not approve as-is.** The plan has a defensible shape but is missing the substance that would make approval meaningful. Several gaps are serious enough that approving now would lock in decisions on weak evidence.

---

## What's good

- Three themes is a sensible number — focus over fragmentation.
- Explicit capacity allocation (60/30/10) is better than implicit allocation.
- Each theme is tied to a stated rationale (requests, flat re-engagement, leaky funnel).

## What's missing or wrong

### 1. The themes are framed as solutions, not problems
- "Shareable shortlist" is a feature.
- "Push notifications" is a channel/mechanism.
- "Onboarding rewrite" is a scope of work.

None of these is framed as "the customer problem we're solving and the outcome we expect to move." Without that framing, the team will optimise for shipping the thing, not for moving the metric. Reframe each as: *for [segment], we believe [problem] is causing [outcome]; if we solve it, [metric] should move by [target]*.

### 2. The evidence behind prioritisation is thin
- "We keep getting requests" — from whom, how many, are they your ICP, do they correlate with retention or revenue, or are they the loudest 5% of users? Request volume is one of the weakest prioritisation signals available.
- "Re-engagement is flat" — flat at what level? Is push the right intervention, or is the problem upstream (the product isn't sticky enough to be worth re-engaging)? Push notifications can mask a retention problem rather than fix it, and they often hurt long-term engagement when used as a band-aid.
- "Funnel is leaky" — where? A "rewrite" is the most expensive possible response to a leaky funnel. Have you instrumented which step leaks? Have you tried smaller fixes first?

### 3. The 60/30/10 allocation isn't justified
Why is shortlist 60 and not 40? Why is onboarding only 10 if the funnel is leaky enough to warrant a rewrite? The numbers feel reverse-engineered from a prior conclusion rather than derived from impact × confidence × effort.

### 4. "Highest priority because we keep getting requests" is the classic build-trap signal
Customer request volume is not the same as customer value, and definitely not the same as business value. The Kano dimension matters too: is the shortlist a delighter, a must-be, or an indifferent? Without that, "they asked for it" can drive you to build something users say they want but don't actually use.

### 5. No appetite, no success criteria, no kill conditions
- How long is each theme allowed to run before you re-evaluate?
- What metric tells you the shortlist worked? (Shares per user? Activation lift? Viral coefficient?)
- Under what evidence would you kill push notifications mid-quarter?
- What does "done" look like for the onboarding rewrite — shipped, or activation-rate moved by X%?

### 6. The onboarding "rewrite" is a one-way door dressed as a theme
Rewrites of user-facing onboarding are high-blast-radius: you affect every new user, you can't easily A/B against the old version once it's gone, and reverting is expensive. A 10% allocation to a rewrite is also a contradiction — rewrites rarely fit in 10% of capacity, so either the scope is wrong or the allocation is wrong.

### 7. No mention of capacity, dependencies, or KTLO
- What % is reserved for bugs, compliance, on-call, platform work?
- Do any of these themes depend on platform capabilities, third-party services (push providers), or other teams?
- Is the 100% allocation across just these three themes, or 100% of "new product capacity"?

### 8. No validation slots
At least two of these themes (push, shortlist) are low-confidence enough to warrant a validation step before a build commitment. Smoke-test the shortlist via a manual share flow; A/B push notification copy on a small cohort. Build slots for low-confidence ideas waste capacity.

---

## What I'd want to see before approving

1. Each theme rewritten as a problem statement with a target metric and target movement.
2. Evidence summary for each theme — what data, what confidence level, what's still unknown.
3. Appetite (time budget) per theme.
4. Kill conditions — what evidence would cause you to stop.
5. Capacity model that includes KTLO and validation slots, not just three feature buckets.
6. For the onboarding rewrite specifically: a decision on whether this is a rewrite or an instrumented sequence of targeted fixes. Default should be the latter.
7. A note on cross-team and platform dependencies.

## Bottom line

Don't approve. The plan is the right shape but not yet the right content. A 30-minute reshape on the items above will produce a plan worth committing to; approving the current version commits a quarter of capacity to under-specified bets.
