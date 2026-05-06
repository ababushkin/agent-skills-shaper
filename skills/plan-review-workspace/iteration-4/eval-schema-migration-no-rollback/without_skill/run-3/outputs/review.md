# Plan Review: NOT NULL column `user_tier` on users table (50M rows)

**Verdict: Do NOT approve as written.** This plan has multiple high-severity issues that will likely cause an outage or data corruption. It needs significant rework before it can ship.

---

## Critical issues (blockers)

### 1. Adding NOT NULL column to a 50M-row table during deploy is dangerous

Depending on the database engine:

- **PostgreSQL (pre-11):** `ALTER TABLE ... ADD COLUMN ... NOT NULL DEFAULT ...` rewrites the entire table and holds an `ACCESS EXCLUSIVE` lock for the duration. On 50M rows, this is minutes-to-hours of full table lock — effectively an outage on the users table.
- **PostgreSQL 11+:** `ADD COLUMN ... NOT NULL DEFAULT <constant>` is fast (no rewrite) **only** if the default is a constant. If the default is computed from another column (`subscription_status`), this optimization does NOT apply and you'll get the rewrite + lock.
- **MySQL/InnoDB:** Online DDL helps, but `ADD COLUMN NOT NULL` with backfill still incurs significant overhead and replica lag.
- **No engine is named in the plan.** That alone is a reason to send this back.

### 2. "Backfill from subscription_status during deploy" is the wrong shape

You cannot safely do a 50M-row backfill inside a deploy window. This needs to be a multi-step migration:

1. Add column as **nullable** (fast, metadata-only on most engines).
2. Deploy application code that **dual-writes** `user_tier` on insert/update.
3. **Backfill in batches** (e.g., 10k rows at a time) as a background job, throttled to avoid replica lag and lock contention. For 50M rows, expect hours-to-days.
4. Verify backfill completeness (count of NULLs == 0).
5. **Then** add `NOT NULL` constraint — and even this is non-trivial at scale (Postgres needs `ADD CONSTRAINT ... NOT VALID` then `VALIDATE CONSTRAINT` to avoid a long lock; or use a `CHECK (col IS NOT NULL) NOT VALID` pattern).
6. Optionally promote check constraint to true `NOT NULL`.

Doing all of this "during deploy" conflates schema migration with code release and removes every safety valve.

### 3. The mapping from `subscription_status` → `user_tier` is undefined

What are the values of `subscription_status`? What are the values of `user_tier`? Is the mapping 1:1, or does it collapse states? What about:

- Users with NULL `subscription_status`?
- Users in transitional states (e.g., `past_due`, `pending_cancel`, `trialing`)?
- Historical/churned users?
- Edge cases (admin accounts, internal test users, B2B accounts on different billing models)?

This mapping is a **business decision** that needs sign-off from product/billing, not an engineering implementation detail. If it's wrong, you've corrupted 50M user records and the only "rollback" is restoring from backup.

### 4. No rollback plan

Once the column exists with NOT NULL constraint and backfilled data:

- You cannot easily drop the column without coordinating with all readers/writers.
- You cannot revert the backfill if the mapping turns out to be wrong (the source of truth — `subscription_status` at backfill time — has now drifted).
- If the backfill partially completes and the deploy fails, you're stuck with a half-populated NOT NULL column that blocks all writes.

This is a **one-way door** decision (per universal Principle 3). It needs commensurate scrutiny.

### 5. No mention of replication, read replicas, or downstream consumers

- Does the schema change replicate cleanly to read replicas? Long DDL locks can cause replica lag spikes.
- Are there ETL jobs, analytics pipelines, or downstream services that read from `users`? Adding a column may break naive `SELECT *` consumers or schema-coupled ORMs.
- Are there any `INSERT INTO users (...)` statements in the codebase that don't include the new column? After NOT NULL is enforced, every one of those breaks.

---

## What I'd require before approval

1. **Database engine + version stated explicitly.**
2. **Multi-phase migration plan** as outlined in #2 above, with each phase as an independently deployable change.
3. **Mapping spec** for `subscription_status` → `user_tier`, signed off by product, with explicit handling of nulls, transitional states, and edge cases.
4. **Backfill strategy**: batch size, throttling, monitoring, expected duration, replica lag SLO.
5. **Rollback plan** for each phase.
6. **Code audit**: every `INSERT` and ORM model touching `users` reviewed for compatibility.
7. **Verification step**: query that confirms backfill completeness and mapping correctness on a sample before promoting to NOT NULL.
8. **Feature flag / gradual rollout** for any application code that depends on the new column.

---

## Recommendation

**Reject.** Send back for redesign as a phased migration with explicit mapping spec and rollback plan. The current plan is roughly three sentences describing what would be a 2–4 week project executed safely. The gap between the plan's confidence and the actual risk is the issue.
