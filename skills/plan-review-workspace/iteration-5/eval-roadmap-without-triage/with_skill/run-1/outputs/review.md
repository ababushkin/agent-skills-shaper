# Plan review: next-quarter-roadmap-three-themes

## Plan reference

> Shape next-quarter roadmap with three themes — shareable shortlist, push notifications, onboarding rewrite — allocated 60/30/10 across them. The shareable shortlist is highest priority because we keep getting requests. Push notifications because re-engagement is flat. Onboarding rewrite because the funnel is leaky. Approve?

## Inputs

- **Appetite**: one quarter (~13 weeks) — implied; not stated as a fixed cap
- **Cynefin domain**: Complex
- **Tier**: Full — selected because appetite exceeds 1 week (full quarter)

---

## Step 1 — Trigger check

Trigger fired: plan appetite > 1 day (a full quarter), and the owner is explicitly asking for approval. Auto-select Full tier because appetite > 1 week.

## Step 1a — Fast-track gate

Does not fire. Appetite is one quarter (not ≤1 day); work is not KTLO/maintenance class. Fall through to normal flow.

## Step 2 — Tier selection

**Full tier.** Selecting attribute: appetite > 1 week (quarter-length roadmap).

## Step 3 — B0 Cynefin classification

**Complex.** User behaviour (re-engagement, funnel conversion, sharing) is emergent — cause-effect is not fully predictable in advance. The plan should include feedback loops and decision points, not deterministic milestones. Implication: a flat 60/30/10 allocation set at the start of the quarter is likely to be wrong; the plan needs explicit checkpoints where allocation can be recalibrated on evidence.

---

## B1 — Problem framing

The plan opens with solution labels ("shareable shortlist", "push notifications", "onboarding rewrite") rather than problem statements. The rationale offered for each is a symptom observation — "requests", "re-engagement is flat", "funnel is leaky" — but none names:

- the specific user segment affected
- the outcome metric we expect to move
- the target level of improvement

This is solution-first framing (Universal P2). A plan that begins with three feature themes and backs into one-line justifications has inverted the correct order. The problem has not been articulated; the solution has been approved first.

**Verdict: SUSTAINED.**

Falsifying condition: the plan is revised to lead with problem statements in the form "For [segment], [problem] causes [negative outcome]; success = [metric] improves by [target]" for each theme, before any solution label appears.

---

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| "Shareable shortlist" — what exactly is shared, to whom, via which channels, and whether this requires backend changes (auth, data access, link expiry) is not stated | SUSTAINED | Plan names the sharing mechanism (e.g. public link vs. in-app invite), access model (who can view), and whether it requires schema or auth changes |
| "Push notifications" — which platform (iOS, Android, web), which notification events, which provider (APNS, FCM, third-party service), opt-in flow, and legal/consent requirements are all absent | SUSTAINED | Plan names platform scope, provider, notification event set, and how opt-in consent is handled |
| "Onboarding rewrite" — scope of rewrite (entire flow vs. specific steps), whether existing users are affected, whether A/B testing is in scope, and what "leaky" means quantitatively are unstated | SUSTAINED | Plan names which funnel steps are in scope, the current drop-off rate at those steps, and whether existing users see any change |
| The 60/30/10 capacity allocation is stated as a final number — it is not clear whether this is of engineering FTE only, or includes design and product | PARTIAL | Plan explicitly states what the allocation covers (eng, design, product) and on what headcount it is based |
| "Push notifications" at 30% of a quarter is plausible for a mature stack; if this is a new capability (likely, given re-engagement is "flat" and notifications were not mentioned as existing), 30% may be severely under-scoped | SUSTAINED | Team confirms push notification infrastructure already exists in production; if not, scope estimate is revised with the infra build included |

---

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| "We keep getting requests" for shareable shortlist → the requests represent a broad user need, not a concentrated vocal minority | 0.5 — anecdote/volume of requests, not validated demand signal | Pull the request data: how many unique users, what segments, what exact ask. Owner: PM. | SUSTAINED — confidence below 5 |
| Re-engagement is flat therefore push notifications will improve it | 0.1 — causal assumption; flat re-engagement may be caused by content, product value, or lifecycle mismatch — not notification absence | Run a 5-minute cohort split: do users who have notifications enabled (if any) re-engage at higher rates? Owner: data analyst. | SUSTAINED — untested causal link; confidence 0.1 |
| Onboarding rewrite will reduce funnel drop-off | 0.5 — "funnel is leaky" is a symptom; root cause (copy, UX, load time, value mismatch, activation event) is unknown | Pull the funnel data for the last 90 days and name the step with the highest drop-off rate and its current conversion. Owner: PM or analyst. | SUSTAINED — assumption of cause not validated |

All three core assumptions score below 5 on the Gilad scale. Under B3, untested assumptions with Confidence < 5 block APPROVE.

---

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Push notification infrastructure — provider (APNS/FCM/third-party), mobile SDK, backend delivery service | Not named | Not confirmed | SUSTAINED — if this is greenfield, it is a multi-week dependency with its own build; not visible in the plan |
| Design capacity — onboarding rewrite and shareable shortlist both require significant UX work | Not named | Not confirmed | SUSTAINED — no mention of design FTE or design lead |
| Legal / consent — push notification opt-in may require legal review (GDPR, CAN-SPAM, app store guidelines) | Not named | Not confirmed | SUSTAINED — jurisdiction and app store compliance not mentioned |
| Cross-team: if "shareable shortlist" requires public-facing URLs, it may require infra/platform team support (CDN, auth service, rate limiting) | Not named | Not confirmed | PARTIAL — platform dependency is possible but depends on the sharing model; not enough information to confirm |

