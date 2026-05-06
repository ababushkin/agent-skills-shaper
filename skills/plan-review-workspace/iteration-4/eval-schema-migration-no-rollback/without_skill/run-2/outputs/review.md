# Plan Review: Add NOT NULL `user_tier` column to users (50M rows)

**Recommendation: Do NOT approve as written. Reshape required.**

This plan compresses three independently risky operations — a schema change, a 50M-row backfill, and a semantic mapping from `subscription_status` — into a single deploy step with no rollback path. Each one alone deserves scrutiny; together they are a one-way door dressed up as a release item.

---

## Critical issues (block approval)

### 1. NOT NULL + 50M rows + "during deploy" is the failure mode

Adding a `NOT NULL` column to a 50M-row table is not a deploy-window operation in any mainstream RDBMS:

- **PostgreSQL (pre-11):** `ADD COLUMN ... NOT NULL DEFAULT x` rewrites the entire table holding an `ACCESS EXCLUSIVE` lock. On 50M rows this is minutes-to-hours of full downtime.
- **PostgreSQL 11+:** `ADD COLUMN ... NOT NULL DEFAULT <constant>` is fast (metadata-only), but `NOT NULL` *without* a default, then backfill, then enforce — is the safe pattern, not what's described.
- **MySQL (InnoDB):** `ALTER TABLE ... ADD COLUMN ... NOT NULL` is typically `ALGORITHM=INPLACE` but still rewrites the clustered index. On 50M rows expect prolonged replica lag and elevated lock contention. `pt-online-schema-change` or `gh-ost` would normally be used here — not a release deploy.

The plan does not name the engine, the migration tool, the lock mode, or the expected duration. That alone is disqualifying.

### 2. No rollback plan

Once the column exists with `NOT NULL` and a backfill has run, rolling back means either:
- Dropping the column (data loss for any writes that happened after deploy that depend on it), or
- Leaving it and reverting application code (now schema and code are out of sync, with implicit dependencies).

Neither is a clean rollback. The plan must specify the rollback path explicitly, including the point-of-no-return.

### 3. Backfill "during deploy" is structurally wrong

A 50M-row backfill should not happen inside a deploy window. The standard expand/contract pattern is:

1. **Expand:** Add column as `NULLABLE`, no default. Ship code that *writes* both old and new.
2. **Backfill:** Run the backfill as a separate, batched, observable, resumable job — over hours or days, with rate limiting to protect replica lag and IOPS.
3. **Verify:** Confirm no NULLs remain; confirm `subscription_status → user_tier` mapping is correct on a sample.
4. **Enforce:** Add `NOT NULL` constraint (in PG, `VALIDATE` separately to avoid full lock).
5. **Contract:** Ship code that *reads* the new column. Remove dual-write later.

Compressing this into a single release is the anti-pattern this whole pattern was designed to prevent.

### 4. The mapping is unspecified — and probably lossy

`subscription_status` → `user_tier` is a semantic translation, not a copy. Questions the plan does not answer:

- What is the full enumeration of `subscription_status` values? (`active`, `trialing`, `past_due`, `canceled`, `paused`, `incomplete`, `unpaid`, etc.)
- How does each map to a tier? Is `trialing` → `free` or `trial`? Is `past_due` → `paid` or `free`?
- What about NULL `subscription_status`? Users who never subscribed?
- Are there grandfathered users, comp accounts, employee accounts, or B2B seats whose tier is *not* derivable from subscription state?
- Is the mapping idempotent and reproducible if the backfill needs to resume after failure?

A mapping table needs to be in the plan, reviewed by product/billing, before any column is added.

### 5. No mention of writes during backfill

While backfill runs, the application is presumably still creating new users and changing subscriptions. The plan must specify:
- New rows: who sets `user_tier` for them? (Application? Trigger? Default?)
- Existing rows whose `subscription_status` changes mid-backfill: are they re-mapped or stale?

Without dual-write or a trigger, the backfill is racing live traffic and will produce inconsistent state.

---

## Operability gaps (also blocking)

- **No SLO impact statement.** A 50M-row migration will affect p95/p99 latency, replica lag, and IOPS. What's the budget? What's the kill switch?
- **No staging rehearsal mentioned.** A migration of this size must be rehearsed on a production-sized dataset with realistic load.
- **No observability plan.** Backfill progress, error rate, lag, lock waits — none specified.
- **No on-call playbook.** If the migration stalls at 3am, what does the on-call do?
- **No communication plan.** Customer support, internal stakeholders, status page.

---

## Required reshape

Before this can be approved, I need to see:

1. **Engine, version, and migration tool** named explicitly.
2. **The mapping table**: every `subscription_status` value → `user_tier`, signed off by product/billing.
3. **Expand/migrate/contract sequence** broken into distinct PRs and distinct deploys, not one release.
4. **Backfill design**: batched, resumable, rate-limited, observable, with a written rollback procedure for each phase.
5. **Dual-write strategy** for in-flight writes during backfill.
6. **Staging rehearsal results** on a production-scale dataset.
7. **SLO/error-budget impact analysis** and a kill switch.
8. **Rollback plan** for each phase, with the point-of-no-return clearly identified.

---

## Verdict

**Reject.** This is a textbook one-way-door change being treated as a routine release. The shape of the plan — three risky operations fused into one deploy, no rollback, undefined mapping, no operability — is the shape of an incident waiting to happen. Reshape into expand/migrate/contract phases over multiple releases and resubmit.
