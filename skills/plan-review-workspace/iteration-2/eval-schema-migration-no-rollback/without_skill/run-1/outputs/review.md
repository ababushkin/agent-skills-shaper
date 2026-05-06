# Plan Review: Add NOT NULL column `user_tier` to `users` (50M rows)

## Verdict: Do not approve as written.

The plan as stated is a recipe for a long outage and a hard-to-reverse production incident. It can become approvable, but only after meaningful rework. Below is what's wrong, what's missing, and what an acceptable version looks like.

---

## What the plan says

> Add NOT NULL column `user_tier` to `users` table (50M rows), backfill from `subscription_status` during deploy, ship in next release.

That is the entire plan. There is no rollout strategy, no rollback plan, no statement of which database engine, no statement of expected lock duration, no statement of how the application will behave during the migration, and no statement of how the data is verified after backfill.

---

## Major problems

### 1. NOT NULL + default-less add on a 50M row table is dangerous on most engines

- **PostgreSQL (modern, 11+):** Adding a column with a constant `DEFAULT` is metadata-only and fast. But adding `NOT NULL` without a default forces a full table scan to verify, and on 50M rows that holds an `ACCESS EXCLUSIVE` lock long enough to stall the application. Adding `NOT NULL` with a non-constant default (e.g. derived from `subscription_status`) is a full table rewrite — minutes to hours of downtime, plus bloat.
- **MySQL/InnoDB:** Depending on version and `ALGORITHM`, this can rebuild the table. Online DDL exists but must be invoked deliberately; the plan does not say so.
- **The plan does not name the engine, the version, or the chosen DDL strategy.** That alone is grounds to reject.

### 2. "Backfill during deploy" is the wrong shape for 50M rows

A single-transaction backfill of 50 million rows during a deploy window will:

- Hold locks that block writes to `users` (the most contended table in most products).
- Generate enormous WAL/redo, risking replication lag and disk pressure.
- Make rollback effectively impossible mid-flight.
- Almost certainly exceed any reasonable deploy window.

The correct shape is a **batched, chunked backfill running independently of the deploy**, with progress tracking, throttling, and the ability to pause and resume.

### 3. The NOT NULL constraint conflicts with the deploy ordering

The standard safe sequence is:

1. Add column as **nullable**, no default (metadata-only, instant).
2. Deploy application code that **writes** `user_tier` on every new/updated row (dual-write).
3. Backfill existing rows in batches, off-peak, with throttling.
4. Verify zero NULLs remain.
5. Add `NOT NULL` constraint (Postgres: via `CHECK ... NOT VALID` then `VALIDATE CONSTRAINT`, then optionally promote to NOT NULL — this avoids the long lock).
6. Deploy application code that **reads** `user_tier`.

The plan collapses all of this into one deploy, which is the failure mode.

### 4. No rollback plan

What happens if the backfill is half-done and the deploy fails? What happens if `user_tier` is set incorrectly for a subset of users and a customer complains the next day? The plan has no answer. Dropping a column you've already started reading from in app code is a multi-deploy unwind. Rollback must be designed before the change ships, not improvised after.

### 5. "Backfill from `subscription_status`" is under-specified

- What is the mapping? `subscription_status` likely has values like `active`, `trialing`, `past_due`, `canceled`, `paused`, `none`. What `user_tier` does each map to? Where is the mapping reviewed and signed off?
- What about NULL `subscription_status`? What about historical states no longer in the enum? What about users created before subscriptions existed?
- Is the mapping idempotent and re-runnable? If we re-run the backfill, does it overwrite or skip?
- Who validates the mapping is correct after backfill — sampling, full reconciliation, or none?

This is the single biggest source of silent data corruption risk in the plan.

### 6. No observability or verification plan

- How do we know the backfill is progressing? (rows/sec, ETA, lag)
- How do we know it succeeded? (row count where `user_tier IS NULL` = 0; distribution of values matches expected distribution of `subscription_status`)
- What alerts fire if the backfill stalls or replication lag exceeds a threshold?
- Is there a sampled correctness check before flipping to NOT NULL?

None of these are mentioned.

### 7. "Ship in next release" implies coupling to the release train

Schema migrations of this size should not be coupled to a feature release. They should run on their own cadence: add-column ships, backfill runs over hours or days, NOT-NULL promotion ships in a later release. Coupling a 50M-row backfill to "next release" means either (a) the release is delayed by the backfill, (b) the backfill is rushed, or (c) the deploy window blows up. None are good.

---

## Smaller issues / questions

- **Indexing.** Will any index be added on `user_tier`? If so, use `CREATE INDEX CONCURRENTLY` (Postgres) or equivalent. Not mentioned.
- **Replicas.** How will the change propagate to read replicas? Will replication lag during backfill cause stale reads?
- **Foreign keys / constraints / partitioning.** Is `users` partitioned? If so, the migration must be applied per-partition. Not mentioned.
- **ORM/code generation.** Does the app's ORM expect the column? Will adding a column it doesn't know about break anything? Will making it NOT NULL break inserts from any path that doesn't set it?
- **Backups.** A 50M-row rewrite materially changes backup size and timing. Worth flagging to the platform team.
- **Compliance / PII.** `user_tier` is probably not PII, but if it derives from billing data it may be regulated. Worth a one-line check.

---

## What an approvable plan looks like

Roughly:

1. **ADR / short design doc** stating: engine + version, expected lock behaviour, batch size, throttle, rollback plan, mapping table for `subscription_status` → `user_tier` (signed off by product), verification plan, observability plan.
2. **Migration 1 (release N):** add `user_tier` as nullable, no default. Metadata-only.
3. **Application change (release N):** dual-write `user_tier` on insert/update of `users`. Reads still tolerate NULL.
4. **Backfill job (out-of-band, after release N):** chunked (e.g. 10k rows per batch), throttled, idempotent, observable, pausable. Runs over hours or days. Progress dashboard. Alert on replication lag.
5. **Verification:** zero NULLs; value distribution sanity-checked against `subscription_status`; sampled rows reviewed.
6. **Migration 2 (release N+1):** add `CHECK (user_tier IS NOT NULL) NOT VALID`, then `VALIDATE CONSTRAINT` (Postgres). Promote to `NOT NULL` if engine requires it, using the validated check to avoid the full scan.
7. **Application change (release N+1 or later):** code begins to rely on `user_tier` being non-null.
8. **Rollback story documented at each step.**

That is approximately three deploys and one out-of-band job — not "ship in next release."

---

## Recommendation

**Reject the plan in its current form.** Send it back with this review and ask for:

- A written design doc covering the seven points above.
- The `subscription_status` → `user_tier` mapping, signed off by product/billing.
- A rollback plan for each phase.
- Concrete numbers: expected lock duration, batch size, throttle rate, expected backfill wall-clock time, replication-lag tolerance.

If those come back well-reasoned, the same underlying change can ship safely — just across multiple releases rather than one.
