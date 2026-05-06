# Plan review: next-quarter-roadmap-three-themes

## Plan reference

Pasted excerpt (no path provided):

> "Review this plan before I approve it: shape next-quarter roadmap with three themes — shareable shortlist, push notifications, onboarding rewrite — allocated 60/30/10 across them. The shareable shortlist is highest priority because we keep getting requests. Push notifications because re-engagement is flat. Onboarding rewrite because the funnel is leaky. Approve?"

## Inputs

- **Appetite**: "next-quarter" — implied ~12 weeks but stated as a horizon, not a fixed cap. No per-theme appetite given. SUSTAINED gap.
- **Cynefin domain**: Complicated — three product bets in a known organisation; cause-effect is knowable with discovery work and customer evidence, not emergent. (If the team has not done that discovery, the domain is closer to Complex and the plan should include feedback loops, which it does not.)
- **Tier**: **Full** — selected because plan appetite > 1 week (a full quarter), and the plan implies cross-team dependencies (push notification platform, onboarding which usually touches auth/identity/marketing copy) that warrant B4–B7.

## Trigger check

Trigger 1 fires: a plan has been produced and the owner is asking for approval ("Approve?"). Trigger 2 fires: appetite > 1 day. Proceeding.

## B0 — Cynefin classification

Complicated. Review emphasises dependencies, evidence quality, and named outcome metrics. Flagging that without per-theme discovery evidence, this drifts toward Complex — at which point deterministic milestones like "60/30/10 allocation" are themselves a defect.

## B1 — Problem framing [GATE]

The plan opens with **solutions**, not problems. Three feature themes are named ("shareable shortlist", "push notifications", "onboarding rewrite") with one-line justifications attached after the fact. PRODUCT_RULES Rule A2 requires every roadmap item to be framed as: *"For [customer segment], we believe [problem] is causing [negative outcome]. If we solve it, we expect [measurable outcome] to improve by [target]."*

None of the three themes are framed this way. "We keep getting requests", "re-engagement is flat", "funnel is leaky" are signals, not problem statements with target metrics. Universal P2 also violated: design starts with the stack/feature, not the problem.

**Verdict: SUSTAINED.** Falsifying condition: plan author can produce a written problem statement per theme in the A2 format with a named customer segment, named target metric, and quantified target — *no record cited in plan text — falsifies if plan author can produce one.*

## B2 — Scope clarity [GATE]

Plan declares three themes and a 60/30/10 split. Nothing else is declared in or out of scope.

| Item | Verdict | Falsifying condition |
|---|---|---|
| "Onboarding rewrite" — likely touches auth, signup, identity, marketing copy, analytics events, possibly billing if trial logic is involved. None named. | SUSTAINED | Plan author produces a scoped surface list naming which onboarding screens/services are touched and which are explicitly out of scope. *No record cited in plan text — falsifies if plan author can produce one.* |
| "Push notifications" — implies a notification platform decision (vendor or in-house), permission UX, opt-in flow, analytics, possibly background workers. None named. | SUSTAINED | Plan author cites an existing notification capability or names the build/buy decision. *No record cited in plan text — falsifies if plan author can produce one.* |
| "Shareable shortlist" — sharing implies auth on shared links, privacy model, abuse vectors (link enumeration), possibly SEO/preview generation. None named. | SUSTAINED | Plan author cites a privacy/abuse model and naming whether shared links are public, signed, or auth-gated. *No record cited in plan text — falsifies if plan author can produce one.* |
| "60/30/10 allocation" — vague: of FTE? of engineering weeks? does it include validation work, KTLO, on-call? PRODUCT_RULES Rule C3 requires explicit capacity allocation including KTLO + validation reserve. | SUSTAINED | Plan author produces a capacity table with KTLO % and validation/discovery % named. *No record cited in plan text — falsifies if plan author can produce one.* |
| "Themes" vs "items" — PRODUCT_RULES Rule B3 requires portfolio-theme classification (Differentiator / Table-stakes / Incremental / etc.). The three labels in the plan are feature buckets, not portfolio themes. | SUSTAINED | Plan author maps each theme to a Doshi portfolio class. *No record cited in plan text — falsifies if plan author can produce one.* |
| "Highest priority" for shortlist based on "we keep getting requests" — silently expands the prioritisation logic from evidence to volume-of-asks. PRODUCT_RULES Rule B7 explicitly rejects "customers asked for it" as a standalone argument. | SUSTAINED | Plan author shows ICE scoring or equivalent for the three themes, not request volume. *No record cited in plan text — falsifies if plan author can produce one.* |

