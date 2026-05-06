# Plan review: schema-migration-user-tier

## Plan reference

> Add NOT NULL column `user_tier` to `users` table (50M rows), backfill from `subscription_status` during deploy, ship in next release.

## Trigger check

Triggered (auto-fire, condition 4): plan touches production data (users table) AND contains a one-way-door decision (schema migration). Trigger 3 (touches code/systems not personally traced this week) likely also fires.

## Step 1a — Fast-track gate

**Does NOT fire.** Precondition 2 fails: not fully reversible. A NOT NULL column added and backfilled to a 50M-row production table cannot be restored to prior state by a one-commit revert — the schema change, the backfill writes, and any read paths that started consuming the column constitute an irreversible state mutation. Precondition 1 also fails: this is a schema migration, not KTLO. Falling through to normal flow.

## Inputs

- **Appetite**: unspecified — plan says "next release" without naming a fixed cap. Flagged under B7.
- **Cynefin domain**: **Complicated** — known cause-effect (schema migration on a large table is a well-understood class of problem with established expert practice: expand-contract pattern, online schema change tooling, batched backfill). Not Complex (no emergent behaviour) and not Clear (the 50M-row scale and NOT NULL constraint require expertise to execute safely).
- **Tier**: **Full** — selected because plan touches production data AND contains a schema migration (one-way door). Both auto-select attributes hold.

## B1 — Problem framing

**SUSTAINED.** The plan opens with a solution ("add NOT NULL column user_tier, backfill from subscription_status") and never names the user or business problem this is solving. Why does the system need user_tier as a first-class column? Who is the consumer (billing? feature gating? analytics?)? What outcome is expected to move? Without a problem statement, the team cannot judge whether the chosen solution (denormalised column with backfill) beats alternatives (computed view, lazy backfill, reference table join).

**Falsifying condition:** plan is amended to include a problem statement with the consumer named and a measurable outcome — e.g. "feature-gating service needs O(1) tier lookup at request time; current join via subscription_status adds 40ms p95 we want to remove."

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| Read-path consumers of `users.user_tier` (which services will start reading the new column?) — undeclared | SUSTAINED | Plan lists every service expected to read user_tier post-launch, with cutover order |
| Backfill semantics for rows where `subscription_status` is NULL, expired, in-grace-period, or pending — undeclared | SUSTAINED | Plan defines the mapping table from every subscription_status value to a user_tier value, including null/edge cases |
| "During deploy" — duration and locking behaviour on a 50M-row table is vague enough to cause an outage | SUSTAINED | Plan names the migration tool (pt-osc / gh-ost / Postgres ADD COLUMN behaviour) and the expected duration with table-lock window |
| Drift handling: what happens when subscription_status changes after backfill? — undeclared | PARTIAL | Plan names whether user_tier is kept in sync via trigger / app-write / scheduled job, or is one-shot |
| Downstream replicas, read replicas, and analytics pipelines that observe schema — undeclared | SUSTAINED | Plan lists each replica/CDC consumer and the order they receive the change |

