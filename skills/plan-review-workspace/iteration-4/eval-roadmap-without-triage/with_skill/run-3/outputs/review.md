# Plan review: next-quarter-roadmap

## Plan reference

Pasted from conversation:

> Shape next-quarter roadmap with three themes — shareable shortlist, push notifications, onboarding rewrite — allocated 60/30/10 across them. The shareable shortlist is highest priority because we keep getting requests. Push notifications because re-engagement is flat. Onboarding rewrite because the funnel is leaky. Approve?

## Inputs

- **Appetite**: Stated as "next quarter" (~13 weeks). No per-theme appetite, no fixed cap per item.
- **Cynefin domain**: Complicated — three roadmap themes with knowable cause-effect (request volume, engagement metric, funnel metric); requires expertise to sequence and validate but not emergent.
- **Tier**: **Full** — auto-selected. Selecting attribute: appetite > 1 week (a full quarter), and roadmap-class plan implies multiple cross-team dependencies and likely one-way doors (push-notification infra, onboarding rewrite touches activation funnel = production data path).

## Step 1 — Trigger check

Trigger 1 fires (owner is about to approve a roadmap) and trigger 2 fires (work exceeds one day — entire quarter). Auto-fire condition also holds (push notifications = vendor lock-in / one-way door candidate; onboarding rewrite likely touches production user data path). Proceed.

## Step 1a — Fast-track gate

Does NOT fire. Failure on precondition 1 (not KTLO — three product themes with outcome claims), precondition 3 (appetite is a full quarter, not ≤1 day), and precondition 4 (push notifications and onboarding rewrite are not minor-version maintenance). Fall through to normal flow.

## B0 — Cynefin

Complicated. Review must emphasise dependencies and risk (per skill).

## B1 — Problem framing

**Verdict: SUSTAINED.**

The plan is structured as **three solutions** ("shareable shortlist", "push notifications", "onboarding rewrite") with one-line rationales attached, not as three problems with measurable target outcomes. Per Universal P2 and Product P2 (Rule A2): "For [customer segment], we believe [problem] is causing [negative outcome]. If we solve it, we expect [measurable outcome] to improve by [target]."

- "We keep getting requests" — request volume ≠ a defined customer problem; volume of asks is the weakest evidence form (Product Rule B7: "a large customer asked for it" / popularity is not a prioritisation argument by itself).
- "Re-engagement is flat" — names a flat metric, not a target movement, not a customer segment, not a hypothesis about why.
- "Funnel is leaky" — vague; no specific step, no quantified drop-off, no segment.

**Falsifying condition:** the plan would be OVERTURNED if each theme included (a) the named customer segment affected, (b) the specific problem, (c) the current baseline number, and (d) the target movement and review window.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| "Shareable shortlist" — undefined surface (web only? mobile? share-via-link vs. native share-sheet vs. social embed?) | SUSTAINED | A scope sentence that names the surfaces, the share targets, and explicitly excludes the others |
| "Push notifications" — silent on platforms (iOS / Android / web push), provider (self-hosted / vendor), opt-in flow, and content strategy. Each is a substantial sub-project. | SUSTAINED | A scope sentence naming platforms, provider choice, and the notification taxonomy in v1 vs. out-of-scope |
| "Onboarding rewrite" — "rewrite" implies replacing the current flow wholesale. Does this touch signup, activation, first-run education, or all three? Touches production auth/identity path. | SUSTAINED | A scope sentence naming exactly which onboarding steps are in-scope and which existing steps are explicitly preserved |
| 10% allocation to onboarding rewrite vs. "leaky funnel" framing | SUSTAINED | Evidence the funnel leak is small enough that a 10% capacity slice can plausibly move it; otherwise the allocation is theatre |
| 60% to shortlist driven by "we keep getting requests" — no business-value or customer-value framing per Product Rule B1 | SUSTAINED | A statement of the customer value AND business value the shortlist is expected to produce, with magnitude estimates |
| Plan does not declare what is NOT on the roadmap | SUSTAINED | An explicit "not doing this quarter" list — Product Principle 5 requires every "yes" carry an explicit "no" |

