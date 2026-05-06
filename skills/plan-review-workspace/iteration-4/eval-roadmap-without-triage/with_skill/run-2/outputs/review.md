# Plan review: next-quarter-roadmap-3-themes

## Plan reference

Plan stated in conversation: "shape next-quarter roadmap with three themes — shareable shortlist, push notifications, onboarding rewrite — allocated 60/30/10 across them. The shareable shortlist is highest priority because we keep getting requests. Push notifications because re-engagement is flat. Onboarding rewrite because the funnel is leaky. Approve?"

## Trigger check

Trigger fired: explicit "Approve?" request to review a plan before approval (When-to-use #1). Auto-fire also applies: roadmap appetite is one quarter (>1 day, >1 week). Proceeding.

## Step 1a — Fast-track gate

Does NOT fire. This is a roadmap, not KTLO/maintenance; appetite >1 day; not a fully-reversible single-commit change. Falling through to normal flow.

## Inputs

- **Appetite**: one quarter (~12 weeks) — but not stated as a fixed cap by the owner; treated as quarter-cycle planning
- **Cynefin domain**: Complicated — known cause-effect with expertise required (re-engagement, funnel optimisation are knowable problems with established practices). Some Complex elements (shareable shortlist behaviour change is emergent), but dominant signature is Complicated.
- **Tier**: Full — selected because appetite >1 week (auto-select rule). Also: roadmap touches multiple themes likely with cross-team dependencies and one-way-door product surface decisions (push notifications infra, onboarding flow architecture).

## B1 — Problem framing

**SUSTAINED.** All three themes are framed as solutions, not problems. PRODUCT_RULES Rule A2 demands: "For [customer segment], we believe [problem] is causing [negative outcome]. If we solve it, we expect [measurable outcome] to improve by [target]."

- "Shareable shortlist" is a feature name, not a problem. The implicit problem ("users want to share lists with others") is unstated and unvalidated. "We keep getting requests" is anecdote-grade evidence (Confidence ~0.5).
- "Push notifications" is a solution. The stated problem ("re-engagement is flat") is closer to a problem statement but lacks segment, magnitude, and target ("flat" is not a metric — flat at what level? for whom? for how long?).
- "Onboarding rewrite" is a solution that pre-commits to scope ("rewrite" implies wholesale replacement before the diagnosis is in). The stated problem ("the funnel is leaky") is directional but not specified — which step? what conversion rate currently? target rate?

Falsifying condition: a re-stated plan in which each theme opens with customer segment + problem + measurable target outcome (PRODUCT_RULES A2/A3 form) would overturn this verdict.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| "Onboarding rewrite" — scope is undefined; "rewrite" can mean copy edits, flow restructure, or full re-architecture spanning 3+ months | SUSTAINED | A scope statement naming exactly which onboarding steps are in scope, what "rewrite" means structurally (copy / flow / infra), and what is explicitly out of scope |
| "Push notifications" — does this include infra build (if absent), permission-prompt UX, content strategy, frequency caps, opt-out, segmentation? Each is a different appetite. | SUSTAINED | Named breakdown of which of these sub-scopes is included at 30% allocation and which is deferred |
| "Shareable shortlist" — sharing implies recipient surface, link generation, permissions model, possible auth-touch for non-users. None declared. | SUSTAINED | Named decision on recipient experience (logged-in only / public link / invite flow) and whether non-user recipients are in scope |
| Cross-theme: 60/30/10 allocation is across themes but not against KTLO, validation, discovery, or reliability work (Rule C3 demands explicit capacity allocation including these) | SUSTAINED | A capacity allocation statement that adds KTLO %, validation %, and reliability % alongside the three themes |
| No portfolio-theme classification (Differentiator / Table-stakes / Incremental / Embarrassment / Customer-special / Tech-foundation / Speculative) per Rule B3 | SUSTAINED | Each theme classified into one of the seven portfolio themes with rationale |
| "Highest priority because we keep getting requests" conflates request volume with impact — is this a Customer-special or a Differentiator? Different prioritisation logic applies | PARTIAL | An ICE score (Impact × Confidence × Ease) per Rule B2 alongside the request-volume signal would resolve this |

Six items surfaced, all SUSTAINED or PARTIAL. Plan-as-stated is under-scoped for a quarter commitment.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| "Users want to share shortlists" — implicit in shareable-shortlist priority. Backed by "we keep getting requests" | 0.5 (anecdote) | 5-min test: count distinct request originators in last 90 days; segment by paid/free; check whether requesters are repeat customers or one-offs. Owner: PM for shortlist surface. | SUSTAINED — Confidence <5 blocks APPROVE |
| "Push notifications will lift re-engagement" — implicit causal claim; no evidence cited that the re-engagement gap is caused by lack of push (vs. content quality, frequency, value-prop, channel mismatch) | 0.1 (opinion) | 5-min test: check existing email/in-app re-engagement performance; if those are also flat, push is unlikely to be the lever. Smoke test: send a one-off push to a cohort that opted in, measure 7-day retention delta. | SUSTAINED — Confidence <5 blocks APPROVE |
| "Onboarding rewrite will fix the funnel" — assumes the leak is structural (fixable by redesign) rather than acquisition-quality, value-prop mismatch, or technical (load times, errors). Wholesale rewrite presumes the diagnosis. | 0.1 (opinion) | 5-min test: pull funnel drop-off step data; if drop-off is concentrated at one specific step, "rewrite" is overshoot — targeted fix wins. If drop-off is distributed, the assumption that a rewrite helps still needs evidence. | SUSTAINED — Confidence <5 blocks APPROVE |

All three top assumptions sit at Confidence 0.1–0.5 (opinion / anecdote). PRODUCT_RULES Rule B6 explicit: "Reject any item whose confidence is below threshold unless the only work being committed to is validation." Plan as stated commits 100% of capacity to build, not validation.

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Push-notification infra (FCM/APNs setup, permission-prompt logic, opt-in/opt-out tracking) — may require platform / mobile team | Not stated | Not stated | SUSTAINED |
| Shareable-shortlist sharing surface — link service, possible auth changes for recipient flows | Not stated | Not stated | SUSTAINED |
| Analytics / event-tracking instrumentation for measuring outcome metrics on all three themes | Not stated | Not stated | SUSTAINED |
| Design / content team capacity for onboarding rewrite (copy + visual + flow) | Not stated | Not stated | SUSTAINED |
| Legal / privacy review for push opt-in flows (GDPR/notification consent) | Not stated | Not stated | SUSTAINED |

Universal Rule B7: unconfirmed cross-team dependencies are the single most common cause of missed commitments. None are confirmed.

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Push-notification platform/vendor choice (FCM, APNs direct, OneSignal, Braze, Customer.io) — vendor lock-in, data residency, cost-at-scale all hard to reverse | None named | None | SUSTAINED |
| Sharing model for shortlists (auth-required vs. public-link vs. invite-only) — schema, permissions, abuse-vector, and recipient-acquisition all flow from this; reversal requires migration and possible UX disruption for users who already shared | None named | None | SUSTAINED |
| Onboarding flow architecture (linear / modular / progressive) — affects every downstream feature gate; rewriting again later is expensive | None named | None | SUSTAINED |

Three undocumented one-way doors. Universal Rule B3 + Agentic P7: alternatives must be named and ADRs paired before commitment.

## B6 — Operability + success metrics

- Metrics: **absent** — no per-theme outcome metric named
- Alerts: **absent** (push delivery failures, shortlist-sharing errors, onboarding-step drop alarms all unnamed)
- Rollback path: **absent** (each theme could ship behind feature flag with kill-switch — not stated)
- Runbook: **absent**
- Capacity headroom: **absent**
- User-visible outcome metric: **absent on all three themes**
  - Shareable shortlist: no named target (e.g., "% of active users who share ≥1 shortlist within 30 days")
  - Push notifications: "re-engagement" not defined (DAU/WAU return rate? 7-day retention? session count?)
  - Onboarding: no named conversion target (current step-N conversion → target step-N conversion)

PRODUCT_RULES Rule A3: "No item ships without a metric that will tell us whether it worked." Plan does not satisfy this on any theme. Universal Rule A6 (operability section) also fails. **SUSTAINED — blocks APPROVE.**

## B7 — Sequencing + capacity

- Critical path: not surfaced. No statement of which theme blocks which, or which depends on a foundational piece (e.g., does push notifications require analytics instrumentation that must land first?).
- Appetite: "next-quarter" is the only time-frame; no per-theme appetite. 60/30/10 is a capacity *split*, not an appetite (Singer: appetite is "how much the problem is worth in time"). For onboarding at 10% of a quarter, that's roughly 1.2 weeks of team capacity — radically inconsistent with "rewrite."
- FTE consistency: 10% allocation against "rewrite" is internally inconsistent. Either the work isn't a rewrite, or the allocation is wrong, or both.
- Validation/discovery slot: 0% allocated, despite three Confidence-<1 assumptions (Rule C3 + Rule B6 violation).

**SUSTAINED.** Allocation math does not match scope intent.

## B8 — Pre-mortem

Assume the quarter has ended and this roadmap failed. Top 3 reasons ranked by likelihood:

1. **(Most likely)** End-of-quarter review shows shareable-shortlist shipped but adoption is <2% of active users — because the "we keep getting requests" signal turned out to be a small loud minority, not a representative segment. The 60% allocation produced a feature few wanted at the cost of the other two themes.
   - **Kill-switch**: Before week 2, run the 5-min test from B3 (count distinct requesters, segment, validate intent with 10-user interview). If <50 distinct requesters or no segment-coherent pattern emerges, drop allocation to 20% (validation-slot only) and reassign capacity.

2. Push notifications shipped on schedule but re-engagement metric did not move — because the underlying re-engagement problem is content/value-prop, not channel. Push opt-in rate also lower than expected (15% vs assumed 40%), so even if the channel worked, the addressable population is small.
   - **Kill-switch**: Smoke-test push on a 5% cohort in week 3 before full build. If 7-day retention delta is <2 percentage points and opt-in is <25%, halt push build and re-route capacity.

3. Onboarding "rewrite" at 10% allocation produced a half-finished re-architecture that left the funnel worse than before — the team ran out of appetite mid-flight and the partial state shipped, breaking the previous flow without delivering the new one.
   - (No kill-switch named; per skill rules, top-2 require kill-switches, this third is recorded for completeness.)

## Recommendation

**REVISE** — at least one SUSTAINED verdict on every required gate (B1, B2, B3, B4, B5, B6, B7). Plan is not ready for approval.

### Conditions

The plan must satisfy each of the following before re-review:

1. **Re-frame each theme as a problem (B1, PRODUCT_RULES A2/A3).** For each of the three themes, write: "For [customer segment], we believe [problem] is causing [negative outcome]. If we solve it, we expect [named outcome metric] to improve by [target] within [timeframe]."

2. **Run idea-triage on each theme (Rule B2/B6).** Score Impact × Confidence × Ease for each. Items with Confidence <5 may only earn validation slots, not build slots. The "shareable shortlist requests" signal must be quantified: how many distinct originators, what segment, what intent.

3. **Classify each theme into a portfolio theme (Rule B3).** Differentiator / Table-stakes / Incremental / Embarrassment / Customer-special / Tech-foundation / Speculative. Allocation across themes must be justified against this classification.

4. **State capacity allocation explicitly across all categories (Rule C3).** Not just 60/30/10 across the three product themes — also KTLO %, validation/discovery %, reliability/error-budget %, and reserved buffer.

5. **Define scope for each theme (B2).** Particularly: what "onboarding rewrite" means structurally; what is in/out of scope for "push notifications"; the sharing model for "shareable shortlist."

6. **Confirm cross-team dependencies in writing (B4, Rule C4).** Push infra, design capacity, analytics instrumentation, legal review for push consent — each owner named and capacity confirmed before the theme enters Now.

7. **Name and document one-way doors (B5, Rule B3, Agentic P7).** Push vendor choice, sharing model, onboarding flow architecture each get an ADR (or committed-to-be-written) listing alternatives considered and reversal cost.

8. **Define the success metric per theme (B6, PRODUCT_RULES A3, P10).** A user-visible outcome metric, not a delivery metric. Done = outcome moved, not feature shipped.

9. **Set a fixed appetite per theme (B7, Rule C1, Universal P8).** A cap, not a range. Verify that the FTE math at the chosen allocation actually fits the scope; if not, cut scope or change allocation — do not extend appetite.

10. **Add validation slots for the three Confidence-<1 assumptions (Rule B6).** The 5-minute tests in B3 should be the first work in the quarter, not bypassed.

A re-review after these conditions are met can use the Quick tier if the appetite and one-way-door surface have been resolved.
