# Plan review: add-not-null-user-tier-backfill

## Plan reference

> "Add NOT NULL column user_tier to users table (50M rows), backfill from subscription_status during deploy, ship in next release."

## Inputs

- **Appetite**: unstated (no fixed cap provided)
- **Cynefin domain**: Complicated — schema migration patterns are knowable with expertise, but the specific risk profile (50M rows, backfill sequencing, NOT NULL constraint) requires deliberate engineering analysis
- **Tier**: Full — auto-selected: plan contains a one-way-door schema migration and touches production data (50M-row table)

---

## Step 1a — Fast-track gate

**Did not fire.** Precondition 2 fails: the plan modifies production schema and backfills 50M production rows. A one-commit revert does not restore prior state without a second migration. Fall-through to full review.

---

## B1 — Problem framing

The plan opens with a solution: "add NOT NULL column user_tier." No problem statement is present. There is no named user or business outcome, no measurable target, and no explanation of why this column is needed now.

**Verdict: SUSTAINED**

Falsifying condition: the plan is revised to open with the problem (e.g., "tier-based feature gating fails because user_tier is not stored on the users record, causing X behaviour for Y users") and a measurable outcome target before B1 can be OVERTURNED.

---

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| Backfill of 50M rows will perform a full sequential scan and may hold row-level locks for minutes or hours, affecting read/write performance on the users table during deploy | SUSTAINED | A batched-backfill plan exists (e.g. background job in chunks of N rows) and the lock strategy is documented |
| The deploy sequence couples three atomic operations (schema change + backfill + release) that each carry independent failure modes — the plan treats them as one step | SUSTAINED | A phased sequence is stated: e.g. (1) add column nullable + default, (2) backfill offline, (3) add NOT NULL constraint, (4) release application code |
| Application code that writes to the users table must handle the new NOT NULL column before the constraint is applied — this is not mentioned in the plan | SUSTAINED | The plan names which application paths write to users and confirms they are updated and deployed before the constraint is applied |
| "During deploy" is too vague to bound the backfill window — it could mean seconds or hours | SUSTAINED | The plan specifies a maximum acceptable backfill duration and a procedure if that window is exceeded |
| "From subscription_status" assumes a deterministic, total mapping — nulls, unknown values, and multi-value cases are not addressed | SUSTAINED | The plan states the mapping rules, names what happens for each edge case (null, unknown, multiple active subscriptions), and confirms no rows will be left unmappable |
| "Next release" is not an appetite — it is a delivery label with no time cap or reversibility window | PARTIAL | A fixed appetite (e.g. "within one sprint") is stated and an explicit go/no-go date is named |

---

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| Backfill can complete within the deploy window without causing lock escalation, replication lag, or user-visible degradation | 0.1 — pure assertion, no measurement | Run `EXPLAIN ANALYZE` on the proposed backfill query against a production-sized staging replica; measure lock duration and lag on replica | SUSTAINED — untested assumption with Confidence < 5 blocks APPROVE |
| subscription_status → user_tier mapping is total: every row in users has a subscription_status value that maps unambiguously to exactly one user_tier | 0.1 — unstated assumption | `SELECT COUNT(*) FROM users WHERE subscription_status IS NULL OR subscription_status NOT IN (<mapped values>);` — must return 0 before migration proceeds | SUSTAINED — untested assumption with Confidence < 5 blocks APPROVE |
| All application code paths that INSERT or UPDATE users are updated to supply user_tier before the NOT NULL constraint is applied | 0.1 — not mentioned in plan | Grep all ORM/SQL callers of users table; confirm each is updated; run integration tests against a schema with the constraint applied | SUSTAINED — untested assumption with Confidence < 5 blocks APPROVE |

---

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| DBA or infra team to execute migration safely on production (batching strategy, lock monitoring, replica lag watch) | No — not mentioned | No | SUSTAINED |
| Application engineers owning all write paths to users table to update their code before constraint is applied | No — not mentioned | No | SUSTAINED |
| Subscription service as authoritative source for the subscription_status → user_tier mapping | No — not confirmed in writing | No | SUSTAINED |

---

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Adding a NOT NULL column to a 50M-row table — rolling back requires a second DDL migration and a second deploy, and may not be feasible mid-deploy if backfill has partially run | No alternatives named | No ADR exists or committed | SUSTAINED |
| Coupling schema migration + backfill + release into a single deploy — if the backfill fails partway, the column exists with a NOT NULL constraint and partially-filled data; rollback is non-trivial | No alternatives named | No ADR | SUSTAINED |

Alternatives that should have been considered and named:
- **Expand-contract / parallel-change pattern**: add column nullable first with a default, deploy application code, backfill offline in background batches, then apply NOT NULL constraint in a separate migration once all rows are filled and all writers supply the value.
- **Shadow table + view**: write to a separate user_tiers table initially, join at read time, migrate later.
- **Feature flag gate**: gate tier-based logic on the application side until the column is reliably populated, decoupling the schema change from the feature launch.