Six SUSTAINED items on B2 alone is a strong signal of plan-level under-specification.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| "Shareable shortlist will deliver value because users keep requesting it" — request volume → impact | **0.5** (anecdote / one-off observation) | Sample 20 requests in support/feedback channels: are users describing a workflow problem the shortlist solves, or asking for unrelated features and being lumped in? Owner: PM. | SUSTAINED — Confidence < 5, blocks APPROVE per skill |
| "Push notifications will move re-engagement" — assumes (a) install base has notifications enabled, (b) opt-in rate will be material, (c) content cadence won't increase churn | **0.1** (assertion — no evidence cited) | Pull current notification opt-in rates from comparable cohorts; check if push channel even exists; smoke-test message intent with 3–5 users | SUSTAINED — Confidence < 5, blocks APPROVE |
| "Onboarding rewrite will fix the leaky funnel" — assumes the leak is caused by onboarding UX, not by acquisition channel mismatch, value-prop confusion, or pricing | **0.1** (assertion) | Run funnel decomposition in analytics: where exactly is the drop-off? Talk to 5 users who churned in the funnel. Owner: PM + analytics. | SUSTAINED — Confidence < 5, blocks APPROVE |
| 60/30/10 capacity split is the right portfolio shape | **0.1** (assertion) | Justify against Product Rule B3 portfolio themes (differentiator / table-stakes / incremental / etc.) and Rule B5 cost-of-delay | SUSTAINED |

**All three named items are at Confidence ≤ 0.5 (opinion / anecdote). Per Product Rule B6, low-confidence items don't get a build slot — they get a validation slot.**

## B4 — Dependencies (Full)

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Push notification provider/infra (vendor evaluation, SDK integration, server-side dispatch service) | NOT NAMED | NOT CONFIRMED | SUSTAINED |
| Mobile platform sign-off (Apple/Google notification policy, entitlement provisioning) | NOT NAMED | NOT CONFIRMED | SUSTAINED |
| Analytics instrumentation for all three themes (success metrics require it) | NOT NAMED | NOT CONFIRMED | SUSTAINED |
| Onboarding rewrite touches auth/identity path → security & legal review (Universal Rule C7: shift-left) | NOT NAMED | NOT CONFIRMED | SUSTAINED |
| Design capacity for onboarding rewrite + shortlist UX work — 10% of one quarter is < 2 designer-weeks if shared | NOT NAMED | NOT CONFIRMED | SUSTAINED |

Universal Rule B7: "Cross-team dependencies are the single most common cause of missed commitments." None confirmed in writing.

## B5 — Reversibility + ADR pairing (Full)

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Push notification vendor selection — switching providers later requires re-instrumenting clients and migrating subscription tokens | NO | NO | SUSTAINED |
| Onboarding "rewrite" wholesale-replacement vs. progressive iteration — wholesale rewrite of an activation funnel is a one-way door (the old funnel and its analytics history are typically deprecated) | NO | NO | SUSTAINED |
| Notification taxonomy / topic schema — once users opt in to topic categories, restructuring later costs re-consent | NO | NO | SUSTAINED |
| Shortlist sharing model (URL structure, permalink semantics, public vs. private defaults) — public URLs become external dependencies | NO | NO | SUSTAINED |

Per Universal P3 and Rule B3, every one-way door requires named alternatives and an ADR. Zero of four named.

## B6 — Operability + success metrics (Full)

- Metrics: **absent** — no per-theme outcome metric named with baseline + target
- Alerts: **absent**
- Rollback path: **absent** (especially significant for onboarding-funnel changes — what if activation drops?)
- Runbook: **absent** (push notification dispatch is on-call surface)
- Capacity headroom: **absent** (push delivery infra has spike characteristics)
- User-visible outcome metric: **absent** — Product Principle 1 (outcomes, not outputs) and Rule A3 violated. "Re-engagement is flat" is a problem framing, not a target.

**SUSTAINED — blocks APPROVE per skill (operability concerns survive revert and are non-negotiable at Full tier).**

## B7 — Sequencing + capacity (Full)

- Critical path: **not surfaced.** Which theme blocks which? Does shortlist sharing depend on auth changes from onboarding rewrite? Does push reuse instrumentation from onboarding work?
- Appetite: stated as "next quarter" — this is a window, not an appetite per Shape Up / Universal Rule C5. Each theme needs its own time-budget cap.
- FTE consistency: 60/30/10 of *what* total? Number of engineers, designers, PMs not named. 10% of a small team ≈ noise; 10% of a large team ≈ a real slice. Cannot evaluate without it.
- Validation budget: per Product Rule C3, capacity should explicitly reserve % for validation/discovery. Not present.
- KTLO / on-call carve-out: not named.

