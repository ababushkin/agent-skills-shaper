# Plan review: schema-migration-user-tier

## Plan reference

Pasted excerpt (the only available input):

> "Review this plan: add NOT NULL column user_tier to users table (50M rows), backfill from subscription_status during deploy, ship in next release. Approve?"

## Inputs

- **Appetite**: Not stated in plan. Plan says "ship in next release" — release cadence not specified, no fixed cap. Treated as **unspecified** for review purposes; this is itself a SUSTAINED finding under B7.
- **Cynefin domain**: **Complicated** — schema migration on a 50M-row production table is a knowable problem with expert practice (online DDL, dual-write, backfill batching), but emergent failure modes (lock contention, replication lag, app-server crash on NOT NULL violation during deploy) push toward the Complex edge. Review emphasises dependencies, reversibility, and operability.
- **Tier**: **Full** — selected because the plan touches production data AND contains at least one one-way door (schema migration on a 50M-row table). Auto-fire condition #4 from the When-to-use section triggers.

## Trigger check

Triggers fired:
1. Plan contains a one-way-door decision (schema migration on production users table). **Auto-fire.**
2. Plan touches production data (users table, 50M rows). **Auto-fire.**
3. Owner is about to approve ("Approve?").

Three triggers; gate passed; proceeding.

## B0 — Cynefin classification

Complicated, leaning Complex. See Inputs.

## B1 — Problem framing

The plan opens with a solution ("add NOT NULL column user_tier"), not a problem. There is no statement of:

- Which user or business outcome motivates introducing a `user_tier` column
- Why the existing `subscription_status` is insufficient (if the backfill is from `subscription_status`, the column may be a denormalisation — but the plan does not say so, and does not name the outcome)
- A measurable target the change is meant to move

**Verdict: SUSTAINED.**
**Falsifying condition:** A revised plan that opens with "For [user/business segment], we believe [problem with current state] is causing [negative outcome]. Adding `user_tier` is the chosen solution because [why this over alternatives]. Success metric: [observable, measurable]." If such a problem statement exists in a doc not shown to the reviewer, citing it overturns the verdict.

(Universal P2; Rule A2; Product P1.)

## B2 — Scope clarity

The plan declares three things in scope: add column, backfill from subscription_status, ship next release. It does NOT declare any of the following, which it nevertheless touches:

| Item | Verdict | Falsifying condition |
|---|---|---|
| Application code that reads/writes the `users` table — every ORM model, every raw SQL path, every read replica consumer must tolerate the new column or the NOT NULL constraint will reject inserts mid-deploy | SUSTAINED | A list of every code path that writes to `users`, with confirmation each tolerates `user_tier` (or has a default). Without that list, the NOT NULL clause is a production-incident generator. |
| Replica lag and read-after-write consistency during backfill — backfilling 50M rows generates replication traffic that can saturate replicas, breaking dependent services | SUSTAINED | A named replica-lag SLO during backfill, with a measured backfill batch size and pacing strategy that holds lag under it. |
| Downstream consumers of `subscription_status` semantics — if `user_tier` is derived from `subscription_status`, any future change to `subscription_status` definitions silently desynchronises `user_tier`. Drift is not addressed. | SUSTAINED | A named owner of the `subscription_status` → `user_tier` mapping, plus a reconciliation job (or a documented decision that drift is acceptable). |
| "during deploy" — backfilling 50M rows during a deploy is not in-scope of any normal release process; it implies an extended deploy window, an in-flight migration, or a deploy that holds open while DDL runs | SUSTAINED | A named deploy-window duration, with the DDL strategy (online? blocking? pt-online-schema-change? Postgres `ADD COLUMN` with default? `ADD COLUMN ... NULL` then UPDATE then `SET NOT NULL`?) explicit. |
| Rollback path — adding a NOT NULL column is reversible (drop column), but rolling back app code that depends on the column after the column is dropped requires a multi-step coordinated rollback. The plan implies single-step rollback. | SUSTAINED | A documented multi-step rollback (expand-contract): step 1 deploys app tolerant of column-present-or-absent; step 2 adds nullable column; step 3 backfills; step 4 sets NOT NULL; rollback unwinds each step. |
| Vague phrase "ship in next release" — release cadence not named; "next release" can be days or weeks | SUSTAINED | A fixed appetite (e.g. "5 working days, single release window"). |

Six SUSTAINED items on a plan with appetite >1 day. The plan is solution-shaped (one sentence) but touches a wide surface area.

## B3 — Assumptions + evidence quality