---

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Push notification provider choice (once users opt in at scale, migrating providers is expensive and risks notification delivery gaps) | No alternatives named | No ADR | SUSTAINED — this is a one-way door; provider alternatives must be named and an ADR committed |
| Onboarding rewrite — if the existing onboarding is replaced rather than iterated, rolling back affects all new users entering the product; data from old funnel steps may be lost | Not addressed | No ADR | SUSTAINED — the plan does not name whether this is a replace or augment strategy; the rollback path is absent |
| Shareable shortlist — if it requires a schema change (e.g. new link/share entity), that is a one-way door on the data model | Not addressed | No ADR | PARTIAL — cannot confirm without knowing the implementation approach; plan must clarify |

---

## B6 — Operability + success metrics

- **Metrics**: absent. No metric is named for any of the three themes.
- **Alerts**: absent.
- **Rollback path**: absent. Particularly concerning for onboarding rewrite (see B5).
- **Runbook**: absent.
- **Capacity headroom**: absent. The 60/30/10 split assumes 100% of capacity is allocatable; no buffer for incidents, KTLO, or unplanned work.
- **User-visible outcome metric**: absent for all three themes. "Re-engagement is flat" is a problem description; the plan names no target (e.g. "increase 7-day re-engagement rate from X% to Y% within 60 days of launch"). Same gap for shareable shortlist and onboarding.

This is a full-tier plan. Absence of operability and outcome metrics blocks APPROVE (Universal Rule A6, Product P1).

---

## B7 — Sequencing + capacity

Critical path is not surfaced. Specific gaps:

1. Push notification infrastructure — if greenfield — is likely the longest lead-time item and a dependency for everything in that theme. It is not sequenced first.
2. Onboarding rewrite at 10% of capacity: if this is a full rewrite of a leaky funnel, 10% of a quarter (~1.3 weeks of one engineer's time) is almost certainly insufficient. The plan does not justify why 10% is the right appetite for a "rewrite."
3. The 60/30/10 allocation is stated as fixed for the quarter. Given a Complex Cynefin domain (B0), there are no named checkpoints where the allocation is revisited based on early evidence (e.g. if push notification infra takes longer than expected, what happens to the 30% allocation?).
4. "One quarter" is a time horizon, not a fixed-cap appetite per initiative. Shape Up (Singer) requires each initiative to have an explicit appetite (the amount of time the problem is worth). None of the three themes has one.

**Verdict**: sequencing and capacity are insufficient. Critical path absent; appetite per theme absent; no rebalancing mechanism named.

---

## B8 — Pre-mortem

Assume the quarter has ended and the roadmap has failed. Top 3 reasons ranked by likelihood:

1. **Push notifications shipped but re-engagement did not move** — the assumption that notification absence caused flat re-engagement was never validated. The actual cause was content or product value mismatch. The 30% of capacity spent on notifications generated opt-ins with no measurable re-engagement lift. Kill-switch condition: at week 4, if cohort data shows users with notifications enabled are not re-engaging at higher rates than those without, pause push notifications work and run a root-cause investigation before continuing.

2. **Shareable shortlist consumed the 60% slot and spilled into push and onboarding** — the sharing mechanism required unplanned auth and infra work (public link model, access control, rate limiting). The 60% allocation was underscoped. Push and onboarding were deprioritised to protect shareable shortlist. Kill-switch condition: at week 3, if the shareable shortlist design reveals backend dependencies not in the original plan, re-scope the quarter before committing to implementation.

3. **Onboarding rewrite at 10% produced a half-done replacement that degraded new-user conversion** — a partial rewrite (10% of quarter ≈ ~1.3 weeks) replaced part of the existing onboarding without completing the full flow. New users encountered an inconsistent experience. No rollback path was defined, so the team could not revert quickly.

---

## Recommendation

**KILL** — the plan's core premises (problem framing, evidence quality, operability) fail simultaneously, and the capacity and dependency picture is sufficiently unclear that approving the plan as written would commit the team to a quarter of work with no defined success criteria and no ability to determine mid-quarter whether the bets are paying off.

### Conditions

The plan must address all of the following before it can reach APPROVE:

1. **B1**: Reframe each of the three themes as a problem statement with a named user segment, a named outcome metric, and a numeric improvement target.
2. **B3-a**: Validate the shareable shortlist demand signal — pull request data by unique user and segment before committing 60% of capacity.
3. **B3-b**: Validate the push-notification causal assumption — check whether users with existing notification access re-engage at higher rates; if no such data exists, time-box a discovery spike before committing 30% of capacity to build.
4. **B3-c**: Name the specific funnel step(s) where onboarding drop-off occurs and the current conversion rate at those steps before committing to a rewrite.
5. **B4**: Confirm whether push notification infrastructure exists in production; if not, surface the greenfield build as a named dependency with its own appetite and owner.
6. **B4**: Name design FTE allocated to each theme.
7. **B4**: Confirm legal/consent review for push notifications is initiated.
8. **B5**: Name the push notification provider alternatives considered and commit to an ADR.
9. **B5**: Name whether onboarding rewrite is a replace or augment strategy and define the rollback path.
10. **B6**: Name a user-visible outcome metric for each theme (not a delivery metric — an outcome metric).
11. **B7**: Give each theme a fixed-cap appetite (not a % of an undefined total). Name the mid-quarter checkpoint where allocation is revisited based on evidence (required given Complex domain).
