# Plan review: next-quarter roadmap (3 themes, 60/30/10)

**Recommendation: Do not approve as written.** The plan has the right shape (themes + allocation) but is missing the substance that makes a roadmap defensible. Below: what's missing, what's risky, and what to fix before the next pass.

---

## 1. Items are framed as solutions, not problems

Each of the three themes is named as a feature/output, not as a customer problem with a target outcome:

- "Shareable shortlist" — what user problem does this solve? Who is the user? What behaviour shifts when they get it?
- "Push notifications" — push is a *mechanism*, not a problem. The stated rationale ("re-engagement is flat") is a metric, not a hypothesis about why.
- "Onboarding rewrite" — "rewrite" pre-commits to a solution. The problem ("funnel is leaky") doesn't tell us *where* it leaks or *why*.

**Fix:** rewrite each item as: *"For [segment], we believe [problem] is causing [outcome]. If we solve it, we expect [metric] to move by [target] within [window]."* If you can't write that sentence, the item isn't ready to commit to.

## 2. No success metrics, no targets, no baselines

There is not a single number anywhere in the plan. "Highest priority because we keep getting requests" is volume-of-noise, not evidence of impact. "Re-engagement is flat" — flat at what? "Funnel is leaky" — leaking how much, where?

**Fix:** for each theme, name (a) the current baseline, (b) the target movement, (c) the measurement window, (d) how you'll attribute the change to this work.

## 3. Evidence is thin and asymmetric

- "Shareable shortlist" rests on inbound request volume. Request count is one of the weakest evidence types — vocal users are not representative, and "asked for it" is not the same as "would use it" or "would pay for it."
- "Push notifications" — no evidence the *channel* is the problem. Re-engagement could be flat because the product gives users no reason to come back, in which case push will train users to ignore notifications and possibly increase uninstalls.
- "Onboarding rewrite" — no analysis of *where* the funnel leaks. A rewrite is the most expensive possible response; targeted fixes at the leakiest step are usually 10x cheaper for similar effect.

**Fix:** before committing build slots, score each item on confidence (opinion / anecdote / data / experiment). Low-confidence items get a *validation* slot, not a build slot.

## 4. The 60/30/10 allocation is unjustified

Why 60/30/10 and not 50/30/20 or 40/40/20? The split appears to be derived from gut, not from cost-of-delay, expected impact, or strategic theme balance. Specifically:

- 60% to the lowest-evidence item (request volume only) is backwards from what the evidence supports
- 10% to onboarding when "the funnel is leaky" suggests the highest-leverage early-stage problem is the under-funded one — leaky funnels compound against everything else
- No mention of capacity reserved for KTLO, validation, or unexpected work — implies 100% of capacity is going to these three themes, which is never true in practice

**Fix:** justify the split against expected impact × confidence × cost-of-delay. Reserve explicit % for KTLO and validation.

## 5. One-way doors are not surfaced

- Push notifications: requires platform permissions, has reputational cost if misused (uninstalls are largely irreversible), creates ongoing operational load (delivery, opt-out, compliance)
- Onboarding rewrite: typically a long-tail commitment — partial rewrites strand users mid-flow, full rewrites take longer than estimated and break instrumentation continuity (you lose trend comparability)
- Shareable shortlist: depends on what "shareable" means — public URLs? auth model? privacy posture? Each is a one-way door if implemented carelessly

**Fix:** for each item, name the irreversible decisions and how you'll de-risk them before committing.

## 6. No appetite (time budget) per item

"Allocated 60/30/10" is a capacity split, not an appetite. Each item also needs: how many weeks is this worth? What's the circuit breaker if it overruns? What does "ship what we have" look like at the time-box?

## 7. No discussion of what is NOT on the roadmap

A roadmap is defined as much by the explicit "no" as the "yes." What got rejected this cycle? What's the opportunity cost of these three themes vs. the next three? Without this, the plan reads as "the loudest three things" rather than a deliberate portfolio choice.

## 8. Strategic context is absent

What is the company / product trying to achieve this year? Which of these themes ladders to that? "Re-engagement is flat" is a symptom — what's the strategic theory about why? If there isn't one, the roadmap is a reaction to symptoms, not a plan to move the business.

## 9. Risks specific to each theme

- **Shareable shortlist** — be very careful about whether "shareable" has been validated as a behaviour vs. just requested as a feature. Sharing features have a notoriously high gap between "requested" and "actually used."
- **Push notifications** — the highest-risk item operationally. Without a clear behavioural model (what triggers, what message, what action), this becomes spam. Recommend prototype-and-test before commit.
- **Onboarding rewrite** — the word "rewrite" should always trigger pushback. Rewrites preserve the problems of the original and add new ones. Funnel-by-step diagnosis first, surgical fixes second, rewrite only as a last resort.

## 10. What I'd want to see before approving

1. Each item rewritten as a problem statement with target metric, baseline, and confidence score
2. Evidence supporting each theme (not just request count or anecdote)
3. Justification for the 60/30/10 split against impact × confidence
4. Explicit KTLO / validation / discovery capacity reserved
5. Appetite per item with circuit-breaker rule
6. The "what we said no to" list
7. For onboarding: funnel diagnostic data showing where it actually leaks before committing to "rewrite"
8. For push: a smaller validation slot to test the re-engagement hypothesis before committing to a build slot

---

**Bottom line:** the shape is right (three themes, explicit allocation), but the contents are output-framed, evidence-light, and pre-committed to solutions. Approving as-is risks burning a quarter on the loudest requests rather than the highest-impact problems. Send back for a problem-framed rewrite with metrics, evidence scoring, and explicit trade-off justification.
