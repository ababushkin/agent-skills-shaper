# Plan review: schema-migration-user-tier-not-null

## Plan reference

Pasted plan (in conversation):

> "Add NOT NULL column user_tier to users table (50M rows), backfill from subscription_status during deploy, ship in next release. Approve?"

## Inputs

- **Appetite**: not stated. Inferred from "ship in next release" — implicitly ≤1 release cycle. **This is itself a SUSTAINED finding under B7**: appetite is not declared as a fixed cap.
- **Cynefin domain**: **Complicated** — schema migrations on large tables have known mechanics, but the plan touches a 50M-row hot table and a NOT NULL constraint, both of which have well-understood failure modes that demand expertise rather than experimentation.
- **Tier**: **Full** — auto-selected. Three of four Full-tier triggers fire:
  1. One-way-door decision (schema migration)
  2. Touches production data (users table)
  3. Cross-team-relevant (any service reading `users` is affected)

## Trigger check

Trigger 4 (auto-fire) holds: schema migration on production data. Review proceeds at Full tier; user override would require written justification.

## B0 — Cynefin

Complicated. Review depth emphasises dependencies, reversibility, and operability. The plan must demonstrate expertise was applied — not that the team will figure it out during deploy.

## B1 — Problem framing

The plan opens with a solution ("add NOT NULL column user_tier"), not a problem. There is no statement of:
- What user or business outcome is being moved
- Why `user_tier` needs to exist on `users` rather than computed/derived from `subscription_status` (which is already the source of truth, per the backfill instruction)
- What measurable target the change is meant to hit

**Verdict: SUSTAINED.** Falsifying condition: a problem statement of the form "For [segment], [problem] causes [negative outcome]; we expect [metric] to move by [target] within [horizon]" appears in the plan. (Universal P2; Product P2.)

If `subscription_status` is already the source of truth, the plan may not need to exist at all — denormalising into a new NOT NULL column may be solving a problem that doesn't exist, or solving the wrong one.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| Application code that writes to `users` (every INSERT path) — must populate `user_tier` once NOT NULL is enforced; not declared in scope | SUSTAINED | The plan enumerates every write path and names the code change for each |
| Read paths and downstream consumers (analytics, billing, BI, replicas, ETL) that may break or behave differently when a new column appears | SUSTAINED | The plan lists every consumer of the `users` table and confirms compatibility |
| Backup/restore tooling, schema dumps, and any cross-environment fixtures that may carry stale rows lacking `user_tier` | SUSTAINED | The plan confirms restore-from-backup paths handle the new column |
| "Backfill from subscription_status" — vague; does not specify mapping rules, handling of NULL/unknown subscription_status, conflict resolution, or what happens to rows where status is ambiguous | SUSTAINED | The plan publishes the explicit mapping table including default and ambiguity rules |
| "During deploy" — vague; does not specify whether backfill runs before, during, or after the schema change, online or offline, in batches or single transaction | SUSTAINED | The plan specifies the exact sequence with batch size, locking strategy, and duration |
| "Ship in next release" — vague; does not specify rollout strategy (all-at-once, canary, region-by-region) | SUSTAINED | The plan names the rollout strategy with stages and progression criteria |

Six SUSTAINED. This is exactly the failure mode of a one-line plan: every word is vague enough to expand silently.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| 50M-row backfill can complete "during deploy" without exceeding deploy window or holding row/table locks long enough to cause production impact | **0.1** (assertion) | Run `EXPLAIN` and a representative batch on a staging clone of comparable size; measure p95 lock duration. Owner: DBA / database platform team | SUSTAINED |
| `subscription_status` cleanly maps to `user_tier` for every row (no NULLs, no edge cases, no orphan users with no subscription_status) | **0.1** (assertion) | `SELECT COUNT(*), subscription_status FROM users GROUP BY subscription_status` plus a check for NULL/unexpected values. Owner: Product / Billing | SUSTAINED |
| Adding a NOT NULL column on a 50M-row table is supported by the database engine without a full table rewrite + exclusive lock (Postgres pre-11 rewrites the table; many MySQL configurations require online DDL tools like gh-ost or pt-osc) | **0.1** (assertion) | Confirm DB engine + version; test on staging clone. Owner: DBA | SUSTAINED |
| All application write paths can be updated to populate `user_tier` in the same release as the schema change without race conditions between deploy and backfill | **0.1** (assertion) | Walk the code paths; confirm the deploy ordering (expand-migrate-contract pattern). Owner: Backend lead | SUSTAINED |
| The next release window is the right time to ship — i.e. no other risky changes coincide and there is rollback capacity | **0.1** (assertion) | Check release calendar and on-call rota. Owner: Release manager | SUSTAINED |