Riskiest assumptions extracted:

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| Every user in the 50M-row `users` table has a `subscription_status` value that maps cleanly to a non-null `user_tier`. (If any user has NULL or an unmapped `subscription_status`, the NOT NULL backfill fails and either aborts or produces silent fallbacks.) | **0.1** — assertion only; no data cited | `SELECT COUNT(*) FROM users WHERE subscription_status IS NULL OR subscription_status NOT IN (<known mappings>);` Run against production read replica. Sign-off: data engineering owner. | SUSTAINED — block APPROVE |
| Backfill "during deploy" is operationally feasible — the deploy window can hold open long enough to backfill 50M rows without timing out, locking the table for writes, or saturating replicas. | **0.1** — assertion only | Time a backfill of 1M rows on a staging clone with production-shaped data; multiply by 50; compare to deploy-window SLA. Sign-off: SRE / on-call lead. | SUSTAINED — block APPROVE |
| The application can be deployed atomically with the schema change — i.e. there is no window during which old app code (unaware of `user_tier`) inserts a row without a value, hitting the NOT NULL constraint. | **0.1** — assertion only; the plan does not describe an expand-contract sequence | Confirm deploy strategy is expand-contract: column added nullable first, app deployed to write the column, backfill runs, then NOT NULL is applied. Sign-off: backend lead. | SUSTAINED — block APPROVE |

All three assumptions sit at Confidence 0.1 (opinion / assertion). The skill's gate is explicit: untested assumptions with Confidence < 5 block APPROVE.

(Universal P4; Agentic P2; Product P4.)

## B4 — Dependencies (Full)

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| DBA / database operator — must execute or approve the DDL on a 50M-row table; must hold a maintenance window | Not in plan | Not in plan | SUSTAINED |
| SRE / on-call — must be staffed for the deploy window, with rollback authority; backfill-related replica saturation may page | Not in plan | Not in plan | SUSTAINED |
| Backend team owning the `users` ORM model — must ship app code that handles the column before NOT NULL applies | Not in plan | Not in plan | SUSTAINED |
| Owners of every other service that reads from `users` (analytics, auth, billing, audit pipelines) — must tolerate the new column and not break on schema diff | Not in plan | Not in plan | SUSTAINED |
| Data team owning `subscription_status` semantics — must confirm the mapping and own the drift question | Not in plan | Not in plan | SUSTAINED |

Five unconfirmed dependencies on a one-way-door change. (Universal Rule B7: unconfirmed cross-team dependencies are the single most common cause of missed commitments.)

**Falsifying condition (per row):** A written confirmation from the named owner that they are aware of the change, have capacity in the deploy window, and have signed off on their part.

## B5 — Reversibility + ADR pairing (Full)

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Adding a denormalised `user_tier` column derived from `subscription_status` (instead of computing the tier at read time, materialising in a view, or putting it in a separate `user_tier` table) | No | No | SUSTAINED |
| Making the column NOT NULL (vs. nullable with default, vs. enum-with-"unknown" sentinel) | No | No | SUSTAINED |
| Backfilling "during deploy" (vs. backfill-before-deploy, vs. lazy backfill on read, vs. dual-write with reconcile) | No | No | SUSTAINED |

The reversal cost of a NOT NULL schema change is non-trivial: dropping the column once application code depends on it requires coordinated rollback of app + schema + backfill. The plan names no alternatives and no ADR.

**Falsifying condition:** An ADR (Nygard format: Context / Decision / Consequences) covering at least these three decisions, with alternatives named and reversal cost documented. (Universal P3, Rule B3; Agentic P7.)

## B6 — Operability + success metrics (Full)

- **Metrics**: Absent. No named DB-side metrics (lock duration, replica lag, rows-per-second backfill rate, error rate on `users` writes), no named app-side metrics.
- **Alerts**: Absent. No alert thresholds named for the deploy window or post-deploy.
- **Rollback path**: Absent. The plan implies single-step ship; expand-contract not named.
- **Runbook**: Absent. On-call has no document for "what does it look like when this fails at 3am."
- **Capacity headroom**: Absent. No statement of replica capacity, primary write capacity, or deploy-window slack.
- **User-visible outcome metric**: Absent. The plan names no outcome the change is meant to move — see B1.

**Verdict: SUSTAINED on every line.** Operability blocks APPROVE on Full tier per skill rules.

**Falsifying condition:** A revised plan with each of the six items named, with thresholds and owners.

(Universal Rule A6; Universal P1, P6; Product P1.)

## B7 — Sequencing + capacity

