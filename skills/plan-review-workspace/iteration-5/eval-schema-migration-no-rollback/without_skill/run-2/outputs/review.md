# Plan Review: Add NOT NULL column `user_tier` to `users` table

**Verdict: Do not approve as stated. Needs rework before proceeding.**

---

## What the plan says

1. Add a `NOT NULL` column `user_tier` to the `users` table (50M rows).
2. Backfill from `subscription_status` during deploy.
3. Ship in the next release.

---

## Critical problems

### 1. NOT NULL + backfill during deploy will lock or break production

On a 50M-row table, you cannot add a `NOT NULL` column and backfill it in a single migration during a deploy. The consequences depend on database:

- **PostgreSQL < 11**: Adding a NOT NULL column with a DEFAULT rewrites the entire table. 50M rows means a full-table lock for potentially minutes. Site down.
- **PostgreSQL ≥ 11**: Adding a NOT NULL column with a constant DEFAULT is instantaneous (stored in metadata). But backfilling from `subscription_status` is not a constant default — it requires a row-level computation, so you still need to update every row.
- **MySQL/MariaDB**: Similar table-lock or copy behavior depending on version and engine.

A mid-deploy backfill of 50M rows at typical write speeds (10k–100k rows/sec with batching) takes seconds to minutes at best. Without batching it will lock the table or saturate I/O and take far longer. This is a high-probability production incident waiting to happen.

### 2. No rollback path is described

The plan has no rollback strategy. If the deploy fails mid-backfill, or the backfill logic is wrong, what happens? With a NOT NULL constraint already applied, any new row inserted during or after a failed migration will fail unless the column has a default. This can take down the application.

### 3. "During deploy" is the wrong time for a data migration at this scale

A 50M-row backfill is a data migration, not a schema migration. It should not run inside a deploy pipeline where it blocks traffic or rollback. These are fundamentally different operations and need to be sequenced separately.

### 4. Backfill logic is unspecified and assumed correct

"Backfill from `subscription_status`" — what is the mapping? Is `subscription_status` nullable? What value does `user_tier` get when `subscription_status` is NULL or has an unrecognized value? If the mapping is wrong, you now have incorrect data in a NOT NULL column with no easy path to correct it under load.

---

## What a safe approach looks like

This is a well-understood class of problem. The standard pattern:

1. **Add the column as nullable** (`user_tier VARCHAR ... NULL`). Zero downtime. No lock.
2. **Backfill in batches** (offline job, not during deploy): update rows in chunks of 1k–10k, with rate limiting, monitored. Run before or after deploy, not during.
3. **Once backfill is complete and verified**, add the NOT NULL constraint (PostgreSQL: `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL` with a `CHECK` constraint trick to avoid a full scan, or validate separately).
4. **Deploy application code** that reads and writes the new column.

Each step is independently reversible. The NOT NULL constraint is only added after the data is confirmed clean.

Depending on the database and version, `ALTER TABLE ... SET NOT NULL` can still be a brief lock — verify what your DB version does and use `NOT VALID` + `VALIDATE CONSTRAINT` (Postgres) if lock-free is required.

---

## What I'd need to approve this

1. A phased migration plan: nullable column first, batched backfill second, constraint third.
2. Explicit backfill logic with handling for NULL and unexpected `subscription_status` values.
3. A rollback procedure for each phase.
4. Estimated backfill duration based on actual write throughput in production.
5. Confirmation that no application code fails if `user_tier` is NULL during the transition window.

---

## Summary

The plan conflates three separate operations (schema change, data migration, constraint enforcement) into one step that cannot be safely executed on a table this size. The risk is a production outage during deploy with no clean recovery path. This is fixable — the pattern is standard — but the plan needs to be reworked before approval.
