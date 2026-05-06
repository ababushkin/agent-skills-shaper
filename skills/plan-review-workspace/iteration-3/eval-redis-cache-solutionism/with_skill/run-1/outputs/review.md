# Plan review: redis-cache-solutionism

## Plan reference

Pasted plan:
> Introduce Redis as a caching layer in front of Postgres for product catalog reads. We'll add a Redis cluster, write a thin client, add cache-invalidation on writes. Approve?

## Inputs

- **Appetite**: not stated. Implied multi-week given cluster + client + invalidation work.
- **Cynefin domain**: Complicated — caching with invalidation is a knowable problem with established expert practice (TTL strategies, write-through vs write-behind, stampede protection), but it is not Clear cause-effect: invalidation correctness, hit-rate behaviour, and failure-mode interaction with Postgres are non-trivial.
- **Tier**: Full — selected because the plan introduces a new vendor / new piece of production infrastructure (Redis cluster). This is a one-way-door per the auto-select rule (vendor lock-in, production data path). Step 1a fast-track gate evaluated and rejected: precondition 1 fails (not KTLO — net new infrastructure) and precondition 2 fails (touches vendor topology).

## Trigger

Trigger 4 (auto-fire): the plan contains a one-way-door decision — vendor introduction (Redis cluster) and a production data path change.

## B0 — Cynefin

Complicated. Review emphasises dependencies, reversibility, and operability per the skill's guidance for this domain.

## B1 — Problem framing

**Verdict: SUSTAINED.**

The plan opens with a solution ("introduce Redis as a caching layer") rather than a problem. There is no statement of:

- Which user or business outcome is being moved (page load time, checkout abandonment, infrastructure cost, Postgres CPU saturation, P95 catalog-read latency).
- The current measured baseline (e.g. "catalog reads currently P95 = 320ms; target P95 = 80ms").
- Why caching, specifically, is the right intervention vs. alternatives (Postgres read replicas, query optimisation, materialised views, CDN edge caching, application-tier in-memory cache, denormalisation).

This is textbook solutionism — a Redis-shaped solution chosen before the problem is named. Universal Principle 2 (design starts with the problem, not the stack). Until the plan is rewritten with a problem statement and a measurable target, the rest of the plan cannot be evaluated on its merits, because we do not know what "success" looks like.

**Falsifying condition:** plan owner produces a problem statement with (a) named affected user/business metric, (b) current baseline number, (c) target number, (d) why catching reads (rather than another intervention) is the chosen lever.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| Cache invalidation on writes — "writes" undefined (which write paths? admin tools, batch jobs, replication, ETL, third-party syncs?) | SUSTAINED | Plan enumerates every write path that touches the catalog and states invalidation handling for each |
| "Thin client" — undefined surface (read-through? cache-aside? write-through? circuit breaker? timeout policy? serialization format?) | SUSTAINED | Plan specifies the client's API contract, failure mode, timeout, and serialization choice with rationale |
| Redis cluster topology (size, replicas, sharding, failover, persistence policy, eviction policy, multi-AZ) | SUSTAINED | Plan names cluster size, replication factor, eviction policy, persistence config, and AZ topology |
| Cache stampede / thundering-herd protection (cold start, key expiry storms, hot keys) — out-of-scope-but-touched | SUSTAINED | Plan names mitigations (singleflight, request coalescing, jittered TTL, locks) or explicitly accepts the risk with rationale |
| Cross-region / cross-environment behaviour (staging, dev, regional failover) | PARTIAL | Plan states which environments get Redis and how dev/test interact with it |
| Negative caching (404 misses on catalog lookups), poison-pill caching of erroneous data | SUSTAINED | Plan names policy for caching not-found and policy for cache poisoning recovery |

Five SUSTAINED on a vendor-introducing plan is consistent with the plan being a one-line solution sketch, not a design.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| Catalog-read latency is the actual bottleneck (and Postgres is the cause) | 0.1 — no data cited | Pull last 30d of Postgres slow-query log + APM P95/P99 for catalog endpoints; identify whether reads are the dominant cost | SUSTAINED |
| Cache invalidation can be made correct enough that stale catalog data is acceptable | 0.1 — assumed, not analysed | Enumerate write paths; for each, state acceptable staleness window and how it will be enforced. Owner: catalog domain owner sign-off | SUSTAINED |
| Redis is the right cache (vs. Postgres read replicas, application-tier cache, CDN, materialised views) | 0.1 — solution-first choice | Spike: instrument current catalog reads; produce one-page comparison of read-replica vs Redis vs CDN with cost, latency, complexity, reversibility | SUSTAINED |
| Operating a Redis cluster is within the team's existing competence and on-call coverage | 0.1 | Confirm with platform/SRE owner: is Redis already operated here? If not, who carries the pager? What's the on-call playbook? | SUSTAINED |
| Read traffic volume justifies cluster (not single instance) | 0.1 | Pull current QPS for catalog reads; size against documented Redis single-instance throughput before committing to "cluster" | SUSTAINED |

All five assumptions sit at Confidence 0.1 (opinion / assumption). Skill rule: untested assumptions with Confidence < 5 block APPROVE.

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Platform/SRE team to provision and operate Redis cluster | Not named in plan | Not named | SUSTAINED |
| Security/InfoSec review for new data-in-cache surface (PII in product catalog? auth tokens? pricing tiers per customer?) | Not named | Not named | SUSTAINED |
| Catalog domain owner sign-off on staleness tolerance and invalidation correctness | Not named | Not named | SUSTAINED |
| Observability team for new metrics, dashboards, alerts (cache hit rate, eviction rate, latency, memory pressure) | Not named | Not named | PARTIAL |
| Cost-of-ownership owner — who pays for Redis infrastructure ongoing? | Not named | Not named | PARTIAL |

