# Plan review: add-user-tier-column

## Plan reference

Pasted plan: "Add NOT NULL column `user_tier` to `users` table (50M rows), backfill from `subscription_status` during deploy, ship in next release."

## Trigger check

Auto-fire trigger #4: schema migration on production data (`users` table, 50M rows). Touches one-way-door territory (column add + NOT NULL constraint + backfill of production data). Trigger fires unambiguously.

## Step 1a — Fast-track gate

Does NOT fire. Precondition #2 (fully reversible) fails: a NOT NULL column add on 50M rows is not a one-commit revert (data has been written, downstream consumers may already read the new column, the migration may have taken locks). Precondition #1 (KTLO class) also fails: schema migrations are explicitly not in the KTLO carve-out list. Fall through to normal flow.

## Inputs

- **Appetite**: unstated — "ship in next release" is a window, not a fixed cap. Appetite is itself a SUSTAINED finding.
- **Cynefin domain**: Complicated. Cause-effect is knowable with database expertise; standard hazards (long locks, replication lag, NOT NULL on populated table) have known mitigations.
- **Tier**: Full — selected because the plan touches production data + schema migration (auto-select condition).

## B0 — Cynefin

Complicated. Emphasise dependencies, reversibility, and operational risk.

## B1 — Problem framing

**SUSTAINED.** The plan opens with a solution (add a column, backfill from `subscription_status`), not a problem. There is no statement of why `user_tier` is needed, what user/business outcome it enables, or why it cannot be derived on read from `subscription_status` (which is already the backfill source — implying the data already exists). If `user_tier` is fully derivable from `subscription_status`, the plan may be adding a denormalised column that creates a permanent consistency-maintenance burden for no behavioural gain.

**Falsifying condition:** owner produces a written problem statement naming (a) the consumer that needs `user_tier` as a stored column, (b) why a derived column / view / app-layer mapping is insufficient, and (c) the user-visible outcome this enables.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| Long-running ALTER TABLE on 50M rows during deploy — locks, replication lag, deploy timeout | SUSTAINED | Plan names the migration tool (gh-ost, pt-osc, Strong Migrations gem, Postgres `ADD COLUMN ... DEFAULT` non-blocking path) and lock/lag budget |
| `subscription_status` → `user_tier` mapping logic — undefined; what values map to what tiers, what about NULL/unknown/cancelled/past-due states | SUSTAINED | Plan includes the explicit value mapping table, including the default for unmappable rows |
| Application code that reads/writes `users` during deploy — dual-write, model validations expecting the new NOT NULL column before backfill completes | SUSTAINED | Plan sequences app deploy vs. migration vs. backfill (expand-migrate-contract pattern named) |
| "During deploy" backfill — is the deploy gated on backfill completion? Backfilling 50M rows in a deploy window is implausible at any reasonable batch rate | SUSTAINED | Plan names backfill mechanism (background job, batched), expected duration, and what happens if deploy completes before backfill |
| Read replicas, analytics warehouse, ETL consumers of `users` | PARTIAL | Plan acknowledges downstream consumers and either confirms compatibility or sequences updates |
| Indexes on `user_tier` — if any consumer queries by tier, missing index = full scan on 50M rows | PARTIAL | Plan names whether `user_tier` will be indexed and how the index is built (CONCURRENTLY) |

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| `ALTER TABLE … ADD COLUMN user_tier NOT NULL` is feasible during a deploy window on 50M rows | 0.1 (assertion) | Run on a restored production snapshot; measure duration + lock behaviour. Owner: DBA / platform sign-off. | SUSTAINED |
| Every existing row has a `subscription_status` value that maps cleanly to a non-null `user_tier` | 0.1 | `SELECT subscription_status, COUNT(*) FROM users GROUP BY 1` — 30 seconds. Confirms there is no NULL/unknown/legacy bucket that breaks NOT NULL. | SUSTAINED |
| The deploy can complete with the migration in-band (no separate maintenance window or staged rollout) | 0.1 | Stage the migration on a replica + measure. Owner: SRE. | SUSTAINED |

All three assumptions sit at Confidence 0.1 (assertion). Per Step 6, untested assumptions with Confidence < 5 block APPROVE.

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| DBA / platform team — review of migration plan, lock/lag budget approval | No | No | SUSTAINED |
| SRE / on-call — deploy-window coordination, rollback rehearsal | No | No | SUSTAINED |
| Data / analytics — downstream consumers of `users` schema | No | No | SUSTAINED |
| Application teams that write to `users` — dual-write coordination during expand phase | No | No | SUSTAINED |

