# Plan Review: NOT NULL column backfill on users table

**Verdict: Do not approve as stated. Requires significant changes before proceeding.**

---

## What the plan proposes

Add a `NOT NULL` column `user_tier` to a `users` table with 50 million rows, backfill from `subscription_status` during deploy, ship in next release.

---

## Critical problems

### 1. The backfill will lock the table and likely take it down

On most databases (PostgreSQL, MySQL with InnoDB), adding a `NOT NULL` column without a default causes a full table rewrite. On a 50M-row table, that is a long-running operation that holds an exclusive lock. During that lock, all reads and writes to `users` fail. The `users` table is almost certainly in the hot path of every user-facing request. This plan, executed as written, will take the site down during deploy.

Even if you add a default value to satisfy the `NOT NULL` constraint at the DDL level (which releases the lock sooner in Postgres 11+), you still have a backfill that touches 50M rows. A naive `UPDATE users SET user_tier = ...` will:
- Hold row locks for minutes or hours
- Flood replication lag
- Saturate I/O and CPU on the primary

### 2. "During deploy" is the wrong window for a backfill of this size

Deploys are time-pressured, often unattended or minimally supervised, and have limited rollback options once they start. A backfill that takes 30–90 minutes does not belong in a deploy window. If it fails partway through, you now have a partially-backfilled table and a partially-deployed application.

### 3. No rollback path is described

If the deploy fails mid-way — migration applied, backfill running, application code deployed — what is the recovery procedure? Rolling back a `NOT NULL` column addition after data has been written to it is painful. The plan doesn't address this at all.

### 4. The NOT NULL constraint is being added before the application is ready for it

If the column doesn't exist yet, the current production code doesn't read or write it. Adding it as `NOT NULL` immediately means any INSERT that doesn't supply `user_tier` will fail. If the application is deployed before the migration completes (or vice versa), you have a window where requests fail.

### 5. The backfill logic is unspecified

"Backfill from `subscription_status`" implies a mapping between `subscription_status` values and `user_tier` values. That mapping is not described. Is it deterministic? Are there null `subscription_status` rows? What happens to them when you add a `NOT NULL` column? These are not minor details — they determine whether the migration even runs to completion.

---

## How this should be done instead

A safe large-table schema migration of this type follows a multi-step, multi-release process:

**Release 1: Add the column as nullable**
```sql
ALTER TABLE users ADD COLUMN user_tier VARCHAR(50);
```
This is fast and safe. No locking, no rewrite. Application code continues working.

**Release 2: Backfill in batches, before or between deploys**
Run the backfill as a separate, monitored job — not during deploy. Process rows in batches of 1,000–10,000 with sleeps between batches to avoid I/O saturation and replication lag. Example structure:
```sql
UPDATE users SET user_tier = <mapping> 
WHERE id BETWEEN :start AND :end AND user_tier IS NULL;
```
Monitor replication lag throughout. This runs over hours or days, not minutes.

**Release 3: Add the NOT NULL constraint**
Only after 100% of rows are confirmed to have a non-null value. In Postgres, use `ADD CONSTRAINT ... NOT NULL` or `SET NOT NULL` with `NOT VALID` + `VALIDATE CONSTRAINT` to avoid a full table scan lock. In MySQL, this is trickier — consider using pt-online-schema-change or gh-ost.

**Release 4: Application code fully migrated**
Once the column is trusted and the old `subscription_status`-based logic is no longer needed.

---

## Questions that must be answered before proceeding

1. **Database and version:** Postgres, MySQL, other? The safe migration approach differs significantly.
2. **Downtime tolerance:** Is planned maintenance possible? If yes, the calculus changes.
3. **Replication setup:** Are there read replicas? How sensitive is replication lag?
4. **Null subscription_status rows:** How many rows have null or unexpected `subscription_status` values, and what should `user_tier` be for them?
5. **Application deploy order:** Will the migration run before or after the application code is deployed?
6. **Rollback plan:** What is the recovery procedure if this fails partway through?

---

## Summary

The plan as described will almost certainly cause an outage on a 50M-row table. The combination of `NOT NULL`, no default, inline backfill during deploy, and no rollback plan are individually concerning — together they are a high-probability incident. Approve only after the plan is rewritten to use a phased, batched approach with an explicit rollback path at each phase.
