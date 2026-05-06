# Plan review: next-quarter roadmap (three themes, 60/30/10 split)

## TL;DR

Do not approve as-is. The plan has the shape of a roadmap but is missing the substance that makes a roadmap reviewable: problems, outcomes, evidence, and trade-offs. Each of the three themes is described as a solution, not a problem; the rationale for each is a one-liner that doesn't survive much scrutiny; and the 60/30/10 allocation appears to be asserted rather than derived. Send back for rework before approving.

---

## What the plan says, in one paragraph

Three themes for next quarter: a shareable shortlist (60%), push notifications (30%), onboarding rewrite (10%). Justifications offered: shortlist gets requests; re-engagement is flat; the funnel is leaky.

---

## What's good

- Only three themes — focus is real, not aspirational. Most quarter plans I see have seven things on them.
- The allocation is explicit (60/30/10) rather than implicit. Even if I disagree with the split, at least it's stated and arguable.
- Each theme connects to a plausible business concern (requests, re-engagement, funnel).

That's the end of the "good" list.

---

## What's missing or wrong

### 1. Each theme is a solution, not a problem

"Shareable shortlist," "push notifications," and "onboarding rewrite" are all solutions. The corresponding problems would be something like: "users can't share their picks with friends, which limits viral acquisition," "re-engagement of dormant users is below benchmark X," "new-user activation drops Y% between step 2 and step 3." Without that framing, the team has no freedom to find a better solution than the one you've already named, and no way to know whether the solution worked.

This matters most for "onboarding rewrite." A "rewrite" is a verb pointing at the artefact, not at the user. What part of onboarding is leaky? For which users? At which step? "Rewrite" could be a 2-week change or a 12-week change depending on the answer, and 10% capacity could be either far too much or nowhere near enough.

### 2. No outcome metrics or targets

For each theme I'd want to see:
- The metric this is meant to move
- The current baseline
- The target by end-of-quarter
- How we'll measure it

"Re-engagement is flat" is a statement, not a target. Is the goal to lift 30-day return rate by 5pp? 10pp? From what to what? Without a number, "done" is undefined and the team will declare victory on ship rather than on outcome.

### 3. The evidence behind each theme is thin

- **Shortlist — "we keep getting requests."** From whom? How many? Is it a vocal minority or a representative signal? Are the requesters the customer segment we want to grow, or the segment that's loudest? "Requests" is the lowest tier of evidence — closer to anecdote than data. Worth investigating, but not worth 60% of a quarter on that signal alone.
- **Push notifications — "re-engagement is flat."** Flat compared to what? Is the diagnosis that we need a new channel, or that the existing channel (email? in-app?) is poorly used? Push notifications are one possible lever for re-engagement; without a diagnosis they could easily be the wrong lever, and a poorly-tuned push strategy can actively hurt retention via uninstalls/notification-off.
- **Onboarding rewrite — "the funnel is leaky."** Where? Which step? Funnel data should exist; if it doesn't, the first piece of work isn't a rewrite, it's instrumentation. If it does, the plan should cite the specific drop-off.

The pattern: each justification is plausible but unverified. That's an idea-bank entry, not a roadmap commitment.

### 4. The 60/30/10 allocation is asserted, not derived

Why 60 to shortlist? Because it's "highest priority because we keep getting requests." But that's a claim about demand, not about expected impact × confidence. A reasonable alternative allocation would be:
- **Heavy on onboarding** if activation is the constraint on growth — fixing a leaky funnel often has higher leverage than any feature added downstream of it.
- **Heavy on push** if retention/re-engagement is the constraint and there's evidence push specifically (vs. lifecycle email, vs. in-app prompts) is the missing channel.
- **Heavy on shortlist** if it's a clear differentiator with viral mechanics that compound over time.

I can't tell from the plan which of these is true. "We keep getting requests" doesn't distinguish "this is a delighter that will compound" from "this is a vocal-minority feature that won't move the metric we care about."

