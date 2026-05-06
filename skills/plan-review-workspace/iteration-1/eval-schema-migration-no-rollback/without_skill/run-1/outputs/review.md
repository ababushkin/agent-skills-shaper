# Plan Review: NOT NULL column `user_tier` on `users` (50M rows)

## Assessment

This plan is not approvable as written. It compresses three independently risky operations — a schema change on a large table, a backfill, and a release — into a single deploy step, with no mention of locking behaviour, backfill strategy, rollback, or verification. On a 50M-row table, each of these is a one-way door if mishandled.

The plan also reads as solution-first ("add NOT NULL column, backfill from subscription_status"). It does not state the problem being solved, the outcome we expect to move, or why `user_tier` must derive from `subscription_status` (vs. being a new source of truth, a computed column, or a denormalisation that can be rebuilt). Without that framing, reviewers cannot judge whether this is the right shape of change at all.

## Concerns

**1. NOT NULL + default on a large table is a foot-gun on most engines.**
On PostgreSQL 11+ a NOT NULL column with a constant default is metadata-only and fast; with a volatile or computed default it rewrites the table. On MySQL/MariaDB (pre-8.0 instant-add), or any engine without instant-add, this acquires a long exclusive lock on a 50M-row table and will cause an outage. The plan does not name the engine, the version, or the lock behaviour expected. That alone blocks approval.

**2. "Backfill during deploy" is the wrong shape.**
Backfilling 50M rows inside a deploy window means: (a) the deploy is now bounded by backfill time, not code-push time; (b) if the backfill fails halfway, the system is in a half-migrated state with no documented recovery; (c) the deploy holds locks or generates replication lag for the duration. The standard pattern is: add nullable column → backfill in batches in the background → add NOT NULL constraint as a separate step once backfilled and verified. Three small batches, not one big one (universal Principle 8).

**3. No rollback plan.**
Once a NOT NULL column is added and application code starts writing to it, rolling back the migration without data loss is non-trivial. The plan says "ship in next release" with no flag, no staged rollout, no rollback procedure. Universal Rule C2: deployment decoupled from release. This plan couples them.

**4. Backfill source is unjustified.**
`subscription_status` → `user_tier` is presented as a given. Is the mapping 1:1? What about users with NULL/expired/legacy `subscription_status`? What's the behaviour for users created during the backfill window (race condition between backfill and new writes)? None of this is addressed.

**5. No observability / verification plan.**
What does success look like? Row count where `user_tier IS NOT NULL` equals total user count? Distribution of tiers matches expected? Universal Principle 1: shipped is not done; observed is done. No metric named, no check defined.

**6. Blast radius is the entire users table.**
The `users` table is almost certainly the most-read table in the system. Any lock, replication lag, or query-plan change here ripples everywhere. This is a one-way door masquerading as a routine migration.

## Recommendation

**Reject and reshape.** Send back with the following required changes before re-review:

1. **State the problem and outcome.** Why does `user_tier` need to exist as a column? What product or operational outcome moves when it does?
2. **Split into staged migrations:**
   - Step 1: Add `user_tier` as nullable, no default. Deploy.
   - Step 2: Dual-write from application code (new rows get `user_tier` set). Deploy behind a flag.
   - Step 3: Backfill historical rows in batches (e.g. 10k rows per batch, throttled, idempotent, resumable). Track progress in a migrations table. Run out-of-band, not in the deploy window.
   - Step 4: Verify backfill (row counts, tier distribution, spot-check sampling).
   - Step 5: Add NOT NULL constraint as a separate migration, only after Step 4 passes.
3. **Name the engine and the lock behaviour expected at each step.** Cite the docs.
4. **Define rollback for each step.** Step 1 and 5 are the dangerous ones; document the undo.
5. **Define observability:** backfill progress metric, error rate, replication lag alarm, query-latency baseline on `users` before/during/after.
6. **Justify the mapping** from `subscription_status` to `user_tier`, including edge cases (NULL, legacy values, in-flight changes).
7. **Decouple deploy from release** — gate any read of `user_tier` behind a feature flag until Step 5 is green.

Happy to re-review once the plan is staged, observable, and reversible.
