# Plan review: redis-cache-product-catalog

## Plan reference

> "Introduce Redis as a caching layer in front of Postgres for product catalog reads. We'll add a Redis cluster, write a thin client, add cache-invalidation on writes. Approve?"

Pasted excerpt; no path on file.

## Inputs

- **Appetite**: Not stated. Minimum realistic estimate: 1–2 weeks (Redis cluster provisioning, client library, invalidation logic, testing, observability). Treated as >1 week for tier-selection purposes.
- **Cynefin domain**: Complicated
- **Tier**: Full — selected because (a) appetite almost certainly exceeds 1 week and (b) the plan contains at least one one-way-door decision (introducing a new distributed infrastructure component and a cache-invalidation topology).

Fast-track gate: does not fire. Precondition 1 fails (this is not KTLO/maintenance — it is a new architectural component). Precondition 2 fails (introducing Redis is not a one-commit revert; cache-invalidation code will be woven into write paths). Precondition 3 fails (appetite unknown but clearly > 1 day). Falling through to full flow.

---

## B0 — Cynefin classification

**Complicated.** Adding a caching layer in front of a relational store is a well-understood pattern with known failure modes (cache stampede, invalidation races, cold-start). Expertise is required to navigate it; cause-effect is knowable but not obvious. Review emphasis: dependencies, reversibility, and operability.

---

## B1 — Problem framing

**SUSTAINED.**

The plan opens with a solution: "introduce Redis as a caching layer." No problem statement appears. There is no mention of:

- What user or business outcome is degraded today.
- What the current p95 read latency or query cost on the product catalog is, or what target improvement is desired.
- Evidence that Postgres read load is the bottleneck (versus application logic, N+1 queries, missing indexes, connection pool exhaustion, or network).

Falsifying condition: the plan is revised to open with "Product catalog read p95 exceeds X ms / Postgres CPU peaks at Y% during Z traffic pattern, and profiling confirms read queries are the dominant cost. Target: reduce p95 below A ms." If a problem statement with a measurable target appears and the target is traceable to user-visible impact, this verdict is overturned.

---

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| Cache-invalidation strategy is underdetermined — "on writes" covers a wide range of complexity (write-through? write-around? TTL fallback? partial invalidation? bulk update events from catalog import jobs?). The plan does not scope which write paths are covered. | SUSTAINED | Plan names every write path that touches the product catalog (including async jobs, admin bulk-edit, import pipelines) and assigns an explicit invalidation strategy to each. |
| Redis cluster topology is undeclared — single-node vs. multi-node, Sentinel vs. Cluster mode, cloud-managed vs. self-hosted. Each choice carries different operational and reversibility implications and different team dependencies. | SUSTAINED | Plan names the cluster topology (e.g. "AWS ElastiCache, Cluster mode disabled, 2 replicas") and records why alternatives were not chosen. |
| "Thin client" scope is vague — could be a 50-line wrapper or a full abstraction layer with serialisation, key namespacing, TTL management, circuit-breaker, and retry logic. Silent expansion is likely. | SUSTAINED | Plan defines the thin client's interface in concrete terms: what it accepts, what it returns, what it does not do. Length/scope is capped explicitly. |
| The plan does not declare what happens on cache miss (Postgres fallback assumed, but not stated), nor what happens on Redis unavailability. | PARTIAL | Plan explicitly states the cache-miss path and the Redis-down degradation behaviour (e.g. "fall through to Postgres with no error surfaced to caller"). |
| Performance testing / load validation is not in scope of the plan — meaning there is no gate before this goes live under real traffic. | SUSTAINED | Plan names a load-test or canary stage before full rollout, or explicitly records the decision to omit one with rationale. |

---

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| Postgres read queries on the product catalog are the bottleneck causing a user-visible problem. | 0.1 — assertion, no evidence cited | Pull Postgres slow-query log and query `pg_stat_statements` for the catalog read queries; confirm top-N queries by total time. 5 minutes. | SUSTAINED — confidence below threshold; assumption untested. |
| Redis will improve the metric that matters (not assumed to only move cache-hit rate, but a user-visible metric). | 0.1 — assertion | Define the target metric now (p95 read latency? requests/sec capacity? Postgres CPU headroom?), measure baseline, and restate the plan with that number. | SUSTAINED — no outcome metric named; confidence unmeasurable. |
| Cache-invalidation logic can be added to all write paths without missing any. | 0.1 — assumption; catalog write paths not enumerated | Grep/audit all write paths to the product catalog (including background jobs, admin interfaces, import scripts) before committing to invalidation approach. Owner: [engineer name]. | SUSTAINED — scope of write paths not known; silent miss is high-probability failure mode. |
| The team has operational capacity to run a Redis cluster (monitoring, failover, backup, upgrade, key eviction tuning). | 0.1 — unstated assumption | Confirm with on-call rotation owner that Redis ops runbook will be written and that pager coverage is added before launch. Owner: [on-call lead]. | SUSTAINED — operability capacity not confirmed. |

All four B3 assumptions carry Confidence 0.1. All four block APPROVE.

---

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Infrastructure / platform team for Redis cluster provisioning (if cloud-managed, e.g. ElastiCache request, VPC peering, security group rules). | Not named in plan. | Not confirmed. | SUSTAINED — unconfirmed dependency. |
| Security / compliance review of a new network-accessible data store (product catalog data classification? PII in catalog? Encryption-at-rest requirement?). | Not named in plan. | Not confirmed. | SUSTAINED — plan does not acknowledge this dependency exists. |
| Any team that owns catalog write paths outside this team's codebase (e.g. a separate import service, a CMS integration). | Not named in plan. | Not confirmed. | SUSTAINED — cross-team invalidation coupling not identified. |

