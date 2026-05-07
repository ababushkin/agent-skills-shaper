# Plan review: add-not-null-user-tier-50m-rows

## Plan reference

> "Add NOT NULL column user_tier to users table (50M rows), backfill from subscription_status during deploy, ship in next release."

## Inputs

- **Appetite**: not stated — implied "next release" (1–2 sprints; assumed ≤2 weeks for tier selection)
- **Cynefin domain**: Complicated — migration patterns are knowable with expertise; scale (50M rows) and deploy-time backfill require deliberate execution, not discovery
- **Tier**: Full — auto-selected: plan contains ≥1 one-way-door decision (NOT NULL schema column) and touches production data (50M-row backfill during deploy)

---

## B1 — Problem framing

**SUSTAINED.**

The plan opens with a solution: "add NOT NULL column user_tier." No problem statement is present. There is no articulation of what business or user outcome requires `user_tier`, why it must be NOT NULL from day one, or what behaviour is broken without it. "Backfill from subscription_status" implies a mapping relationship exists, but the mapping rules, failure cases, and edge conditions are not stated.

**Falsifying condition**: a written problem statement appears that names (a) the business/user outcome this column enables, (b) why NOT NULL is required immediately rather than nullable-then-constrain, and (c) the mapping rule from `subscription_status` → `user_tier` including nulls, unknowns, and mismatches.

---

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| Deploy-time backfill on 50M rows — not declared as a scope risk | SUSTAINED | Plan explicitly names estimated backfill duration, lock behaviour on the DB engine in use, and whether the deploy window is sized to accommodate it |
| Mapping logic from `subscription_status` to `user_tier` — undeclared | SUSTAINED | A mapping table or rule set appears in the plan, including what happens when `subscription_status` is NULL, unknown, or in a state without a `user_tier` equivalent |
| Application code that reads/writes `user_tier` — undeclared as in-scope | SUSTAINED | Plan names all application callsites that will need updating before or concurrent with the migration, and confirms no code path will attempt to write a row without supplying `user_tier` |
| Rollback path — not in scope at all | SUSTAINED | Plan includes a rollback procedure: at minimum, whether dropping the column is possible post-deploy, and whether the backfill is reversible or destructive |

**Note:** Four SUSTAINED items on B2, not three. Zero of the four can be hand-waved as vague — they are concretely absent.

---

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| Backfill during deploy is safe — table won't lock or cause downtime on 50M rows | 0.1 (assertion; no evidence cited) | Run `EXPLAIN` on the backfill query; check DB engine docs for lock behaviour on `ALTER TABLE … NOT NULL` with concurrent writes; time a dry-run on a staging clone of prod size | SUSTAINED |
| `subscription_status` covers all rows — no NULLs, no unmapped states | 0.1 (assumption; no data cited) | `SELECT COUNT(*) FROM users WHERE subscription_status IS NULL OR subscription_status NOT IN (<known values>)` — takes seconds | SUSTAINED |
| Application code can supply `user_tier` on all INSERT/UPDATE paths before the column is NOT NULL | 0.1 (implicit assumption; no audit performed) | Search codebase for all `INSERT INTO users` and `UPDATE users` callsites; confirm each either sets `user_tier` or is wrapped in the deploy ordering | SUSTAINED |

All three assumptions have Confidence 0.1 (opinion/assertion). All three block APPROVE under B3 rules.

---

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| DB engine behaviour under `ALTER TABLE … NOT NULL` on 50M rows (Postgres/MySQL/etc.) — not named | No — DB engine not even stated | N/A — no one assigned | SUSTAINED |
| Application deploy ordering — application must not write rows without `user_tier` before backfill completes | No owner named | No sequencing plan | SUSTAINED |
| DBA / platform team sign-off on migration window | Not mentioned | Not mentioned | SUSTAINED |
| Monitoring / on-call coverage during backfill + deploy | Not mentioned | Not mentioned | SUSTAINED |

---

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| NOT NULL constraint on `user_tier` — once added with live data, removing requires another migration and deploy cycle | No alternatives stated | No ADR mentioned or committed | SUSTAINED |
| Deploy-time backfill (destructive write to 50M rows) — if mapping is wrong, data is corrupted in place | No alternatives stated (e.g. nullable → populate → constrain; background job pre-deploy; expand-contract pattern) | No ADR | SUSTAINED |

**Alternatives not considered in the plan:**

1. **Nullable first, constrain later** — add `user_tier NULL`, deploy application code that populates it on write, run a background backfill job over days rather than at deploy-time, then add the NOT NULL constraint in a follow-up migration once coverage is 100%.
2. **Expand-contract (parallel column)** — populate a shadow column, verify it matches expected distribution, then swap constraint.
3. **Default value as safety net** — add the column with a safe default (e.g. `'unknown'`) to avoid NOT NULL enforcement during deploy, then tighten the constraint once all rows are confirmed populated and application code is validated.

None of these are named, let alone rejected with justification. This is an undocumented one-way door.

---

## B6 — Operability + success metrics

