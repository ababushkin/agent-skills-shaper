# Plan review: redis-product-catalog-cache

## Plan reference

Inline plan from owner: "Introduce Redis as a caching layer in front of Postgres for product catalog reads. We'll add a Redis cluster, write a thin client, add cache-invalidation on writes. Approve?"

## Inputs

- **Appetite**: Not stated. Inferred ≥1 week (new Redis cluster provision + client + invalidation across all writers is multi-day even before correctness work). Owner must confirm a fixed cap.
- **Cynefin domain**: Complicated. Cache-invalidation is a known-hard problem with knowable solutions, but emergent staleness/thundering-herd behaviour pushes toward Complex if traffic is non-trivial.
- **Tier**: **Full** — selected because the plan contains a one-way-door decision (introducing a new infrastructure component / vendor topology) and inferred appetite >1 week. Auto-select rule fired.

### Trigger check

Trigger 1 (owner about to approve a plan) AND Trigger 4 (auto-fire: architecture choice — new datastore in the request path). Proceeding.

### Fast-track gate

Did NOT fire. Failed precondition #1 (not KTLO/maintenance — net-new infrastructure component) and #2 (not fully reversible — once writers depend on cache invalidation, revert requires unwinding invalidation logic and traffic patterns, not a one-commit revert).

## B1 — Problem framing

**Verdict: SUSTAINED.** The plan opens with a solution ("introduce Redis as a caching layer"), not a problem. There is no stated user or business outcome — no latency target, no Postgres bottleneck evidence, no read-volume number, no cost driver. "Product catalog reads are slow" is not in the plan, and even if it were, "slow" is not a number (Universal Rule A4).

