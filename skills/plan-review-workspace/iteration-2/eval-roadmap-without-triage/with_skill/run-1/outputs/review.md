# Plan review: next-quarter-roadmap-3-themes

## Plan reference

Pasted prompt:

> Shape next-quarter roadmap with three themes — shareable shortlist, push notifications, onboarding rewrite — allocated 60/30/10 across them. The shareable shortlist is highest priority because we keep getting requests. Push notifications because re-engagement is flat. Onboarding rewrite because the funnel is leaky. Approve?

## Trigger check [GATE]

Trigger #1 fires: a roadmap has been produced and the owner is about to approve it ("Approve?"). Trigger #2 also fires: a quarterly roadmap by definition exceeds one day of execution. Trigger #4 auto-fires: an "onboarding rewrite" is a rewrite — touching the entry funnel for new users is a one-way-door class change (high blast radius on activation, hard to revert without churn). Proceeding.

## Inputs

- **Appetite**: one quarter (~13 weeks). Stated as a quarter, no per-theme appetite given. **Already a defect** — see B7.
- **Cynefin domain**: Complicated, leaning Complex. The themes are knowable with expertise, but each theme's outcome (sharing virality, re-engagement, activation) is emergent and behaviour-driven. A deterministic milestone plan will mis-fit Complex sub-domains.
- **Tier**: **Full** — auto-selected. Selecting attribute: appetite > 1 week (one quarter), and the onboarding rewrite is a one-way-door touching the activation funnel.

---

## B0 — Cynefin classification

Complicated overall, with the shortlist + onboarding sub-themes drifting into Complex (user behaviour, virality coefficients, activation curves are emergent, not deterministic). Push notifications is more squarely Complicated (known mechanics, knowable engagement uplift). Implication: the plan needs feedback loops, not fixed milestones, on at least two of the three themes.

---

## B1 — Problem framing [GATE]

**Verdict: SUSTAINED.**

The plan is solution-first across all three themes. Each theme is named as a feature ("shareable shortlist", "push notifications", "onboarding rewrite"), not as a problem with a measurable target outcome. Compare PRODUCT_RULES Rule A2 format: *"For [customer segment], we believe [problem] is causing [negative outcome]. If we solve it, we expect [measurable outcome] to improve by [target]."* None of the three themes is written this way.

The thin justifications offered are not problem statements:

- "we keep getting requests" — a demand signal, not a problem statement. Who is asking? For what job-to-be-done? What outcome do they fail to achieve today?
- "re-engagement is flat" — closer to a problem, but no segment, no baseline, no target.
- "the funnel is leaky" — a metaphor, not a measurement. Where in the funnel? How leaky? Compared to what?

**Falsifying condition (would prove this verdict wrong):** the owner produces a written problem statement per theme, each in Rule A2 format, with a named customer segment, a baseline metric value, and a target delta. Until then, the plan violates Universal P2 and Product P2 (items are problems, not solutions).

---

## B2 — Scope clarity [GATE]

| Item | Verdict | Falsifying condition |
|---|---|---|
| "Shareable shortlist" — sharing surface (channels: link, social, email, in-app?), recipient experience (logged-in vs. anon), permissions/privacy model, abuse/spam handling — none declared in scope | SUSTAINED | The plan names the share channels in scope, the recipient view spec, and the privacy/abuse policy decision |
| "Onboarding rewrite" — does this include sign-up, first-run experience, activation milestones, empty states, sample data, tutorials, or all of them? "Rewrite" is open-ended | SUSTAINED | The plan names the specific funnel steps being rewritten and which are explicitly out of scope |
| "Push notifications" — platform coverage (iOS/Android/web), permission-prompt strategy, content/templating system, frequency caps, opt-out flow, deliverability monitoring — none declared | SUSTAINED | The plan names which platforms, which notification categories, and the permission/consent strategy |
| "60/30/10 allocation" — allocation of what? Engineering FTE? Calendar weeks? Designer time? Product capacity? Implicit, expandable | SUSTAINED | The plan defines the unit of allocation and names the per-theme cap in that unit |
| "Highest priority" for shortlist — is this sequencing (do first), capacity (most FTE), or quality bar (most polish)? Vague enough to expand silently | PARTIAL | The plan distinguishes priority-as-sequence from priority-as-allocation |
| Cross-theme dependencies — push notifications likely depends on onboarding for permission-prompt timing; sharing likely depends on onboarding for empty-state triggers — undeclared | SUSTAINED | The plan surfaces inter-theme dependencies and sequences accordingly |

Six SUSTAINED/PARTIAL hits on a one-quarter plan. Scope is severely under-specified.

---

## B3 — Assumptions + evidence quality [GATE]

| # | Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|---|
| 1 | "We keep getting requests" → "shortlist sharing will move a meaningful business metric" | **0.5** — anecdotal request volume; no count, no segment, no link to retention/acquisition/revenue | Pull request log; count distinct requesters in last 90 days; segment by ARR or cohort. If <20 distinct requesters or all from one segment, downgrade priority | SUSTAINED |
| 2 | "Re-engagement is flat" → "push notifications will lift re-engagement" | **0.1** — opinion-grade leap; no evidence push specifically (vs. email, in-app, lifecycle content) is the right lever | Run a 1-week lifecycle email A/B as a cheaper proxy; or pull industry benchmarks for push uplift in similar product categories. Without this, the plan commits 30% of capacity to an unvalidated lever | SUSTAINED |
| 3 | "The funnel is leaky" → "a rewrite (vs. targeted fixes) is the right intervention" | **0.1** — diagnosis (leak) does not imply prescription (rewrite). Rewrite is the most expensive intervention available and the assumption that it's the right one is unstated | Pull funnel-step conversion rates; identify the worst step; test a single targeted fix on that step (1-week experiment) before committing to rewrite | SUSTAINED |
| 4 (implicit) | "60/30/10 is the right allocation" — allocation chosen by perceived priority, not by expected ICE × confidence | **0.1** — opinion | Score each theme via idea-triage / ICE before locking allocation. Allocation should fall out of scoring, not precede it | SUSTAINED |
| 5 (implicit) | "These three themes are the top three problems worth solving this quarter" — no other candidates considered, no opportunity cost stated | **0.1** — opinion | Produce the candidate list (≥6 problems considered) and the elimination rationale | SUSTAINED |

All five riskiest assumptions sit at 0.1–0.5 Confidence. **Per the skill rule: untested assumptions with Confidence < 5 block APPROVE.** Five do.

---

## B4 — Dependencies [GATE, Full only]

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Push notifications: APNs/FCM credentials, deliverability infra, mobile platform team capacity | Not named | Not named | SUSTAINED |
| Push notifications: legal/privacy review for permission-prompt copy + consent storage (GDPR/CCPA) | Not named | Not named | SUSTAINED |
| Shareable shortlist: backend permissions model (who can see what), abuse/spam tooling, possibly a public-link service | Not named | Not named | SUSTAINED |
| Onboarding rewrite: design capacity, copy/content capacity, analytics instrumentation for new funnel steps | Not named | Not named | SUSTAINED |
| Cross-theme: shared analytics platform must support new event taxonomy across all three themes | Not named | Not named | SUSTAINED |
| Onboarding rewrite: dependency on existing experiments/feature flags — rewriting onboarding while live experiments run is a coordination burden | Not named | Not named | SUSTAINED |

Six unconfirmed dependencies. Per Universal Rule B7, unconfirmed cross-team dependencies are the single most common cause of missed commitments. The plan has surfaced none.

---

