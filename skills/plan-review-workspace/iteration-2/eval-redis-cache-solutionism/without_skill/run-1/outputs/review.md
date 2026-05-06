# Review: Redis caching layer in front of Postgres for product catalog reads

**Verdict:** Do not approve as-is. The plan jumps to a solution before establishing the problem. There is enough missing context that approving this would mean accepting a meaningful operational and complexity cost on faith. Recommend reshaping into a problem-first proposal with evidence before committing to Redis.

---

## What the plan says

- Add a Redis cluster
- Write a thin Redis client
- Add cache invalidation on writes to product catalog
- Purpose: cache product catalog reads in front of Postgres

That's the entire description. There is no problem statement, no measured baseline, no target, no alternatives considered, no operability plan, no rollout plan, no cost estimate.

---

## Primary concern: this is solution-first

The plan starts with "introduce Redis" rather than with a problem. The right shape would be:

- What is broken or insufficient about the current product catalog read path?
- Who is affected, and how badly?
- What is the measured baseline (p50/p95/p99 latency, QPS, DB CPU, error rate)?
- What target are we trying to hit, and why that target?
- What alternatives have we considered, and why is Redis the answer?

Without those, "approve Redis cluster" is a bet on a guess. It might be the right call. We can't tell from what's written.

---

## Specific gaps and questions

### 1. Problem and evidence

- Is Postgres actually the bottleneck? What does the slow-query log show? What's the buffer cache hit ratio? Is the DB CPU-bound, IO-bound, or connection-bound?
- What's the read/write ratio on the product catalog? (If writes are frequent, cache invalidation overhead can erase the gains.)
- What's the access distribution? A long-tail catalog with low repeat-read rate gets little from caching.
- Is this a latency problem, a throughput problem, or a cost problem? The right solution differs sharply between the three.

### 2. Alternatives not considered

Before adding a whole new datastore, the cheaper, less-novel options should be ruled out in writing:

- **Postgres tuning:** indexes, query plans, `work_mem`, connection pooling (PgBouncer), `pg_stat_statements` review.
- **Read replicas:** routes catalog reads off the primary; no new technology, no cache-coherence problem.
- **Application-level in-process cache:** LRU/TTL in the API process. Cheaper to operate than a Redis cluster. Sufficient for many catalog workloads.
- **CDN / edge cache for catalog responses:** if the catalog is read over HTTP and largely public, the cache belongs at the edge, not next to the DB.
- **Materialized views or denormalized read models** in Postgres itself.

A Redis cluster is one of the most expensive answers on this list operationally. It needs to be justified against the cheaper ones, not assumed.

### 3. Cache invalidation — "the hard problem"

"Add cache-invalidation on writes" is one line in the plan and is doing enormous load-bearing work. Specifics needed:

- Invalidation strategy: write-through, write-around, write-behind, or TTL-only?
- What happens to readers between a write and the cache invalidation propagating? Can stale reads cause downstream incorrectness (pricing, inventory, promotions, eligibility)?
- What's the consistency contract being offered to consumers? "Eventually consistent" is fine if stated; not fine if assumed.
- Out-of-band writes: are there any code paths or batch jobs that mutate the catalog without going through the application's write path? If yes, those will silently produce stale cache entries forever.
- Multi-region / multi-writer concerns?

This is the part most likely to produce subtle, hard-to-reproduce bugs in production. It deserves more than one bullet.

### 4. Operability is absent

A Redis cluster is a stateful, distributed system. The plan says nothing about:

- SLOs/SLIs for the cache (hit rate target, latency, availability)
- Failure modes: what happens when Redis is down? Does the system fail open (read through to DB) or fail closed (return errors)? Thundering herd on cold cache?
- Capacity planning: working set size, eviction policy, memory headroom
- Topology: cluster vs. sentinel vs. managed (ElastiCache / MemoryDB / Upstash)? HA across AZs?
- Observability: hit/miss rates, latency, evictions, replication lag, key distribution
- Backup, persistence (AOF/RDB or none), upgrade path
- On-call runbook for cache poisoning, hot keys, memory pressure, network partitions
- Security: auth, TLS, network isolation, secret rotation

### 5. Rollout, blast radius, reversibility

- How is this rolled out? Behind a feature flag, with progressive percentage rollout, with the ability to disable instantly?
- Blast radius if the cache returns wrong data: which downstream systems are affected?
- Reversibility: how do we turn it off? Is the read path designed so the cache is genuinely optional, or will removing it become a one-way door once dependencies grow on its latency profile?

### 6. Cost

No mention of cost. A production-grade Redis cluster (managed, multi-AZ, enough RAM for the working set, plus replicas) is not free, and the recurring cost is often higher than the one-shot engineering cost. The plan should compare TCO against the alternatives.

### 7. Team / operations fit

- Does the team already operate Redis? If not, this is a new on-call surface, new dashboards, new failure modes, new hiring criterion.
- "Innovation tokens" question: is Redis already in the stack? If yes, fine. If no, it needs to earn its slot against the existing stack.

### 8. Definition of done

There is no success criterion. What does "this worked" look like? Examples of what would be acceptable:

- "p95 catalog read latency drops from X ms to under Y ms at peak QPS"
- "DB CPU at peak drops from X% to under Y%"
- "Catalog read cost per request drops from $X to $Y"

Without a target, we cannot tell after the fact whether the cache earned its place, and we cannot decide whether to expand, hold, or roll it back.

---

## What I'd want to see before approving

A reshaped plan with:

1. **Problem statement** — what's broken now, with measured numbers.
2. **Target** — the metric that will move and by how much.
3. **Alternatives considered** — at minimum: PG tuning, read replica, in-process cache, CDN. Why each was rejected (or why Redis was chosen as the best of a shortlist).
4. **Cache design** — invalidation strategy, consistency contract, failure mode, stale-read handling.
5. **Operability section** — SLOs, alerts, failure modes, runbook, capacity model.
6. **Rollout plan** — flag, progressive rollout, kill switch.
7. **Cost estimate** — both build cost and recurring infra cost.
8. **Definition of done** — measurable outcome and how we'll observe it post-launch.

A page of writing covers all of this. It is much cheaper than discovering the wrong answer in production.

---

## If something has to be done now

If there is real production pain and the team needs immediate relief, the lowest-risk first step is almost never "stand up a Redis cluster." It is usually one of:

- Profile the actual slow path (`pg_stat_statements`, APM traces) — often reveals an indexing problem solved in an afternoon.
- Add a small in-process LRU on the hottest endpoints behind a feature flag — minutes to deploy, trivial to remove, no new infrastructure.
- Add a read replica and route catalog reads to it.

Any of these can be tried first. If they're insufficient, the case for Redis becomes evidence-based rather than assumed, and the eventual Redis design will be informed by what the cheaper attempts taught you about the workload.

---

## Bottom line

Not approved. The proposal is a solution looking for a justification. The risk isn't that Redis is the wrong choice — it might well be the right one — it's that the team doesn't yet know whether it is, and approving it now commits to operational complexity that may not pay back. Reshape into a problem-first proposal with measured baseline, alternatives, and an operability plan, and bring it back.