Six SUSTAINED in B2. This is a high-defect plan on scope alone.

## B3 — Assumptions + evidence quality [GATE]

Three implicit assumptions, all untested in the plan text.

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| "Shareable shortlist will move a metric we care about because we keep getting requests" — request volume is anecdotal demand signal, not evidence of impact. | **0.5** (anecdote) | 5-min: name the requesters, the metric expected to move, the size of segment affected, and an existing benchmark from any similar feature. Owner: PM. | SUSTAINED |
| "Push notifications will lift re-engagement because re-engagement is flat" — assumes the cause of flatness is *absence of pushes*, not content quality, retention curve, or product-market fit. | **0.1** (assumption) | 5-min: cite which cohort's re-engagement is flat, what hypothesis links the flatness to push absence, and what a benchmark uplift looks like from comparable products. Owner: data/PM. | SUSTAINED |
| "Onboarding rewrite will fix the leaky funnel" — assumes a *rewrite* (full re-do) is the right intervention vs. a targeted fix on the leakiest step. Universal Rule B1 (smallest solution): a full rewrite is an enormous solution to an unspecified problem. | **0.1** (assumption) | 5-min: name the specific funnel step(s) leaking, the drop-off rate, the hypothesised cause, and the smallest test that would validate the cause. Owner: PM/data. | SUSTAINED |

All three Confidence scores are below the 5 threshold. PRODUCT_RULES Rule B6 says low-confidence items get a validation slot, not a build slot. **None of the three themes currently qualify for a build slot under the project's own rules.**

## B4 — Dependencies (Full) [GATE]

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Push notification platform (build/buy + APNs/FCM credentials, opt-in UX) | Not named | Not named | SUSTAINED — *no record cited in plan text — falsifies if plan author can produce one.* |
| Onboarding touches identity/auth (likely) and marketing copy (almost certain) | Not named | Not named | SUSTAINED — *no record cited in plan text — falsifies if plan author can produce one.* |
| Sharing model — privacy review, possibly legal sign-off on PII in shared links | Not named | Not named | SUSTAINED — *no record cited in plan text — falsifies if plan author can produce one.* |
| Data/analytics owner to define and instrument outcome metrics for all three | Not named | Not named | SUSTAINED — *no record cited in plan text — falsifies if plan author can produce one.* |

Universal Rule B7: unconfirmed dependencies are the single most common cause of missed commitments. Four unconfirmed dependencies on a quarter-long plan is a structural red flag.

## B5 — Reversibility + ADR pairing (Full) [GATE]

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Push notification platform/vendor choice (vendor lock-in is a classic one-way door) | No | No | SUSTAINED — *no record cited in plan text — falsifies if plan author can produce one.* |
| Sharing privacy model (public vs signed vs auth-gated — once shipped publicly, retracting is user-visible churn) | No | No | SUSTAINED — *no record cited in plan text — falsifies if plan author can produce one.* |
| "Onboarding rewrite" implies replacing rather than incrementing — a wholesale replacement of a live funnel is a high-blast-radius change | No | No | SUSTAINED — *no record cited in plan text — falsifies if plan author can produce one.* |

Three undocumented one-way doors. Universal P3, Rule B3 violated on each.

## B6 — Operability + success metrics (Full) [GATE]

- Metrics: **absent** — no outcome metrics named for any theme.
- Alerts: **absent**.
- Rollback path: **absent** (especially load-bearing for the onboarding rewrite, which can tank acquisition silently).
- Runbook: **absent**.
- Capacity headroom: **absent**.
- User-visible outcome metric per theme: **absent** for all three.

PRODUCT_RULES Rule A3 requires every roadmap item to carry a measurable success criterion. Universal Rule A6 requires an Operability section. Both fail on every theme. Product P1 (outcomes, not outputs): the plan reads as a list of outputs. SUSTAINED across the board.

## B7 — Sequencing + capacity (Full)