A 60% allocation to a single theme is also a big bet on it. Big bets are fine, but they should be backed by the strongest evidence in the portfolio, not the weakest (and "requests" is the weakest of the three justifications offered here).

### 5. No mention of customer value AND business viability

Each theme could plausibly be either or both, but the plan doesn't say. Some specific gaps:

- **Shortlist** — what's the business case? Viral acquisition (new signups via shared shortlists)? Engagement uplift on the sharer side? Premium feature gating? Without a stated business hypothesis, we're building because customers asked, which is a customer-value-only roadmap and a known failure mode.
- **Push** — what does "re-engagement" mean for the business? DAU? Revenue? Retention curve shape? And what's the cost side (notification fatigue, opt-out rates, platform policy risk)?
- **Onboarding** — clearer business case (activation → LTV) but we still need the number.

### 6. No mention of what's NOT on the roadmap

Three themes is good focus, but a roadmap is also defined by its explicit "no"s. What did these three beat? What's getting deferred to later? What KTLO/maintenance/tech-debt capacity is reserved? A 100% feature roadmap with no reliability/platform allocation is a bet that nothing breaks next quarter, which is not a bet I'd take.

### 7. No appetites or shape

Is "shareable shortlist" a 4-week effort or a 12-week effort? Same for push and onboarding. Without an appetite per theme, the 60/30/10 allocation is meaningless — it's allocating an unspecified amount of capacity across themes of unspecified size. The team needs to know: how much time is each theme worth, and what's the shape of "shipped" for each?

### 8. No dependencies or risk surface

Push notifications in particular have meaningful dependencies — platform permissions, user opt-in flows, notification infrastructure (if not already in place), backend triggers, possibly app-store review implications. Onboarding rewrites typically touch growth analytics, A/B testing infrastructure, copy/translation, design systems. None of this is acknowledged. Surprises here are the most common cause of a quarterly plan slipping.

---

## Specific questions I'd want answered before approving

1. For each theme: what user problem, for which user segment, with what current metric value, targeting what new value, by when?
2. What's the strongest evidence we have for each theme's expected impact? (Not "we're hearing it" — actual data, experiments, comparable launches.)
3. What's the appetite (time budget) for each theme?
4. What did these three beat? What's the explicit deferred list?
5. What % of capacity is reserved for KTLO, reliability, and validation/discovery work? Is the 60/30/10 over 100% of capacity, or over the feature-work slice?
6. For push specifically: is the diagnosis that we need push, or that re-engagement is broken? If the latter, why is push the right lever vs. email/in-app/lifecycle?
7. For onboarding: where exactly is the funnel leaking? Do we have the instrumentation to know? If not, is the first chunk of that 10% actually instrumentation?
8. What does "done" look like for each theme — what shipped artefact, what observed outcome?
9. What are the cross-team dependencies (platform, infra, design, legal/policy for push)?
10. Are any of these one-way doors (e.g., push opt-in is ~one-way for many users)? How are we de-risking those?

---

## My recommendation

**Do not approve.** Send back with:

1. Reframe each theme as a problem-and-outcome statement, not a solution.
2. Attach a metric, baseline, and target to each.
3. Show the evidence behind each — and where the evidence is thin, the first chunk of work in that theme is validation, not build.
4. Justify the 60/30/10 allocation as a function of expected impact × confidence × ease, not "we keep getting requests."
5. Add the explicit deferred list and the KTLO/reliability reserve.
6. Add appetites per theme and surface cross-team dependencies.

If the team comes back with that and the picture still says 60/30/10 across these three themes, I'll happily approve. The current version is a slide, not a roadmap.

---

## One narrower take, if you want it

If I had to bet today, I'd flip the allocation: more weight on the leaky funnel, less on the shortlist. Reasoning:

- Activation problems compound — every user we lose at onboarding is a user we never get to re-engage or share-with.
- "Requests" is weaker evidence than "measured drop-off in our own funnel data."
- Push to fix flat re-engagement is mid-confidence; it's a plausible lever but not obviously the right one without diagnosis.

But this is a guess from the outside. The right answer is the one the team produces after doing the framing above.
