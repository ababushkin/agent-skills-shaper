# Plan review: next-quarter-roadmap-three-themes

## Plan reference

> Shape next-quarter roadmap with three themes — shareable shortlist, push notifications, onboarding rewrite — allocated 60/30/10 across them. The shareable shortlist is highest priority because we keep getting requests. Push notifications because re-engagement is flat. Onboarding rewrite because the funnel is leaky. Approve?

## Inputs

- **Appetite**: One quarter (>1 week; exact FTE not stated)
- **Cynefin domain**: Complex — each theme involves emergent user behaviour (sharing, re-engagement, onboarding conversion) with no deterministic cause-effect chain confirmed; outcomes depend on feedback from real usage
- **Tier**: Full — selected because plan appetite exceeds 1 week (auto-select attribute)

---

## B1 — Problem framing

The plan names three themes and offers one-line rationales for each. None of the rationales constitute a problem statement. "We keep getting requests" is a demand signal, not a problem. "Re-engagement is flat" is a symptom, not a defined problem (flat relative to what baseline, for which cohort, over what window?). "The funnel is leaky" is a cliché with no specificity — which stage leaks, by how much, for which user segment?

**Verdict: SUSTAINED.**

The plan is solution-first for all three themes. Each theme names an output ("shareable shortlist," "push notifications," "onboarding rewrite") without naming the user problem it addresses or the measurable outcome it aims to move.

Falsifying condition: Show a problem statement for each theme in the form "For [segment], [specific problem] causes [measurable negative outcome]; solving it should move [metric] by [target] within [window]." If those statements exist in a companion doc, link them. If they don't exist, B1 is SUSTAINED.

---

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| "Shareable shortlist" touches sharing infrastructure (link generation, auth bypass or token logic, analytics events for shares) — none of this is declared in scope | SUSTAINED | Plan explicitly names link generation, token scoping, and share analytics as in-scope and costed against the 60% allocation |
| "Push notifications" implies platform permissions (iOS/Android opt-in flows), notification service (FCM/APNs integration or vendor selection), and preference management UI — all undeclared | SUSTAINED | Plan lists the notification stack components in scope and confirms the vendor/platform already exists in the product |
| "Onboarding rewrite" at 10% allocation (roughly 1–2 weeks) is vague enough to silently expand — "rewrite" routinely doubles in scope mid-execution | SUSTAINED | Plan bounds the onboarding scope explicitly: which screens, which flows, which metrics it will and will not touch |
| 60/30/10 allocation is stated as a ratio but the denominator (total FTE-weeks) is absent — the ratio is meaningless without it | PARTIAL | Plan states total team capacity and confirms 60/30/10 maps to named FTE-weeks per theme |
| Interaction between themes is undeclared — onboarding and push notifications both touch the new-user funnel; conflicts are invisible | PARTIAL | Plan states whether the themes are sequenced, parallel, or have shared surface area and how conflicts are resolved |

---

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| "We keep getting requests" justifies 60% of quarterly capacity for shareable shortlist | 0.1–0.5 — volume and source of requests unspecified; could be 3 power users or 300; no frequency, recency, or segment data stated | Pull the last 90 days of request volume by source (support, in-app, sales); segment by user tier; confirm it represents a broad customer base, not a concentrated one. Owner: PM | SUSTAINED — blocks APPROVE |
| "Re-engagement is flat" means push notifications will move it | 0.1 — flat re-engagement may be caused by content quality, product-market fit drift, competition, or notification fatigue from other channels; push is one possible lever, not a confirmed one | Pull re-engagement cohort data; run a spike to identify whether lapsed users cite "didn't remember" (addressable by push) or other reasons (not addressable by push). Owner: analytics | SUSTAINED — blocks APPROVE |
| "Onboarding rewrite" at 10% allocation will materially improve funnel conversion | 0.1 — no funnel drop-off data cited; no stage named; no hypothesis about which friction the rewrite removes | Pull funnel data by stage; identify the single highest-drop step; confirm the drop is a UX/friction problem (rewrite-addressable) vs. expectation mismatch or pricing (not rewrite-addressable). Owner: PM + design | SUSTAINED — blocks APPROVE |

All three riskiest assumptions score at or below 0.5 on the Gilad scale (opinion/anecdote). None have been tested. Per the skill's rule, untested assumptions with Confidence < 5 block APPROVE.

---

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Push notifications require a notification delivery service (FCM, APNs, or a vendor like OneSignal/Braze) — infrastructure or vendor contract needed | Not named | Not stated | SUSTAINED — no owner, no confirmation this exists or will be procured within the quarter |
| Shareable shortlist likely requires auth/token service changes and link-routing infrastructure — platform or backend team dependency | Not named | Not stated | SUSTAINED — plan does not name the team responsible for link infrastructure |
| Onboarding rewrite requires design and content — is design capacity within the 10% allocation or separate? | Not named | Not stated | PARTIAL — allocation is ambiguous on whether design FTE is included |

---

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Push notification platform/vendor selection — once users opt in and notification history accumulates, switching vendors requires re-opt-in campaigns and data migration | No alternatives named | No ADR mentioned | SUSTAINED — vendor selection is a one-way door; the plan must name alternatives considered (build vs. vendor; which vendors evaluated) before it can be approved |
| Shareable links architecture — public link format and token scheme affect SEO, analytics, and future access-control design; hard to change once links are in circulation | No alternatives named | No ADR mentioned | SUSTAINED — link architecture is a one-way door; alternatives must be named |
| Onboarding rewrite — lower reversibility risk if the rewrite is behind a flag; the plan does not state whether a flag or gradual rollout is planned | Not stated | Not mentioned | PARTIAL — confirm whether the rewrite is feature-flagged or a hard cut-over |