All five riskiest assumptions sit at Confidence 0.1 (opinion). None has been tested. Per Step 6, untested assumptions with Confidence < 5 block APPROVE.

**Verdict: SUSTAINED across all five.**

## B4 — Dependencies (Full)

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| DBA / database platform team — schema change review, online DDL tooling, lock-impact assessment | Not confirmed | Not confirmed | SUSTAINED |
| SRE / on-call — deploy window, rollback readiness, incident coverage during a 50M-row backfill | Not confirmed | Not confirmed | SUSTAINED |
| Billing / Product — authoritative mapping of `subscription_status` → `user_tier`, including ambiguous and historical states | Not confirmed | Not confirmed | SUSTAINED |
| Data / Analytics — schema-aware consumers of `users`, including warehouse ETL and BI dashboards | Not confirmed | Not confirmed | SUSTAINED |
| Backend service teams — every service that writes to or reads from `users` and may hit a NOT NULL violation post-cutover | Not confirmed | Not confirmed | SUSTAINED |

Five external dependencies, none confirmed. Universal Rule B7: unconfirmed cross-team dependencies are the single most common cause of missed commitments. **Verdict: SUSTAINED across all five.**

## B5 — Reversibility + ADR pairing (Full)

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Adding a NOT NULL column on a 50M-row production table — reversal requires an additional migration, a redeploy, and (if data was lost or corrupted) a restore from backup. The window of irreversibility opens the moment writes start populating the column. | None | None | SUSTAINED |
| Choice of single-step (NOT NULL from the start) vs. expand-migrate-contract (nullable column → backfill → enforce NOT NULL once verified) — these are not equivalent in blast radius | Not considered | None | SUSTAINED |
| Choice to denormalise into `users` vs. derive `user_tier` from `subscription_status` at query time vs. materialised view — a structural choice affecting every future read | Not considered | None | SUSTAINED |

This is the heart of the problem. The plan crosses three one-way doors without naming any of them, considering alternatives, or committing to an ADR. Universal P3 + Universal Rule B3 + Agentic P7 all fail simultaneously.

**Verdict: SUSTAINED across all three.** This bucket alone is sufficient to block APPROVE; the Quick-tier reversibility carve-out explicitly does not apply (and this is a Full-tier review anyway).

## B6 — Operability + success metrics (Full)

- **Metrics**: absent. No metric named for backfill progress, DB CPU/IO during migration, replication lag, error rate on writes to `users`, or NOT NULL violation count.
- **Alerts**: absent. No alert defined on backfill duration, lock wait time, deploy duration overrun, or write-path errors.
- **Rollback path**: **absent — and the prompt's title flags this as the named scenario**. There is no rollback plan. Rolling back a NOT NULL column add on a 50M-row table after writes have started is non-trivial: the column must be dropped (cheap) but any code paths now expecting the column will break, and any data written through the new code paths is lost in the revert. The plan must specify the deploy ordering (expand-migrate-contract) so that rollback at any stage is bounded.
- **Runbook**: absent. No on-call documentation for "what to do if backfill stalls at 30M rows," "what to do if the deploy window expires mid-backfill," or "what to do if a NOT NULL violation fires in production."
- **Capacity headroom**: absent. No statement of expected DB load increase during backfill, replication-lag tolerance, or concurrent-deploy compatibility.
- **User-visible outcome metric**: absent. No metric named whose movement would tell us whether the change worked. (Product P1.)

**Verdict: SUSTAINED on every line.** Universal Rule A6 (operability section) and Product P1 (outcomes not outputs) both fail. This bucket alone blocks APPROVE.

## B7 — Sequencing + capacity (Full)