- **Critical path surfaced?** No. The plan does not name what blocks what — DDL before app deploy? App deploy before DDL? Backfill before NOT NULL? The "during deploy" phrase elides all of this.
- **Appetite fixed?** No. "Ship in next release" is not a fixed cap; it is a hope. Per skill rules, "an appetite of '2–4 weeks' is not an appetite; it is a hope" — "next release" is worse.
- **Team FTE consistent with appetite?** Cannot evaluate without an appetite. SUSTAINED on the appetite question alone.

**Verdict: SUSTAINED.**
**Falsifying condition:** A written sequence — "Day 1: deploy app tolerant of column. Day 2: ADD COLUMN nullable. Day 3–5: backfill in batches of N rows/sec. Day 6: SET NOT NULL. Each step has a rollback step." — with the appetite fixed at a specific number of working days.

## B8 — Pre-mortem (Full)

Adopting prospective hindsight: assume the plan shipped and failed within its (unstated) appetite. Top 3 reasons by likelihood:

1. **The deploy window held open while backfill ran on 50M rows; replica lag exceeded SLO; downstream services (auth, billing, analytics) read stale data; an authentication-adjacent service returned wrong tier values to paying customers; on-call was paged before the backfill completed; rolling back required undoing a partial backfill.** This is the highest-likelihood failure because the plan's "backfill during deploy" phrase compresses three operationally distinct things into one.
   - **Kill-switch condition:** Replica lag exceeds X seconds during backfill OR backfill rate drops below Y rows/sec for >2 minutes → pause backfill, hold deploy, escalate to SRE before continuing.

2. **A subset of users had NULL or unmapped `subscription_status` values; the backfill failed mid-run on those rows; the team patched by inserting a default ("free"); the default silently mis-tagged paying customers as free-tier; a billing audit caught it three weeks later.** High likelihood because B3 assumption #1 sits at Confidence 0.1.
   - **Kill-switch condition:** Pre-deploy query `SELECT COUNT(*) FROM users WHERE subscription_status IS NULL OR subscription_status NOT IN (<mapping>)` returns >0 → block deploy until mapping is complete or fallback is explicitly named and approved.

3. **Old app code (deployed before the migration window closed) inserted a new user row without a `user_tier` value; the NOT NULL constraint rejected the insert; user signups failed for the duration of the deploy window; the failure mode was visible only in error logs and not in the deploy dashboard.** Medium likelihood because the plan does not name an expand-contract sequence; without it, this is the default failure.
   - (Kill-switch not required for top 2 only, but: any insert error rate on `users` exceeding baseline triggers immediate rollback.)

## Recommendation

**REVISE — strong lean to KILL if revisions are not produced.**

The plan as written has zero unresolved sustaining gates passed. Every required Full-tier bucket (B1, B2, B3, B4, B5, B6, B7) returned at least one SUSTAINED verdict. The plan's core premise (a NOT NULL schema change on a 50M-row production table backfilled "during deploy") is not impossible — it is a known, executable change — but the plan as stated does not contain the artefacts that would make it safe to approve.

KILL is reserved for plans whose core premise fails. Here the premise is recoverable: a revised plan with a problem statement, an expand-contract sequence, an ADR for the three one-way-door decisions, confirmed dependencies, and an operability section would be approvable. **REVISE** is therefore the correct verdict, with the conditions below.

### Conditions (must be satisfied before APPROVE)

1. **B1 — Problem statement.** Replace the solution-first opening with: target user/business outcome, why `user_tier` (vs. computing from `subscription_status` at read time), and a measurable success metric.
2. **B2 — Scope.** Enumerate every code path that writes to `users`. Name a deploy strategy (expand-contract or equivalent). Name the replica-lag SLO during backfill. Name the drift-management plan for `subscription_status` → `user_tier`. Replace "ship in next release" with a fixed appetite in working days.
3. **B3 — Assumptions.** Run all three 5-minute tests (NULL/unmapped count, backfill rate on staging clone, expand-contract confirmation). Raise each assumption's Confidence to ≥5 before approval.
4. **B4 — Dependencies.** Get written confirmation from each of the five named owners (DBA, SRE, backend lead, downstream-service owners, data owner of `subscription_status`).
5. **B5 — ADR.** Write one ADR covering the three one-way-door decisions, with alternatives named.
6. **B6 — Operability.** Name metrics, alerts, rollback path, runbook, capacity headroom, and a user-visible outcome metric.
7. **B7 — Sequencing.** Publish the day-by-day sequence with explicit rollback at each step.
8. **B8 — Kill-switches.** Wire the two named kill-switch conditions into the deploy tooling, not just the plan document.

If any of conditions 1–7 cannot be satisfied within the appetite the team can actually commit to, the verdict escalates from REVISE to KILL — and the team should adopt a different strategy (e.g. nullable column, lazy backfill, no NOT NULL until reconciliation completes).
