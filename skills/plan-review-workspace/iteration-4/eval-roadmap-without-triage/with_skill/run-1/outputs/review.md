# Plan review: next-quarter-roadmap-3-themes

## Plan reference
Pasted in conversation: "shape next-quarter roadmap with three themes — shareable shortlist, push notifications, onboarding rewrite — allocated 60/30/10 across them. The shareable shortlist is highest priority because we keep getting requests. Push notifications because re-engagement is flat. Onboarding rewrite because the funnel is leaky."

## Inputs
- **Appetite**: one quarter (≈12 weeks) — fixed cap implied by "next-quarter roadmap"
- **Cynefin domain**: Complicated — known cause-effect chains exist (re-engagement, funnel conversion, shortlist demand) but require expertise and feedback loops to validate; not a Clear checklist domain.
- **Tier**: Full — selected because appetite >>1 week and the plan implies multiple cross-team dependencies (notification infra, funnel instrumentation, shortlist UX) plus likely production-data and one-way-door touches (push notification provider lock-in, onboarding routing).

Trigger fired: owner is about to approve a plan ("Approve?"); auto-fire on appetite > 1 day.

Step 1a fast-track gate: does NOT fire. This is roadmap shaping, not KTLO; appetite >1 day; multi-week themes are not one-commit-revertible. Falling through to normal flow.

## B1 — Problem framing
**Verdict: SUSTAINED.** The plan is solution-first across all three themes. "Shareable shortlist," "push notifications," and "onboarding rewrite" are features, not problems. Per Universal P2 and Product Rule A2, each item should read "For [segment], we believe [problem] is causing [outcome]. If we solve it, [metric] will improve by [target]." The given justifications ("we keep getting requests", "re-engagement is flat", "funnel is leaky") are signals, not problem statements with measurable targets. Falsifying condition: produce three statements in the Rule A2 form, each naming a customer segment, an observable problem, and a numeric outcome target — if those exist and I missed them, the verdict overturns.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| "Onboarding rewrite" — implies touching auth, first-run, activation analytics, possibly billing/trial logic; none declared | SUSTAINED | Plan names the specific flows in/out of scope (e.g. "signup form + first 3 screens; not auth, not trial conversion") |
| "Push notifications" — silent on iOS/Android/web split, opt-in flow, provider choice, deep-link infra | SUSTAINED | Plan declares platform scope, opt-in scope, and whether deep-link routing is in or out |
| "Shareable shortlist" — silent on persistence model, public vs. authed sharing, abuse/moderation, SEO surface | SUSTAINED | Plan declares share-link scope (public-URL vs. authed), persistence layer, and moderation posture |
| 60/30/10 allocation — vague: % of FTE? engineering only? includes design/PM? | PARTIAL | Allocation restated as named FTE-weeks per theme against a stated capacity baseline |
| "Highest priority" for shortlist — undefined whether priority means sequence, capacity share, or stop-gate | PARTIAL | Plan defines "priority" operationally (does shortlist block the others, or just consume the largest slice?) |
| No KTLO/operational reserve called out — implies 100% of capacity goes to themes | SUSTAINED | Plan names KTLO and discovery/validation reserve per Product Rule C3 |

Three SUSTAINED items on a quarter-scale plan; B2 is doing real work here.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| "We keep getting requests" → users will actually use a shareable shortlist enough to move a metric | 0.5 (anecdote) | Pull request count + segmenting users; or ship a fake-door "Share" button and measure clicks for 1 week | SUSTAINED |
| "Re-engagement is flat" → push notifications will fix it (causal claim, not just correlated) | 0.1 (opinion / unverified causal leap) | Name the specific re-engagement metric, current value, and the mechanism by which push moves it; cite one comparable case study or smoke-test result | SUSTAINED |
| "Funnel is leaky" → an onboarding *rewrite* is the right intervention vs. targeted fixes at the leakiest step | 0.1 (opinion) | Funnel breakdown by step + drop-off rates; identify the single biggest leak before committing to "rewrite" framing | SUSTAINED |
| Implicit: 60/30/10 is the right capacity split given relative impact and confidence | 0.1 (assertion) | Run ICE per theme (Product Rule B2) and let the scores drive allocation, not the other way round | SUSTAINED |
| Implicit: team has the capacity for three concurrent themes without context-switching cost | 0.1 (assertion) | Compare against last quarter's actual delivered work; subtract KTLO and on-call load | SUSTAINED |

