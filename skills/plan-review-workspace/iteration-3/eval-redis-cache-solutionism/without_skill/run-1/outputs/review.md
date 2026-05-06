# Plan Review: Redis Cache for Product Catalog Reads

## Verdict: REVISE — do not approve as written

This plan is solution-first. It names a technology (Redis cluster), an architectural pattern (cache-aside with invalidation), and an implementation shape (thin client) — but it does not name the problem being solved, the user-visible outcome the change is meant to move, or the threshold that would tell us the change worked. Approving it would be approving a build, not a bet.

## What's missing

### 1. Problem statement
"Introduce Redis as a caching layer" is a solution. The plan does not say:
- What read latency is today (p50 / p95 / p99)?
- What latency is required, and by whom (which user surface, which page)?
- Is the pain latency, throughput, Postgres CPU, cost, or something else?
- Is there evidence the catalog read path is actually the bottleneck (traces, slow-query logs, APM data)?

Without this, "Redis" is an answer in search of a question.

### 2. Success metric
There is no measurable outcome. A complete plan would say something like: "p95 catalog read latency on the PDP from 380ms to <80ms, measured at the edge, sustained over a week." Without a number, "done" is undefined and the post-launch review (universal Principle 1: shipped is not done; observed is done) has nothing to check.

### 3. Alternatives considered
Caching in front of Postgres is one option among several. The plan does not show that any of these were considered and rejected:
- **Postgres-side fixes:** missing indexes, query rewrites, materialised views, `pg_stat_statements` review, connection pool tuning, read replicas. Often a 10x latency win with no new component.
- **Application-level caching:** in-process LRU, HTTP cache headers + CDN at the edge for catalog pages (catalogs are usually highly cacheable at the CDN tier).
- **Read replicas + routing:** scales reads without introducing a second consistency model.
- **Materialised view / denormalised read model** in Postgres itself.

A CDN in front of catalog pages is often the cheapest, lowest-risk, highest-leverage option for product catalogs and is conspicuously absent.

### 4. Cost of the chosen path (one-way door)
Introducing Redis is close to a one-way door. Once writes invalidate Redis and reads are served from Redis, the system has:
- A second data store with its own failure modes, capacity model, and on-call runbook
- A new consistency model (cache-aside + invalidation has well-known race conditions: thundering herd, stale reads on invalidation failure, dual-write divergence)
- A new dependency in the read path — Redis outage is now a catalog outage unless explicitly designed around
- Cluster operations: failover, resharding, version upgrades, monitoring, capacity planning
- A new "innovation token" spent — is this the best use of it?

The plan acknowledges none of this.

### 5. Cache invalidation correctness
"Add cache-invalidation on writes" is one line in the plan and is the hardest part of the work. Open questions:
- Single-writer or multi-writer? Async replication? Are writes done via a transactional outbox, or fire-and-forget after the DB commit?
- What happens when invalidation fails (Redis down, network partition, app crashes between commit and invalidate)?
- TTL strategy as a backstop?
- How are bulk writes (catalog imports, price updates) handled — invalidate per-row or flush by tag?
- Negative caching for missing SKUs?
- How is staleness bounded and observable?

"Cache invalidation is one of the two hard things in computer science" is a cliché because it's true. A one-line treatment is a red flag.

### 6. Operability
Missing entirely:
- SLO for the new read path
- Failure-mode behaviour (does the app fall back to Postgres on Redis failure, and has the resulting load on Postgres been capacity-modelled?)
- Rollback plan (how do we turn this off in production in five minutes?)
- Feature-flag / canary plan (which catalog routes, which percentage of traffic, for how long?)
- Cache hit-rate target and what we do if we don't hit it
- On-call runbook for Redis cluster incidents

### 7. Cost
A Redis cluster is not free in dollars or operational load. The plan should compare the dollar + ops cost of the Redis path against alternatives (CDN, read replica, query optimisation) before committing.

## What a revised plan would look like

A version of this plan I would approve starts with:

> **Problem:** Product detail page p95 latency is 420ms; product team wants <120ms to support the planned recommendation rail. Tracing shows 280ms is spent in three N+1 catalog queries. Catalog is read 50:1 vs. write.
>
> **Target:** p95 PDP catalog-read latency <60ms, sustained over 7 days at production load. Cache hit rate >90% steady state.
>
> **Alternatives considered:**
> - Query optimisation + index: spike showed 180ms achievable, falls short of target.
> - CDN edge cache for PDP HTML: rejected — personalised content per user.
> - Read replica: doesn't solve per-query latency, only throughput.
> - In-process LRU: rejected — fleet of 80 app pods, low hit rate per pod.
> - **Selected: Redis** — shared cache across pod fleet, sub-ms reads, well-understood at our scale.
>
> **Risks named:** invalidation correctness, Redis outage = degraded read path (mitigation: fall back to Postgres with circuit-breaker, capacity tested for 100% fallback).
>
> **Operability:** SLO 99.9% on read path, alerts on hit-rate drop, runbook for Redis failover, feature flag per catalog route, canary 1% → 10% → 100% over 2 weeks.
>
> **Reversibility:** flag off restores Postgres-only path within 60s; cluster decommission is a 1-week project if we need to abandon.

## Bottom line

Reject the current framing; do not approve. Send back for: a problem statement with measured baseline, a numeric success target, alternatives evaluated (especially CDN and Postgres-side fixes), an explicit one-way-door acknowledgement, an invalidation design with failure-mode handling, and an operability section. If the team comes back and the data still says Redis is the right answer, this becomes a quick approval — but it has to start from the problem, not the technology.
