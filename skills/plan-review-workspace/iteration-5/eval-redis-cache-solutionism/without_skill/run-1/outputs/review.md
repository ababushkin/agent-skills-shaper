# Plan Review: Redis Caching Layer for Product Catalog

## Summary verdict

Not approved as stated. The plan describes a solution before establishing that the solution is the right one. Several assumptions are implicit and unverified, and the operational cost is understated. The idea may be sound — but we can't tell yet.

---

## What the plan gets right

- Scope is narrow (product catalog reads only), which is a good instinct.
- Cache-invalidation on writes is mentioned, which shows awareness of the main failure mode. Most proposals skip this.
- "Thin client" suggests an intent to keep the integration surface small.

---

## What's missing before approval

### 1. The problem isn't stated

The plan proposes Redis as an answer but never says what question it's answering. Is Postgres slow under current load? Are p99 read latencies unacceptable? Is there a specific capacity ceiling being approached? "Caching is good for reads" is not a problem statement — it's a heuristic.

Without a measured problem, there's no way to know whether this will work, and no way to evaluate success afterwards. What metric are we trying to move, and by how much?

### 2. Have cheaper options been ruled out?

Redis is not the first thing to try. Before adding a new system to operate:
- Is the slow query indexed correctly?
- Has connection pooling been tuned?
- Are there expensive ORM patterns generating N+1 reads?
- Has the Postgres query plan been inspected under realistic load?
- Would read replicas serve the purpose without introducing a cache-coherence problem?

None of these are mentioned. If they've been tried and ruled out, say so explicitly. If they haven't, this plan is premature.

### 3. Cache invalidation is the hard part — it's one bullet point

"Add cache-invalidation on writes" is doing a lot of work in a short phrase. Product catalogs are notoriously tricky:
- What constitutes a write? Direct DB writes, ETL jobs, admin tools, bulk imports, downstream event-driven updates?
- What's the invalidation strategy — TTL, explicit delete, write-through, event-driven?
- What happens during a partial failure where the write commits but the cache invalidation doesn't?
- What's the staleness tolerance? Is serving a stale price for 30 seconds acceptable? 5 minutes?

These questions have different answers for different fields in a product catalog (price vs. description vs. stock level), and the plan treats them as one concern. Cache bugs are hard to detect and hard to debug. This section needs an order of magnitude more detail.

### 4. Operational cost is real and not acknowledged

A Redis cluster is:
- Another system to monitor, alert on, upgrade, and scale
- Another failure mode (what happens to reads if Redis goes down — graceful fallback or outage?)
- Another source of runbooks and on-call burden
- Another infrastructure cost

This isn't a reason to reject the plan, but it needs to be weighed explicitly. The plan reads as if Redis has no cost beyond the initial implementation.

### 5. What does success look like?

There are no acceptance criteria. If we ship this, how do we know it worked? What's the target cache hit rate? What latency improvement are we aiming for? What happens if we ship it and cache hit rate is 20% — do we declare success anyway?

---

## Risks not mentioned

- **Cold start**: On deployment or after a cache flush, all reads hit Postgres simultaneously. If that's what was causing the load problem, the first deploy could cause an incident.
- **Memory sizing**: Product catalogs can be large. What's the eviction policy when Redis fills up? LRU silently degrades hit rate — has that been modelled?
- **Read-your-own-write consistency**: After a user updates a product, do they see the update immediately or does the cache make them see stale data? This is a UX concern that shows up as a support ticket.
- **Testing**: How do you write reliable tests for a system whose behaviour depends on cache state? Integration tests that hit Redis are order-sensitive and flaky.

---

## What would make this approvable

1. A paragraph stating the measured problem (latency numbers, load numbers, Postgres metrics).
2. A short list of alternatives considered and why they were ruled out.
3. A concrete invalidation design — not a bullet, a diagram or a decision: which strategy, what staleness tolerance, what failure behaviour.
4. A success metric with a number attached.
5. An operability section: monitoring, alerting, fallback behaviour when Redis is unavailable.

The underlying instinct — read-heavy product catalog, caching is a reasonable lever — is defensible. But a plan that's one paragraph long for a distributed systems change of this complexity is not ready to approve. The detail that matters is almost entirely in the cache invalidation design and the failure modes, and those are exactly what's missing.

**Status: Revise and resubmit.**