All five are below Confidence 5; all block APPROVE per the gate. Universal P4 and Product P4.

## B4 — Dependencies (Full)

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Push notification provider (APNs/FCM/vendor like OneSignal/Braze) | Not named | Not named | SUSTAINED |
| Mobile app release cadence (push needs client-side support and store review) | Not named | Not named | SUSTAINED |
| Analytics/instrumentation team for funnel measurement (onboarding) | Not named | Not named | SUSTAINED |
| Design capacity for three themes in one quarter | Not named | Not named | SUSTAINED |
| Legal/privacy review for push opt-in (GDPR/ePrivacy notification consent) | Not named | Not named | SUSTAINED |
| Sharing surface — SEO, link preview (OG tags), abuse reporting if public | Not named | Not named | SUSTAINED |

Universal Rule B7: unconfirmed cross-team dependencies are the single most common cause of missed commitments. Six unconfirmed deps on a quarter-scale plan is a load-bearing concern.

## B5 — Reversibility + ADR pairing (Full)

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Push notification vendor choice (Braze/OneSignal/Iterable/in-house) — switching costs are high once user tokens, segmentation, and templates exist | No | No | SUSTAINED |
| Shareable shortlist URL/persistence schema — public URLs, once minted, are forever (link rot, SEO, abuse, GDPR delete) | No | No | SUSTAINED |
| Onboarding "rewrite" — replacing the funnel rather than iterating on it discards the calibration data baked into the current flow | No | No | SUSTAINED |

Three undocumented one-way doors. Universal P3 and Rule B3: name the alternatives or commit to ADRs before approval. Agentic P7: artefact memory matters — without ADRs, the next agent has no model of why these were chosen.

## B6 — Operability + success metrics (Full)