## B5 — Reversibility + ADR pairing [GATE, Full only]

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Onboarding rewrite — rewriting the activation funnel touches the entry experience for every new user; reverting after weeks of live traffic means re-confusing returning new users and losing instrumentation continuity | No alternatives named (e.g. targeted-fix sequence, A/B'd partial rewrite, JTBD-driven redesign of one step) | No ADR | SUSTAINED |
| Push notifications — a botched permission-prompt strategy permanently denies push consent on iOS for users who decline; that decision is recoverable only via re-prompt flows that add friction | No alternatives named (lifecycle email first, in-app messaging first, soft-prompt vs. native-prompt strategy) | No ADR | SUSTAINED |
| Shareable shortlist — the URL/permissions model is a public contract; once external links exist in the wild, schema changes require redirects forever | No alternatives named (private share-by-email vs. public link, signed URLs vs. opaque IDs) | No ADR | SUSTAINED |
| 60/30/10 allocation lock for the quarter — committing capacity in advance with no kill-switch is itself a one-way door against the bets that turn out to be wrong | No alternative named (e.g. allocate 60% to discovery first, then commit; or stage-gate at week 4) | No ADR | SUSTAINED |

Four undocumented one-way doors. Each is a silent commitment per Agentic P7.

---

## B6 — Operability + success metrics [GATE, Full only]

- **Metrics**: absent. No metric named per theme.
- **Alerts**: absent. No deliverability/error-budget posture for push notifications, no funnel-regression alarm for onboarding.
- **Rollback path**: absent. Onboarding rewrite has no rollback strategy; push has no opt-out-of-rollout mechanism named.
- **Runbook**: absent.
- **Capacity headroom**: absent. 60/30/10 sums to 100% — no reserve for KTLO, validation, incident response, or opportunistic work. PRODUCT_RULES Rule C3 requires explicit reserve.
- **User-visible outcome metric**: **absent on all three themes.** Per Product P1 (outcomes, not outputs) and Rule A3, every roadmap item ships with a measurable success criterion. None of the three themes has one. "We keep getting requests" is not an outcome metric. "Re-engagement is flat" hints at one but no baseline/target is named. "Funnel is leaky" hints but no metric.

**Verdict: SUSTAINED on all six dimensions.** Operability section is entirely absent. This alone blocks APPROVE.

---

## B7 — Sequencing + capacity (Full only)

- **Critical path**: not surfaced. The plan implies parallel execution across three themes, but does not name what blocks what. Onboarding rewrite likely needs to land *before* push permission-prompt strategy is finalised (push opt-in often happens during onboarding); shortlist likely needs onboarding event hooks for empty-state triggers.
- **Appetite**: a quarter, total. Per-theme appetite is implied by allocation but not stated as a fixed cap. "60% of a quarter" is ~7.8 weeks of allocated capacity for shortlist — but is that the cap or the target? Per Universal Rule C1, appetite must be a cap.
- **FTE consistency**: unverifiable. The plan states an allocation but not the team size, so 60% of unknown capacity is unknown work. PRODUCT_RULES Rule C3: capacity allocation must be explicit.
- **No discovery/validation slot**: 60/30/10 is fully build allocation. PRODUCT_RULES Rule C3 explicitly requires a reserve for validation. Given the Confidence scores in B3, the plan needs a *substantial* discovery slot before any build slot is justified — not zero.
- **No KTLO reserve**: see B6.

**Verdict: SUSTAINED.**

---

## B8 — Pre-mortem (Full)

Adopt prospective hindsight — assume the plan shipped and failed by end of quarter. Top 3 reasons ranked by likelihood:

1. **Onboarding rewrite slipped past appetite and shortlist's empty-state hook is blocked.** The rewrite turned out to be three rewrites (sign-up + first-run + activation milestones) because scope was never bounded. Mid-quarter, onboarding is half-rebuilt and half-original, instrumentation is split, and the shortlist team is waiting on event hooks that don't exist yet. Outcome: nothing ships completely; activation regresses temporarily on the half-rebuilt cohort.
   - **Kill-switch:** at week 4, if onboarding rewrite has not landed a single funnel-step replacement end-to-end behind a flag, freeze it and revert to targeted fixes on the worst-converting step.

2. **Push notification permission-prompt strategy backfires; iOS opt-in rate is below 30%.** Prompt copy, timing, and pre-prompt flow were not designed; the platform team shipped the native prompt at app open, users declined, and the consent rate makes the channel useless for the re-engagement use case it was supposed to serve. The 30% capacity allocated to push produced a feature that doesn't reach enough users to move re-engagement. Permission decline is permanent on iOS without re-prompt flows.
   - **Kill-switch:** at week 6 (mid-rollout), if 7-day push opt-in among new users is <40%, halt rollout and pivot to lifecycle email/in-app messaging for the re-engagement goal.

3. **The shortlist ships, gets shared by ~5% of users, but doesn't move acquisition or retention** — because "we keep getting requests" came from a small, vocal segment whose needs don't generalise. Sixty percent of the quarter is spent on a feature that delights its requesters and has no measurable broader business impact. (This is the canonical Cagan build-trap outcome.)
   - **Kill-switch:** before build, demand the request-log analysis from B3-#1. If <20 distinct requesters or single-segment, downgrade allocation.

---

## Recommendation

**KILL** — and re-shape via `idea-triage` + roadmap shaping before re-submitting.

Rationale: this is not a roadmap; it is a list of three solution names with a percentage split. Per PRODUCT_RULES Rule A2/A3/A6, none of the three items is in roadmap-eligible form (no problem statement, no outcome metric, no confidence). Per Universal Rule A4, no NFR target exists. Per B3, all five riskiest assumptions sit at Confidence 0.1–0.5; PRODUCT_RULES Rule B6 says low-confidence items don't get a build slot — they get a validation slot. Per B5, four undocumented one-way doors. Per B6, operability section entirely absent. The plan asks for approval to commit a quarter of capacity to bets whose evidence-grade is at or near opinion. Approving it would commit the team to the canonical build-trap pattern.

KILL is the correct verdict (rather than REVISE) because the issues are not local fixes to a sound plan — the plan's premise (allocate capacity by perceived priority across pre-named features) is itself the defect. The path forward is to start over with problems, not solutions.

### Conditions before re-submission as a roadmap

1. Run `idea-triage` on each theme to produce: problem statement (Rule A2), customer segment, outcome metric with baseline + target (Rule A3), Confidence score (Gilad), portfolio-theme classification (Rule B3), Kano classification (Rule B4), and ICE score (Rule B2).
2. For each theme with Confidence < 5, replace its build slot with a time-boxed validation slot (Rule B6). The B3 5-minute tests above are the starting set.
3. Surface and confirm in writing the six dependencies in B4 with named owners and capacity windows.
4. Write an ADR per one-way door in B5 with alternatives considered and reversal cost.
5. Add operability per theme: outcome metric, alerts, rollback path, runbook ownership.
6. Reserve explicit capacity for KTLO and discovery (Rule C3). 60/30/10 summing to 100% is incorrect.
7. State the appetite per theme as a fixed cap (Rule C1), with named kill-switch conditions at the appetite midpoint.
8. Surface the candidate set that produced these three themes and the elimination rationale (Principle 5: every yes requires an explicit no).

Until these are addressed, the quarterly commit is unsafe.
