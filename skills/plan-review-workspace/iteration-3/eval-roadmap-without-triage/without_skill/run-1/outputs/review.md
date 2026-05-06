# Plan review: next-quarter roadmap (3 themes, 60/30/10)

## TL;DR

**Recommendation: REVISE before approving.**

The plan has the right shape (small number of themes, explicit allocation, named rationales) but each theme is currently a *solution label* with anecdotal justification rather than a problem with a measurable outcome and an evidence-backed bet. Approving as-is risks committing 90% of next quarter's capacity to two themes whose underlying problem framing has not been validated. Tighten the framing, attach metrics and confidence levels, then approve.

---

## What's good

- Three themes is the right order of magnitude — focus over fragmentation.
- Allocation is explicit (60/30/10) rather than implicit "we'll see what fits."
- Each theme has a named *reason*, not just a name.
- The 10% slot for onboarding suggests you already sense the lower confidence on that one — good instinct.

---

## What's missing or wrong

### 1. Themes are framed as solutions, not problems

All three items are written as features ("shareable shortlist," "push notifications," "onboarding rewrite"). The roadmap should hold *problems* tightly and *solutions* loosely. Right now the team has been handed three pre-decided solutions, which closes off the better solutions they might have found.

Re-frame each as: "For [segment], [problem] is causing [negative outcome]. If we solve it, we expect [metric] to move by [target] within [window]."

- "Shareable shortlist" → what is the customer trying to do that they can't? Share a curated list with a friend? Collaborate? Save for later? "We keep getting requests" doesn't tell you which of these.
- "Push notifications" → the *outcome* is re-engagement. Push is one of many possible interventions (email, in-app prompts, content recommendation, onboarding-to-habit loop). Naming the channel locks you in.
- "Onboarding rewrite" → "the funnel is leaky" is a symptom, not a problem. Where in the funnel? Which step? For which segment? A rewrite is an enormous appetite for an undiagnosed issue.

### 2. No measurable success criteria

None of the three themes has a target metric. "Re-engagement is flat" and "the funnel is leaky" are observations, not goals. Before approval, each theme needs:
- The specific metric (e.g. D7 retention, signup-to-activation conversion, shares-per-active-user)
- The current baseline
- The target movement and the window

Without these, you cannot tell at end-of-quarter whether the bet paid off — which means you also can't learn from it.

### 3. Confidence is unstated and probably uneven

Using a rough confidence scale (Gilad-style, 0.1 = opinion, 0.5 = anecdotal, 2-3 = survey/analytics, 5+ = experimental evidence):

- **Shareable shortlist — confidence ~0.5.** "We keep getting requests" is anecdotal. How many requests? From which segment? Are they your highest-value users or your loudest? Is the feature they're describing actually the same thing, or are you bucketing 4 different requests into one label? Allocating 60% of the quarter's capacity to a 0.5-confidence bet is the highest-risk move in the plan.
- **Push notifications — confidence ~0.5–1.** "Re-engagement is flat" is a real metric observation, but the *causal link* between "push notifications exist" and "re-engagement improves" is the unverified bet. Plenty of products have shipped push and seen no re-engagement lift.
- **Onboarding rewrite — confidence depends on whether you have funnel data.** If you have step-by-step drop-off data with a clear cliff, this could be 2–3. If "leaky funnel" is a vibe, it's 0.5.

The 60/30/10 allocation implies the highest-confidence bet should get the most capacity. Right now the highest-allocated bet (shortlist) appears to be the lowest-confidence one. That inversion is a red flag.

### 4. No triage / discovery work named

For low-confidence items, the right move is not a build slot — it's a *validation slot*. A two-week discovery effort on the shortlist (interview the people requesting it, prototype two variants, look at usage of any existing share-adjacent flows) could turn 0.5 into 3 before you commit 60% of the quarter. The current plan skips discovery and goes straight to build.

### 5. No business-value framing

For each theme, what's the business outcome? Revenue, retention, virality, reduced support cost, defensibility? "Customers ask for it" is a customer-value signal but not a business-value one. A roadmap item should clear both bars.

### 6. No appetite, no kill criteria, no dependencies

- What is the time budget for each theme? "Next quarter" implies 12 weeks but the 60/30/10 split needs to translate into actual weeks per theme.
- What would cause you to kill a theme mid-flight? E.g., "if shareable shortlist v1 doesn't lift shares-per-user by 15% in two weeks of canary, we stop and reshape."
- What cross-team dependencies (mobile platform teams for push, design for onboarding, infra for sharing/permissions)? These need surfacing now, not in week 4.

### 7. The problem space is "complex," not "complicated"

Two of the three themes (re-engagement, activation/onboarding) live in the part of the product where cause-and-effect is genuinely emergent — you can't reason your way to the right answer; you have to probe, sense, respond. That argues for treating these as *experiments with discovery slots*, not as *builds with locked appetites*.

---

## Falsifying conditions (what would change the verdict?)

I'd reverse to APPROVE if any of these hold and you can show evidence:
- **Shortlist:** you have a written tally of >50 distinct requests, segmented, showing the same underlying job-to-be-done; OR a prior smoke test (e.g., a "share" button stub that measured intent).
- **Push:** you have prior evidence that your specific re-engagement problem is *notification-shaped* (e.g., users who do return cite "I forgot about it" rather than "I didn't find it valuable").
- **Onboarding:** you have funnel analytics showing a clear drop-off step and a hypothesis about the cause, not just an aggregate completion rate.

If none of these are in hand, the right move is:
1. Run formal triage on the three themes (problem framing, ICE/confidence scoring, kill criteria).
2. Convert at least the shortlist (and probably push) into time-boxed *discovery* slots for the first ~2-3 weeks of the quarter.
3. Re-allocate after discovery — the 60/30/10 split should be earned, not declared.

---

## Suggested next step

Don't approve yet. Ask the proposer for:
- A one-page brief per theme: problem statement, target customer, current evidence, proposed metric, baseline, target, appetite, kill criteria, top-3 risks.
- A confidence score per theme with the reasoning.
- A discovery plan for any theme below confidence ~2.

Then re-review. If those land cleanly, this becomes an easy approve.
