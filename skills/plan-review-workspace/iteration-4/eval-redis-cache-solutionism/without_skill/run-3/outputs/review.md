# Plan Review: Redis Cache Layer for Product Catalog

## Verdict: Do not approve as written. Reshape required.

This plan jumps to a solution before the problem is established. Approving it would commit the team to a one-way-ish door (operational dependency on a Redis cluster, a new invalidation contract spanning every write path) without evidence the underlying problem warrants it.

---

## What's missing

### 1. The problem is not stated
The plan describes *what* will be built, not *what is wrong today*.
- What is the current p50/p95/p99 latency on product catalog reads?
- What is the current Postgres load attributable to catalog reads?
- What is the user-visible symptom — slow page loads, timeout errors, scaling cost, peak-traffic instability?
- What is the target after the change, expressed as a number?

Without these, "approve" means approving infrastructure on faith. We can't tell afterwards whether the change worked.

### 2. Cheaper alternatives have not been considered in writing
Adding Redis is the heavyweight option. Before committing, the plan should rule out:
- **Postgres query tuning / indexing** — has an EXPLAIN been run on the slow queries? Is there a missing index?
- **Postgres read replicas** — already in the stack? Cheaper to scale horizontally without a new system.
- **In-process caching** (per-app-instance LRU) — zero new infrastructure, often sufficient for catalog-style read patterns.
- **HTTP / CDN caching** — product catalog is often the most cacheable thing in the system at the edge. Why isn't this the first move?
- **Materialised views or denormalised read tables in Postgres** — keeps the data plane single.
- **PgBouncer / connection pooling tuning** — if the bottleneck is connections, not query time.

A plan that proposes Redis without naming why these alternatives are insufficient is solution-first thinking.

### 3. Cache invalidation is hand-waved
"Add cache-invalidation on writes" is the entire hard part of this project, written in seven words. The plan must specify:
- **Which writes?** Direct DB writes from this service? Writes from other services? Writes from admin tools, batch jobs, replication, ETL, manual SQL?
- **What invalidation strategy?** Write-through, write-behind, TTL-only, explicit invalidation, event-driven via CDC?
- **What is the consistency contract?** Read-your-writes? Eventual consistency with a stated bound? Strong consistency?
- **What happens on partial failure?** Postgres write succeeds, Redis invalidation fails — now the cache lies. For how long? With what blast radius?
- **What about multi-key invalidation?** Updating a category affects N product entries. How is this enumerated?

This is the famous "two hard things in computer science" problem and the plan does not engage with it.

### 4. Operability is absent
- SLOs for the cache layer? Hit-rate target? Latency budget?
- What happens when Redis is down? Fallback to Postgres directly, or fail closed?
- Cache stampede / thundering-herd protection (request coalescing, jittered TTLs)?
- Memory sizing — what working-set size is expected, what eviction policy, what happens at eviction?
- Monitoring — cache hit rate, eviction rate, latency, memory headroom, replication lag?
- Cost — Redis cluster TCO vs. the alternatives above?
- Failure modes — split brain in the Redis cluster, network partition between app and Redis, slow Redis pulling down the read path?

### 5. Reversibility is not named
A Redis dependency is not strictly a one-way door, but the invalidation contract embedded across every write path is sticky. Once 30 write sites depend on cache-aware code, ripping it out costs a quarter. The plan should name this explicitly and decide it is worth it.

### 6. "Thin client" is a smell
"Thin client" usually becomes a thick client within two quarters as serialisation, key-namespacing, multi-get, pipelining, retry, circuit-breaking, and observability concerns accumulate. Either adopt a mature client library (and name it), or budget for the thick client honestly.

---

## What I'd send back for

A revised plan that:
1. States the problem as a measured outcome (current vs. target latency / load / cost / error rate).
2. Lists the cheaper alternatives considered and explains why each is insufficient with evidence.
3. If Redis is still the answer, specifies the invalidation strategy concretely, including the consistency contract and partial-failure behaviour.
4. Includes an operability section: SLOs, fallback behaviour, monitoring, capacity, stampede protection, cost.
5. Proposes a small first slice — e.g. cache one read path behind a feature flag, measure the hit rate and the latency improvement, then decide whether to expand. Not a cluster + thin client + invalidation across the board as a single bet.

## Recommended next step

Before approving any build, run a one-week spike: profile the current catalog read path, identify the actual bottleneck, and try the cheapest viable mitigation (likely indexing, HTTP caching, or in-process caching) in a measured experiment. If that doesn't close the gap, the case for Redis writes itself — and the design doc that follows will be far better grounded.