- Metrics: **absent** — no theme names a target metric or a current baseline
- Alerts: **absent**
- Rollback path: **absent** — particularly acute for push (notification storm risk) and onboarding (can't easily roll back if mid-quarter cohorts started in the new flow)
- Runbook: **absent**
- Capacity headroom: **absent** — no operational reserve declared
- User-visible outcome metric: **absent on all three themes**. "Re-engagement is flat" and "funnel is leaky" are present-state observations, not target outcomes. Per Product P1 and Rule A3, every roadmap item ships with a metric, current value, and target.

Absence on both halves blocks APPROVE. This is the single biggest defect in the plan: no theme has a definition-of-done in outcome terms, so there is no way to know mid-quarter whether to continue, pivot, or kill.

## B7 — Sequencing + capacity (Full)

- **Critical path**: not surfaced. Which theme blocks which? Does push depend on a mobile release cycle that gates the other two? Is the funnel instrumentation a precondition for measuring whether the onboarding rewrite worked?
- **Appetite**: nominally one quarter, but no per-theme appetite given. "60/30/10" is an allocation, not an appetite. Per Universal Rule C1 / Product Rule C1, each theme needs a fixed time cap.
- **FTE consistency**: undeclared. Three concurrent themes against a real team probably means each theme runs at ~⅓ velocity due to context-switching unless explicitly siloed; the plan does not address this.
- **No discovery slot**: per Product Rule B6, low-confidence items should occupy a validation slot, not a build slot. All three themes are currently low-confidence (B3) and would warrant validation work first.

## B8 — Pre-mortem

Prospective-hindsight: it is end-of-quarter and the roadmap has failed.

1. **Most likely failure (push notifications)**: the team built the infrastructure and shipped notifications, but re-engagement did not move because the underlying cause of flat re-engagement was content/value, not notification frequency. Post-mortem reveals the team never tested the causal assumption. **Kill-switch**: 2-week smoke test using existing channels (email push, in-app banner) to test whether *any* re-engagement nudge moves the metric, before building the push infrastructure.
2. **Second most likely (onboarding rewrite)**: the rewrite shipped to new cohorts mid-quarter; activation got *worse* because the new flow optimised for a different metric than the old one was implicitly tuned for. Plan included no A/B harness, so the team cannot cleanly attribute. **Kill-switch**: A/B test the rewrite against current onboarding for a hold-out cohort; do not roll out 100% until the test reads positive on the named activation metric.
3. **Third (shortlist)**: built the feature, usage was modest (~5% of users), no measurable lift on any business metric, but the team called it "done" because it shipped. Classic feature-factory outcome (Product P10).

Quick-tier reversibility carve-out: does NOT apply. This is Full-tier; auto-select attributes (appetite, dependencies, one-way doors) preclude reversibility carve-out.

## Recommendation

**REVISE** — the plan currently fails B1 (problem framing), B2 (scope), B3 (assumptions/confidence), B4 (dependencies), B5 (reversibility/ADRs), and B6 (operability + outcome metrics). It is a list of features with a percentage allocation, not a roadmap of problems-to-solve with confidence-weighted bets. Do not approve in current form.

### Conditions

Before re-review, the plan must:

1. **Reframe each theme as a problem statement** in the Product Rule A2 form: "For [segment], we believe [problem] causes [negative outcome]. If solved, [metric] will improve by [target]." Three rewritten items, each with a named customer segment and numeric target.
2. **Attach a Confidence score (Gilad scale) and an evidence trail** to each theme. Anything below Confidence 5 enters a **validation slot**, not a build slot (Product Rule B6). Likely outcome: at least two of the three themes need a 1–2-week discovery sprint before earning a build commitment.
3. **Run ICE scoring** (Impact × Confidence × Ease) per Product Rule B2 and let the scores justify the 60/30/10 allocation — or change the allocation to match the scores. "We keep getting requests" is not an Impact argument.
4. **Declare capacity allocation explicitly** per Product Rule C3: % to themes, % to KTLO, % to validation/discovery. The current plan implies 100% to themes, which is a known anti-pattern.
5. **Name the one-way doors and commit to ADRs** before build starts: push vendor choice; shortlist URL/persistence schema; onboarding "rewrite vs. iterate" decision. List alternatives considered for each (Universal Rule B3, Agentic P7).
6. **Surface and confirm the six cross-team dependencies in B4** in writing with named owners and capacity windows (Universal Rule B7). Particular attention to mobile release cadence (push) and design capacity (all three).
7. **Define operability per theme** (Universal Rule A6): for push, the rollback story for a notification storm; for onboarding, the A/B harness and cohort hold-out plan; for shortlist, the abuse/moderation/GDPR-delete posture.
8. **Define success metrics with current baselines and targets** per Product Rule A3. Each theme gets a single primary outcome metric, a current value, a target, and a measurement window. Without this, the post-launch impact review (Product Rule D1) is impossible to run.
9. **Set per-theme appetites as fixed caps** (Product Rule C1, Universal Rule C1) and surface the critical path between themes. Whichever theme depends on funnel instrumentation must sequence after that instrumentation lands.
10. **Run pde-idea-triage** on each theme before re-review — the symptoms above (solution-first framing, missing problem statements, undeclared confidence) are exactly what the triage gate exists to catch upstream of roadmap shaping.

If the conditions above produce a plan with all three themes still warranting build slots, re-run plan-review at Full tier. The likely outcome is that one theme survives as a build commitment, one moves to a validation slot, and one is sent back to the idea bank pending evidence.
