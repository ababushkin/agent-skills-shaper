# Plan review: add-not-null-user-tier

## Plan reference
Pasted from prompt: "Add NOT NULL column `user_tier` to `users` table (50M rows), backfill from `subscription_status` during deploy, ship in next release."

## Inputs
- **Appetite**: not stated. Plan says "next release" — treated as a hard cap of one release window, but undefined in calendar time. SUSTAINED finding under B7.
- **Cynefin domain**: Complicated. Schema migration on a 50M-row table on a hot system is knowable with expertise (online DDL patterns, dual-writes, lock contention) but the plan as written treats it as Clear, which it is not.
- **Tier**: Full — auto-selected because the plan touches production data, contains a schema migration (one-way door), and the migration class (NOT NULL on a large table) cannot be safely reversed in one commit. Fast-track gate did not fire (precondition 2 failed: not fully reversible; precondition 1 failed: schema migration is not KTLO).

## B1 — Problem framing
**SUSTAINED.** The plan is solution-first. It opens with "add NOT NULL column user_tier" — a schema action — with no problem statement, no user or business outcome, and no measurable target. Why does `user_tier` need to exist? Why NOT NULL rather than nullable? Why backfill from `subscription_status` rather than treat it as a derived view? None of this is framed.
- *Falsifying condition:* a one-paragraph problem statement is produced of the form "for [users / business], we need [outcome]; today this is blocked because [gap]; success looks like [metric]," and it justifies the NOT NULL constraint specifically.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| Application code that reads/writes `users` and now must populate `user_tier` on insert (every signup path, every admin tool, every backfill job, every test fixture) — undeclared | SUSTAINED | Plan enumerates every write path to `users` and shows each is updated to set `user_tier` before the NOT NULL constraint is enforced. |
| Downstream consumers of `subscription_status` that may diverge once `user_tier` is the source of truth (analytics, billing, support tooling, any cached read replicas) — undeclared | SUSTAINED | Plan names every consumer of `subscription_status` and states whether each migrates to `user_tier`, stays on `subscription_status`, or both. |
| Replication lag and read-replica behaviour during the backfill on a 50M-row table — undeclared | SUSTAINED | Plan names the replication topology, the expected lag during backfill, and the threshold at which backfill pauses. |
| "During deploy" — the entire migration strategy is hidden inside this phrase | SUSTAINED | Plan distinguishes (a) add nullable column, (b) backfill in batches, (c) dual-write from app code, (d) verify zero NULLs, (e) add NOT NULL constraint — as separate, individually-revertable steps, not "during deploy." |
| "Backfill from subscription_status" — vague enough to silently expand: what's the mapping function? what about NULLs in `subscription_status`? what about historic states (cancelled, paused, trialing)? | SUSTAINED | Plan publishes the exact mapping table from every distinct `subscription_status` value (including NULL) to a `user_tier` value, signed off by the team that owns billing/subscription semantics. |
| "Ship in next release" — vague enough to silently expand into "we'll keep iterating" | PARTIAL | Plan names a single release with a fixed cutover sequence and a defined rollback point per step. |

If zero SUSTAINED appeared on a 50M-row schema migration, B2 was run leniently. Six SUSTAINED items is consistent with the plan's actual surface area.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| `subscription_status` cleanly maps 1:1 to a `user_tier` for all 50M rows (no NULLs, no orphan states, no historical-only states) | 0.1 (assertion in plan) | `SELECT subscription_status, COUNT(*) FROM users GROUP BY 1` — 5 minutes. Then have the billing/subscriptions owner sign off the mapping table. | SUSTAINED |
| The backfill can complete "during deploy" — i.e. inside a deploy window, while the app is up, without lock contention or replication lag breaching SLO | 0.1 (asserted, not measured) | Run the backfill query against a recent prod snapshot or a dedicated read replica; measure wall-clock and lag. 5–30 min depending on access. | SUSTAINED |
| Adding a NOT NULL column to a 50M-row table is safe in one step on the chosen database engine (Postgres pre-11 rewrites the whole table; MySQL behaviour varies; even Postgres 11+ requires care with the DEFAULT value and constraint timing) | 0.1 (engine not even named) | Name the database engine and version; cite the engine's documented behaviour for `ALTER TABLE ... ADD COLUMN ... NOT NULL DEFAULT ...` on a 50M-row table; confirm against current docs (Agentic P2: hallucination is the default; sources are the brake). | SUSTAINED |

All three assumptions sit at Confidence 0.1 (opinion). Universal P4 and Step 6 of the skill: untested assumptions with Confidence < 5 block APPROVE. Each is testable in under 30 minutes — there is no excuse to ship without testing them.

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| DBA / database platform team — review of the migration plan and lock/replication impact | Not named | Not confirmed | SUSTAINED |
| Owner of `subscription_status` semantics (billing / subscriptions team) — sign-off on the `subscription_status` → `user_tier` mapping | Not named | Not confirmed | SUSTAINED |
| Owners of every downstream consumer of `subscription_status` and `users` — agreement that the new column does not break their reads / contracts | Not named | Not confirmed | SUSTAINED |
| On-call / SRE — awareness of the migration window, paging coverage during backfill, and rollback playbook approval | Not named | Not confirmed | SUSTAINED |

