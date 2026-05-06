# Plan review: Redis cache layer for product catalog reads

## Assessment

The plan as written is solution-first, not problem-first. It opens with "introduce Redis as a caching layer" — that is a chosen implementation, not a stated problem. Reading it through the lens of what a reviewer needs to approve, the plan is missing almost every element that would let me say yes with any confidence:

- No problem statement. Why are catalog reads a problem today? Slow? Expensive? Overloading Postgres? Causing user-visible latency? We don't know.
- No measurable outcome. What metric is this supposed to move, and by how much? p95 read latency? DB CPU? Cost per request? Without a target, "done" is undefinable.
- No evidence. Has Postgres actually been shown to be the bottleneck? Has anyone profiled the slow reads? Are the catalog queries genuinely uncacheable today (no PG buffer cache hit, no app-level memoisation, no CDN/edge caching for product pages)?
- No alternatives considered. PG read replicas, query/index tuning, materialised views, in-process LRU cache, HTTP/CDN caching at the edge, denormalised read model — none mentioned. Redis may be the right answer; without alternatives the plan can't demonstrate that.
- No NFRs. What latency target? Availability? Consistency tolerance (how stale can the cache be)? Cache size? Eviction policy? Hit-rate target?
- No operability section. SLOs, alerts, dashboards, runbook, rollback plan, capacity headroom for the new Redis cluster, on-call coverage, failure-mode behaviour (what happens when Redis is down — fail open to PG, or fail the request?).
- No reversibility/blast-radius framing. A new piece of infra is a one-way door of meaningful weight; the plan treats it as a routine change.
- No appetite/time-box. Redis-cluster + thin client + invalidation on writes is non-trivial — easily a multi-week project once you include ops, security (auth, network policy), DR, and the long tail of cache-invalidation bugs.

In short: this is a feature-factory framing of an infrastructure decision. It tells me what someone wants to build but not why, not how we'll know it worked, and not what we considered instead.

## Concerns

1. **Solutionism / one-way door.** Standing up a Redis cluster commits the team to operating a new stateful system: HA, failover, persistence policy, version upgrades, security boundary, monitoring, on-call expertise. That's a significant innovation-token spend. It needs justification against the boring defaults (PG tuning, replicas, edge caching).

2. **Cache invalidation is the hard part, mentioned in one phrase.** "Add cache-invalidation on writes" is the line in the plan I trust least. Catalog data has many write paths (admin tools, bulk imports, pricing jobs, inventory updates, A/B-test config, localisation). Every missed path is a stale-cache bug that ships wrong prices or wrong stock to customers. The plan needs an enumeration of write paths and a strategy (write-through vs. write-around, TTL backstop, event-driven invalidation, key versioning) — not a one-liner.

3. **Consistency model is unspecified.** Product catalog reads sound innocuous, but "price" and "in-stock" are inside this surface. Stale-by-N-seconds is fine for descriptions; not fine for prices during a flash sale or for stock at checkout. The plan must name what is cached, what is not, and the staleness contract for each.

4. **No evidence the bottleneck is where the plan assumes.** Catalog reads being slow can be: missing index, N+1 ORM pattern, poor query plan, cold PG buffer cache, app-tier serialisation cost, cross-region latency, or genuinely PG-bound throughput. Each has a different fix, and Redis only helps the last one. A spike — measure first, where exactly is the time going — is cheaper than a Redis rollout and may make Redis unnecessary.

5. **Alternative: PG read replica + better caching at the edge.** Many product-catalog workloads are dominated by anonymous, cacheable HTTP traffic. A CDN/edge cache with sensible `Cache-Control` and surrogate keys often eliminates 80–95% of read traffic before it reaches the app, with no new stateful infra to operate. This isn't named in the plan at all.

6. **Alternative: in-process cache.** For hot, small, mostly-read catalog metadata, an in-process LRU with short TTL gives most of the win at zero ops cost. Worth ruling out before committing to a cluster.

7. **"Thin client" is hand-wavy.** Connection pooling, timeout/retry policy, circuit-breaker on Redis outage, key namespace, serialisation format, schema evolution, and observability hooks are all non-trivial decisions hidden inside that phrase.

8. **Operability gap.** What's the SLO? What burns the error budget — Redis unavailability, cache-miss storms, hot-key contention? What's the rollback (feature flag the read path)? None of this is in the plan.

9. **Security posture.** Redis in front of catalog data may not be high-sensitivity, but auth, network isolation (VPC/private subnet), TLS, and least-privilege credentials still need to be explicit.

## Recommendation

**Do not approve as written.** Send back for reshaping. Specifically:

1. **Restate as a problem, not a solution.** "Catalog reads at p95 are X ms today; we need them at Y ms" or "Postgres read CPU is at Z% during peak and threatens checkout latency" — something measurable.
2. **Produce evidence.** Run a one-week measurement spike: profile the slow path, confirm Postgres is the bottleneck, identify the top N queries by time, check whether index/query/replica fixes would close the gap. This is a small, time-boxed bet before committing to new infrastructure.
3. **Consider the boring alternatives in writing.** Edge/CDN caching, PG read replicas, query/index tuning, materialised views, in-process cache. If Redis still wins after that comparison, the plan will be much stronger and the team will know why.
4. **If Redis remains the answer, expand the plan to include**: NFR targets (latency, hit-rate, staleness tolerance per data class), an enumeration of all write paths and the invalidation strategy for each, the consistency contract (especially for price and stock), failure-mode behaviour when Redis is unavailable, operability section (SLOs, alerts, dashboards, runbook, rollback via feature flag), security posture, and an appetite (time-box) for the build.
5. **Ship behind a feature flag with a measured rollout** — start at 1% of read traffic, watch hit-rate, latency, and invalidation lag, then ramp.

Approval blocked pending: problem statement with metric and target, evidence Postgres is the actual bottleneck, written comparison against at least two boring alternatives, and an operability + invalidation plan with the depth the risk warrants.
