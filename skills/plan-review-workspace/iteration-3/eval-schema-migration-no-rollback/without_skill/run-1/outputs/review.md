# Plan Review: Add NOT NULL `user_tier` column to users table

**Plan summary:** Add NOT NULL column `user_tier` to `users` table (50M rows), backfill from `subscription_status` during deploy, ship in next release.

**Recommendation: DO NOT APPROVE — REVISE.**

This plan is dangerously underspecified for a production change of this size and reversibility profile. It is a one-way door dressed up as a routine migration. Below I lay out the reasoning by domain, the risks, and the concrete revisions required before this can be approved.

---

## Cynefin domain

This sits in the **Complicated** domain. The mechanics of online schema change on large tables are well understood (good practice exists), but they require expert judgment, sequencing, and instrumentation. It is not Simple (no "just run the migration" recipe applies safely at 50M rows with NOT NULL during deploy), and it is not Complex (the failure modes are knowable in advance). Treat it accordingly: design first, sequence carefully, instrument heavily.

## Reversibility / blast radius

This is a **one-way door with a large blast radius**:

- The change touches the `users` table — almost certainly a hot, central table whose locking behaviour will fan out across the system.
- A NOT NULL column added in one shot on 50M rows will, on most engines (Postgres pre-11 in particular, and MySQL with default settings), require a full table rewrite under an exclusive lock. Even on engines that support it as a metadata-only operation, the constraint validation against existing rows is non-trivial.
- "Backfill during deploy" implies the deploy window blocks until 50M rows are written. Even at 10k rows/sec that's >80 minutes; realistic backfills against a live primary are slower and contend with production traffic.
- Once the column exists with NOT NULL and is being read/written by the new code path, **rolling back is not free** — you must drop the column (which itself takes a lock) or leave a vestigial nullable column that the old code doesn't know about.

A change of this profile demands the **Full review tier**: production data, central table, one-way door auto-fires.

---

## Bucket-by-bucket review

### B1 — Problem framing

**Verdict: SUSTAINED.** The plan describes *what* (add column, backfill, ship) but not *why*. There is no problem statement, no user/business outcome, no measurable success criterion. We cannot evaluate whether the schema change is the right solution because we do not know what problem it solves. A computed view, a denormalised cache, or even a feature-flagged read-through from `subscription_status` may all be cheaper and more reversible.

**Falsifying condition:** if the team can produce a written problem statement showing that `user_tier` must be a persistent column (not derivable on read) because of join-cost or query-shape constraints with named workloads, this is satisfied.

### B2 — Constraints / NFRs

**Verdict: SUSTAINED.** No NFRs named. We need: maximum acceptable lock duration, maximum acceptable read/write latency degradation during backfill, deploy window length, on-call coverage, error-budget impact. "Ship in next release" is not a constraint; it's a wish.

### B3 — Alternatives

**Verdict: SUSTAINED.** No alternatives considered in writing. The standard expand-migrate-contract pattern is the obvious alternative and is not mentioned: (1) add the column nullable with a default; (2) backfill in chunks via a background job, throttled, with progress metrics; (3) dual-write from application code; (4) verify backfill complete; (5) add the NOT NULL constraint as a separate, validated step (e.g. `ALTER TABLE … ADD CONSTRAINT … NOT VALID` then `VALIDATE CONSTRAINT` in Postgres); (6) drop the dual-write once the new column is canonical. This is the boring, well-trodden path. The plan as written skips it.

### B4 — Dependencies / sequencing

**Verdict: SUSTAINED.** "Backfill during deploy" couples three things that should be decoupled: the schema change, the data backfill, and the application release that depends on the new column. If any one fails, all three are in an inconsistent state. Deploy ≠ release; backfill ≠ either.

### B5 — Reversibility / ADR

**Verdict: SUSTAINED.** No Alternatives section. No ADR named. No reversibility analysis. For a one-way door of this magnitude, a written ADR (Context / Decision / Consequences) is the minimum bar. The decision to make the column NOT NULL at creation time, rather than via a deferred constraint addition, is itself an architecturally significant decision and is not justified.

### B6 — Operability / success metrics

**Verdict: SUSTAINED.** Multiple critical gaps:

- **No rollback path named.** What happens if the deploy fails halfway through the backfill? What happens if the new column is wrong (subscription_status mapping is buggy)? "Drop the column" on a 50M-row table is itself a long-locking operation.
- **No backfill progress metrics named.** How will on-call know whether the backfill is healthy, stalled, or about to exhaust the deploy window? Rows-processed-per-second, ETA, lag against primary, replication lag — all unspecified.
- **No capacity headroom analysis.** A full table rewrite or chunked backfill against a hot table consumes IO, CPU, WAL/binlog volume, and replica lag budget. None of this is sized.
- **No SLO impact assessment.** What does this do to p95 read/write latency on `users` during the backfill? What's the error-budget cost?
- **No monitoring/alert plan.** No named dashboards, no alert thresholds, no on-call runbook.

### B7 — Stop-the-line conditions

**Verdict: SUSTAINED.** The plan does not name conditions under which the migration aborts itself. At minimum: replica lag exceeding threshold, primary CPU above threshold, error rate on `users` queries above threshold, deploy window approaching exhaustion. Without explicit abort conditions, "something's wrong" turns into a 3am judgement call by whoever happens to be on-call.

### B8 — Evidence / verification

**Verdict: SUSTAINED.** No staging rehearsal mentioned. No load test against a representative dataset. No verification that the `subscription_status → user_tier` mapping is correct and stable. For a one-way door, the only acceptable evidence is "we ran this against a production-shaped dataset and observed the following."

---

## Required revisions before approval

1. **Problem statement and success metric.** Write down what business/engineering outcome this column enables, why a persistent column (not a view/derivation) is required, and what metric will move.
2. **ADR.** Context, decision, alternatives (including expand-migrate-contract), consequences, reversibility cost.
3. **Re-shape to expand-migrate-contract.** Add column nullable. Backfill in chunked background job with throttling and progress metrics. Validate. *Then* add NOT NULL constraint as a separate, instrumented step.
4. **Decouple deploy from release.** Schema change, backfill, and application cutover are three separate, independently rollback-able steps gated by feature flags.
5. **Operability plan.** Named dashboards, named metrics (rows/sec, ETA, replica lag, primary CPU, p95 latency on `users`), named alert thresholds, named abort conditions, named on-call runbook, named rollback procedure for each stage.
6. **Capacity sizing.** Show the maths: how long does the backfill take at the throttled rate, what's the IO/CPU/WAL impact, what's the replica-lag budget.
7. **Staging rehearsal.** Run against a production-shaped dataset; record timing, lag, and error metrics; attach to the ADR.
8. **Mapping verification.** Prove the `subscription_status → user_tier` mapping is total (every existing value maps), stable (won't change during backfill), and correct (sampled validation).

---

## Bottom line

As stated, this plan would be approved by no senior reviewer who has lived through a botched online schema change. The defaults it skips — nullable-then-validate, chunked backfill, decoupled release, observability, rollback — are the defaults precisely *because* the failure modes it doesn't address have repeatedly taken systems down.

**Recommendation: REVISE.** Re-submit with the eight items above addressed. If the team's appetite cannot accommodate that work, the alternative recommendation is **KILL** — do not ship a one-way door without the safeguards.
