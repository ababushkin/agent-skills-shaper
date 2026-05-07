# Plan review: add-not-null-user-tier-50m-rows

## Plan reference

> "add NOT NULL column user_tier to users table (50M rows), backfill from subscription_status during deploy, ship in next release. Approve?"

## Inputs

- **Appetite**: unstated (plan implies single release cycle; treated as ≤1 week for tier selection)
- **Cynefin domain**: Complicated — cause-effect is knowable with expertise, but the sequencing of a NOT NULL migration on a large table is non-trivial and failure modes are well-documented
- **Tier**: Full — selected because: (1) schema migration = one-way door, (2) production data touched (50M live rows), (3) backfill during deploy = tight coupling of schema and data change

**Fast-track gate**: did not fire. Precondition 2 fails (not fully reversible — NOT NULL column addition in most DB engines requires a table rewrite or lock; dropping the column post-ship loses data). Precondition 1 also fails (not KTLO — this is a schema change with data migration logic).

---

## B1 — Problem framing

**SUSTAINED.**

The plan opens with a solution: "add NOT NULL column user_tier." There is no problem statement. The following are absent:

- What user or business outcome this column enables
- What is currently broken or missing without it
- What measurable target would tell us the migration succeeded from a product perspective

A plan that begins with a column name has already committed to a solution before the problem is visible. This matters here because the riskiest attribute of the plan — backfilling from `subscription_status` during deploy — is a consequence of a design choice, not a requirement. An alternative design (nullable column, application-layer default, separate backfill job) might satisfy the same underlying need with a safer execution path.

**Falsifying condition**: the plan is revised to open with a problem statement of the form "users currently have no `user_tier` attribute, which prevents [specific capability] from working for [specific user segment]; the goal is [measurable outcome]." If that statement exists and the NOT NULL + inline backfill approach is the only feasible approach given the stated constraints, B1 is OVERTURNED.

---

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| Table lock / AccessExclusive lock during ALTER TABLE on 50M rows | SUSTAINED | Plan explicitly states lock strategy (e.g. `ADD COLUMN ... DEFAULT` in Postgres 11+ avoids rewrite; or migration tool like `pt-online-schema-change` / `gh-ost` is named) |
| Application behaviour during migration window (reads/writes hitting the table while backfill is in progress) | SUSTAINED | Plan names the in-flight state: does the app handle rows where `user_tier` IS NULL during the backfill phase, or is a feature flag suppressing reads until backfill completes? |
| Backfill logic correctness — what happens when `subscription_status` is NULL, empty, or contains a value with no mapping to a valid `user_tier` | SUSTAINED | Plan defines the mapping exhaustively and names the behaviour for unmapped values (fail, default, skip) |
| Rollback strategy for the column itself once it ships and data is live | SUSTAINED | Plan names rollback path — column can only be removed with a subsequent migration; is that acceptable, and what is the plan if the backfill produced bad data? |

Zero of the four items above are declared in scope in the plan. The plan names only two moves: "add column" and "backfill during deploy." All four items are execution-critical.

---

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| Backfill of 50M rows completes within the deploy window without causing replication lag, lock contention, or timeout | 0.1 — assertion; no timing data cited | Run `EXPLAIN ANALYZE` on the backfill query against a production-scale copy; measure rows/sec; divide into 50M; compare to deploy window length. Owner: DBA / infra lead. | SUSTAINED — untested, Confidence < 5 |
| Every row in `users` has a non-NULL `subscription_status` value that maps cleanly to a valid `user_tier` | 0.1 — assertion; no data quality audit cited | `SELECT COUNT(*) FROM users WHERE subscription_status IS NULL OR subscription_status NOT IN (<valid values>)` run against production read replica before migration. Owner: whoever owns the backfill query. | SUSTAINED — untested, Confidence < 5 |
| Adding a NOT NULL column with a backfill is safe to run inline during a standard deploy (no table rewrite, no prolonged lock, no deadlock with concurrent writes) | 0.1 — assertion; DB engine version and migration strategy not stated | Name DB engine + version; verify whether `ADD COLUMN ... DEFAULT` avoids full rewrite (Postgres ≥11 does for non-volatile defaults; MySQL/MariaDB differs); cite migration tool if used. Owner: DBA. | SUSTAINED — untested, Confidence < 5 |

