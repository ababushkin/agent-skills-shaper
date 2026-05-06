# Plan review: Redis cache in front of Postgres for product catalog reads

**Recommendation: Do not approve as written.** The plan jumps to a solution before establishing that caching is the right answer, and elides most of the operational and correctness work that makes a cache safe in production. Below is what I'd want answered before this becomes a "yes."

---

## 1. The plan starts with a solution, not a problem

The proposal opens with "introduce Redis." That's a "how," not a "what" or a "why." Before approving, I need:

- **What is the actual problem?** Is read latency too high? Is Postgres CPU saturated? Are we hitting connection limits? Is it cost? Each of these has a different best answer, and only some of them are "add a cache."
- **What are the numbers?** What's current p50/p95/p99 read latency for catalog queries? What's the QPS? What's the Postgres load profile? What's the target after the change? "Faster" is not a target.
- **What's the cost of doing nothing?** Is this a current production fire, a forecasted scaling problem, or a "we read it on a blog" problem?

Without those, we can't tell whether Redis solves it, whether a smaller intervention solves it, or whether we're solving the wrong problem.

## 2. Cheaper alternatives haven't been considered

A cache is a meaningful new piece of infrastructure with its own failure modes. Before adding one, I'd want to see explicit consideration of:

- **Postgres-side fixes first.** Are the catalog queries indexed properly? Is there an obvious N+1? Would a materialised view, a covering index, or query rewriting close the gap? Postgres can serve a *lot* of catalog reads if the queries are right.
- **Read replicas.** If the issue is read load on the primary, a read replica is operationally simpler than a cache and doesn't introduce a consistency model.
- **Application-level caching.** In-process LRU on the API tier can be the right answer for hot, small, slowly-changing catalog data — no new infra, no new failure modes, no invalidation protocol across nodes.
- **CDN / HTTP caching.** If catalog reads are HTTP-cacheable (and product catalog often is), a CDN with appropriate TTLs and surrogate keys is dramatically cheaper than running a Redis cluster.
- **PgBouncer / connection pooling.** If the issue is connection exhaustion, this is the right tool, not Redis.

The plan should name which of these were considered and why they were rejected.

## 3. "Cache invalidation on writes" is doing all the heavy lifting in one phrase

This is the hard part of the entire project, and it's a single clause. Specifically I want to see:

- **Invalidation strategy.** Write-through? Write-around with TTL? Write-behind? Each has very different consistency and complexity properties.
- **What does "on writes" mean operationally?** Is the write path the only mutation source? What about: bulk imports, admin tools, batch jobs, replication from upstream systems, manual DB edits during incidents, schema migrations that touch data?
- **Failure modes.** What happens when the invalidation message is lost? When Redis is up but the invalidation pub/sub is down? When two writers race? When a write succeeds in Postgres but the cache delete fails?
- **Stale-read tolerance.** What's the maximum acceptable staleness? Seconds? Minutes? "Eventually consistent" without a number is not a spec. A pricing or inventory field has very different tolerance from a product description.
- **Cache stampede / thundering herd.** When a hot key expires, what prevents a thousand concurrent requests from hitting Postgres simultaneously? (Single-flight, request coalescing, probabilistic early refresh — pick one.)
- **Negative caching.** Do we cache "not found" responses? For how long? This affects 404 storms and enumeration-style attacks.

If none of these are answered, "cache-invalidation on writes" is a euphemism for "we'll figure it out," and that's where data-correctness bugs come from.

## 4. The Redis cluster itself is being treated as a checkbox

"Add a Redis cluster" hides a meaningful amount of work:

- **Topology.** Single primary with replicas? Redis Cluster with sharding? Managed (ElastiCache, MemoryDB, Upstash) or self-hosted? Each has different operational profiles.
- **Sizing.** Working set size? Eviction policy (`allkeys-lru`, `volatile-lru`, `noeviction`)? What happens when memory pressure causes eviction of keys we expected to be present?
- **Persistence.** AOF, RDB, none? Does this cache need to survive a restart, or is cold-start acceptable?
- **HA and failover.** What's the RTO/RPO? What's the behaviour during a failover — does the application gracefully degrade to Postgres-only?
- **Network and latency.** Same AZ? Same region? What's the round-trip cost relative to the Postgres query we're trying to avoid? (A poorly placed cache can be slower than the DB.)
- **Security.** AuthN, TLS in transit, network isolation, secrets handling for the client.

## 5. Operability is missing entirely

The plan has no observability or rollout story. Before approving I need:

- **Metrics:** hit rate, miss rate, eviction rate, latency p50/p95/p99 of cache vs origin, invalidation lag, error rates, memory utilisation.
- **Alerts:** hit rate dropping below threshold, invalidation backlog, Redis unreachable, memory at capacity, replication lag.
- **Rollout plan:** dark launch (read both, compare, serve from Postgres), then shadow, then percentage rollout, with a kill switch (feature flag) at every layer.
- **Rollback plan:** can we turn the cache off instantly without code changes? If the cache returns wrong data in production, what's our recovery path?
- **Runbook:** what does on-call do at 3am when hit rate collapses, when Redis is down, when invalidation is lagging, when stale data is reported by a customer?

## 6. Blast radius and reversibility

- **Reversibility.** Adding the read path with a flag is two-way-door (good). Changing the write path to publish invalidations is harder to reverse if other consumers come to depend on it (one-way-door creep). The plan should note this.
- **Blast radius.** If the cache returns stale or wrong data, what's the worst-case customer impact? Wrong price shown? Stock shown for an out-of-stock SKU leading to oversell? This sets the bar for the consistency guarantees we need.
- **Correctness over availability or vice versa?** If Redis is degraded, do we serve stale data, fall back to Postgres (and risk overload), or fail closed? This is a product decision dressed as a technical one.

## 7. Cost and TCO

- Redis cluster cost (compute + memory + network).
- Engineering cost: client library, invalidation infrastructure, observability, on-call training, postmortem cycles for cache-related incidents.
- Cognitive cost: every future engineer touching the catalog read or write path now has to reason about cache coherence.

A small Postgres tuning project might deliver 80% of the value at 5% of the TCO. That comparison isn't in the plan.

## 8. Scope and definition of done

- Which catalog endpoints? All of them? Hot ones only? List by name.
- What's the success metric? "p95 read latency under Xms at Y QPS, with hit rate above Z%, with no measurable increase in incorrect catalog reads." Pick numbers.
- When do we know we're done? When do we know we should roll back?

---

## What I'd want before I approve

A short design doc that includes:

1. **Problem statement with current numbers and a target.**
2. **Alternatives considered** (Postgres tuning, read replica, in-process cache, CDN) and why each was rejected.
3. **Consistency model**: maximum staleness, invalidation strategy, behaviour under partial failure.
4. **Operability plan**: metrics, alerts, dashboards, runbook, rollback.
5. **Rollout plan**: flagged, staged, with shadow comparison.
6. **Cost estimate**: infra + engineering + ongoing operational load.
7. **Scope**: which endpoints, in what order, with explicit success criteria.

If the answer to "have we tried tuning Postgres first" is "no," I'd start there before approving any new infrastructure. Caching is a powerful tool but it's also one of the most reliable ways to introduce subtle, customer-visible correctness bugs — and the plan as written doesn't yet show that we've earned the right to take on that complexity.

**Decision: changes requested.**
