# Plan review: next-quarter-roadmap-three-themes

## Plan reference

Inline plan from owner:

> Shape next-quarter roadmap with three themes — shareable shortlist, push notifications, onboarding rewrite — allocated 60/30/10 across them. The shareable shortlist is highest priority because we keep getting requests. Push notifications because re-engagement is flat. Onboarding rewrite because the funnel is leaky. Approve?

## Trigger

Trigger 1 fires: owner explicitly asked "Review this plan before I approve it." Trigger 2 also fires: appetite is one quarter (≫1 day). Trigger 3 likely fires: roadmap shaping touches multiple product surfaces beyond any single piece of recently-traced code.

**Step 1a — Fast-track gate**: Did NOT fire. Precondition 1 fails — this is roadmap shaping, not KTLO/maintenance. Fall through to normal flow.

## Inputs

- **Appetite**: one quarter (~12 weeks) — but the appetite is per-theme-allocation, not per-outcome. Appetite is effectively unbounded inside each theme.
- **Cynefin domain**: **Complex**. Three themes (sharing behaviour, re-engagement, funnel) all sit in the emergent / behavioural-feedback space. Outcomes are not deterministically derivable from inputs; feedback loops are required.
- **Tier**: **Full** — selected because appetite >1 week AND ≥3 implicit dependencies (multiple product surfaces, likely cross-team) AND the allocation decision itself is a one-way door for the quarter (Universal P3).

## B1 — Problem framing

**Verdict: SUSTAINED.**

The plan opens with **themes** (solutions) and **rationales as one-line hand-waves** ("we keep getting requests", "re-engagement is flat", "the funnel is leaky") — not with problems framed per Product Rule A2 (customer segment, problem, negative outcome, target metric, expected delta).

- "Shareable shortlist" is a feature name, not a problem. "We keep getting requests" is anecdote, not a measured problem.
- "Re-engagement is flat" names a metric trend but no segment, no target delta, no hypothesis about cause.
- "Funnel is leaky" names a symptom, no specific stage, no cohort, no target conversion delta.

There is no measurable outcome attached to any theme. By Product Rule A3, no theme is ready for the roadmap.