**SUSTAINED.**

## B8 — Pre-mortem (Full)

Adopting prospective hindsight: it's end-of-quarter and the roadmap failed.

**Top 3 reasons, ranked by likelihood:**

1. **Push notifications shipped but moved nothing** — opt-in rate was ~15%, of those a fraction engaged with notifications, and re-engagement metric moved <1%. The team built infrastructure for a problem that wasn't notification-shaped (the actual cause of flat re-engagement was lack of new content / habit formation / cohort-specific churn). 30% of quarter spent; outcome unmoved. *Kill-switch:* before infra build, run a manual "fake door" — instrument a single notification through a hand-rolled channel to a 5% cohort and measure 14-day re-engagement lift. If <2pp, kill the theme.

2. **Onboarding "rewrite" at 10% allocation produced a half-rewrite that's neither the old flow nor a coherent new one.** Activation regressed because the half-built flow shipped to a partial cohort to "get learnings" and broke trust signals. *Kill-switch:* hard pre-commit that nothing onboarding-funnel ships without an A/B test holdout, AND a stop-loss rule (if activation drops >X% on the test arm for >Y days, auto-revert).

3. **Shortlist shipped on time, was used by a small power-user cohort, did not change retention or any business metric** — confirming the request volume was a vocal-minority signal rather than a population-level need. The team realised at end-of-quarter there was no success metric agreed in advance, so the debate about "did it work" is unresolved. *Kill-switch (for top-2 only — this one is a learning-loss not a delivery-loss).*

**Kill-switches named for top 2 per skill requirement.**

## Recommendation

**REVISE** — substantial structural defects across all gating buckets.

This is not an APPROVE-blocking nitpick set; it is a plan that does not yet meet the threshold of being a roadmap under PRODUCT_RULES. The plan is solution-first (Rule A2 violation), every theme is at Confidence ≤ 0.5 (Rule B6: should be in validation slots, not build slots), portfolio-theme classification is missing (Rule B3), capacity allocation is unanchored to actual FTE (Rule C3), every one-way door is undocumented (Rule B5 / Universal P3), operability is wholly absent (Rule A6), and success metrics are wholly absent (Principle 1 / Rule A3 / Rule D1). The Quick-tier reversibility carve-out does not apply: this is Full-tier, the plan touches production data paths (auth, funnel, notifications), and B5/B6 are SUSTAINED.

KILL was considered but rejected: the underlying problem-area instincts (re-engagement, activation, sharing) are plausibly worth pursuing, just not in this shape.

### Conditions before APPROVE

1. **Reframe each theme as a problem with measurable outcome** per Product Rule A2 format. Replace solution names ("shortlist", "push notifications", "onboarding rewrite") with outcome statements (e.g., "increase D30 retention of activated users by Xpp" — and then let solution discovery happen).
2. **Move all three themes from build slot to validation slot** until at least one passes Confidence ≥ 5 via spike, smoke test, fake-door, or analytics decomposition (Product Rule B6). Allocate validation budget explicitly (Rule C3).
3. **Run idea-triage** on each candidate theme to produce ICE scores with Confidence per Gilad scale and portfolio-theme classification per Rule B3. The 60/30/10 split should fall out of triage, not precede it.
4. **Decompose the funnel before approving an onboarding "rewrite"** — identify the specific failing step. A rewrite of the wrong step costs the same as the right step and yields nothing.
5. **Run a fake-door / single-cohort smoke test for push notifications** before infra commitment. Vendor selection is a one-way door — produce an ADR with at least 2 alternatives if/when that decision is made.
6. **Name the per-theme appetite as a fixed cap** (Universal Rule C1) and the actual FTE on each theme. "60% of what" must be a number.
7. **Add Operability section per Universal Rule A6** — at minimum, success metric + baseline + target + measurement window per theme; rollback story for onboarding; runbook stub for push.
8. **Add explicit "not doing this quarter" list** per Product Principle 5.
9. **Identify and confirm cross-team dependencies in writing** (analytics, security, mobile platform, design) per Universal Rule B7 before any theme enters "Now."
10. **Re-submit for plan-review** once 1–9 are addressed; a roadmap that survives this revision will be substantively different from the one submitted.

---

*Review per `skills/plan-review/SKILL.md` Full tier; B0–B8 executed.*