Universal Rule B7: unconfirmed cross-team dependencies are the single most common cause of missed commitments. The plan names zero of these.

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Adding a NOT NULL column to a 50M-row table — once shipped, removing it requires another full migration; once any client writes to it, removing it is a contract break | No alternatives named (nullable column + application-level invariant; CHECK constraint deferred; computed/generated column from `subscription_status`; view-based abstraction) | No ADR named or committed | SUSTAINED |
| "Backfill during deploy" — once the data is written, rolling back the deploy does not roll back the data; partial backfill on failure leaves a mixed state | No alternative sequencing named (batched async backfill behind a feature flag, with the NOT NULL constraint added only after verification) | No ADR named or committed | SUSTAINED |
| Choice of `subscription_status` as the source of truth for `user_tier` — once enshrined as a column, this coupling is hard to undo | No alternative source named (e.g. an explicit tier assignment service) | No ADR named or committed | SUSTAINED |

Universal P3 and Rule B3: every one-way door must record alternatives considered and reversal cost. Three one-way doors, zero alternatives recorded, zero ADRs.

## B6 — Operability + success metrics

- **Metrics**: absent. Plan names no metric for migration progress, backfill lag, write-error rate, or NULL count over time.
- **Alerts**: absent. No alert on backfill stall, on replication lag breaching SLO, on NULL writes during the window between column-add and constraint-enforcement, on application errors from code paths that haven't been updated.
- **Rollback path**: absent. "Backfill during deploy" implies a single deploy step; what is the revert? `ALTER TABLE ... DROP COLUMN` on 50M rows is itself a heavy operation and does not restore any rows that were modified by dual-writing application code.
- **Runbook**: absent. No on-call instructions for "backfill stalled at 60%" or "replication lag exceeded threshold mid-deploy."
- **Capacity headroom**: absent. No statement of database CPU/IO headroom during the backfill window, no statement of locking impact on concurrent writes.
- **User-visible outcome metric**: absent. What user or business outcome will be observed post-launch to confirm `user_tier` did the thing it was added to do? (Product P1: outcomes, not outputs.)

Six-for-six absent. Universal Rule A6: absence of operability blocks approval. SUSTAINED across the bucket.

## B7 — Sequencing + capacity

The plan collapses the entire migration into "during deploy" — a single step where in reality there are at least five (add nullable column → dual-write from app → batched backfill → verify zero NULLs → add NOT NULL constraint), each individually committable and individually revertable. The critical path is not surfaced; the appetite is "next release," which is not a fixed cap in calendar terms; FTE is not stated. SUSTAINED.

The "fixed time, variable scope" discipline (Universal Rule C1 / Shape Up) is reversed here: scope is fixed (the whole migration in one step), time is the variable (whatever "the next release" turns out to be).

## B8 — Pre-mortem

Adopting prospective hindsight: it's two weeks after the release. The migration failed. Top three reasons, ranked by likelihood:

1. **`subscription_status` had values the mapping didn't anticipate** — NULLs, legacy states (`trialing`, `paused`, `pending_cancellation`), states owned by another team that were added since the mapping was drafted. Backfill wrote a wrong tier for some users; downstream billing or feature-gate logic now treats them as the wrong tier; support tickets spike. *Kill-switch:* before adding the NOT NULL constraint, run `SELECT subscription_status, user_tier, COUNT(*) FROM users GROUP BY 1, 2` and require zero rows with `user_tier IS NULL` AND zero unmapped `subscription_status` values; alert if either fails.
2. **Backfill on 50M rows held locks / blew out replication lag / exhausted the deploy window** — the deploy timed out mid-backfill, leaving the table in a half-migrated state with the application code now expecting `user_tier` to be set. Writes started failing; cascading errors. *Kill-switch:* run the backfill OUT of the deploy path, in batches with explicit pause/resume, with a replica-lag circuit breaker that pauses when lag exceeds a named threshold (e.g. 30s).
3. **Application write paths weren't all updated** — a forgotten admin tool, a backfill job, a webhook handler, a test fixture, a data-import pipeline inserts a new user without setting `user_tier`. Once the NOT NULL constraint is on, that insert fails and a user-facing flow breaks. (No kill-switch named — but the precondition is to grep every `INSERT INTO users` and every ORM `User.create`/`User.new` call site before the constraint is added.)

## Recommendation

**REVISE** — the plan must not be approved in its current form.

### Conditions

The plan is sent back. Before re-review, the owner must:

1. Add a problem statement that justifies the NOT NULL constraint specifically and names the user/business outcome the column exists to enable (B1).
2. Decompose the migration into separately revertable steps: (a) add nullable column with backfill default behaviour decided, (b) update all application write paths to populate `user_tier`, (c) batched async backfill with a replica-lag circuit breaker, (d) verify zero NULLs and zero unmapped `subscription_status` values, (e) add NOT NULL constraint as a separate deploy. Each step has a named revert. (B2, B5, B7.)
3. Name the database engine and version; cite the documented behaviour for the chosen `ALTER TABLE` against a 50M-row table; produce a measurement from a recent prod snapshot or read replica (B3).
4. Publish the full `subscription_status` → `user_tier` mapping table including NULLs and every distinct historical value (`SELECT subscription_status, COUNT(*) FROM users GROUP BY 1`); have the billing/subscriptions owner sign it off in writing (B3, B4).
5. Confirm the DBA/platform team, the billing/subscriptions owner, downstream consumers of `subscription_status`, and on-call/SRE are named and have agreed in writing (B4).
6. Write an ADR recording the alternatives considered (nullable column with application-level invariant; computed/generated column; view-based abstraction; explicit tier assignment service) and why NOT NULL on a backing column was chosen (B5).
7. Add the operability section: backfill-progress metric, replica-lag alert, NULL-count alert, rollback steps per migration step, on-call runbook for the named failure modes (B6).
8. Replace "next release" with a fixed appetite in calendar days, and either commit to fitting all five steps inside it or schedule the steps across multiple releases (B7).
9. Name the user-visible outcome metric that will be observed post-launch to confirm the change moved what it was meant to move (B6, Product P1).