- **Critical path**: not surfaced. Plan does not name what blocks what. The implicit ordering (`schema change → backfill → NOT NULL enforcement → application code update`) is one of several possible orderings, each with different risk profiles, and the plan picks none explicitly.
- **Appetite**: "next release" is a hope, not a cap. No fixed time budget. Per Universal Rule C1 / Shape Up appetites, this is not a commitment, it is a wish.
- **FTE consistent with appetite**: unanswerable — neither FTE nor appetite is stated.

**Verdict: SUSTAINED.** Falsifying condition: the plan publishes a sequenced, time-boxed Gantt or task list with named owners and a fixed appetite cap.

## B8 — Pre-mortem (Full)

Adopt prospective hindsight: the plan shipped and failed within its appetite. Top 3 reasons ranked by likelihood:

1. **Backfill held a long-running lock or saturated DB IO during deploy, causing a production incident.** Reads/writes to `users` queued, dependent services timed out, on-call paged, deploy was rolled back mid-backfill leaving the table in a half-migrated state. This is the single most common failure mode for large-table NOT NULL additions and the reason expand-migrate-contract exists.
   - **Kill-switch**: monitor backfill lock wait p95 and replication lag; abort and revert if either exceeds threshold within the first 5% of rows.

2. **`subscription_status` did not cleanly map to `user_tier` for some non-trivial fraction of rows** (NULLs, legacy values, churned users, B2B accounts with shared subscriptions). The NOT NULL constraint was violated at backfill time, the migration aborted, and the team had to scramble to invent a default mapping under deploy-window pressure — locking in a bad data decision permanently.
   - **Kill-switch**: run the count-by-status query before the deploy; if any unexpected value or NULL appears, halt and reshape.

3. **Application code paths were not all updated to populate `user_tier`, so post-cutover the next INSERT from a missed code path threw a NOT NULL violation in production.** Could be a job, a worker, an admin tool, a third-party integration — anything writing to `users` outside the main API paths.

This is a high-risk pre-mortem. All three failure modes are realistic, named, and specific.

## Recommendation

**REVISE** — bordering on **KILL** if the underlying problem framing (B1) cannot be defended.

One-line rationale: the plan crosses three one-way doors with zero alternatives considered, no operability plan, no rollback path, all key assumptions at Confidence 0.1, no dependencies confirmed, and a problem statement that does not exist. Approving this would be approving a wish, not a plan.

### Conditions

The plan must satisfy ALL of the following before re-review:

1. **B1**: Open with a problem statement. Name the user/business outcome, the metric, and the target. Justify why `user_tier` must be a denormalised NOT NULL column rather than derived from `subscription_status`.
2. **B2**: Enumerate every code path (read and write) that touches `users`. Specify the backfill mapping table including NULL/ambiguous cases. Specify the rollout strategy (canary/all-at-once/region-by-region).
3. **B3**: Run the five named 5-minute tests. Raise Confidence on every assumption to ≥5 before proceeding, or accept SUSTAINED and reshape.
4. **B4**: Confirm in writing the five named owners (DBA, SRE, Billing/Product, Data/Analytics, Backend leads).
5. **B5**: Write an ADR naming the alternatives considered (expand-migrate-contract vs. single-step; denormalise vs. derive vs. materialised view). Reversal cost must be named for each.
6. **B6**: Add an Operability section: backfill progress metric, lock-wait alert, replication-lag alert, on-call runbook, capacity-headroom estimate, named user-visible outcome metric.
7. **B7**: Replace "next release" with a fixed appetite. Publish the critical path. Confirm FTE.
8. **Adopt the expand-migrate-contract pattern as the default unless an ADR justifies otherwise**: (a) add column nullable; (b) deploy code that writes to it; (c) backfill in batches with progress tracking; (d) verify; (e) enforce NOT NULL in a separate migration; (f) drop the source column or derivation only after a soak period. Each step is independently revertible. The current plan collapses all six steps into one and loses revertibility entirely.

If the team cannot defend B1 — i.e. there is no problem requiring `user_tier` as a column at all — escalate from REVISE to **KILL**.

---

*Reviewer note: this plan is a textbook example of solution-first framing on a one-way-door change. The specific request "ship in next release" is the tell — the question being asked is "when," and the questions that should be asked first ("why," "how do we revert," "what could go wrong on 50M rows") have not been opened.*
