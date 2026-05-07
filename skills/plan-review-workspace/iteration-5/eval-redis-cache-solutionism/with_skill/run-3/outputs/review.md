# Plan review: redis-cache-product-catalog

## Plan reference

> "Introduce Redis as a caching layer in front of Postgres for product catalog reads. We'll add a Redis cluster, write a thin client, add cache-invalidation on writes. Approve?"

## Inputs

- **Appetite**: Not stated (asked to approve without one)
- **Cynefin domain**: Complicated — caching is a well-understood pattern; the correct approach is knowable with expertise but requires evidence-based selection among alternatives
- **Tier**: Full — selected because the plan contains ≥1 one-way-door decision (Redis cluster addition = architectural choice + vendor dependency)

---

## Fast-track gate

Did not fire. Precondition 1 fails: this is not KTLO/maintenance (not a SemVer bump, lint config, doc change, or test cleanup). Normal full-tier flow runs.

---

## B1 — Problem framing

The plan opens with the solution ("introduce Redis as a caching layer") before naming any problem. There is no statement of: which latency percentile is failing and by how much, what load pattern motivated the investigation, what user-visible symptom prompted this, or what business outcome is at stake.

**Verdict: SUSTAINED**

Falsifying condition: a problem statement exists that names the current p95 read latency on the product catalog endpoint, the target latency, the load pattern that produced the symptom (e.g. peak RPS), and the user or business impact of the current state. If that statement exists and precedes the solution choice, this verdict is OVERTURNED.

---

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| Redis cluster topology (single-node vs. cluster mode; cloud-managed vs. self-hosted) is not declared in scope but will be decided implicitly during "add a Redis cluster" | SUSTAINED | Plan explicitly states topology choice, who owns it, and how it was selected |
| Cache warming / cold-start behaviour on deploy or failover is not mentioned | SUSTAINED | Plan names the cold-start strategy (pre-warm job, lazy-fill, or explicit tolerance window) |
| Serialisation format for cached objects is unaddressed — it determines schema coupling and migration cost | PARTIAL | Plan references a specific serialisation choice; migration path on model change is named |
| "Thin client" is vague — library selection, connection pooling, timeout, retry, and circuit-breaker behaviour are undeclared | SUSTAINED | Plan names the library, connection pool size, timeout values, and circuit-breaker behaviour |
| "Cache-invalidation on writes" does not specify which writes (single record, bulk import, admin override, async jobs) | SUSTAINED | Plan enumerates every write path that must trigger invalidation and names the invalidation strategy for each |
| "Product catalog reads" is undefined — all reads? specific endpoints? does it include search? faceted filtering? | SUSTAINED | Plan names the exact read paths (endpoints or query patterns) in scope |

---

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| Postgres read latency on the product catalog is the bottleneck causing the user/business problem | 0.1 — assertion, no profiling or APM data cited | Owner runs `EXPLAIN ANALYZE` on the top 5 catalog queries and checks p95 via APM; if Postgres is not the bottleneck, this plan solves the wrong problem | SUSTAINED — blocks APPROVE |
| Cache invalidation on writes is tractable — all write paths are known and enumerable | 0.1 — assumed; no audit of write paths cited | Owner enumerates write paths (API, admin, bulk import, async workers) and confirms each is reachable from the invalidation logic | SUSTAINED — blocks APPROVE |
| A Redis cluster is within the team's operational capability (provisioning, monitoring, failover, on-call runbook) | 0.1 — assumed; no ops capability assessment cited | Owner confirms with the infrastructure/DevOps team that managed Redis is available on the current cloud tier and that an on-call runbook template exists | SUSTAINED — blocks APPROVE |

All three assumptions score 0.1 (opinion/assertion). All three block APPROVE under Universal P4 / Rule B6: untested assumptions with Confidence < 5 block approval.

---

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Infrastructure / DevOps team — Redis cluster provisioning, networking, secrets management | Not named, not confirmed | Unknown | SUSTAINED |
| Cloud provider — managed Redis tier availability and cost envelope | Not confirmed | Unknown | SUSTAINED |
| On-call rotation — must absorb Redis as a new failure domain | Not named, not confirmed | Unknown | SUSTAINED |

No cross-team dependency is confirmed in writing. This is the single most common cause of missed commitments (Universal Rule B7). None of these can be assumed away — a Redis cluster that hasn't been provisioned is not a caching layer; it's a plan to have a caching layer.

---

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Redis cluster adoption — operational overhead, team upskilling, and cache-as-source-of-truth coupling make this moderately expensive to reverse once traffic depends on it | No alternatives named | No ADR | SUSTAINED |

The plan names no alternatives. Alternatives that should have been considered before selecting Redis:

- **In-process LRU cache** (e.g. in the application process): zero new infrastructure, lower latency, no network hop, limited to single-instance or requires sticky routing
- **Read replica** (Postgres): solves read-contention without a new failure domain; slower writes don't benefit but reads scale horizontally
- **CDN / HTTP response caching** at the edge: effective if reads are user-agnostic; cache-invalidation is simpler (TTL or purge)
- **Query optimisation + index tuning**: should be ruled out before adding infrastructure — if the bottleneck is a missing index, adding Redis is a 2-week project solving a 2-hour problem
- **Application-layer fragment caching**: lower scope than a full Redis cluster; often achieves 80% of the benefit at 20% of the operational cost

