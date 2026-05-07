# Plan Review: Redis Caching Layer for Product Catalog Reads

## Summary verdict

Not ready to approve. The plan describes a solution without establishing that it solves a real, measured problem. Before any Redis work starts, I need to see the evidence that justifies it.

---

## What's missing before this plan is actionable

### 1. No problem statement

The plan starts with the solution: "introduce Redis as a caching layer." There is no statement of what is actually wrong. Some possibilities:

- Product catalog pages are slow for users
- Postgres is under CPU/IO pressure
- P95 read latency is breaching an SLO
- The catalog scales poorly under traffic spikes

These are different problems with different best solutions. Without naming the actual problem, there is no way to evaluate whether Redis is the right fix — or even the right category of fix.

**Ask:** What metric is broken, by how much, and what does "fixed" look like?

### 2. No evidence that Postgres is the bottleneck

Adding a caching layer in front of a database that isn't the bottleneck adds operational complexity with zero benefit. Common alternatives to investigate first:

- Are catalog queries actually slow, or is the problem elsewhere (serialization, N+1s, network, rendering)?
- Are indexes missing or stale?
- Is connection pooling undersized (PgBouncer)?
- Could materialized views or read replicas absorb the load at lower cost?

Running `EXPLAIN ANALYZE` on the slow queries costs nothing. A Redis cluster costs engineering time, operational overhead, and ongoing infrastructure spend.

**Ask:** Have you profiled where the time actually goes? What does the slow query log show?

### 3. Cache invalidation is the hard part — and it's underspecified

"Add cache-invalidation on writes" is four words that describe months of potential correctness bugs. The plan needs to answer:

- What is the invalidation strategy? Key-based eviction on write? TTL-based expiry? Event-driven invalidation?
- What are the write paths? Are catalog writes centralized in one service, or scattered across admin tools, import jobs, partner APIs?
- What is the acceptable staleness window? A product showing an outdated price for 30 seconds may be fine; an outdated price for 30 minutes during a flash sale is a business problem.
- What happens when a write succeeds but cache invalidation fails? Is the system inconsistent until TTL expires?

Cache invalidation is where caching systems fail in production. "Thin client + invalidation on writes" glosses over the part that will actually consume engineering time and produce production incidents.

### 4. No failure mode analysis

Redis going down should not take down product catalog reads. The plan does not mention:

- Fallback behavior when Redis is unavailable (fail open to Postgres, or fail closed?)
- Whether the cluster is configured for high availability (Redis Sentinel or Cluster mode)
- Circuit breaker / health check integration
- What the blast radius is if a deployment bug corrupts the cache

A caching layer that makes your application less reliable than without it is not an improvement.

### 5. No operability plan

- Who is on-call for Redis?
- What does the runbook look like for a cache stampede?
- What metrics and alerts will tell us the cache is working (hit rate, eviction rate, latency distribution)?
- How will we know post-launch whether the cache is actually helping?

### 6. The scope of "product catalog reads" is undefined

- Does this include search queries? Faceted filters? Individual product detail pages? Inventory levels?
- Are catalog reads the majority of DB load, or a minority?
- What is the read:write ratio? A catalog that is written frequently (inventory updates, pricing changes) will have a low hit rate and the cache will provide little benefit while adding all the invalidation complexity.

---

## What would make this approvable

1. **A measured problem**: latency numbers, query times, DB metrics, SLO breaches — something observable.
2. **Evidence that the database is the bottleneck**: profiling output, slow query log, ruling out application-layer causes.
3. **Alternatives considered**: at minimum, missing indexes and read replica — why are those insufficient?
4. **A concrete invalidation design**: which write paths, which strategy, what the failure mode is when invalidation fails.
5. **A rollback plan**: how do we turn this off if it makes things worse?
6. **Success criteria**: what does the cache hit rate need to be? What latency reduction are we targeting?

---

## Recommendation

Send this back for a problem definition and a profiling pass before any design work on the Redis layer. This is two days of investigation that could save weeks of implementation and months of operational pain.

If profiling confirms Postgres reads are the bottleneck and simpler fixes are insufficient, come back with an invalidation design and the items above — and this is likely approvable at that point.
