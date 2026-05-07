# Plan Review: Q-Next Roadmap

## Summary verdict

Not ready to approve. The allocation rationale is weak, the success criteria are absent, and two of the three items are driven by symptoms rather than diagnosed problems. This plan needs sharpening before it earns a commitment.

---

## What's good

- Three themes is a reasonable number. Focus is a real constraint and this respects it.
- The 60/30/10 split at least makes the priority order explicit. Most plans don't bother.
- All three areas are plausible places to invest — none is obviously wrong on its face.

---

## What's missing or weak

### 1. Rationale is anecdote, not evidence

Each theme is justified by a single sentence of feeling:

- "We keep getting requests" — for shareable shortlist
- "Re-engagement is flat" — for push notifications
- "The funnel is leaky" — for onboarding rewrite

These are prompts for investigation, not justifications for commitment. "We keep getting requests" tells me nothing about whether the requester's problem is the right one to solve, whether this solution is the right response, or how many users are affected. "The funnel is leaky" is true of almost every onboarding flow in existence — where exactly, how much, and what's causing it?

Before approving, I'd want to see: what does the data actually say? What's the measured drop-off? What did we learn from talking to users?

### 2. No success criteria on any of the three items

What does success look like at the end of the quarter? If we ship the shareable shortlist, how do we know it worked? If push notifications go out, what re-engagement rate would validate the bet?

Without this, the review at the end of the quarter will be "we shipped it" — which is not a review, it's a status update. You can't course-correct mid-quarter if you don't know what you're steering toward.

### 3. The onboarding rewrite is a solution, not a problem

"Onboarding rewrite" pre-commits to a large, expensive effort. The problem is "the funnel is leaky." Those are not the same thing. A full rewrite is one response; targeted copy changes, removing a step, a single UX fix at the highest drop-off point — all of these are also responses. The plan has jumped to solution before the problem is understood. A rewrite is particularly expensive to walk back if it turns out the real issue was something narrower.

### 4. The 60/30/10 allocation has no capacity model behind it

60/30/10 of what? How many engineers? What are the teams working on these? The shareable shortlist getting 60% sounds like a choice, but without knowing what 60% translates to in weeks of engineering work, it's an opinion, not a plan.

### 5. Push notifications as a re-engagement lever is a bet worth examining before committing

"Re-engagement is flat" may or may not be a push notification problem. It might be a content quality problem, a product-market fit problem, a notification fatigue problem, or something else entirely. Push notifications are a bet on the cause — but the cause isn't established. This doesn't mean the bet is wrong; it means the confidence level is low, and the plan should acknowledge that rather than presenting it as obvious.

---

## What I'd want before approving

1. For each theme: what specific metric are we trying to move, by how much, within what timeframe?
2. For shareable shortlist: what do the requests actually say? What are users trying to do that they can't do now?
3. For onboarding: where exactly does the funnel leak? What's the measured drop-off at each step?
4. For push notifications: what diagnosis says notifications are the right lever for flat re-engagement?
5. A rough capacity model: what does 60/30/10 actually mean in terms of team-weeks?
6. What is not on this roadmap that was considered and cut? A plan with no trade-offs visible has probably not made any.

---

## Bottom line

The themes are reasonable starting points. The plan as written is a list of directions, not a set of bets — it has no measurable outcomes, no evidence behind the prioritisation, and at least one item that has already leapt past problem definition into solution space. Tighten these up and it's approvable. As-is, approving it means committing a quarter of capacity to things we can't evaluate at the end.
