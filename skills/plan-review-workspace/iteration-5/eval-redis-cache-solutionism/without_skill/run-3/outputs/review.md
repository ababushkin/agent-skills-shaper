# Plan Review: Redis Caching Layer for Product Catalog Reads

## Overall verdict

**Not approved as stated.** The plan jumps straight to a solution without establishing that the problem warrants it. Before committing to a Redis cluster, the team needs to answer some basic questions it hasn't answered yet.

---

## What's missing before this makes sense

### 1. What's the actual problem?

The plan says "product catalog reads" but doesn't say:

- What's the current read latency, and what's the target?
- What does the read volume look like — requests per second, peak vs. steady state?
- Is Postgres actually the bottleneck? Have you profiled it, or is this a guess?
- Are there specific queries that are slow, or is this a general sense that things feel sluggish?

Caching is a solution. It's not obvious yet what problem it's solving. A slow product catalog could be caused by missing indexes, N+1 queries, untuned connection pooling, a poorly written query, or a Postgres config issue — none of which require Redis. Without measurement, this plan is an architectural bet on an unconfirmed hypothesis.

### 2. What does the data access pattern actually look like?

Redis is a good answer for read-heavy, write-infrequent, tolerance-for-brief-staleness workloads. Product catalogs often fit this profile — but not always. Questions that matter:

- How frequently do catalog items change? High write frequency makes cache invalidation hard and the cache hit rate low.
- How large is the catalog? Redis is an in-memory store; cost scales with dataset size.
- Are reads concentrated (hot products) or uniformly distributed? A cache is most valuable when there's concentration — the Pareto principle working in your favour.

### 3. Have simpler alternatives been ruled out?

Before adding a new infrastructure dependency, there are cheaper options worth considering:

- **Postgres read replicas** — if the bottleneck is read throughput, a replica costs less operationally than a Redis cluster and doesn't introduce cache invalidation complexity.
- **Connection pooling tuning** (PgBouncer, etc.) — if the problem is connection overhead, this is a config change, not an architecture change.
- **Query optimisation / index review** — the most common cause of slow reads. Should be ruled out first.
- **HTTP-level or application-level caching** — if the catalog is read by a single service, in-process caching (e.g. a simple LRU in front of the DB call) may be sufficient.

The plan doesn't mention any of these. That's a gap.

---

## Issues with the plan as written

### Cache invalidation is the hard part — the plan glosses over it

"Add cache-invalidation on writes" is one line in a plan that otherwise describes infrastructure setup. Cache invalidation is where this kind of project typically goes wrong. Questions the plan needs to answer:

- Invalidation strategy: TTL-based, write-through, write-around, event-driven? Each has different consistency guarantees and different failure modes.
- What happens when a write partially fails — is the cache invalidated anyway, or does stale data persist?
- What's the blast radius if the invalidation logic has a bug? Do customers see stale pricing, stale availability, stale descriptions?
- If there are multiple services writing to the catalog (or this is expected in future), how does cross-service invalidation work?

The invalidation design needs to be specified before the PR is approved, not figured out during implementation.

### "A Redis cluster" is a significant operational commitment

A Redis cluster — as opposed to a single Redis instance — is a distributed system with its own failure modes: split-brain, slot migration, failover latency, client-side routing requirements. If the team hasn't operated Redis at cluster scale before, this is an innovation token being spent. Questions:

- Is cluster mode actually needed, or would a single primary with a replica suffice?
- Who will be on-call for Redis? Does the team know how to diagnose Redis memory pressure, eviction issues, and cluster failover?
- What's the monitoring story — what alerts exist for cache hit rate, memory usage, eviction rate, replication lag?

If the answer to any of these is "we'll figure it out," that's a risk that should be surfaced explicitly, not buried.

### "Thin client" is undefined

A thin client could mean many things. What does it actually encapsulate? Does it handle:

- Connection pooling / connection lifecycle?
- Serialisation format (JSON? MessagePack? Protobuf?)?
- Error handling — what happens when Redis is unavailable? Does the system fall back to Postgres, or does it return an error?
- Key namespacing and versioning (how do you do a full cache flush on a schema change)?

The fallback behaviour is particularly important. If Redis goes down and the application starts throwing 500s instead of falling back to Postgres, you've traded one availability risk for a worse one.

---

## What a stronger version of this plan looks like

1. **Establish the baseline**: Profile current read latency by query type. Identify the specific bottleneck with data.
2. **Rule out cheaper fixes first**: Index review, query analysis, connection pooling audit. Document why each isn't sufficient.
3. **Validate the caching hypothesis cheaply**: Before a Redis cluster, try application-level caching with a short TTL on the most expensive query path. Measure whether it moves the needle.
4. **If Redis is the right call**, spec the following before building:
   - Deployment topology (cluster vs. primary/replica) with justification
   - Invalidation strategy with explicit consistency guarantees
   - Fallback behaviour on Redis unavailability
   - Observability plan (hit rate, eviction rate, latency, error rate)
   - Rollback plan if Redis introduces regressions
5. **Define done**: What latency target confirms success? What does the post-launch metric review look like?

---

## Summary

The plan describes how to add Redis, not why Redis is the right answer to a problem that hasn't been precisely stated. That ordering — solution first, problem second — is the most common source of unnecessary complexity in infrastructure projects. The team should spend a day profiling before spending a sprint building.

If measurement confirms that Postgres is the bottleneck, that read patterns are cache-friendly, and that simpler alternatives don't suffice — then a Redis caching layer is a reasonable bet, and I'll approve it with a proper spec attached.