Five SUSTAINED-or-PARTIAL items. The plan's terseness is itself a scope-clarity defect.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| `subscription_status` is a complete, clean source of truth for tier (no NULLs, no unmapped values, no historical edge cases on 50M rows) | 0.1 (assumption, no evidence cited) | 5-min test: `SELECT subscription_status, COUNT(*) FROM users GROUP BY 1` — surface the actual value distribution including NULL count | SUSTAINED |
| Adding NOT NULL column + backfill "during deploy" can complete in a deploy window without locking the table or blocking writes | 0.1 (assumption — Postgres ADD COLUMN NOT NULL with default rewrites the table on older versions; on Postgres 11+ it's metadata-only ONLY for constant defaults; backfill of 50M rows from another column is never instant) | 5-min test: confirm Postgres version, confirm whether default is constant or computed; estimate backfill time on a representative slice | SUSTAINED |
| One release cycle is enough time to do this safely | 0.1 (no evidence) | Owner sign-off: DBA / platform on-call lead must confirm | SUSTAINED |

All three riskiest assumptions score 0.1 on Gilad — opinion/assumption with no cited evidence. **Per Step 6, untested assumptions with Confidence < 5 block APPROVE.**

## B4 — Dependencies (Full)

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| DBA / platform team — review migration plan, online schema tool selection, capacity reservation during backfill | Not named in plan | Not confirmed | SUSTAINED |
| On-call team during the deploy window (long-running migration changes paging posture) | Not named | Not confirmed | SUSTAINED |
| Downstream consumers of `subscription_status` and any service that will adopt `user_tier` — coordination on read order | Not named | Not confirmed | SUSTAINED |
| Analytics / data warehouse team — schema change propagates to ETL | Not named | Not confirmed | SUSTAINED |
| Backup / point-in-time-recovery validation before destructive change | Not named | Not confirmed | SUSTAINED |

Per Universal Rule B7, unconfirmed cross-team dependencies are the single largest cause of missed commitments. Five surfaced; none confirmed.

## B5 — Reversibility + ADR pairing (Full)

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Schema change to a 50M-row production table (NOT NULL column, backfilled from another column) | No — plan names a single approach | No ADR named or committed | SUSTAINED |
| Choice of `subscription_status` as backfill source (vs. computed view, derived table, reference table join, lazy column with default) | No | No | SUSTAINED |
| Coupling tier semantics to a column that may need to evolve independently of subscription_status | No | No | SUSTAINED |

A NOT NULL column with backfill is among the most expensive schema changes to reverse — once the column exists, application code adopts it, downstream systems adopt it, and the path back to "no column" requires undoing all of that. The plan records no alternatives and commits to no ADR. **SUSTAINED on the headline reversibility check.**

## B6 — Operability + success metrics (Full)

- **Metrics**: **absent.** Plan names no metrics for the migration itself (rows backfilled per second, lag from start, error rate on inserts during backfill).
- **Alerts**: **absent.** No alerts named for migration stall, replication lag spike, lock-wait queue growth, or write-path latency regression.
- **Rollback path**: **absent.** Plan does not describe how to roll back if the migration stalls or fails partway through. A NOT NULL column with backfill mid-flight has no clean revert without forward-fix engineering — this needs to be planned, not improvised at 3am.
- **Runbook**: **absent.** No on-call runbook for what to do if backfill exceeds the deploy window, if locks accumulate, if a downstream replica falls behind.
- **Capacity headroom**: **absent.** No estimate of the IO/CPU/replication-lag impact of writing 50M rows during the deploy. No statement of whether the backfill will be batched, throttled, or executed in a single transaction.
- **User-visible outcome metric**: **absent.** The plan names no outcome — what user-visible behaviour is expected to change? What metric will confirm the change worked? Without this, "done" cannot be defined.

**SUSTAINED on both halves.** Operability section is entirely missing. Per Universal Rule A6, this alone blocks APPROVE.

## B7 — Sequencing + capacity (Full)

- **Critical path**: not surfaced. The plan does not name what blocks what (e.g. does column add precede backfill in the same deploy, or are they staged?).
- **Appetite fixed?**: no. "Ship in next release" is a calendar pointer, not a fixed appetite cap. There is no statement of "if the migration exceeds N hours, we cut and revert."
- **FTE consistent?**: cannot evaluate — no team or capacity named.

The single-deploy framing ("backfill during deploy") collapses three distinct phases (schema change, backfill, cutover) into one event, which is the textbook way to turn a recoverable problem into an outage. Industry-standard pattern is expand-contract: (1) add nullable column, (2) backfill incrementally, (3) start dual-writing, (4) flip reads, (5) add NOT NULL constraint, (6) drop old source. This plan does (1)+(2)+(5) atomically.

## B8 — Pre-mortem (Full)

Prospective hindsight: the plan shipped and failed within its appetite. Top 3 reasons ranked by likelihood:

1. **Backfill during deploy locked or slow-queried the users table, causing write-path latency spike and a partial outage; rollback was attempted but the column already existed and downstream code had started reading it.** Most likely failure mode. **Kill-switch:** dry-run the backfill on a production-clone with timing measured; require backfill plan to be batched/throttled with a stated "abort if exceeds N minutes" trigger BEFORE starting deploy.
2. **`subscription_status` contained NULL or unmapped values (expired, trialing, churned-but-grandfathered) and the NOT NULL constraint failed mid-backfill, leaving the table in a half-migrated state with no clean rollback.** **Kill-switch:** run `SELECT subscription_status, COUNT(*) FROM users GROUP BY 1` and validate every value maps to a defined tier BEFORE writing the migration; require a default-tier fallback for unmapped values.
3. **Downstream consumer (analytics ETL, replica, CDC pipeline) broke on the schema change and was discovered hours later when a dashboard went stale.** No kill-switch named in the plan; this is a discoverability failure that the dependency review (B4) is meant to prevent.

## Recommendation

**REVISE** — multiple unresolved SUSTAINED verdicts across B1, B2, B3, B4, B5, and B6. The plan as written is a one-line solution sketch for a class of work (50M-row schema migration with backfill on a production table) that has well-known failure modes the plan does not address. The Quick-tier reversibility carve-out does not apply — Full tier was auto-selected precisely because the plan is not reversible.

This is on the boundary of KILL: the plan's core premise — "do all of this in one deploy" — is structurally unsafe at 50M rows. If the owner cannot commit to the expand-contract restructuring below, the recommendation upgrades to KILL.

### Conditions

Before re-review, the plan must:

1. **B1**: Add a problem statement naming the consumer of `user_tier` and the measurable outcome expected. (Universal P2.)
2. **B2**: Define the backfill mapping for every `subscription_status` value, including NULL, expired, pending, and any in-grace state. List read-path consumers and the cutover order.
3. **B3**: Validate the three SUSTAINED assumptions before execution — (a) actual `subscription_status` value distribution on production, (b) Postgres version and ADD COLUMN behaviour with the chosen default, (c) DBA/platform on-call sign-off on the migration window. Each must move from Confidence 0.1 to ≥5.
4. **B4**: Name and confirm in writing: DBA/platform owner, on-call lead, downstream consumer owners, analytics/ETL owner, backup-validation owner.
5. **B5**: Write an ADR naming alternatives considered (computed column, expand-contract migration with nullable column + incremental backfill + NOT NULL last, denormalised column, reference table). Record the chosen approach with reversal cost.
6. **B6**: Add the operability section in full — backfill throughput metric, replication-lag alert, write-latency alert, rollback path (likely "leave column nullable until backfill verified, defer NOT NULL to a separate deploy"), on-call runbook, capacity headroom estimate, and a user-visible outcome metric.
7. **B7**: Restructure as expand-contract across multiple deploys: (a) add nullable column, (b) batched/throttled backfill with progress metric, (c) dual-write from application, (d) verify, (e) add NOT NULL constraint in a separate deploy, (f) optionally drop the source. Each phase has its own appetite cap and its own revert.
8. Set a fixed appetite per phase, not "next release."
