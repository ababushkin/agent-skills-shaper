# Plan review: next-quarter-roadmap-three-themes

## Plan reference

> Shape next-quarter roadmap with three themes — shareable shortlist, push notifications, onboarding rewrite — allocated 60/30/10 across them. The shareable shortlist is highest priority because we keep getting requests. Push notifications because re-engagement is flat. Onboarding rewrite because the funnel is leaky. Approve?

## Inputs

- **Appetite**: One quarter (~12 weeks) — duration implied, no fixed cap stated; treated as >1 week for tier selection
- **Cynefin domain**: Complicated
- **Tier**: Full — selected because appetite > 1 week and ≥3 themes with interdependent capacity allocation

---

## Step 1 — Trigger check

Trigger fires: the plan explicitly asks "Approve?" and the work described exceeds one day of effort (a full quarter). Proceeding to tier selection.

## Step 1a — Fast-track gate

Does NOT fire. Precondition 1 fails: this is a product roadmap, not a KTLO/maintenance class change. Precondition 3 fails: appetite is one quarter. Falling through to normal flow.

## Step 2 — Tier selection

**Full tier** selected. Selecting attribute: appetite is >1 week (one quarter). Additionally, plan carries ≥3 themes each representing distinct capability investments with cross-functional dependencies.

## Step 3 — B0 Cynefin classification

**Complicated.** Each of the three themes involves knowable cause-effect relationships (re-engagement via push, conversion via onboarding, sharing via shortlist) but requires expert analysis to validate. The domain is not Clear (the right solutions are not obvious from the descriptions) and not Complex (the outcomes are not emergent — they can be planned with discovery). Review emphasis: dependencies, evidence quality, critical path.

---

## B1 — Problem framing

The plan opens with three solutions (shareable shortlist, push notifications, onboarding rewrite) and then supplies motivation in reverse: "we keep getting requests," "re-engagement is flat," "the funnel is leaky." This is solution-first. Each theme has a one-line business signal but no stated measurable outcome target.

**Verdict: SUSTAINED.**

What would overturn this: for each theme, a problem statement of the form "For [customer segment], [problem] is causing [outcome]. If solved, we expect [metric] to improve by [target] within [timeframe]." Supplying a direction without a measurable target leaves the team with no way to know whether they succeeded.

---

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| "Shareable shortlist" scope: what is shared, how, to whom, from which surfaces, with what privacy model | SUSTAINED | Plan explicitly names the sharing primitive (link, embed, copy?), the surfaces it applies to, and the access model (public/private/org-scoped) |
| "Push notifications" scope: which platforms (iOS/Android/web), which notification types, opt-in flow, and unsubscribe/suppression logic — all undeclared | SUSTAINED | Plan names the notification types in scope, the platforms targeted, and confirms opt-in/unsubscribe flows are included or explicitly excluded |
| "Onboarding rewrite" scope: which funnel steps are in scope, which are excluded, whether existing users are affected | SUSTAINED | Plan names the start and end points of the rewrite scope (e.g., "signup through first value action") and states whether existing-user flows are touched |
| 60/30/10 allocation: whether this is FTE-weeks, budget, or story points — undeclared, so cannot be verified | PARTIAL | Plan states the unit of allocation (e.g., "60% of engineering FTE-weeks for the quarter") so the split can be confirmed against actual headcount |
| Silent expansion risk: "onboarding rewrite" phrasing invites scope creep beyond the leaky funnel into redesigning onboarding content, copy, and onboarding emails | SUSTAINED | Plan names three specific onboarding steps that are in scope and explicitly excludes content/copy work unless stated |

Zero-SUSTAINED check: 4 SUSTAINED items. Consistent with a plan at this level of abstraction.

---

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| "We keep getting requests" justifies shareable shortlist as the highest-priority investment | 0.5 — anecdote, request volume; no frequency, no segment breakdown, no evidence of retention or revenue impact | Owner produces a 30-day request log with segment tagging and estimated revenue impact per request type | SUSTAINED — confidence below 5 blocks APPROVE |
| "Re-engagement is flat" means push notifications will move re-engagement | 0.1 — correlation assumed; push is one of many possible causes; no evidence that push is the correct lever vs. email, in-product nudges, or content gaps | Owner presents a cohort analysis showing what re-engaged users have in common and whether notification-delivered traffic historically converts | SUSTAINED — confidence below 5 blocks APPROVE |
| "The funnel is leaky" means an onboarding rewrite is the fix (vs. a targeted patch to the highest-drop step) | 0.5 — funnel data likely exists but a "rewrite" is a solution, not a validated response to a diagnosis | Owner names the specific funnel step with highest drop, confirms it is caused by the onboarding experience (not traffic quality or product-market fit), and shows that fixing that step is worth 10% of the quarter's capacity | SUSTAINED — confidence below 5 blocks APPROVE |

All three riskiest assumptions score below 5. All three block APPROVE.

---

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Push notifications — mobile platform capability: iOS APNs / Android FCM setup, device token management, delivery pipeline | Not named | Not confirmed | SUSTAINED — this is non-trivial platform work; if mobile infra doesn't own a push delivery layer, the 30% allocation is insufficient |
| Push notifications — opt-in/legal: GDPR/CCPA consent for push, unsubscribe audit | Legal/compliance owner not named | Not in scope statement | SUSTAINED — marketing/push notifications carry regulatory obligation; silent assumption it is handled |
| Onboarding rewrite — design dependency: rewrite implies new UX, which implies design capacity at 10% of quarter | Design owner not named | 10% is thin for a rewrite | PARTIAL — 10% may be workable if the design work is already done; not confirmed |
| Cross-theme sequencing: push notifications may depend on onboarding rewrite if new users are a target segment for push | Not named | Not addressed | PARTIAL — potential sequencing dependency not surfaced |