**Falsifying condition:** the plan is rewritten to open with a problem statement of the form "For [segment], product-catalog read latency at p95 is [X ms] against an SLO of [Y ms], driven by [evidence: query plan, lock contention, IOPS ceiling, cost]. We expect cache introduction to move p95 to [Z ms] within [horizon]." If that statement can be written truthfully, B1 flips to OVERTURNED. If it cannot, the plan is solution-first and the right next step is measurement, not Redis. (Universal P2; agentic P3.)

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| Every writer of catalog data (admin tools, batch importers, third-party sync jobs, background workers) is implicitly in scope for invalidation changes — not declared | SUSTAINED | Plan enumerates every code path that writes to the affected catalog tables and confirms each will call the invalidation hook |
| Read paths beyond the "product catalog" — search indexes, recommendation feeds, pricing engine, analytics ETL — may share rows; staleness contract not declared | SUSTAINED | Plan names the exact tables/columns cached, the read paths that consume them, and which paths tolerate staleness vs. require strong consistency |
| "Thin client" is vague — connection pooling, retry/backoff, circuit-breaker, serialisation format, key-naming scheme, TTL policy, negative caching are all "thin client" decisions that silently expand | SUSTAINED | Plan replaces "thin client" with a contract listing each of: pool config, retry policy, circuit-breaker behaviour on Redis outage, serialisation format, key schema, TTL strategy, negative-cache policy |
| Local dev + CI environment changes (Redis fixture, test isolation) — not mentioned | PARTIAL | Plan names how Redis is provided in local dev and CI, and what tests run without it |
| Observability scope (cache hit-rate metric, staleness detection, invalidation lag) — not mentioned | SUSTAINED | Plan declares the metrics that will be emitted and the dashboards/alerts that will read them (see B6) |
| "Add a Redis cluster" elides cluster sizing, multi-AZ, failover behaviour, backup, eviction policy | SUSTAINED | Plan names cluster topology, node sizing rationale, eviction policy (allkeys-lru? volatile-lru?), failover behaviour, and whether persistence is on |

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| Postgres is actually the bottleneck for catalog reads (not app code, not N+1, not network, not serialisation) | 0.1 — not stated, asserted by choice of Redis | Pull last 7 days of p95 latency broken down by span: SQL exec vs. app vs. serialisation. If SQL <30% of latency, Redis won't move the needle. | SUSTAINED |
| Cache invalidation can be made correct with the planned "invalidate on write" approach (Phil Karlton's two hard things) | 0.1 — assumption | Name the consistency contract: read-your-writes? eventual? bounded staleness? Then walk through three concrete write→read race scenarios and show the invalidation handles each. | SUSTAINED |
| Read traffic has a hot-set that benefits from caching (skewed access pattern, not uniform) | 0.1 — assumption | Sample 1 hour of read logs; compute the top-1% key share of total reads. If the top 1% of keys serves <50% of reads, the hit-rate will disappoint. | SUSTAINED |
| Operating a Redis cluster (HA, failover, version upgrades, capacity planning) is within current team capacity | 0.1 — assumption | Name the on-call engineer who will own Redis at 3am and confirm familiarity. If managed (Elasticache/MemoryStore), name the budget owner. | SUSTAINED |
| Cheaper alternatives (Postgres tuning, read replica, query rewrite, application-tier in-process LRU, materialised view, CDN edge cache for catalog reads) have been considered and rejected | 0.1 — not mentioned | Owner produces a one-paragraph rejection note for each. If any is plausible and cheaper, Redis is the wrong default (Universal P10: boring tech / innovation tokens; Universal P5: code is liability). | SUSTAINED |

All five sit at Confidence 0.1 (opinion). Per skill rule: untested assumptions with Confidence <5 block APPROVE.

## B4 — Dependencies (Full only)

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Platform/Infra team to provision Redis cluster (or cloud-managed equivalent) | No — not named | No | SUSTAINED |
| Security review for new datastore (data classification: does product catalog contain PII, pricing, contractual data?) | No | No | SUSTAINED |
| FinOps / budget approval for Redis spend (cluster + bandwidth + ops) | No | No | SUSTAINED |
| Every team that writes to catalog tables must integrate invalidation hooks | No — implicit | No | SUSTAINED |
| Observability team / dashboards to add cache metrics and alerts | No | No | SUSTAINED |

Universal Rule B7: unconfirmed cross-team dependencies are the single most common cause of missed commitments. Five unconfirmed here.

## B5 — Reversibility + ADR pairing (Full only)

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Introducing a new datastore class (Redis) into the production request path | No alternatives named | No ADR | SUSTAINED |
| Coupling write paths to invalidation logic (every writer becomes Redis-aware) | No | No | SUSTAINED |
| Choice of Redis vs. Memcached vs. application-tier in-process cache vs. CDN-edge vs. Postgres-side caching (pgbouncer, prepared statements, materialised views) | No | No | SUSTAINED |
| Cluster topology (self-hosted vs. managed, single-region vs. multi-region) | No | No | SUSTAINED |

The reversal cost is high: once writers carry invalidation logic and reads assume cache presence, reverting means more than `git revert` — it means restoring previous read-path performance assumptions and unwinding writer code. Universal P3 + Rule B3 + Agentic P7: this requires written alternatives and an ADR before commitment.

## B6 — Operability + success metrics (Full only)

- Metrics: **absent** — no cache hit-rate, miss-rate, latency-by-source, invalidation lag, eviction rate, memory headroom, connection pool saturation, error rate
- Alerts: **absent** — no SLO defined, no alert thresholds
- Rollback path: **absent** — no kill switch (e.g. feature flag to bypass cache and read straight from Postgres), no documented procedure for "Redis is down, fall back to Postgres" behaviour
- Runbook: **absent** — no on-call procedure for Redis outage, eviction storm, hot-key, thundering herd on cold start
- Capacity headroom: **absent** — no working-set sizing estimate, no eviction-rate target, no budget for traffic-spike headroom
- User-visible outcome metric: **absent** — no named outcome metric (p95 catalog-read latency, error rate, conversion impact). "We added Redis" is an output, not an outcome (Product P1)

Six-of-six absent. SUSTAINED. Universal Rule A6: absence of operability section blocks APPROVE on a Full-tier plan.

## B7 — Sequencing + capacity (Full only)

Critical path is not surfaced. The plan reads as three parallel work items ("add a cluster", "write a thin client", "add cache-invalidation on writes") but the real critical path is: measure → consistency contract → invalidation design → walking-skeleton with one read path → load-test → roll out per writer → operability before any production traffic. Appetite is not stated and is not fixed; with five SUSTAINED dependencies it is unbounded by definition. Team FTE consistency cannot be assessed. SUSTAINED.

## B8 — Pre-mortem

Assume the plan shipped and failed within its (unstated) appetite. Top three reasons, ranked by likelihood:

1. **Cache invalidation bug ships stale prices/inventory to customers.** A write path was missed (most likely a background job or admin tool the team forgot was a writer) and the cache served stale data for hours before anyone noticed — because no staleness metric was emitted. **Kill switch:** feature flag bypassing cache (read-through to Postgres) deployed before any read traffic uses Redis; staleness probe (write a known sentinel row, read via cache, alert on lag >N seconds) running continuously.
2. **Redis didn't move p95 because Postgres wasn't the bottleneck.** Three weeks of work later, p95 is unchanged, the team adds Redis to the architecture diagram and quietly moves on (Universal Principle 1 violation: shipped ≠ done). **Kill switch:** before shipping, define the latency target and the measurement window; if p95 hasn't moved by [Y ms] within [N days] of full rollout, revert and write a postmortem.
3. **Operational surprise:** Redis cluster fails over (or hits memory ceiling and starts evicting hot keys), thundering herd hammers Postgres, Postgres falls over, total catalog outage. The plan made Postgres weaker (no longer sized for full read traffic) without making Redis HA-tested. No kill-switch named here because the plan has no rollback path — that is the finding.

## Recommendation

**REVISE** — the plan has six SUSTAINED bucket findings (B1, B2, B3, B4, B5, B6) and one SUSTAINED on sequencing (B7). Quick-tier reversibility carve-out does not apply (Full-tier plan, one-way door present, B5 SUSTAINED). The plan is solution-first, lacks a problem statement, lacks evidence that Redis solves the unstated problem, and has no operability or success metrics.

This is not a "tighten and approve" — the core defect is that **the problem is undefined**. Until B1 is satisfied, the rest of the plan is structurally premature. Do not split B1 from the rest as "we'll add metrics later" — without a target metric, "later" never arrives, and the work cannot be evaluated as success or failure (Product P10 / "done means outcome moved").

### Conditions

The plan must satisfy all of the following before it returns for approval:

1. **B1 — Problem statement.** Named user/business outcome with current measurement and target ("p95 catalog read is X ms, target Y ms; current Postgres CPU at peak is Z%; cost driver is …"). Without this, stop here — measure first.
2. **B3 — Bottleneck evidence.** Latency breakdown showing SQL is the dominant component for catalog reads. If it isn't, Redis won't help and the plan is wrong-shaped.
3. **B5 — Alternatives + ADR.** Written rejection of: Postgres tuning + read replica; in-process LRU at application tier; CDN/edge cache for catalog endpoints; Memcached. ADR drafted with chosen approach, alternatives, reversal cost.
4. **B3 — Consistency contract.** Explicit statement: read-your-writes / eventual / bounded staleness, and three worked write→read race scenarios showing invalidation behaviour.
5. **B2 — Writer enumeration.** Every code path (services, batch jobs, admin tools, third-party sync, migrations) that writes catalog rows is named, with the integration plan for invalidation.
6. **B6 — Operability.** Hit-rate, miss-rate, invalidation lag, eviction rate, memory headroom metrics defined; SLO + alerts named; cache-bypass feature flag committed; on-call runbook drafted; cluster topology with HA, eviction policy, sizing rationale.
7. **B6 — Success metric.** Named outcome metric (p95 latency target with measurement window) that will determine whether the work gets kept, iterated, or reverted post-launch.
8. **B4 — Dependencies confirmed.** Infra, Security, FinOps, every writer-team owner, Observability — each named and confirmed in writing within plan appetite.
9. **B7 — Appetite.** Fixed cap (e.g. "6 weeks") with critical path surfaced; not a range.
10. **B8 — Kill-switch.** Cache-bypass flag and staleness probe both deployed and exercised before any production read traffic uses the cache.

If conditions 1, 2, and 3 cannot be satisfied (i.e. there is no measured Postgres bottleneck, or simpler alternatives are clearly cheaper), the recommendation upgrades from REVISE to **KILL** — Redis is the wrong tool, and the right next step is measurement plus a smaller intervention.