No dependency owner is named in the plan. This is the single most common cause of missed commitments (Universal Rule B7).

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Schema change on production `users` table — column drop is reversible but data changes (backfill) are not, and any downstream read of `user_tier` makes the column drop a breaking change | No | No | SUSTAINED |
| NOT NULL constraint as the initial state — vs. nullable + backfill + add NOT NULL later (expand-migrate-contract) | No | No | SUSTAINED |
| Stored denormalisation of a derivable value — vs. computed column / view / app-layer mapping | No | No | SUSTAINED |

No alternatives are named. No ADR. The plan commits to a one-way door without recording why the one-way door was chosen over the documented safer pattern (expand-migrate-contract: add nullable, dual-write, backfill in batches, verify, then add NOT NULL).

## B6 — Operability + success metrics

- **Metrics**: absent. No migration-progress metric, no backfill-rows-completed metric, no replication-lag alarm.
- **Alerts**: absent. No alarm for long-running migration, replication lag breach, or backfill stall.
- **Rollback path**: absent. "Backfill during deploy" with NOT NULL implies that a mid-deploy failure leaves the schema in a partially-applied state. There is no described rollback for a half-completed backfill or a failed `ALTER`.
- **Runbook**: absent. On-call has no documented response to "migration is hung at 70%" or "replication lag exceeded threshold."
- **Capacity headroom**: absent. No estimate of additional disk (column add doubles row width during rewrite on some engines), I/O, or replica lag impact.
- **User-visible outcome metric**: absent. No statement of what user behaviour or business metric `user_tier` enables and how that will be measured post-launch (Product P1).

Operability absence on a Full-tier plan blocks APPROVE per Step 9.

## B7 — Sequencing + capacity

Critical path is not surfaced. Appetite is "next release" — a window, not a cap. There is no FTE estimate. The implicit sequence (single-step migrate-and-backfill in the deploy) is the sequence the rest of this review argues against; the safer sequence (expand → backfill → verify → contract) is multi-release and not acknowledged.

## B8 — Pre-mortem

Assume the plan shipped and failed within the appetite. Top 3 reasons ranked by likelihood:

1. **The deploy times out / rolls back mid-migration.** `ALTER TABLE ... ADD COLUMN ... NOT NULL DEFAULT <expr>` on 50M rows takes long enough to exceed deploy-timeout windows or hold locks long enough to break the application. Half-applied state requires manual DBA recovery.
   - **Kill-switch:** restored-snapshot rehearsal of the migration on production-sized data; if duration > deploy budget, abort and reshape to expand-migrate-contract before scheduling.
2. **NOT NULL violation during backfill** — at least one row's `subscription_status` doesn't map to a defined `user_tier` value (NULL, legacy enum, unknown future state); migration aborts or backfill leaves rows that violate the constraint when it is added.
   - **Kill-switch:** pre-flight `SELECT subscription_status, COUNT(*) FROM users GROUP BY 1` and a written mapping table covering every observed value, with an explicit fallback bucket. Run before migration is scheduled.
3. **Replication lag spike takes read replicas out of service** — the long-running write blocks replication, application reads start failing or returning stale data, on-call has no runbook.

## Recommendation

**REVISE.**

Multiple SUSTAINED verdicts on B1 (problem framing absent), B2 (scope), B3 (all three Confidence-0.1 assumptions), B4 (no dependency owners confirmed), B5 (one-way door without alternatives or ADR), and B6 (operability entirely absent). The Quick-tier reversibility carve-out does not apply — a NOT NULL schema change with backfill on 50M rows is, by construction, not fully reversible.

### Conditions

Before APPROVE, the plan must:

1. **State the problem.** Why `user_tier` as a stored column rather than derived from `subscription_status`? Name the consumer and the user/business outcome.
2. **Reshape to expand-migrate-contract.** Add the column nullable; deploy. Backfill in batches with progress metric; verify zero unmapped rows. Add NOT NULL in a separate migration. Three releases, not one.
3. **Provide the value mapping.** Run the audit query against current `subscription_status` distribution; produce the explicit mapping table including a fallback for unmappable values.
4. **Rehearse on a restored snapshot.** Measure migration duration, lock behaviour, and replication lag on production-sized data. Get DBA sign-off.
5. **Name owners.** DBA, SRE, data/analytics, and any application team that writes to `users` must be named and have confirmed capacity within the appetite.
6. **Write the ADR.** Record the alternatives considered (single-step migration vs. expand-migrate-contract vs. derived column / view) and why the chosen approach wins. Per Universal Rule A3 + Agentic P7.
7. **Add the operability section.** Migration-progress metric, replication-lag alert, rollback path for each phase (including half-completed backfill), on-call runbook, capacity headroom estimate, and a user-visible outcome metric tied to the original problem statement.
8. **Convert appetite to a fixed cap.** "Next release" is a window; pick a date or a fixed engineering-week budget.

Do not ship the plan as written.
