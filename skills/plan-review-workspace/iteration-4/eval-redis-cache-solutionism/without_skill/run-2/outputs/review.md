# Plan review: Redis cache for product catalog reads

**Verdict: Do not approve as written. Send back for problem framing and evidence.**

The plan jumps straight to a solution ("add Redis", "thin client", "cache invalidation on writes") without establishing that Postgres read latency or load is actually the problem worth solving — let alone that Redis is the right answer. This is a classic solutionism pattern: the proposer has chosen the technology before defining the constraint.

---

## What's missing

### 1. The problem is undefined
- What is the current p50/p95/p99 read latency for product catalog queries?
- What is the current Postgres load (CPU, IOPS, connection count, replica lag)?
- What user-facing or business symptom is driving this? Slow PDPs? Checkout timeouts? Cost? Headroom for a launch?
- What is the target latency / load reduction, and how was it derived?

Without these numbers, "introduce Redis" is a solution looking for a problem. Postgres can comfortably serve tens of thousands of catalog reads per second with proper indexing, materialized views, or a read replica — none of which require operating a second stateful system.

### 2. Alternatives not considered
The plan lists one option. At minimum, the design should compare:
- **Postgres-side**: better indexes, partial indexes, covering indexes, materialized views, `pg_stat_statements` to find the actual slow queries.
- **Read replicas**: cheaper to operate than a Redis cluster, no cache-coherence problem.
- **Application-level caching**: in-process LRU (per app instance), or a CDN in front of catalog API responses (likely the cheapest answer for read-heavy product catalogs).
- **HTTP caching**: `Cache-Control` + edge cache for catalog endpoints. For a product catalog (mostly read, low write rate, tolerable staleness), this is often the right answer and avoids a stateful tier entirely.
- **Materialized denormalization**: precompute the catalog read shape into a single table refreshed on write.

If Redis still wins after this comparison, fine — but the comparison must exist in writing.

### 3. Cache invalidation is hand-waved
"Add cache-invalidation on writes" is the hardest sentence in the plan, written as if it's the easiest. Specifics needed:
- **Invalidation strategy**: write-through, write-around, write-behind, TTL-only, or event-driven invalidation? Each has different consistency and complexity profiles.
- **What's the cache key shape?** Per-SKU? Per-query? Per-search-result? Search-result caching is notoriously hard to invalidate correctly.
- **Cross-region / multi-writer**: if writes can happen from multiple services or regions, how do invalidations propagate? Race between write-commit and invalidate-publish?
- **Stampede protection**: what happens when a hot key expires under load? (Single-flight, probabilistic early expiry, etc.)
- **Stale-read tolerance**: what's the acceptable staleness window for product data (price, inventory, availability)? Pricing/inventory caching has well-documented business-impact failure modes.

### 4. Operability is absent
- **SLOs**: what's the cache hit rate target? What's the latency SLO with cache cold vs warm?
- **Failure mode**: when Redis is down or partitioned, does the app fall back to Postgres (and survive the thundering herd) or fail closed?
- **Capacity**: how big does the cluster need to be? Working-set size estimate? Eviction policy?
- **Observability**: hit rate, miss rate, eviction rate, p99 latency, key cardinality, memory pressure — instrumented before launch?
- **On-call**: who pages? What's the runbook for "cache returning stale prices" or "cache cluster down"?
- **Backup/restore**: do we need persistence? Replication topology? Failover behaviour?

### 5. One-way doors not named
Adding a stateful cache tier is a meaningfully one-way door:
- A second stateful system to operate, monitor, patch, version-upgrade.
- Application code becomes coupled to the cache shape — removing it later is a multi-quarter project.
- Correctness bugs from cache invalidation will be hard to reproduce and will surface as customer-visible price/inventory wrongness.
- Vendor / managed-service lock-in (ElastiCache vs Memorystore vs self-hosted) is itself a sub-decision.

The plan treats this as a small additive change. It is not.

### 6. Boring-technology check failed
Postgres with a tuned read path or a CDN in front of read endpoints is the boring answer. Redis is the interesting answer. Interesting answers need written justification — what does Redis uniquely solve that the boring options can't?

### 7. Cost / TCO not considered
Redis cluster ops, monitoring, on-call burden, engineer-time-to-build, ongoing cache-invalidation bug tail. Compared to: a CDN config change, or `CREATE INDEX`, or a read replica.

---

## What I'd ask for before approving

1. **Problem statement with numbers**: current latency/load, target latency/load, business symptom.
2. **Alternatives table**: at minimum Postgres tuning, read replica, HTTP/CDN caching, in-process cache, Redis — with cost, complexity, blast-radius columns.
3. **Cache-coherence design**: invalidation strategy, key shape, staleness tolerance, stampede protection, failure-mode behaviour.
4. **Operability plan**: SLOs, instrumentation, runbook, capacity model, failover behaviour.
5. **Time-boxed spike** (1–2 weeks) on the top-2 alternatives before committing to a build, with a written recommendation at the end.

If the spike confirms Redis is the right answer and the design doc fills the above gaps, then approve. As-is: not yet.
