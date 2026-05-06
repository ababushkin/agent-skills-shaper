# Plan review: add-user-tier-not-null-column

## Plan reference

Pasted from prompt:
> Add NOT NULL column `user_tier` to `users` table (50M rows), backfill from `subscription_status` during deploy, ship in next release.

## Inputs

- **Appetite**: unstated. Plan says "next release" with no time cap. Treated as >1 day for tier selection (50M-row backfill alone exceeds 1-day appetite for any safe execution path).
- **Cynefin domain**: Complicated — known cause-effect at this table scale (online schema change patterns are well-understood) but requires expertise to execute without lock contention, replication lag, or deploy-window failure.
- **Tier**: Full — auto-selected because the plan (a) contains a one-way-door schema migration on 50M rows, (b) touches production data, and (c) implies cross-team coordination (deploy + DB ops). Fast-track gate did NOT fire: class is not KTLO, change is not fully reversible (dropping a NOT NULL column post-write is a data-loss operation, not a one-commit revert).

## B0 — Trigger and gate notes

- Trigger: auto-fire (schema migration + production-data touch).
- Fast-track gate evaluated and failed on preconditions 1 (not KTLO) and 2 (not fully reversible).

## B1 — Problem framing

**Verdict: SUSTAINED.** The plan opens with a solution ("add NOT NULL column user_tier, backfill from subscription_status") with no problem statement. There is no stated user or business outcome, no measurable target, no reason this column must exist now versus later or as nullable versus NOT NULL. Universal P2 violation.

- **Falsifying condition**: a one-line problem statement of the form "For [segment], we need [outcome] which requires user_tier to exist as NOT NULL because [specific downstream constraint, e.g. a query path that cannot tolerate NULLs, a billing calculation, a regulatory reporting need]." Absent that, the NOT NULL constraint itself is unjustified — a nullable column would deliver the same data with vastly lower migration risk.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| Application code that writes to `users` (every INSERT path) — must be updated to supply `user_tier` before the NOT NULL constraint is applied, but the plan doesn't mention it | SUSTAINED | A list of every code path that INSERTs into `users` with confirmation each one supplies `user_tier`, OR a default value declared at the column level |
| Replica lag during a 50M-row backfill — the backfill will generate substantial WAL/binlog volume; the plan doesn't acknowledge replica impact | SUSTAINED | Named batch size, throttle rate, and observed replica-lag tolerance from a prior backfill of comparable volume on this DB |
| Downstream consumers of `users` (analytics ETL, replicas, CDC streams, search index) — schema change propagates; not mentioned | SUSTAINED | An enumerated list of downstream consumers with confirmation that each tolerates the new column or has a planned update |
| "Backfill from subscription_status" — undefined mapping. What `subscription_status` values map to what `user_tier` values? Is the mapping reversible? What about NULL `subscription_status`? | SUSTAINED | A documented mapping table (subscription_status → user_tier) with explicit handling for NULL, unknown, and edge-case values |
| "During deploy" — vague. Is this a single transaction during deploy? A background job kicked off by deploy? A blocking step that holds the deploy open until 50M rows are written? | SUSTAINED | Named execution mechanism with time-bound: e.g. "online migration via gh-ost / pt-online-schema-change run over N hours, deploy ships the schema once backfill completes" |
| "Ship in next release" — appetite is unstated and the constraint is calendar-driven not capacity-driven | SUSTAINED | A fixed appetite (e.g. "2 weeks of engineering time, including online-migration runtime") with the next-release date treated as a separable concern |

Six SUSTAINED items at this aggression level confirms the plan is dangerously underspecified for its blast radius.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| A NOT NULL column can be added to a 50M-row table during a normal deploy window without causing app-blocking lock contention | 0.1 (opinion) | DBA sign-off + a staging-environment timing test on a comparable-size table. Most engines (Postgres pre-11, MySQL without online DDL tooling) will rewrite the table or hold an ACCESS EXCLUSIVE/metadata lock. On Postgres 11+, NOT NULL with a non-volatile DEFAULT can be metadata-only — but with a backfill from another column it is NOT a metadata-only operation | SUSTAINED |
| Every existing row has a `subscription_status` value that maps cleanly to a non-null `user_tier` | 0.1 (opinion) | `SELECT COUNT(*) FROM users WHERE subscription_status IS NULL` plus a value-distribution query — both runnable in <5 min | SUSTAINED |
| The deploy window is long enough to backfill 50M rows | 0.1 (opinion) | Throughput test on staging or a calculation: at typical 1–10k rows/sec throttled writes that's 1.4–14 hours. Confirm the deploy strategy can absorb that, or move backfill out of deploy entirely | SUSTAINED |
| Application writes to `users` will all have a `user_tier` value at cutover so the NOT NULL constraint will not break inserts | 0.1 (opinion) | Code grep + named owner per write path; OR, safer: ship the column nullable, deploy code that writes it, backfill, THEN add the NOT NULL constraint as a separate change | SUSTAINED |
| Rollback is not needed because the change "just works" | 0.1 (opinion) | Documented rollback procedure for: (a) schema-only revert (DROP COLUMN — destroys data), (b) backfill-only revert (UPDATE users SET user_tier = NULL — fails because NOT NULL), (c) constraint-only revert (ALTER TABLE DROP CONSTRAINT). The plan as stated has no clean revert path | SUSTAINED |

