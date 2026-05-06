# Plan review — next-quarter roadmap (three themes)

## Assessment

The plan as presented is a **theme list with allocations**, not a roadmap. It names three areas of work (shareable shortlist, push notifications, onboarding rewrite), assigns capacity percentages (60/30/10), and offers a one-line rationale per theme. That is the start of a planning conversation, not the end of one. I would not approve it in this form.

What's there:
- Three named work areas
- An explicit capacity split (good — most plans skip this)
- A gestural rationale for each (requests, flat re-engagement, leaky funnel)

What's missing — and the gaps are load-bearing:

1. **No problems, just solutions.** Every theme is named as a feature ("shareable shortlist," "push notifications," "onboarding rewrite"). None is framed as a customer problem with an outcome to move. "We keep getting requests" is not a problem statement — it's volume. Requests for what, from whom, solving what underlying job? "Re-engagement is flat" names a metric symptom but not the customer behaviour we want to change or why push specifically is the right lever. "Funnel is leaky" doesn't say which step, for which segment, with what magnitude.
2. **No outcome metrics or targets.** What does success look like at end of quarter? "Shareable shortlist shipped" is not an outcome. "X% of new users send a shortlist within 7 days, lifting D7 retention by Y points" is.
3. **No confidence calibration.** "Highest priority because we keep getting requests" is opinion-grade evidence (Confidence Meter ~0.5 — anecdotal). Have we sized the segment asking? Run a smoke test? Looked at usage of any existing share-adjacent surface? Without this, 60% of capacity is being committed on vibes.
4. **No alternatives considered.** Push notifications are *one* re-engagement lever among many (email, in-product, lifecycle triggers, content recommendations, fixing the cause of disengagement upstream). The plan jumps to the channel without arguing why it beats the alternatives.
5. **No appetite per theme.** 60% of a quarter is a lot of capacity to allocate to a problem we haven't sized. What's the time budget for each theme? When does the circuit breaker trip?
6. **No dependencies, risks, or operability considerations.** Push notifications in particular carry platform (APNs/FCM), permission-prompt UX, deliverability, and frequency-capping concerns. None mentioned.
7. **Allocation logic is unjustified.** Why 60/30/10? Why is shortlist 6× the capacity of onboarding when "leaky funnel" sounds like a higher-impact business problem? The numbers feel back-derived from a preferred answer.

## Concerns

**Highest concern — solution-shaped roadmap.** Three of three items are framed as features. This is the build-trap pattern: the team is being handed answers before the questions are agreed. Once "shareable shortlist" is on the roadmap, every conversation becomes about scoping the share feature, not about whether sharing is the right intervention for the underlying problem (whatever that is).

**Confidence is undocumented and probably low.** "We keep getting requests" is the weakest form of evidence. Volume of requests correlates poorly with willingness to use, much less with outcome impact. Onboarding rewrite at 10% smells like "we know it matters but we don't want to face it" — under-investment in the highest-leverage funnel work is a classic anti-pattern.

**Push notifications has a customer-trust cost the plan doesn't price in.** Permission prompts, opt-out rates, OS-level throttling, and reputational damage from poorly-targeted pushes are real. A push programme without a clear segmentation and frequency model usually moves the metric for two weeks and then degrades engagement net-net.

**No theme has a kill criterion.** What evidence at week 3 / week 6 would cause us to stop work on any of these? Without that, the plan implicitly commits to shipping all three regardless of what we learn.

**Strategic context is absent.** Which company-level priority does each theme serve? If we can't say, the roadmap is a grab-bag.

## Recommendation

**Do not approve as-is. Send back for re-shaping.** This is a healthy "no" — the plan isn't bad, it's premature.

Specific asks before re-review:

1. **Re-frame each theme as a problem statement** in the form: "For [segment], we believe [problem] is causing [negative outcome]. If we solve it, we expect [metric] to move by [target] within [timeframe]."
2. **Attach an ICE-style confidence score** to each, with the evidence cited. If shortlist confidence is opinion-only (0.5 or below), it earns a *validation slot*, not a 60% build slot — a time-boxed discovery effort to raise confidence before we commit capacity.
3. **List one or two alternatives per theme** and say in writing why the chosen approach beats them. Especially for push notifications.
4. **Set an appetite per theme** (Shape Up style). E.g., "shortlist: 6 weeks, two engineers; if we can't ship a shaped solution in that, we cut scope or kill — we don't extend."
5. **Justify the 60/30/10 split** against expected impact × confidence × ease, not preference. I'd expect a leaky funnel to fight hard for more than 10%.
6. **Name kill criteria** — what would we have to see by mid-quarter to stop each theme.
7. **Connect each theme to a stated strategic priority.** If you can't, the theme has to either earn its way back via evidence or come off the list.

If, after this rework, the plan still lands at 60/30/10 with the same three themes, fine — but it'll land there with reasoning we can defend, kill criteria we can act on, and outcomes we can measure. That's a roadmap. What's currently on the table is a wishlist with percentages.

**Decision: not approved. Returned for re-shaping along the seven points above.**