---

## B6 — Operability + success metrics

- **Metrics**: absent — no query performance metric, no backfill progress metric, no error rate on writes to users table
- **Alerts**: absent — no alert on replication lag spike, no alert on query duration regression, no alert on backfill failure
- **Rollback path**: absent — no procedure stated for if the migration fails mid-backfill; NOT NULL + partial fill = broken state with no stated recovery
- **Runbook**: absent
- **Capacity headroom**: absent — 50M rows, no stated estimate of backfill duration, no stated I/O headroom on the database host
- **User-visible outcome metric**: absent — no outcome metric stated (what user behaviour or business metric does adding user_tier improve, and how will we confirm it moved?)

All six operability items are absent. This blocks APPROVE under B6.

---

## B7 — Sequencing + capacity

The stated sequence — add NOT NULL column + backfill during deploy + ship — is the most dangerous ordering for this class of change.

Critical path issues:
1. The NOT NULL constraint is applied before the backfill is confirmed complete. Any row not yet backfilled will fail the constraint.
2. The application release is coupled to the schema change. Old application code deployed during the migration window will fail writes if it does not supply user_tier.
3. No appetite is stated as a fixed cap. "Next release" does not bound the work.

The correct critical path for a migration of this class is:
1. (Schema) Add column nullable with a safe default → deploy → confirm no regressions
2. (Backfill) Run batched offline backfill → confirm 0 rows unmapped
3. (Constraint) Apply NOT NULL constraint → confirm
4. (Application) Deploy code that supplies user_tier on all write paths → confirm
5. (Cleanup) Remove default if appropriate

No single step in this sequence should be coupled to the others in one deploy.

---

## B8 — Pre-mortem

**Assume the plan shipped and failed within its appetite. Top 3 failure modes:**

**1. Table lock / replication lag causes production outage during backfill (Likelihood: High)**
A single `UPDATE users SET user_tier = ... WHERE ...` against 50M rows acquires row locks for the duration. On PostgreSQL this will not escalate to a table lock but will generate enormous WAL, spike replication lag on replicas, and degrade all concurrent reads/writes on the users table for minutes to hours. On MySQL with ALGORITHM=COPY the table is locked for the full duration.
Kill-switch: run `EXPLAIN ANALYZE` on the backfill query on a production-sized replica before any production run; abort if estimated duration exceeds the maintenance window.

**2. NOT NULL constraint applied before all writers are updated causes write failures on the old code path (Likelihood: High)**
During a rolling deploy, old application instances continue writing to users without supplying user_tier. The NOT NULL constraint immediately causes INSERT/UPDATE failures on those paths. This is a live production write failure, not a data-quality issue.
Kill-switch: confirm zero old-code instances are running before applying the NOT NULL constraint; use a feature flag or separate deploy to enforce ordering.

**3. subscription_status has nulls or unmapped values — backfill fails partway, leaving the column in a partially-filled state with a NOT NULL constraint (Likelihood: Medium)**
If any row has a subscription_status value not covered by the mapping, the backfill UPDATE either sets user_tier to NULL (violating the NOT NULL constraint) or raises an error partway through. If the constraint was already applied, the table is now in a broken state: some rows have user_tier, some do not, and new writes that don't supply user_tier will fail.
Kill-switch: validate the mapping is total (`SELECT COUNT(*) ... WHERE subscription_status NOT IN (...)` = 0) before any DDL runs.

---

## Recommendation

**KILL** — the plan's execution sequence is structurally unsafe for a 50M-row production table. The coupling of NOT NULL DDL + backfill + release into a single deploy creates a failure mode (partial backfill + constraint violation + write failures on old code) that has no stated rollback path and could cause a live production write outage.

This is not a REVISE verdict because the problem is not a missing detail — it is a wrong execution model. The plan must be rebuilt around the expand-contract migration pattern before it can be reviewed again.

### Conditions to move from KILL to REVISE

The plan must satisfy all of the following before it re-enters review:

1. **B1**: Opens with a problem statement and a measurable outcome target.
2. **B2**: States a phased sequence (nullable + default → backfill → constraint → application code) — no single-deploy coupling.
3. **B3**: Provides evidence (not assertion) that:
   - Backfill duration is acceptable (measured on a production-sized replica)
   - Mapping is total (zero unmapped rows confirmed by query)
   - All application write paths are identified and updated
4. **B4**: Names owners for DBA execution, application code changes, and subscription service mapping confirmation — all confirmed in writing.
5. **B5**: Records at least two alternatives considered (expand-contract, shadow table) with reversal cost for the chosen approach; commits to writing an ADR.
6. **B6**: Names: backfill progress metric, replication lag alert, write-error-rate alert, rollback procedure for each phase, and a user-visible outcome metric.
7. **B7**: States a fixed appetite for each phase; names the go/no-go check at each phase boundary.