All three highest-risk assumptions carry Confidence 0.1. None have a named owner or a committed pre-execution test. Per B3 gate rules, all three block APPROVE.

---

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| DBA / infrastructure team (lock strategy, migration tool selection, production timing window) | No — not named in plan | No | SUSTAINED |
| Deploy pipeline (backfill must be sequenced relative to app code deploy; wrong order causes NOT NULL constraint violations on insert) | No — deploy order not specified | No | SUSTAINED |
| Application code change (app must write `user_tier` on new inserts before or simultaneously with the constraint going live; or the column needs a DB-level default during transition) | No — no app-layer change is mentioned | No | SUSTAINED |

The plan implicitly requires at least three coordinated actors. None are named. The most dangerous unconfirmed dependency is the application code: if new rows are inserted after the NOT NULL constraint is added but before the app code populates `user_tier`, every insert fails. The plan does not address this at all.

---

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| NOT NULL constraint on 50M-row production table (requires migration to remove; data already backfilled cannot be un-backfilled without a new job) | No alternatives named | No ADR | SUSTAINED |
| Backfill from `subscription_status` during deploy (couples schema migration and data migration into a single deploy event; failure mid-deploy leaves table in a partially-backfilled inconsistent state) | No alternatives named | No ADR | SUSTAINED |

**Alternatives not considered:**

1. **Nullable column first, NOT NULL constraint later.** Add `user_tier NULL`, backfill as a separate offline job with batching and rate limiting, then add the constraint once 100% of rows are populated and verified. Decouples schema change from data migration; each step is independently reversible.
2. **DB-level DEFAULT + application-layer NOT NULL.** Add the column with a DB-level default (e.g. `DEFAULT 'free'`) so existing rows get a value atomically; enforce NOT NULL at the application layer first; drop the default later once backfill is verified. Avoids backfill during deploy entirely.
3. **Online schema change tool** (`pt-online-schema-change`, `gh-ost`). Builds shadow table, migrates with low lock time, cuts over atomically. Standard for large tables.

None of these are named in the plan. A one-way door with no alternatives recorded is an undocumented commitment. Per B5 gate rules, this blocks APPROVE.

---

## B6 — Operability + success metrics

- **Metrics**: absent. No replication lag monitoring, no row-count progress tracking during backfill, no error rate on inserts post-deploy.
- **Alerts**: absent. No alert named for constraint violation errors on insert, which is the primary failure mode if app code is not coordinated.
- **Rollback path**: absent. The plan does not name what happens if backfill fails at 40M rows, or if post-deploy monitoring reveals bad data. Dropping a NOT NULL column is a subsequent migration; bad backfill data requires a data correction job. Neither is planned.
- **Runbook**: absent. No on-call guidance for the deploy window: what to watch, what constitutes abort, who has the kill switch.
- **Capacity headroom**: absent. No statement on whether the DB can sustain the backfill I/O alongside production traffic. 50M rows at typical update rates will generate significant WAL / binlog volume.
- **User-visible outcome metric**: absent. No metric named that would confirm the migration achieved its business purpose (as opposed to confirming it completed).

Both halves of B6 fail. This blocks APPROVE independently of B1–B5.

---

## B7 — Sequencing + capacity

Critical path is not surfaced. The plan names two steps ("add column," "backfill") but does not state:

1. Whether the column is added before or after app code is deployed (order matters: wrong order = constraint violation on insert)
2. Whether the backfill runs before or after the NOT NULL constraint is applied (order matters: constraint before backfill = immediate failure on pre-existing NULL rows)
3. Whether a post-backfill verification step exists before the constraint is enforced
4. What the abort criterion is if the backfill stalls or causes lag

Appetite is not fixed — "next release" is a delivery target, not a time budget or a cap. FTE is not stated.