---

## B6 — Operability + success metrics

- **Metrics**: Absent. No metric is named for any theme. "Re-engagement is flat" is an observation, not a metric with a target.
- **Alerts**: Absent. Push notification delivery failures, opt-out spikes, and share link error rates are all unmonitored by this plan.
- **Rollback path**: Absent. No rollback strategy stated for any theme.
- **Runbook**: Absent.
- **Capacity headroom**: Absent. 60/30/10 is a ratio; no absolute FTE stated.
- **User-visible outcome metric**: Absent for all three themes. The plan lists delivery targets (themes) not outcome targets (metric movements).

B6 is fully SUSTAINED. No outcome metric, no operability plan.

Falsifying condition: Plan names, per theme: (1) the primary outcome metric and its current baseline and target, (2) the rollback mechanism, (3) at least one alert that would fire if the theme is causing harm post-launch.

---

## B7 — Sequencing + capacity

The critical path is not surfaced. Three themes are allocated percentages but no sequencing is stated — is push notifications blocked on any onboarding work? Does the shareable shortlist depend on auth infrastructure that must land first?

Appetite is stated as "next quarter" — not a fixed cap. A quarter is a date range, not an appetite in the Shape Up sense; there is no statement of what gets cut if scope expands.

FTE consistency: total team size is unstated. 60/30/10 of an unknown denominator produces an unknown workload. Whether a 4-person team or an 8-person team can execute all three themes in one quarter is unverifiable.

**Verdict: SUSTAINED** on all three sub-checks (critical path, fixed appetite, FTE stated).

Falsifying condition: Plan states total team FTE, names the critical path (what must land before what), and commits to a scope-reduction rule if any theme exceeds its appetite before the end of quarter.

---

## B8 — Pre-mortem

The plan shipped. It is end of quarter. Three failure modes, ranked by likelihood:

**1. Shareable shortlist ships but sharing rate is negligible (most likely)**
The "we keep getting requests" signal turned out to be a small cluster of power users. Most users don't share shortlists because sharing is not a workflow pattern in this product. The 60% capacity spend produces a low-adoption feature. Kill-switch: two weeks post-launch, if the share-initiation rate is below [X]% of active users, pause further investment and run a user interview sprint before continuing.

**2. Push notification opt-in rate is low; re-engagement does not move (second most likely)**
Users who have already lapsed do not opt into notifications at the re-engagement moment. Notification opt-in requires prior trust and active product engagement. The channel cannot reach the exact cohort it was designed to re-engage. Kill-switch: if opt-in rate at end of onboarding is below [Y]% after two weeks of launch, halt notification send campaigns and investigate opt-in UX before scaling.

**3. Onboarding rewrite consumes more than its 10% allocation and is cut mid-quarter, shipping in a partial state that makes the funnel worse**
"Rewrite" at 10% is the most schedule-fragile item. A partial onboarding rewrite — new screens for some steps, old screens for others — often performs worse than either the old or the new version alone due to context discontinuity. Kill-switch condition: if scope has expanded past 10% allocation by week 4, either cut to the single highest-impact screen change or defer entirely to next quarter — do not ship a partial rewrite.

---

## Recommendation

**KILL** — the plan's core premise fails on three independent grounds:

1. **B1 SUSTAINED**: No problem statement exists for any theme. All three themes are solution-first. The plan cannot be approved without knowing what user problem each theme solves and what outcome metric it targets.

2. **B3 SUSTAINED (all three assumptions)**: Every prioritisation rationale scores ≤0.5 on the Gilad confidence scale. "Keep getting requests," "re-engagement is flat," and "funnel is leaky" are unvalidated opinions. At this confidence level, 60/30/10 capacity allocation is arbitrary — there is no evidence basis to prefer this portfolio over any other.

3. **B5 SUSTAINED (two one-way doors)**: Push vendor selection and share-link architecture are both one-way doors with no alternatives documented and no ADR committed. The plan would lock the team into consequential architectural decisions without recording the alternatives considered.

KILL does not mean "abandon these themes." It means: this plan is not approvable in its current form. The corrective path is:

- Run idea-triage on each theme to produce problem statements with outcome metrics and confidence scores before re-entering the roadmap
- Validate the three riskiest assumptions (request volume, re-engagement root cause, funnel stage) with ≤2 weeks of discovery work
- Return with a revised plan that names owners, metrics, rollback paths, and the alternatives considered for the two one-way doors

Themes may survive triage; this plan does not.

### Conditions for re-submission

1. Problem statement per theme: segment, problem, measurable outcome target, time window
2. Confidence score per theme: minimum 2.0 (survey/experiment data) before committing build capacity
3. Push vendor alternatives documented; ADR committed before vendor selection finalised
4. Share-link architecture alternatives documented; ADR committed before implementation begins
5. Total FTE stated; absolute allocation per theme confirmed against that denominator
6. Outcome metric per theme: current baseline and target delta named
7. Rollback path named per theme
8. Critical path surfaced: what blocks what across the three themes