Universal Rule B7: unconfirmed cross-team dependencies are the single most common cause of missed commitments. Five dependencies, zero confirmed.

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Introduce Redis as a stack component (new vendor, new operational surface, new language of failures) | No alternatives named | No ADR cited or committed | SUSTAINED |
| Cache-invalidation contract baked into write paths across the catalog domain | No alternatives | No ADR | SUSTAINED |
| Thin-client API surface — once code is written against it, the API is sticky | No alternatives | No ADR | SUSTAINED |

Three one-way doors, zero ADRs, zero recorded alternatives. Universal Principle 3 (architecture = expensive-to-change decisions; minimise that set) and Rule B3 (blast radius and reversibility cost named).

Reversibility cost of Redis introduction is not "low": once cache-aside or read-through is wired through hot paths and the team builds operational muscle around Redis, ripping it out requires re-baselining read latency, retraining on-call, removing client code, and decommissioning infrastructure. This is a one-way door.

## B6 — Operability + success metrics

- **Metrics**: absent. No mention of cache hit rate, eviction rate, miss latency, Redis memory pressure, connection pool saturation, key cardinality.
- **Alerts**: absent.
- **Rollback path**: absent. Plan does not name how to disable the cache layer (feature flag? per-route flag? kill switch?) or what happens to in-flight requests when Redis is unhealthy.
- **Runbook**: absent. No on-call guidance for: Redis primary failover, memory exhaustion, partial cluster outage, cache poisoning, hot-key contention.
- **Capacity headroom**: absent. No sizing rationale.
- **User-visible outcome metric**: **absent — and this is the hinge.** No outcome metric is named. The plan does not say "after launch we will observe X moving by Y%." Without an outcome metric, the plan cannot satisfy Universal Principle 1 (shipped is not done; observed is done) or Product Principle 1 (outcomes, not outputs).

**Verdict: SUSTAINED on both halves.** This is an Operability section that does not exist.

**Falsifying condition:** plan adds (a) a named user-visible outcome metric with target and measurement window, (b) the operability sub-list above with named owners.

## B7 — Sequencing + capacity

Critical path is not surfaced. Three pieces of work are listed in parallel ("add cluster, write client, add invalidation") with no statement of which blocks which, no appetite cap, no FTE statement. An unsequenced multi-component plan is a hope, not a plan. SUSTAINED.

**Falsifying condition:** plan names the sequence (typically: spike + measurement → ADR → cluster provisioning → client + non-prod validation → progressive rollout per route, behind flag → measurement of outcome metric → decision to expand or roll back), with a fixed appetite for each phase.

## B8 — Pre-mortem

Assume the plan shipped and failed within its appetite. Top 3 failure modes by likelihood:

1. **Cache invalidation correctness defect leaks stale catalog data to customers** (pricing, availability, SKU-level attributes). Customers see the wrong price; trust and revenue impact. The "thin client + invalidation on writes" framing hides the hard problem: write paths that bypass the client (admin tools, ETL, replication, third-party syncs) silently produce stale entries with no detection.
   - **Kill-switch:** route-level feature flag to disable cache reads instantly; staleness canary that compares cache-served values against Postgres ground truth on a sampled basis and alerts above a threshold.
2. **Redis was the wrong intervention — actual bottleneck was elsewhere** (a missing Postgres index, an N+1 query, a CDN gap). Team ships Redis, hit-rate looks fine, but the user-visible metric does not move because the latency was never in the read path the cache sits in front of.
   - **Kill-switch:** measurement-first phase produces the baseline and identifies the dominant cost component before any Redis work begins; if measurement shows Postgres reads are not the bottleneck, the plan is killed before cluster provisioning.
3. **Operational burden exceeded forecast.** Redis cluster failover, memory pressure incidents, hot-key contention, and connection-pool exhaustion become recurring on-call pages. The team's operational capacity is consumed managing the cache layer rather than shipping product work.
   - (Top-2 kill-switches as above; this one is monitored via on-call burden review at the end of the appetite.)

## Recommendation

**REVISE** — plan is solution-first, has zero stated outcome metric, zero recorded alternatives, zero confirmed dependencies, and three undocumented one-way doors. The defect is not in the choice of Redis; the defect is that the choice was made before the problem was named and measured.

### Conditions to clear before re-review

1. **Problem statement first.** Rewrite the plan opening as: "For [customer segment], catalog read [outcome metric] is currently [baseline]. Target: [number]. Caching is the proposed lever because [evidence]." Until this exists, no further review is meaningful. (B1)
2. **Measurement spike before any build.** Time-boxed (≤3 days) instrumentation of current catalog reads — APM P50/P95/P99, Postgres slow-query log, hit-rate-if-cached estimate. Output: a one-pager with the dominant-cost finding. This validates B3 assumption #1 before committing engineering time. (B3, B7)
3. **Alternatives ADR.** One-page ADR comparing Redis vs Postgres read replicas vs application-tier cache vs CDN vs materialised views, with reversibility and total cost of ownership for each. (B5)
4. **Operability section.** Named metrics, named alerts, named rollback (per-route feature flag), named on-call owner, named runbook outline, sizing rationale. (B6)
5. **Dependencies confirmed in writing.** Platform/SRE owner for cluster operation, Security review owner, catalog domain owner for staleness tolerance. (B4)
6. **Cache-correctness design.** Enumerate every write path that touches the catalog; state invalidation handling for each; name the staleness canary that will detect failures. (B2, B8 #1)
7. **User-visible outcome metric named, with target and measurement window.** This is the definition-of-done for the work. (B6, Product P1)

When conditions 1–4 are addressed, run plan-review again at Full tier. The plan as currently stated cannot be approved.