An ADR must be committed to before approval. An undocumented one-way door is a silent commitment (Agentic P7; Universal Rule B3). SUSTAINED verdict on B5 cannot be overridden by the Quick-tier reversibility carve-out — this plan is Full tier.

Falsifying condition: an ADR exists that names all five alternatives above (or an equivalent set), states why each was rejected, and records the reversal cost of Redis adoption. If that ADR exists and is linked from the plan, this verdict is OVERTURNED.

---

## B6 — Operability + success metrics

- **Metrics**: Absent. No cache-hit rate, miss rate, Redis memory utilisation, or Postgres load-before/after named.
- **Alerts**: Absent. Redis eviction rate, connection pool exhaustion, latency spike — none defined.
- **Rollback path**: Absent. "Remove Redis" is not a rollback plan. Named rollback requires: feature flag that bypasses Redis and falls through to Postgres, tested before deployment.
- **Runbook**: Absent. What does on-call do when Redis is unreachable? The plan must name the degraded-mode behaviour (pass-through to Postgres, serve stale, return error).
- **Capacity headroom**: Absent. Redis memory footprint for the product catalog is not estimated; eviction policy (LRU, LFU, no-eviction) not named.
- **User-visible outcome metric**: Absent. The plan names no outcome metric — not p95 latency target, not error rate, not conversion rate improvement. "We added a cache" is a delivery metric, not an outcome metric. (Product P1: outcomes, not outputs.)

All six operability sub-items are absent. This is a full SUSTAINED on B6. Absence on either the operability half or the success-metrics half blocks APPROVE.

---

## B7 — Sequencing + capacity

- **Critical path**: Not surfaced. The sequence of (1) confirm bottleneck via profiling, (2) select topology, (3) provision cluster, (4) implement client, (5) implement invalidation, (6) load test, (7) roll out behind flag is not named.
- **Appetite**: Not stated. No cap is defined. "Approve?" implies a desire to start immediately without a time budget. An appetite of "undeclared" is not an appetite.
- **FTE**: Not stated. No team size or allocation is named.

An appetite that isn't declared is a plan that cannot be circuit-broken. Universal Rule C1 (appetite as a cap, not a target) cannot be applied. SUSTAINED.

---

## B8 — Pre-mortem

Assume the plan shipped and failed within its appetite. Top 3 failure modes by likelihood:

**1 (most likely): Cache invalidation is incomplete — stale data reaches users on bulk import or async update paths.**
The plan says "cache-invalidation on writes" without auditing all write paths. Product catalogs are commonly updated via admin bulk import, third-party feed sync, or async pricing jobs — none of which go through the same code path as single-record writes. When one of these paths fires without triggering invalidation, users see stale prices or inventory.
Kill-switch condition: before shipping, produce an exhaustive list of all write paths (including async jobs, admin tools, and import pipelines) and confirm each one is covered by an invalidation test. If the list cannot be produced in a half-day audit, the plan's invalidation model is unproven.

**2: Redis becomes a single point of failure and the fallback path is untested.**
The plan does not name a degraded-mode behaviour. When Redis goes down (eviction, OOM, network partition), the application either throws errors (bad) or falls through to Postgres (correct, but only if the fallback is implemented and tested). The fallback path is almost never tested before it is needed. Consequence: Redis downtime = catalog downtime, not Redis downtime = temporary latency increase.
Kill-switch condition: a circuit-breaker or feature flag that bypasses Redis and falls through to Postgres must be tested under load before the cache is enabled in production. If this test does not exist at the time of rollout, the rollout is blocked.

**3: The bottleneck was not Postgres — it was something else (serialisation, N+1 queries, downstream API calls) — and Redis provides no relief.**
No profiling evidence is cited. If the actual bottleneck is N+1 queries (fetching associated records one-by-one), caching will cache the symptom but not fix the cause. The team ships Redis, observes no improvement, and must investigate from scratch with a new infrastructure dependency already in production.

---

## Recommendation

**KILL** — the plan's core premise (Redis is the right solution) has not been established, and the plan as written cannot be approved in any revised form without first:

1. Producing profiling evidence that Postgres read latency is the bottleneck (not query structure, not serialisation, not downstream services).
2. Considering and ruling out alternatives (read replicas, in-process cache, CDN, query optimisation) in a written ADR.

If profiling confirms Redis is appropriate, the plan warrants **REVISE** rather than KILL, with all of the following required before re-approval:

### Conditions for REVISE (if profiling confirms Redis is appropriate)

1. **B1**: Add a problem statement: current p95 latency, target, load pattern, and user/business impact.
2. **B3/A1**: Produce profiling evidence (APM trace or `EXPLAIN ANALYZE` output) confirming Postgres reads are the bottleneck.
3. **B3/A2**: Audit all write paths and confirm each is covered by the invalidation strategy. Name the strategy (event-driven, write-through, TTL).
4. **B3/A3**: Confirm with infrastructure/DevOps that managed Redis is available and operational capability exists.
5. **B5**: Write an ADR naming all alternatives considered and rejected, with reversal cost for Redis adoption named.
6. **B6**: Name: cache-hit rate alert threshold, eviction policy, rollback feature flag, degraded-mode behaviour (what happens when Redis is unreachable), and user-visible outcome metric (target p95 latency post-launch).
7. **B7**: State an appetite (fixed cap), critical path, and FTE allocation.
8. **B4**: Confirm infrastructure team capacity and cloud-provider Redis tier in writing.

A plan that does not open with a measured problem and does not name a measured outcome is not a product or engineering plan — it is a solution in search of a problem.