---

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Push notification infrastructure: once device tokens are collected and a delivery pipeline is built, the schema and platform contract are expensive to change | No alternatives named (e.g., in-app notifications, email re-engagement, SMS) | No ADR | SUSTAINED — the plan commits to push without naming why push over email/in-app; an ADR must exist before build begins |
| Onboarding rewrite: a rewrite (vs. targeted patch) is a one-way door — rewriting onboarding discards the iteration history baked into the current flow | No alternatives named (e.g., A/B patch the high-drop step, run a targeted experiment) | No ADR | SUSTAINED — "rewrite" is a loaded word that implies discarding working code; the plan must name why rewrite is preferred over targeted fix |
| Shareable shortlist: sharing model (link/embed/permission) is an expensive-to-change surface; affects data model and access control | No alternatives named | No ADR | PARTIAL — less severe than push or onboarding, but sharing access model is still a data-model decision worth an ADR |

---

## B6 — Operability + success metrics

- **Metrics**: Absent. No user-visible outcome metrics named for any theme.
- **Alerts**: Absent. Push delivery failure rate, push opt-in rate, onboarding conversion rate — none declared.
- **Rollback path**: Absent. No rollback described for push infrastructure, onboarding changes, or sharing model.
- **Runbook**: Absent.
- **Capacity headroom**: Partially addressed. 60/30/10 split is stated but unit is undefined (see B2).
- **User-visible outcome metric**: Absent. "Re-engagement is flat" is a current-state description, not a target. "Funnel is leaky" is a diagnosis, not a success criterion.

**Verdict: SUSTAINED on both halves.** No outcome metric named for any theme; no operability plan exists. Both halves block APPROVE.

---

## B7 — Sequencing + capacity

Critical path: not surfaced. The plan does not name what blocks what across three themes. If push notifications require platform work that isn't started, it blocks the 30% allocation from producing anything shippable in Q.

Appetite: not fixed as a cap. "Next quarter" is a calendar window, not a scoped appetite. The plan does not state what gets cut if push takes longer than 30% of FTE-weeks supports.

FTE consistency: cannot be verified — the 60/30/10 split has no unit, no team size, and no named owners per theme.

**Verdict: SUSTAINED.** Three sub-gaps: (1) critical path absent, (2) appetite is a window not a cap, (3) FTE allocation unverifiable.

---

## B8 — Pre-mortem

Assume the plan shipped and failed within the quarter. Top three reasons ranked by likelihood:

**1. Push notifications built but not adopted (highest likelihood).** The team builds push delivery infrastructure but opt-in rates are near zero because users have no context for why they should allow notifications. Re-engagement metric does not move. Kill-switch: instrument opt-in prompt conversion at day 7 of build; if <10% of eligible users opt in during a soft-launch cohort, pause and run a discovery sprint before full rollout.

**2. Onboarding rewrite overshoots appetite and blocks shareable shortlist (high likelihood).** "Rewrite" scope expands from targeted funnel fix to full redesign; design and engineering absorb most of the quarter; shareable shortlist ships at 40% of intended spec. Kill-switch: at the 4-week mark, if onboarding has consumed >50% of its 10% allocation with no shippable increment, descope to the single highest-drop funnel step and freeze the rest.

**3. Shareable shortlist requests were long-tail, not high-frequency (moderate likelihood).** Requests came from a vocal minority; sharing feature ships but active usage is <5% of users; no retention or revenue impact. Kill-switch: before starting build, survey the top 20 requesting users on whether they would share if the feature existed today and what they would share; if fewer than 15 confirm active intent, reprioritise.

---

## Recommendation

**REVISE**

The plan has six categories of unresolved SUSTAINED findings across B1, B2, B3, B4, B5, B6, and B7. None of the three themes has a measurable outcome target, a named evidence base above Confidence 0.5, an ADR for its one-way-door decisions, or an operability plan. APPROVE is blocked until the conditions below are addressed.

### Conditions

1. **B1 — Problem framing**: Rewrite each theme as a problem statement with a measurable target (metric + magnitude + timeframe). Solution-first framing is not approvable.

2. **B3 — Shareable shortlist evidence**: Produce a 30-day request log with segment tagging and estimated impact. Confidence must reach ≥2 (survey data) before the 60% allocation is approved.

3. **B3 — Push notifications lever**: Present a cohort analysis confirming push is the correct re-engagement lever. Confidence must reach ≥5 (experiment or validated channel data) before build begins.

4. **B3 — Onboarding diagnosis**: Name the specific funnel step with highest drop and confirm a rewrite (vs. targeted patch) is the appropriate intervention. Confidence must reach ≥2 before scoping a rewrite.

5. **B4 — Push infrastructure dependency**: Name the team/owner responsible for push delivery infrastructure, confirm capacity exists within the quarter, and confirm opt-in/legal review is scheduled.

6. **B5 — ADR for push and onboarding rewrite**: Before build begins on either, write an ADR naming alternatives considered and reversal cost. Push ADR must address why push over email/in-app. Onboarding ADR must address why rewrite over targeted patch.

7. **B6 — Success metrics**: Name one user-visible outcome metric per theme with a target value and observation window. Examples: "weekly re-engagement rate for push-opted-in users +15% within 6 weeks of launch"; "step-2 funnel completion rate +8% within 30 days of onboarding rewrite." Delivery metrics (shipped / not shipped) are not sufficient.

8. **B7 — Appetite and capacity**: State the unit for the 60/30/10 split (FTE-weeks), name team size, name what gets cut per theme if the appetite is exceeded, and surface any cross-theme sequencing dependency.