---

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Introducing Redis as a new infrastructure dependency — once cache-invalidation logic is woven into write paths, removal requires surgery across multiple call sites. | No alternatives named. The plan does not consider: Postgres read replicas, query result caching at application layer (in-process), materialized views, index tuning, connection pooling improvements, or CDN-level catalog caching. | No ADR exists or committed. | SUSTAINED — undocumented one-way door. Plan must name alternatives considered and why each was rejected, and must commit to an ADR. |
| Invalidation-on-write coupling — every future write path must include cache invalidation or risk serving stale data; this is an invisible contract that accumulates over time. | Not acknowledged in the plan. | No ADR. | SUSTAINED — silent long-term coupling not named or recorded. |

---

## B6 — Operability + success metrics

- **Metrics**: Absent. Plan names no cache hit rate target, no latency metric, no Redis memory usage metric, no eviction rate alert.
- **Alerts**: Absent. No alert on Redis unavailability, cache miss rate spike, or key eviction rate exceeding threshold.
- **Rollback path**: Absent. No statement on how to disable the cache layer without a full deploy (feature flag? config toggle?). Given the invalidation logic is woven into write paths, rollback is not trivial.
- **Runbook**: Absent. No on-call documentation committed.
- **Capacity headroom**: Absent. No sizing for Redis memory relative to product catalog size (number of keys × serialised value size × TTL × hot-key distribution).
- **User-visible outcome metric**: Absent. "Cache-invalidation on writes" is a delivery metric. No user-visible outcome (latency reduction, checkout completion rate, page load time) is named.

All six operability dimensions absent. This bucket fully SUSTAINED and blocks APPROVE.

---

## B7 — Sequencing + capacity

- **Critical path**: Not surfaced. The plan does not name what must complete before what. Likely critical path: (1) enumerate write paths → (2) choose invalidation strategy → (3) provision cluster → (4) write client → (5) wire invalidation → (6) load test → (7) canary → (8) full rollout. Steps 1 and 2 are gates for the rest; the plan omits them entirely.
- **Appetite**: Not stated. "Approve?" implies urgency without committing to a time budget. This violates Universal Rule C1 (appetite is a cap set at the start).
- **FTE**: Not stated. Unknown if one engineer or three.

SUSTAINED on appetite and critical path. Insufficient information to assess FTE consistency.

---

## B8 — Pre-mortem (Full tier: top 3 reasons)

Assume the plan shipped and failed within its appetite.

**Reason 1 (highest likelihood): Cache invalidation misses a write path, serving stale catalog data to users.**
The plan's coverage of write paths is assumed, not audited. A background job, an admin bulk-edit, or an import pipeline that bypasses the thin client will silently serve stale prices, stock levels, or product details.
Kill-switch condition: before wiring invalidation, produce a complete list of every write path to the product catalog table(s) with owner sign-off. Any write path not on the list is a blocker.

**Reason 2 (second likelihood): Redis unavailability causes a cascade failure rather than graceful degradation.**
No degradation behaviour is named. If the Redis client throws on connection failure and the application does not have a fallback path, a Redis outage becomes a product catalog outage. Given Redis is a new dependency, its failure modes are not yet represented in the on-call team's mental model.
Kill-switch condition: before launch, define and test the Redis-down code path explicitly (fault injection or kill the test Redis and run the full request path).

**Reason 3: Cache stampede on cold start or invalidation event.**
A bulk catalog update or a Redis restart will invalidate a large key set simultaneously, sending a thundering herd to Postgres at exactly the moment the cache was meant to protect it. The plan does not name a stampede-prevention strategy (probabilistic early expiration, request coalescing, or staggered TTLs).

---

## Recommendation

**KILL / REVISE** — the plan's core premise (Redis fixes a problem) is unverified, and the plan contains five separate categories of SUSTAINED finding. A plan in this state should not proceed to implementation.

More precisely:

- **KILL the plan as stated.** A solution-first plan with no problem statement, no measurable target, no enumerated write paths, no operability design, and no ADR for a one-way-door decision is not a plan — it is a proposal at best.
- **REVISE to proceed.** If the team believes Redis is the right approach, the revised plan must satisfy the conditions below before re-review.

### Conditions

1. **B1** — Open with a problem statement: named metric, measured baseline, measurable target. (e.g. "Product catalog p95 read latency is 420 ms. Target: < 80 ms. Postgres slow-query log confirms catalog reads are the dominant cost.")
2. **B1 / B5** — Name and reject the alternatives: Postgres read replica, materialized views, index audit, in-process cache, CDN catalog cache. One paragraph each with reason for rejection.
3. **B2** — Enumerate every write path to the product catalog (including jobs and external integrations). Assign an invalidation strategy to each. Cap the thin client's scope in writing.
4. **B3** — Run `pg_stat_statements` query and attach results to the plan before any Redis work begins. Confirm the bottleneck is what the plan assumes.
5. **B4** — Confirm infra/platform dependency (cluster provisioning) and security/compliance review dependency in writing before commitment.
6. **B5** — Commit to writing an ADR covering: Redis vs. alternatives, chosen invalidation strategy, cluster topology, known long-term coupling implications.
7. **B6** — Add an Operability section: hit-rate target, eviction alert, Redis-down degradation behaviour, feature flag for rollback, on-call runbook owner, Redis memory sizing.
8. **B6** — Name the user-visible outcome metric that will be measured post-launch (not hit rate — something a user or business stakeholder can observe).
9. **B7** — State an explicit appetite (fixed cap) and the critical path showing write-path audit and invalidation strategy as gates before any implementation.
10. **B8** — Name the stampede-prevention strategy for cold-start and bulk-invalidation events.