The correct safe sequence for this class of migration is well-established:
1. Deploy app code that writes `user_tier` on new inserts (with a fallback default)
2. Add column as nullable with a DB default
3. Backfill existing rows in batches offline, verify 100% coverage
4. Add NOT NULL constraint (fast in Postgres ≥12 if all rows already non-null)
5. Remove DB default once app is authoritative

None of this sequence is present in the plan.

---

## B8 — Pre-mortem

Assume the plan shipped as written and failed. Top 3 reasons, ranked by likelihood:

1. **[Most likely] Application inserts fail with NOT NULL constraint violation during deploy.** The app code that writes `user_tier` is deployed simultaneously with the schema migration, but the schema migration runs first (as migrations always do). Rows inserted in the window between migration completion and app code activation have no `user_tier` value. Every insert fails. Error rate spikes; on-call is paged; rollback requires dropping the column (another migration) or reverting app code while the constraint remains. **Kill-switch condition**: monitor `INSERT` error rate on `users` table for constraint violations in the 10 minutes following migration execution. If error rate > 0, halt deploy and page DBA immediately.

2. **[Likely] Backfill runs for hours, causes replication lag, degrades read performance, triggers alerts in unrelated systems.** 50M rows updated in a single transaction or tight loop without batching creates a large WAL/binlog event. Replicas fall behind. Read traffic routed to replicas returns stale data. Monitoring systems that depend on replica freshness start alerting. The migration "completes" but the system is in a degraded state for an extended period. **Kill-switch condition**: monitor replication lag during backfill. If lag exceeds 30 seconds, abort backfill and assess. Pre-commit: run backfill against a production-scale staging copy and measure actual duration + lag impact before scheduling the production run.

3. **[Possible] Backfill produces incorrect `user_tier` values because `subscription_status` contains unexpected values (NULL, legacy enum values, data quality issues).** Rows receive a wrong or default `user_tier` silently. The NOT NULL constraint is satisfied (no errors), but downstream business logic that reads `user_tier` produces wrong results — billing, feature gating, analytics. This failure is invisible at deploy time and surfaces hours or days later through business metric anomalies.

---

## Recommendation

**KILL** — the plan as stated cannot be safely approved.

The plan is not REVISE because the defects are not editorial. The core sequencing of the migration is unsafe (backfill during deploy, NOT NULL applied before app code is coordinated, no rollback path), and the plan cannot be fixed by adding a few sentences. It requires a redesign of the execution approach before it comes back for review.

### Conditions to re-submit as REVISE (not APPROVE)

A revised plan must address all of the following before it can be re-reviewed:

1. **B1**: Open with a problem statement (what is broken without `user_tier`, for whom, what measurable outcome the migration enables).
2. **B3-1**: Provide a backfill timing estimate based on actual measurement against a production-scale copy (rows/sec, total duration, expected replication lag). Confidence must reach ≥5 (experiment-level) before scheduling the production run.
3. **B3-2**: Run `SELECT COUNT(*) FROM users WHERE subscription_status IS NULL OR subscription_status NOT IN (<exhaustive list>)` on the production read replica. Document the result and the handling for every non-standard value.
4. **B3-3 / B5**: Name the DB engine and version. State the migration tool or technique that avoids a full table lock. Name the three alternatives (nullable-first, db-default, online schema change tool) and document why the chosen approach is preferred over each.
5. **B4**: Name the DBA or infrastructure owner. Name the deploy pipeline owner. Document the exact migration sequence (which step runs in which order, relative to app code deployment).
6. **B5**: Write an ADR covering the one-way-door decisions: NOT NULL vs nullable-first, inline backfill vs offline batch job, chosen migration tool vs alternatives.
7. **B6**: Name: (a) rollback path if backfill fails mid-run; (b) rollback path if post-deploy data quality check reveals bad backfill values; (c) alert condition (insert error rate on `users`); (d) replication lag threshold that triggers abort; (e) user-visible outcome metric that confirms the migration achieved its business purpose.
8. **B7**: State the safe execution sequence (app code first, then nullable column, then offline backfill in batches, then NOT NULL constraint). Fix the appetite as a cap.