- **Critical path**: not surfaced. Onboarding rewrite likely needs analytics in place *first* to measure the leak it claims to fix. Push notifications likely need an opt-in built in onboarding, creating a sequencing dependency between two of the three themes that the plan does not acknowledge.
- **Appetite**: "next quarter" is a horizon, not a cap. Per-theme appetites absent. PRODUCT_RULES Rule C1 requires an appetite per item. Universal Principle 8 (small batches): a quarter-long un-broken-down theme is a big-batch failure mode.
- **FTE consistency**: "60/30/10" is not a capacity allocation; it is a ratio. Not validated against actual team FTE. KTLO and validation reserve missing (Rule C3).

SUSTAINED on all three sub-points.

## B8 — Pre-mortem (Full — top 3)

Assume the quarter has ended and the plan failed. Most likely failure modes, ranked:

1. **Onboarding rewrite ships, funnel does not improve, root cause turns out to be a single step (e.g. email verification or paywall placement) that a targeted fix would have addressed in 1 week.** The "rewrite" framing pre-committed the team to a large solution before the problem was diagnosed. Universal Rule B1 violation realised. **Kill-switch**: at week 2, require a one-page funnel-step diagnosis showing the specific step(s) responsible for >70% of the leak. If the diagnosis identifies a single step, abandon "rewrite" framing and cut scope to the targeted fix.

2. **Push notifications ship, re-engagement does not lift, because the flat re-engagement was a content/retention problem, not a notification-absence problem. Notification permission opt-in rates come in below industry benchmark (~40-60%), capping any uplift to a fraction of the user base.** **Kill-switch**: before any build, run a manual outbound test (email or in-app banner to the inactive cohort) and measure return-rate uplift. If that uplift is <X%, the push channel is not the bottleneck and the work is killed.

3. Shareable shortlist ships to the requesting users, but those users are a small vocal minority; the feature does not move retention or growth metrics for the broader base; it adds surface area (privacy review, abuse handling, link rot) that consumes ongoing capacity without commensurate return. (No kill-switch named — this is the third-ranked risk; per the skill, only the top 2 require kill-switches.)

## Recommendation

**REVISE — bordering on KILL.** The plan is solution-first across all three themes (B1 SUSTAINED), has six SUSTAINED scope defects (B2), three sub-5 Confidence assumptions (B3), four unconfirmed dependencies (B4), three undocumented one-way doors (B5), zero operability or outcome metrics (B6), no per-theme appetite or critical path (B7), and a pre-mortem that surfaces a high-likelihood failure on every theme.

This is not an approval blocker that can be patched with a few notes. The plan as stated is a list of features with ratios, not a roadmap of problems with outcomes. Under PRODUCT_RULES the plan does not currently meet the bar to occupy a Now slot for any of its three themes. KILL is on the table; REVISE is offered because the underlying *problems* (sharing demand, retention flatness, funnel leak) may well be real — they just have not been framed, evidenced, or scoped yet.

### Conditions (must satisfy before APPROVE)

1. **Re-frame each theme as a problem statement** in PRODUCT_RULES A2 format with a named customer segment, named outcome metric, and quantified target. Solutions held loosely; problems held tightly.
2. **Run idea-triage** on each of the three themes before they re-enter the roadmap, producing an ICE score and Confidence scores. Themes with Confidence < 5 go to a validation slot (Rule B6), not a build slot.
3. **Map each theme to a portfolio class** (Doshi, Rule B3) and state the explicit capacity allocation including KTLO and validation reserve (Rule C3) — not a 60/30/10 ratio in isolation.
4. **Set per-theme appetites** as fixed caps, not "the quarter" (Rule C1). Surface the critical path linking analytics → onboarding instrumentation → push opt-in flow.
5. **List dependencies and confirm owners in writing** for the four named in B4 (push platform, identity/auth, marketing copy, privacy/legal, data/analytics owner).
6. **Write ADR-equivalents** for the three one-way doors in B5 (notification vendor, sharing privacy model, onboarding replace-vs-iterate) including alternatives considered.
7. **Add an Operability section** per theme: outcome metric, alert, rollback path, capacity headroom (Rule A6).
8. **Pre-validate the highest-risk assumption per theme** with a 5-minute test or a short discovery spike before any build slot is committed.

Until at least conditions 1–3 are met, the plan should not occupy a Now slot. Conditions 4–8 must be met before high-integrity commitment (Rule C2).
