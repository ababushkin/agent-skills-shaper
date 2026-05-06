# Plan review: next-quarter roadmap (3 themes, 60/30/10)

**Recommendation: Do not approve as written.** The plan has the right ingredients but is reasoning at the wrong level — it is a list of solutions with a capacity split, not a roadmap of bets. Below are the gaps to close before this is approvable.

---

## 1. The themes are solutions, not problems

Each item is named as a thing-to-build:

- "Shareable shortlist"
- "Push notifications"
- "Onboarding rewrite"

That's solution language. The roadmap should name the **problem** and the **outcome** we expect to move. Re-frame each one:

- *Shareable shortlist* → "Users who curate a shortlist have no way to share it; we believe this is suppressing viral acquisition / collaborative use." Outcome: shortlist-driven invites per active curator.
- *Push notifications* → "Re-engagement is flat at X%; we believe absence of a re-engagement surface is a primary cause." Outcome: D7/D30 return rate.
- *Onboarding rewrite* → "Funnel drops Y% between step A and step B; we believe step structure is the cause." Outcome: activation rate (named step) within N days.

If you can't write each item in that "problem → expected outcome → metric" form, you don't understand the bet well enough to commit a quarter to it.

## 2. The justifications are weak in different ways — and that matters

Each theme's stated rationale fails a different test:

| Theme | Stated reason | Problem with the reasoning |
|---|---|---|
| Shareable shortlist | "We keep getting requests" | Request volume is anecdotal demand, not validated impact. Who is asking — power users, churned users, sales? How many requests, vs. how many users? Cagan's warning about feature-request roadmaps applies directly. |
| Push notifications | "Re-engagement is flat" | Diagnosis ≠ prescription. Push is **one** intervention against flat re-engagement. Email, in-app, lifecycle content, fixing the underlying retention reason are others. Why push? |
| Onboarding rewrite | "The funnel is leaky" | "Rewrite" is the largest, most expensive, highest-blast-radius response to a leaky funnel. Where in the funnel is the leak? Have you tried the smallest interventions first? |

Each of these would fail a basic ICE pass: high stated impact, low or unstated confidence, and unspecified ease.

## 3. The 60/30/10 split is unjustified

Three numbers without inputs is a vibe, not an allocation. Questions the split should answer but doesn't:

- Why 60 to shortlist? Is shortlist work scoped to consume 60% of a quarter, or is 60% of capacity the appetite cap?
- Is 10% on onboarding rewrite plausible, given the word "rewrite"? Rewrites are notoriously underestimated; 10% suggests either it's not a rewrite or it won't actually ship.
- Where is KTLO, on-call, security work, platform work, validation/discovery? A roadmap that allocates 100% to feature themes is implicitly claiming zero other obligations exist. That is never true.
- What's the team size and shape? 60/30/10 across one team of six is a different statement than across three squads.

## 4. Missing: confidence levels on each bet

For each theme, what is the evidence the proposed work will move the named metric? Possible levels:

- Anecdote / requests (low)
- Quantitative observation of the gap (medium)
- Prior experiment, comparable benchmark, prototype validation (higher)
- Live A/B test or smoke test (highest)

If shortlist is sitting on "users keep asking," that's the lowest tier. Push and onboarding sound like they have the gap quantified but no validation that the proposed solution closes it.

Low-confidence items should consume **validation slots** (a spike, a prototype, a smoke test), not full build slots.

## 5. Missing: appetite / time budget per theme

There's no statement of how much time each theme is allowed to consume before re-evaluation. "60% of capacity" is an allocation, not an appetite. A theme without an appetite expands until the quarter ends.

Set, for each theme: appetite in weeks, what we ship if we hit it, what we cut if we don't, what triggers a kill.

## 6. Missing: customer value × business viability

For each theme, articulate both:

- **Customer value** — whose life gets better, by how much, in what way
- **Business viability** — what does this do for revenue, retention, acquisition cost, brand, defensibility

Onboarding rewrite is plausibly both. Shareable shortlist is plausibly viral-acquisition-driven business value, but only if the *shareable* part actually drives shares — which is a behavioural assumption that hasn't been tested. Push notifications has an obvious business case (retention) but a real customer-value risk: poorly-shaped push is a churn driver, not a retention tool.

## 7. Missing: what's being said "no" to

A roadmap is defined as much by what's excluded as what's included. What candidate work is being deferred to make room for these three themes? If the answer is "nothing, this is what we had capacity for," then the prioritisation hasn't actually happened — you've just labelled the existing plan.

## 8. Missing: dependencies and one-way doors

- **Push notifications** is partly a one-way door: opt-in prompts can only be asked once on most platforms; bad first ask burns the channel permanently. Has the prompt strategy been designed?
- **Push** also requires platform infra (APNs/FCM, notification service, preference centre, analytics). Is that built? If not, the 30% allocation is wrong.
- **Onboarding rewrite** likely touches auth, user model, analytics events. Cross-team dependencies?
- **Shareable shortlist** touches permissions, public URLs, possibly auth, possibly SEO. Privacy review needed?

## 9. Missing: how we'll know if it worked

For each theme, name:

- The single primary metric
- Acceptable secondary metrics
- Guardrail metrics that, if they regress, mean we roll back regardless of the primary
- The observation window (how long after launch we judge)

Without this, "done" defaults to "shipped" — which is the build-trap definition.

## 10. Sequencing is missing

Three themes in parallel at 60/30/10 implies all three start at the start of the quarter. Is that correct, or should one go first and inform the others? In particular: if onboarding fixes activation, does that change what shortlist or push need to do? Order matters.

---

## What approval would need

Before I'd approve, I'd want:

1. Each theme rewritten as **problem + customer + outcome metric + target**.
2. **Confidence level** stated for each, with the evidence behind it.
3. **Appetite** (in weeks) per theme, with what gets cut if it overruns.
4. **Capacity reality check**: where is KTLO, validation, on-call, platform work? Is 60/30/10 of *feature* capacity, or of *all* capacity?
5. **Smallest-thing-first analysis** for each theme — especially "onboarding rewrite," where the word "rewrite" is doing too much heavy lifting.
6. **Validation work surfaced** for the lowest-confidence theme (likely shortlist): a spike, prototype, or smoke test before the build commitment.
7. **One-way-door call-out** for push notifications: the prompt strategy is its own design problem.
8. **Explicit "no" list** — what's being deferred, and what evidence would bring it back.
9. **Definition of done** per theme, including the metric observation, not just ship date.
10. **Dependencies identified** and confirmed with owning teams in writing.

## Bottom line

The instinct behind the three themes may well be right. The plan as stated doesn't show the work to support that. Approving it as-is would lock the team into three builds where two of them (push, onboarding rewrite) are over-scoped responses to under-diagnosed problems and one (shortlist) is being driven by request volume rather than evidence of impact.

Send back for re-shaping along the lines above.
