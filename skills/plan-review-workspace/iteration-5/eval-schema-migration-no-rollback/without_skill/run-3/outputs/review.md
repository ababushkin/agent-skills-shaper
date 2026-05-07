# Plan Review: Add NOT NULL column `user_tier` to `users` table

**Verdict: Do not approve as stated. Significant operational risk. Requires rework before proceeding.**

---

## What the plan says

- Add a `NOT NULL` column `user_tier` to the `users` table
- Table has 50M rows
- Backfill from `subscription_status` during deploy
- Ship in next release

---

## What's wrong

### 1. NOT NULL + backfill-during-deploy is a race condition

Adding a `NOT NULL` column to a 50M-row table without a default value means the database engine must either:

a. Lock the table for the duration of the backfill (hours on most engines), or
b. Reject all writes to `users` until the column has a value for every row

Neither is acceptable in a production system with active traffic. The plan conflates two distinct operations — schema change and data migration — and proposes to run them as a single atomic deploy step. That doesn't work safely at this scale.

### 2. No default value means no safe migration path

The standard safe approach for adding a NOT NULL column to a large table is:

1. Add the column as `NULL` with no constraint
2. Backfill in batches (not all at once)
3. Add a `DEFAULT` value so new writes are covered
4. Validate the backfill is complete
5. Add the `NOT NULL` constraint in a separate migration

The plan skips every step except the last intent. This is the exact sequence that causes production outages.

### 3. Backfilling 50M rows "during deploy" is not a deploy operation

A batch backfill of 50M rows will take minutes to hours depending on the database, hardware, and query complexity. Running this inside a deploy window means:

- The deploy is not idempotent
- Rollback is non-trivial or impossible once the migration runs
- If the deploy fails partway through, the table is in a partially-migrated state with a partially-enforced constraint

The plan has no mention of rollback, which at 50M rows is almost certainly not a simple "drop column" — especially if application code has already been deployed that depends on `user_tier` being present.

### 4. The backfill logic is unspecified

"Backfill from `subscription_status`" says nothing about:

- What the mapping from `subscription_status` values to `user_tier` values is
- What happens to rows where `subscription_status` is NULL or has unexpected values
- Whether this mapping has been validated against the actual data distribution
- Whether the backfill query will produce a full table scan and lock contention

At 50M rows, a poorly written backfill query can saturate I/O, cause replication lag, and degrade unrelated queries for the duration.

### 5. No mention of zero-downtime migration tooling

There is no mention of whether the team is using a tool like `pt-online-schema-change`, `gh-ost`, or a database-native online DDL (e.g., MySQL 8+ `ALGORITHM=INPLACE`, Postgres `pg_repack`, or a phased migration pattern). For a 50M-row table, using the right tooling is not optional — it is the difference between a non-event and a production incident.

---

## What I'd want to see before approving

1. **Migration split into phases**: column added nullable first, backfill run offline as a batched operation, NOT NULL constraint added only after validation confirms zero NULL rows.

2. **Batched backfill plan**: rows processed in chunks (e.g., 10k at a time with a sleep between batches) to avoid lock escalation and replication lag spikes. Estimated duration with a benchmark on a recent prod snapshot.

3. **Mapping specification**: explicit documentation of how each `subscription_status` value maps to a `user_tier` value, including what happens to edge cases (NULL, unknown values, legacy states).

4. **Rollback plan**: what does rollback look like at each phase? If application code is deployed before the migration completes, can we roll back the application code independently? This needs an explicit answer.

5. **Deployment sequencing**: clarify whether the application code change (which presumably reads `user_tier`) is deployed before, during, or after the migration. The column must exist and be populated before any code that treats it as NOT NULL is deployed. The plan implies these happen together ("during deploy") — that needs to be explicit and correct.

6. **Monitoring during migration**: which metrics are being watched? Replication lag, query duration, lock waits, error rates. Who is on-call during the migration window?

---

## Risk rating

**High.** The plan as written has a realistic path to a multi-hour production outage or partial data corruption on a core user table. The fix is not complicated — it's a well-understood pattern — but it requires the team to slow down and execute the migration in phases rather than collapsing it into a single deploy step.