**Falsifying condition**: Owner produces, for each theme, a Rule-A2 problem statement with a named target metric and target delta within 24 hours. If those exist already and were merely truncated in the prompt, B1 downgrades to PARTIAL.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| "Shareable shortlist" — no scope around what's shared, with whom, on what surfaces (web/iOS/Android/email), what permissions, what privacy review | SUSTAINED | A scope doc names target surfaces, sharing model (link/social/embed), and privacy/auth boundary before allocation is locked |
| "Push notifications" — no scope around platforms (iOS/Android/web push), opt-in flows, content rules, frequency caps, regulatory (GDPR/CAN-SPAM/Apple's notification permissions) | SUSTAINED | A scope doc names platforms, consent model, and frequency/cap policy |
| "Onboarding rewrite" — "rewrite" is the most scope-vague verb in product. New users only? Existing users re-onboarded? Mobile vs web? Which funnel stage? | SUSTAINED | Plan names the specific funnel stage (signup, activation, first-value), the cohort, and bounds the rewrite to either net-new or replacement |
| Allocation 60/30/10 — of what? Engineering FTE? Calendar weeks? Discovery + delivery combined? | SUSTAINED | Plan states the allocation unit explicitly (FTE-weeks vs calendar weeks vs budget) |
| No idea-triage record cited for any theme | SUSTAINED | A triage record exists per theme with confidence + ICE scores per Product Rules B2, B6 |
| No portfolio-theme classification (Doshi: differentiator / table-stakes / incremental / embarrassment / customer-special / tech-foundation / speculative) per Product Rule B3 | SUSTAINED | Each theme is classified into one of the seven portfolio themes |

Six SUSTAINED items on a quarter-long plan — well above the "zero hits = lenient review" threshold. This plan's scope is effectively undefined.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| "Users want a shareable shortlist" (because we keep getting requests) | **0.5** — anecdote (request count not given; bias: vocal minority) | Pull the actual request count + segment, or run a 5-min smoke test (paint-the-door link in nav + CTR) | SUSTAINED |
| "Push notifications will lift re-engagement" (because re-engagement is flat) | **0.1** — opinion: causal claim with zero supporting evidence cited; flat re-engagement could be content, timing, audience, or pricing | Owner names the specific re-engagement metric, the cohort, and one piece of evidence that push (vs in-app, vs email, vs content) is the right lever | SUSTAINED |
| "Onboarding rewrite will fix funnel leakage" (because the funnel is leaky) | **0.1** — opinion: no diagnostic cited; "leaky funnel" without stage attribution names a symptom not a cause | Pull funnel data: which stage drops? Is the leak in onboarding at all, or downstream (activation, week-2 retention)? | SUSTAINED |
| Implicit: "60/30/10 is the right allocation" | **0.1** — assertion with no derivation shown (not ICE-derived, not cost-of-delay-derived) | Owner shows the ICE × theme calculation that yields 60/30/10 (per Product Rule B2) | SUSTAINED |
| Implicit: "These three themes are the highest-value bets available next quarter" | **0.1** — opinion: no idea-bank comparison cited; what was rejected? | Owner cites the idea-bank shortlist and why these three displaced others (Product Rule A6) | SUSTAINED |

All five assumptions sit at Confidence ≤0.5. **None has Confidence ≥5.** Per the workflow, untested assumptions with Confidence <5 block APPROVE.

## B4 — Dependencies (Full only)

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Engineering capacity for three parallel themes at 60/30/10 | NO | NO | SUSTAINED |
| Design capacity (onboarding rewrite is design-heavy) | NO | NO | SUSTAINED |
| Mobile platform owners (push requires iOS + Android infra) | NO | NO | SUSTAINED |
| Privacy/legal review (sharing + push consent) | NO | NO | SUSTAINED |
| Analytics instrumentation for outcome metrics (B6) | NO | NO | SUSTAINED |
| Notification provider (FCM/APNs/SNS/OneSignal) | not named | not named | SUSTAINED |

Six unconfirmed dependencies on a quarter-long plan. Universal Rule B7 names cross-team dependencies as the single most common cause of missed commitments.

## B5 — Reversibility + ADR pairing (Full only)

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Quarter-long allocation 60/30/10 | NO — no other allocations considered | NO | SUSTAINED |
| Choosing "shortlist sharing" as the highest-priority bet (displaces other themes for the whole quarter) | NO | NO | SUSTAINED |
| Push notification platform choice (vendor lock-in if a specific provider is adopted) | NO | NO | SUSTAINED |
| Onboarding "rewrite" vs incremental optimisation (rewriting is much harder to roll back than tweaking) | NO | NO | SUSTAINED |

Quarter-allocation is itself a one-way door for the quarter — opportunity cost is not recoverable mid-quarter. Plan must either record the alternatives considered or be sent back.

## B6 — Operability + success metrics (Full only)

- **Metrics**: ABSENT. No baseline metric stated for any theme; no target delta.
- **Alerts**: ABSENT.
- **Rollback path**: ABSENT (no feature-flag plan, no staged rollout for any theme).
- **Runbook**: ABSENT.
- **Capacity headroom**: ABSENT.
- **User-visible outcome metric**: ABSENT for all three themes. "Flat re-engagement" and "leaky funnel" are diagnostic phrases, not target outcome metrics with deltas (Product P1: outcomes, not outputs).

**Verdict: SUSTAINED.** Operability + success metrics are blocking absences for a Full-tier plan.

## B7 — Sequencing + capacity (Full only)

- **Critical path**: not surfaced. The three themes are presented as parallel allocations; nothing names what blocks what (e.g. push depends on consent-flow design from onboarding work; sharing depends on auth/privacy review that legal also has to do for push).
- **Appetite**: "next quarter" — fixed cap (~12 weeks) but per-theme appetites within that are unstated. Per Universal Rule C1 / Shape Up, appetite must be set per item, not just at the portfolio level.
- **FTE**: not named. 60/30/10 of an unspecified denominator is not a capacity plan.

## B8 — Pre-mortem

Adopting prospective hindsight (Klein): the quarter ends, the roadmap failed.

Top 3 reasons ranked by likelihood:

1. **Themes were prioritised by request volume / vibe, not by ICE × confidence × cost-of-delay (Product Rules B2, B5).** End of quarter: shareable shortlist shipped, ~3% of users used it once, no impact on retention or growth. The "we keep getting requests" signal turned out to be a vocal minority. Re-engagement push lifted opens but not the underlying outcome metric (DAU/WAU). Onboarding "rewrite" took 8 weeks and the funnel didn't move because the leak wasn't in onboarding.
   - **Kill-switch**: at week 3, run idea-triage retroactively; if any theme's confidence is still <5 after 3 weeks of discovery, pause delivery on that theme and return to discovery.
2. **Allocation 60/30/10 locked early; new evidence mid-quarter showed onboarding was the highest-leverage bet, but reallocation was politically impossible after commitments were made.**
   - **Kill-switch**: at week 4 and week 8, re-score themes against the same ICE rubric used at the start; if rank order changes by ≥1 position, the allocation is reopened (Product Rule C5).
3. **Cross-team dependencies (mobile, privacy, design) slipped because no owner had been confirmed in writing before the quarter started.** Push didn't ship because Apple's notification consent flow needed legal review that started in week 7.

(Reasons 1 and 2 are the load-bearing failure modes; reason 3 is the operational tax.)

## Recommendation

**REVISE** — the plan is solution-first (B1 SUSTAINED), scope-undefined (six B2 SUSTAINED), evidence-thin (five B3 SUSTAINED, all Confidence ≤0.5), missing operability and outcome metrics entirely (B6 SUSTAINED), and contains four un-ADR'd one-way doors (B5 SUSTAINED). The Quick-tier reversibility carve-out does not apply (Full tier; quarter-long allocation is not one-commit-revertable).

### Conditions

The plan must address the following before re-review:

1. **Run `idea-triage` on each of the three themes before allocation is locked.** Each theme produces: a Product-Rule-A2 problem statement, a target outcome metric with delta, an ICE score with explicit confidence (Gilad), and a Doshi portfolio-theme classification.
2. **Replace allocation-by-rationale with allocation-by-evidence.** 60/30/10 must be derived from ICE × confidence × cost-of-delay, not from intuition. Show the working.
3. **Cite the idea-bank** to show why these three themes displaced others (Product Rule A6).
4. **Raise B3 confidence above 0.5 for the load-bearing assumption per theme** before committing engineering capacity. The 5-minute tests are listed in B3; run them or assign owners. Specifically: pull the actual request count + segment for shortlist, name the specific re-engagement metric and lever evidence for push, and pull funnel-stage data for onboarding (the leak may not be in onboarding at all).
5. **Author a one-page allocation ADR** naming alternatives considered (e.g. 100/0/0, 50/25/25, 0/50/50, all-onboarding) and the reversal cost of each. Per Universal Rule A3 + B5.
6. **Add operability + outcome-metric section per theme**: baseline metric, target delta, observation window, kill-switch threshold, rollback path. Per Universal Rule A6 + Product P1.
7. **Confirm dependencies in writing** with mobile, design, privacy/legal, analytics, and any notification-provider owner before week 1. Per Universal Rule B7.
8. **Set per-theme appetites** (not just a quarter-level allocation) and name the per-theme circuit-breaker (Universal Rule C1 / Shape Up).

Once 1–4 are addressed, re-run plan-review against the revised plan; conditions 5–8 can be folded into the revision in the same pass.
