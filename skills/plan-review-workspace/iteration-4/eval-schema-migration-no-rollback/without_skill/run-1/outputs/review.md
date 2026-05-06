# Plan Review: Add NOT NULL `user_tier` Column to `users` Table

**Verdict: Do NOT approve as written.** This plan has multiple high-severity issues that will likely cause an outage or extended downtime on a 50M-row table. It needs to be rewritten before it goes near production.

---

## Summary of the plan

> Add `NOT NULL` column `user_tier` to `users` table (50M rows), backfill from `subscription_status` during deploy, ship in next release.

That's it. That's the entire plan. The thinness of the plan is itself the first red flag — a schema change of this magnitude on a table this size deserves a written migration plan, not a one-line approval request.

---

## Critical issues (blocking)

### 1. `NOT NULL` column added in a single step on 50M rows will lock the table

On most major RDBMSes this is the failure mode:

- **PostgreSQL (pre-11):** `ALTER TABLE users ADD COLUMN user_tier <type> NOT NULL DEFAULT <x>` rewrites the entire table while holding an `ACCESS EXCLUSIVE` lock. On 50M rows that's potentially many minutes to hours of total downtime for any reader or writer of `users`.
- **PostgreSQL 11+:** Adding a `NOT NULL` column with a constant default is fast (metadata-only), **but** the plan says "backfill from `subscription_status`" — that's not a constant default, it's a per-row computed value, so the metadata-only optimisation does not apply.
- **MySQL/InnoDB:** Online DDL helps, but adding `NOT NULL` without a default still typically requires a table copy depending on version and `ALGORITHM`/`LOCK` choice. 50M rows is hours.
- **The plan does not name the database engine or version.** That alone makes the plan unreviewable.

### 2. Backfill "during deploy" is the wrong place to do it

A 50M-row backfill is not a deploy step. It is a multi-hour (potentially multi-day) operation that needs:

- Batching (e.g. 1k–10k rows per batch with a sleep between batches) to avoid replication lag, lock contention, and IO saturation.
- Progress tracking and the ability to resume on failure.
- Monitoring of replication lag, CPU, IOPS, and lock waits.
- A way to abort cleanly if it goes wrong.

If you run this inside the deploy:
- The deploy will time out (most CI/CD systems kill long-running deploys).
- A failure mid-backfill leaves the system in an inconsistent state that is hard to recover from.
- You have blocked all other deploys for the duration.

### 3. There is no rollback plan

This is a **one-way door** decision and the plan acknowledges nothing of the sort.

Rolling back a `NOT NULL` column addition is non-trivial:
- Dropping the column on 50M rows is itself a heavy operation on some engines.
- If application code in the new release reads/writes `user_tier`, you can't roll back the app without first reversing the migration — but you also can't easily reverse the migration with the new app version still running.
- You'd be stuck with whatever broken state production lands in.

The standard pattern is **expand → migrate → contract**, in separate releases:

1. **Release N:** Add `user_tier` as nullable. Deploy.
2. **Release N (post-deploy job):** Backfill in batches with monitoring. No app dependency on the column yet.
3. **Release N+1:** App code starts dual-writing `user_tier` on new/updated users.
4. **Release N+2:** Verify backfill complete, add `NOT NULL` constraint (use `NOT VALID` + `VALIDATE CONSTRAINT` on Postgres to avoid full lock).
5. **Release N+3:** App code uses `user_tier` as source of truth; old column/logic deprecated.

The proposed "do it all in one release" plan collapses all of these into a single failure point with no rollback.

### 4. The backfill source is under-specified and probably wrong

"Backfill from `subscription_status`" raises immediate questions the plan does not answer:

- What are the valid values of `subscription_status`?
- What are the valid values of `user_tier`?
- What is the mapping function between them? Is it 1-to-1? Are there edge cases (NULL `subscription_status`, deprecated statuses, trial users, churned users, B2B vs. B2C)?
- What happens to users with `subscription_status = NULL` if the new column is `NOT NULL`?
- Is `subscription_status` itself stable, or is it being modified concurrently?

Without an explicit mapping table and an explicit answer for every edge case, the backfill will either crash partway through (on an unmapped value) or silently assign wrong tiers to a non-trivial slice of the user base. Either is a P0 incident waiting to happen.

### 5. No mention of replication, read replicas, or write traffic

50M-row tables in production are almost always replicated. The plan does not mention:

- Whether replicas can keep up with the backfill (replication lag is the most common backfill failure mode).
- Whether the application has writes hitting `users` during the migration that need to also populate `user_tier`.
- Whether there's a read-replica-served read path that might see the column before/after the backfill completes.

### 6. No observability plan

What metrics tell us the migration is healthy? What alerts fire if it's not? What's the SLO for `users` reads/writes during the migration window? None of this is in the plan.

### 7. "Ship in next release" — what's the appetite, what's the deadline pressure?

If "next release" is in three days, this plan is a guaranteed incident. If it's in three weeks and "next release" just means "the next planned release window," that's slightly better but the plan still needs the rewrite above. The plan should state the time budget and what we'd cut if it doesn't fit.

---

## Lesser issues

- **No data validation step.** After backfill, before applying `NOT NULL`, you should verify zero NULL rows remain via a `SELECT COUNT(*) WHERE user_tier IS NULL`. The plan implies the constraint is added at the end of the deploy with no verification.
- **No mention of indexes.** Will `user_tier` need an index? If yes, that's another table-locking operation (use `CREATE INDEX CONCURRENTLY` on Postgres).
- **No mention of feature flags.** The application code that depends on `user_tier` should be feature-flagged so it can be turned off without a redeploy if the migration goes sideways.
- **No staging rehearsal mentioned.** A migration of this size should be rehearsed on a staging copy of production-scale data, with timing measurements, before being attempted on prod.

---

## What I would approve

A rewritten plan that:

1. Names the DB engine, version, and replication topology.
2. Splits the work into expand → backfill → constrain → contract, across at least 2–3 releases.
3. Adds the column as nullable in release 1, with no `NOT NULL` constraint.
4. Backfills out-of-band (a script or job, not the deploy), in batches, with progress tracking, monitoring, and the ability to pause/resume.
5. Provides an explicit, complete mapping from `subscription_status` to `user_tier`, including handling of NULLs and edge cases.
6. Adds the `NOT NULL` constraint in a later release using a no-lock-equivalent path for the engine in question (e.g. Postgres `NOT VALID` + `VALIDATE`).
7. Has a written rollback plan for each step.
8. Has SLOs, alerts, and a verification query for backfill completeness.
9. Has been rehearsed on staging at production scale, with timing recorded.

Until then: **do not approve.**

---

## TL;DR

A `NOT NULL` column add with a per-row backfill on a 50M-row table, executed inside a deploy, in a single release, with no rollback plan and no engine specified, is one of the most reliable ways to take a production database down. This plan is roughly four releases of work compressed into one line of approval request. Send it back.