- **Metrics**: absent — no mention of how post-deploy health is measured
- **Alerts**: absent — no mention of error rate, query latency, or replication lag alerts during backfill
- **Rollback path**: absent — the plan has no rollback. Dropping a NOT NULL column is a second migration; if the backfill produced bad data, there is no described procedure
- **Runbook**: absent
- **Capacity headroom**: absent — 50M-row backfill will consume significant DB I/O; no mention of whether this will saturate IOPS, spike replication lag, or hit read replicas
- **User-visible outcome metric**: absent — the plan states no observable user or business outcome it is trying to move

Both halves of B6 are entirely absent. This blocks APPROVE.

---

## B7 — Sequencing + capacity

Critical path is not surfaced. The plan implies a single-step deploy ("backfill during deploy"), which is the riskiest possible sequence for a 50M-row table:

1. Application code must be compatible with the new column **before** the migration runs — otherwise any in-flight INSERT will fail with a NOT NULL violation.
2. The migration must complete the backfill **before** the NOT NULL constraint is enforced — otherwise rows inserted between migration start and backfill completion will violate the constraint.
3. The rollback state is undefined at every point in this sequence.

Appetite is not fixed. "Next release" is a target, not a time-boxed cap. No FTE is named. No estimate of backfill duration is given (50M rows at typical batch rates can run minutes to hours depending on hardware and concurrency settings — this is unacknowledged).

**SUSTAINED** — sequencing is described in one clause ("backfill during deploy") that conceals the critical ordering problem.

---

## B8 — Pre-mortem

Assume the plan shipped and failed. Top 3 failure modes, ranked by likelihood:

**1 (highest likelihood): NOT NULL constraint fires during deploy, causing application errors or failed deploys.**
The deploy runs `ALTER TABLE users ADD COLUMN user_tier VARCHAR NOT NULL` while the application is still live. Any INSERT or UPDATE hitting the table before or during the backfill — new user signup, subscription change — produces a NOT NULL constraint violation, causing 500 errors or failed transactions. On a 50M-row table, the backfill takes non-trivial time; the window for this failure is wide.
Kill-switch: deploy monitoring showing 5xx spike within 60 seconds of migration start; kill-switch is an automated rollback gate on error rate. Pre-condition: define the error rate threshold before the deploy begins.

**2 (second likelihood): Backfill produces wrong `user_tier` values due to unmapped `subscription_status` states.**
The mapping from `subscription_status` → `user_tier` is assumed complete and correct. If any rows have NULL, deprecated, or unexpected `subscription_status` values, the backfill either fails mid-run (if the query errors) or silently writes a wrong tier (if a DEFAULT is applied). Wrong tier data affects downstream systems (pricing, feature flags, permissions) immediately on deploy — and the data is now in production with no rollback path described.
Kill-switch: run `SELECT subscription_status, COUNT(*) FROM users GROUP BY subscription_status` pre-deploy and validate every status value maps to a known tier. If unmapped states exist, the deploy does not proceed.

**3 (third likelihood): Backfill saturates DB I/O and causes replication lag, surfacing as stale reads on read replicas.**
A single UPDATE statement touching 50M rows without batching will hold a long-running transaction, spike WAL/binlog volume, and cause replica lag to spike. Read-heavy paths routed to replicas will see stale data during the window. Duration is unestimated; impact to read-heavy features (recommendations, dashboards) is unacknowledged.
Kill-switch (structural): batch the backfill in chunks (e.g. 10k rows per batch with a short sleep between) and monitor replica lag in real time; abort if lag exceeds threshold.

---

## Recommendation

**KILL** — the plan cannot be approved or revised in its current form without addressing a structural sequencing defect.

The plan describes a deploy-time backfill on 50M rows with a NOT NULL constraint, no rollback path, no mapping validation, and no operability plan. This is not a scope gap that can be addressed by adding a line to the plan — the sequencing approach itself is wrong. The correct sequence (expand-contract or nullable-first) requires a different migration structure, not a better-written version of the same plan.

### Conditions to unblock (all must be met before re-submission)

1. **B1**: Add a problem statement naming the business/user outcome, why NOT NULL is required immediately, and the complete mapping rule from `subscription_status` → `user_tier` including edge cases.
2. **B2/B5**: Replace the deploy-time backfill approach with a safe migration sequence — nullable-first, background backfill, constraint-later is the standard pattern for this class of change on large tables. Name and reject alternatives in writing (ADR).
3. **B3**: Run `SELECT subscription_status, COUNT(*) FROM users GROUP BY subscription_status` before any migration work; confirm every value maps to a known tier.
4. **B3**: Audit all application INSERT/UPDATE paths for `users` table; confirm each supplies or tolerates `user_tier` throughout the migration window.
5. **B4**: Name the DB engine; confirm lock behaviour on the chosen migration approach with DBA or platform owner in writing.
6. **B6**: Add rollback path (what happens if backfill produces wrong data), monitoring plan (error rate, replica lag, IOPS during migration), and a user-visible outcome metric.
7. **B7**: Fix the appetite to a named cap (not "next release"); estimate backfill duration on staging with prod-sized data.