All five assumptions sit at Confidence 0.1. Universal P4 violation: untested assumptions with Confidence < 5 block APPROVE.

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| DBA / DB-ops review and execution-window approval | No — not mentioned | No | SUSTAINED |
| Application teams owning every INSERT path on `users` | No | No | SUSTAINED |
| Downstream data consumers (ETL, search, analytics, CDC) | No | No | SUSTAINED |
| Online schema-change tooling (gh-ost, pt-osc, pg-osc, or native DDL strategy) — does the team have it operationalised? | No | No | SUSTAINED |
| On-call / SRE coverage for the deploy window given the elevated risk | No | No | SUSTAINED |

Universal Rule B7 violation: zero confirmed dependencies on a plan that has at least five.

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| NOT NULL constraint on a populated 50M-row column — once production rows are written and code depends on non-null, removing the constraint is reversible but removing the column is data-destructive | No | No | SUSTAINED |
| Backfill mapping `subscription_status → user_tier` — once 50M rows are written under a specific mapping, reversing requires either preserving `subscription_status` or accepting data loss | No | No | SUSTAINED |
| "During deploy" execution model — coupling schema change to deploy means a deploy rollback after backfill begins is not a clean operation | No | No | SUSTAINED |

Universal P3 + Rule B3 violation: alternatives not named; ADR not committed. The most obvious alternative — ship column nullable, backfill async, add NOT NULL in a follow-up release — is not even mentioned.

## B6 — Operability + success metrics

- **Metrics**: absent. No mention of backfill progress metric, replica-lag metric, lock-wait metric, INSERT error rate.
- **Alerts**: absent. No alert on backfill stalled, replica lag exceeding threshold, post-deploy INSERT failures, or NOT NULL constraint violations during cutover.
- **Rollback path**: absent. The plan has no rollback at all — see B5.
- **Runbook**: absent. No on-call procedure if backfill stalls mid-deploy or if the deploy hangs waiting for the backfill.
- **Capacity headroom**: absent. No statement on DB CPU/IOPS headroom during backfill, replica capacity, or WAL/binlog disk consumption.
- **User-visible outcome metric**: absent — and unclear it would even exist, because B1 has no problem statement to derive a metric from.

Universal Rule A6 violation. Operability section is entirely absent on a Full-tier plan.

## B7 — Sequencing + capacity

- **Critical path**: not surfaced. The plan implies "schema change → backfill → NOT NULL constraint" all happen "during deploy" but doesn't name the order or what blocks what.
- **Appetite**: not fixed. "Next release" is a deadline, not an appetite. The actual work is bounded by backfill throughput (hours), DBA review (days), and code changes to write paths (days–weeks).
- **FTE consistency**: not stated. Single-person plan? Cross-team? Unknown.

The sequencing implied by the plan (schema change AND backfill AND NOT NULL constraint AND deploy as a single atomic event) is the highest-risk possible sequencing for a 50M-row change. Standard safer sequence: (1) add column nullable + default, (2) deploy code that writes it, (3) backfill async with throttle, (4) verify zero NULLs, (5) add NOT NULL constraint as separate migration, (6) drop the source column or default if applicable.

## B8 — Pre-mortem (Full)

Top 3 failure modes ranked by likelihood:

1. **Deploy hangs waiting for the backfill, on-call rolls back, application writes during partial-backfill state produce inconsistent data.** Most likely outcome of executing the plan literally as written. Kill-switch: a precondition check before the deploy that the backfill must already be complete (i.e. backfill is NOT part of deploy) and the only deploy-time operation is applying the NOT NULL constraint on an already-populated column.
2. **NOT NULL constraint application fails because some rows have NULL `subscription_status` (and therefore NULL `user_tier` after backfill), aborts the deploy mid-flight, leaving the column added but not constrained, with code expecting non-null reads.** Second most likely. Kill-switch: a pre-flight query `SELECT COUNT(*) FROM users WHERE subscription_status IS NULL` run before the deploy starts; if non-zero, the deploy is blocked and the mapping for NULL is resolved first.
3. **Backfill saturates DB IOPS and replica lag, causing user-facing query latency spike and read-replica fallback exhaustion during deploy window.** Third. Kill-switch is a watchdog metric: replica-lag SLO breach pauses the backfill; deploy is decoupled from backfill so the pause does not extend the deploy window.

## Recommendation

**REVISE** — at minimum the following must be addressed before this plan can be approved:

### Conditions

1. **Add a problem statement** (B1) specifying why `user_tier` is needed, what outcome it serves, and why NOT NULL specifically is required versus a nullable column with application-level defaulting.
2. **Decouple backfill from deploy** (B7, B8). Standard safer sequence: (a) ship nullable column with a default, (b) deploy code that writes it on every INSERT path, (c) backfill async with throttle and replica-lag governance, (d) verify zero NULLs, (e) add NOT NULL constraint as a separate small migration. Each of these is independently revertable; the plan as written is not.
3. **Define the `subscription_status → user_tier` mapping in writing**, including explicit handling for NULL and unknown values (B2, B3).
4. **Confirm dependencies in writing** (B4): DBA sign-off on execution plan, every INSERT-path owner confirming their code supplies `user_tier`, downstream consumer owners confirming the new column.
5. **Write an ADR** (B5) capturing alternatives considered (notably the nullable-first sequence) and the rollback procedure for each stage.
6. **Add the operability section** (B6): backfill-progress metric, replica-lag alert, INSERT-failure-rate alert, runbook for backfill-stall during deploy, capacity headroom statement.
7. **Run the B3 5-minute tests now** — at least the NULL-count query on `subscription_status` and the staging-environment timing test for the schema change. These are minutes of work and would either confirm or refute the riskiest assumptions before any further planning.

The underlying intent (have a `user_tier` column on `users`) is reasonable and should not be killed. The execution plan as written is not safe and would predictably fail or cause an incident — REVISE, do not APPROVE.
