# Plan review: redis-cache-product-catalog

## Plan reference

Pasted excerpt (no file path supplied):

> "Review this plan: introduce Redis as a caching layer in front of Postgres for product catalog reads. We'll add a Redis cluster, write a thin client, add cache-invalidation on writes. Approve?"

## Inputs

- **Appetite**: Not stated. Plan does not declare a time cap. Treated as `unknown — owner must supply`. For tier-selection purposes, the plan is treated as exceeding 1 week because (a) "add a Redis cluster" is multi-day infrastructure work, (b) cache-invalidation on writes is non-trivial, and (c) no upper bound was named.
- **Cynefin domain**: **Complicated**. Caching in front of a relational store is a well-understood class of problem with known failure modes (stale reads, thundering herd, cache stampede, invalidation races). It is not novel/emergent (Complex), but it is not a simple checklist either (Clear). Expert-known, expert-knowable.
- **Tier**: **Full** — auto-selected. Selecting attributes that fire:
  - One-way-door decisions present (introducing a new datastore tier, vendor/runtime lock-in to Redis cluster operations, change to read path of catalog).
  - Touches production data path (product catalog reads).
  - No appetite supplied — defaulted to >1 week per tier-selection rule.

## Trigger check

Trigger 1 fires: an LLM-style plan has been produced and the owner is asking "Approve?" Auto-fire trigger 4 also fires: the plan contains one-way-door decisions (new datastore tier, read-path topology change). Proceeding past gate.

---

## B0 — Cynefin classification

Complicated. Implication for review: emphasise dependencies, named failure modes, and reversibility. Do not accept "we'll figure invalidation out in code" — the failure modes here are catalogued in the literature and the plan should engage with them by name.

## B1 — Problem framing [GATE]

The plan opens with a **solution** ("introduce Redis as a caching layer"), not a problem. There is no statement of:

- What user-visible or business outcome is failing today
- What the current p50/p95/p99 read latency on product catalog is
- What the target latency, throughput, or cost outcome is
- Whether the bottleneck has been measured or assumed
- Whether Postgres has been tuned (indexes, connection pooling, read replicas, materialised views, `pg_stat_statements` analysis) before reaching for a second datastore

**Verdict: SUSTAINED.** Solution-first plan; Universal P2 violation; Agentic P3 violation.

**Falsifying condition:** The plan would be overturned on this point if the owner produces (a) a measured baseline for product-catalog read latency and throughput, (b) a target metric with a number, and (c) evidence that lower-cost interventions inside Postgres have been considered and rejected with reasons. Absent these three, B1 stays SUSTAINED.

This single SUSTAINED verdict is sufficient on its own to block APPROVE — the rest of the review continues for completeness, but the recommendation is determined here.

## B2 — Scope clarity [GATE]

The plan declares three things in scope: Redis cluster, thin client, cache-invalidation on writes. The plan touches more than that.

| Item | Verdict | Falsifying condition |
|---|---|---|
| **Operational surface area** — runbooks, on-call training for Redis, alerting, capacity planning, failover testing. Not declared. | SUSTAINED | Owner produces an operability section naming SLOs, alerts, runbook owner, and on-call rotation impact. |
| **Deployment topology** — Redis cluster sizing, region/AZ placement, network path, TLS, auth, secret rotation. Not declared. | SUSTAINED | Owner produces a topology doc with sizing rationale, failure-domain placement, and secret-management story. |
| **Cost envelope** — cluster cost, network egress, observability cost. Not declared. | SUSTAINED | Owner produces a monthly cost estimate with headroom, and confirms it fits the cost budget. |
| **"Thin client"** (declared in scope, vague) | PARTIAL | Owner names: connection pooling strategy, timeout/retry policy, circuit-breaker behaviour on Redis outage, serialization format, key schema, TTL policy. Without these, "thin" expands silently. |
| **"Cache-invalidation on writes"** (declared in scope, vague) | SUSTAINED | Owner names: which write paths are covered, ordering guarantee (write-through vs. write-around vs. write-behind), behaviour under partial failure (DB write succeeds, invalidation fails — what then?), and consistency model exposed to readers. "Cache invalidation" without a named strategy is the famous hard problem in a one-line bullet. |
| **Read-path fallback** — what happens when Redis is unavailable | SUSTAINED | Owner names the degradation contract: do reads fall through to Postgres (and can Postgres take that load?), or do they fail? Capacity headroom on Postgres for full-fallback traffic must be confirmed. |

Six items surfaced; five SUSTAINED, one PARTIAL. This is consistent with a plan written at solution-naming depth rather than design depth.

## B3 — Assumptions + evidence quality [GATE]

Implicit assumptions extracted:

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| Postgres read latency is the actual bottleneck for the catalog experience | **0.1 — opinion** | 5-min test: pull `pg_stat_statements` and APM p95 for the catalog read path. If the slow span is not the Postgres query, the entire plan is solving the wrong problem. | SUSTAINED — block APPROVE per B3 rule (Confidence < 5, no validation). |
| Cache hit rate will be high enough to justify the cost (i.e., catalog reads have a hot working set) | **0.1 — opinion** | 5-min test: query log analysis — what % of catalog reads target the top-N products in a 1-hour window? If the working set is wide and uniform, the cache hit rate will be poor and the spend buys little. | SUSTAINED. |
| Cache invalidation can be made correct enough that stale reads are tolerable | **0.5 — anecdote** (industry wisdom that this is hard) | Named owner sign-off required from the team that owns catalog correctness. Stale-read SLO must be named (e.g., "≤30s staleness for price changes" or "strong consistency required for inventory"). | SUSTAINED — needs explicit consistency contract. |
| Redis cluster operability is within the on-call team's existing skill set | **0.1 — opinion** | Named owner: SRE/platform lead. If Redis operations are new to the team, training and runbook cost belong in the appetite. | SUSTAINED. |
| Postgres can carry full read load if Redis fails (or the system can degrade gracefully) | **0.1 — opinion** | 5-min test: current Postgres CPU/IOPS headroom × current cache-miss-equivalent load. If headroom <2x, a Redis outage becomes a catalog outage. | SUSTAINED. |

Top three riskiest: (1) bottleneck assumption, (2) hit-rate assumption, (3) Postgres-fallback-capacity assumption. None has Confidence ≥ 5. **B3 blocks APPROVE.**

## B4 — Dependencies [GATE, Full]

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Platform/SRE — provisions and operates the Redis cluster | Not named | Not confirmed | SUSTAINED |
| Security — review of new datastore tier (auth, TLS, secret rotation, network policy) | Not named | Not confirmed | SUSTAINED |
| Observability — metrics/logs/traces shipped from Redis client and cluster | Not named | Not confirmed | SUSTAINED |
| Catalog write-path team(s) — every writer must adopt the invalidation contract | Not named | Not confirmed | SUSTAINED — the worst silent dependency. If even one writer bypasses the invalidation hook, stale reads become a long-tail correctness bug. |
| FinOps / budget owner — new monthly spend | Not named | Not confirmed | SUSTAINED |

Universal Rule B7: unconfirmed cross-team dependencies are the single most common cause of missed commitments. Five surface here. **B4 blocks APPROVE.**

## B5 — Reversibility + ADR pairing [GATE, Full]

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Introducing a second datastore tier on the read path | No alternatives named | No ADR | SUSTAINED |
| Choice of Redis (vs. Memcached, vs. read-replica + connection pooler, vs. Postgres-internal materialised views, vs. application-level in-process cache, vs. CDN-edge caching for catalog responses) | No alternatives named | No ADR | SUSTAINED |
| Cache-invalidation strategy (write-through / write-around / TTL-only / event-driven via CDC) | Not named — "cache-invalidation on writes" is one bullet | No ADR | SUSTAINED |
| Cluster topology (managed service vs. self-hosted; cluster mode vs. sentinel) | No alternatives named | No ADR | SUSTAINED |

Reversibility cost: introducing a Redis tier is two-way-door at first commit (you can revert), but becomes one-way-door fast — once read latency budgets are set against the cached path, removing Redis means re-tuning Postgres to absorb the load you spent months avoiding. Universal P3 demands this be named explicitly. **B5 blocks APPROVE.** ADR pairing per Agentic P7 is also missing.

## B6 — Operability + success metrics [GATE, Full]

- **Metrics**: not named. Required: cache hit rate, p50/p95/p99 read latency (cached and fallback), Redis CPU/memory/eviction rate, invalidation lag, stale-read rate.
- **Alerts**: not named. Required at minimum: hit-rate floor, eviction-rate ceiling, Redis cluster health, invalidation-failure rate.
- **Rollback path**: not named. Required: feature flag to disable cache reads (fall through to Postgres) without redeploy, and confirmation Postgres can carry the resulting load.
- **Runbook**: not named. Required: cold-start procedure (avoid thundering herd on cluster restart), invalidation backlog drain procedure, partial-cluster-failure procedure.
- **Capacity headroom**: not named (see B3 #5).
- **User-visible outcome metric**: **absent**. The plan does not name what success looks like to a user — e.g., "catalog page p95 TTFB under 200ms for 95% of sessions." Without this, "done" cannot be defined per Universal P1 and Product P1.

**B6 blocks APPROVE.** Universal Rule A6 violated; Product P1 violated.

## B7 — Sequencing + capacity (Full)

- **Critical path**: not surfaced. The plan lists three things in parallel (cluster, client, invalidation) without a sequence. The actual dependency chain is closer to: measure baseline → ADR on alternatives → ADR on invalidation strategy → cluster provisioning → security review → client + invalidation behind feature flag → shadow read → percentage rollout → bake → declare success against outcome metric.
- **Appetite**: not stated — see Inputs. An unstated appetite is not a cap; it is open-ended scope.
- **FTE consistency**: cannot be assessed without an appetite or a named team.

**Verdict: SUSTAINED.** Owner must supply a fixed appetite and a sequence before this plan is reviewable for capacity fit.

## B8 — Pre-mortem (Full: top 3 reasons)

Adopting prospective hindsight: the plan shipped, and within its appetite the project failed. The top three reasons, ranked by likelihood:

1. **Cache invalidation was incomplete and produced visible stale reads on price/inventory.** A writer in another service updated catalog rows directly (or through a path that bypassed the invalidation hook). Customers saw stale prices; trust took a hit; the team spent the next sprint hunting writers and adding a CDC-based invalidator anyway. **Kill-switch condition:** before percentage rollout, run a writer audit — every code path that writes to product catalog tables must be enumerated and either go through the invalidation hook or be ticketed for migration. If the audit cannot enumerate writers exhaustively, do not roll out.

2. **The bottleneck wasn't where we thought it was.** After Redis went live, p95 catalog latency barely moved because the slow span was N+1 ORM calls or template rendering or an external pricing-service call — not the Postgres query. The cache fronts the wrong layer. The cluster spend bought nothing measurable. **Kill-switch condition:** require a measured baseline before provisioning any infrastructure. If APM does not show Postgres catalog reads as the dominant slow span, halt and re-frame.

3. **A Redis cluster incident became a catalog outage.** Failover took longer than expected, or the read path didn't degrade gracefully to Postgres because Postgres didn't have headroom for full traffic. The cache moved from "performance optimization" to "availability dependency" without anyone deciding it should. *(Kill-switch condition not required for #3 per skill rules — top 2 only — but the implied condition is the headroom check from B3 #5.)*

## Recommendation

**REVISE** — the plan opens with a solution rather than a problem (B1), surfaces five SUSTAINED scope expansions (B2), carries five untested low-confidence assumptions (B3), names zero confirmed dependencies (B4), records zero alternatives or ADRs for four one-way doors (B5), declares no operability or outcome metric (B6), and supplies no appetite or sequence (B7). Every gate bucket returned at least one SUSTAINED verdict. The verdict is REVISE rather than KILL because the *underlying* problem (catalog read performance) may well be real and worth solving — but the artefact in front of us is a solution shopping list, not a plan, and approval at this state would be approving the rationalisation pattern the skill exists to prevent.

The Quick-tier reversibility carve-out does **not** apply: tier is Full, B5 itself is SUSTAINED, B6 is SUSTAINED, and the plan touches production read paths.

### Conditions

Before re-review, the owner must:

1. **Rewrite B1 as a problem statement** with measured baseline, target metric, and the alternatives inside Postgres that have been considered and rejected with reasons (per Universal P2; falsifies B1).
2. **Validate or downgrade the top three B3 assumptions** to Confidence ≥ 5 with named evidence: bottleneck location (APM data), working-set hot-rate (query log analysis), Postgres fallback capacity (current headroom × projected miss-equivalent load).
3. **Produce an ADR** that names alternatives to Redis (read replicas + connection pooling, materialised views, application-level cache, CDN edge caching, Memcached) and the reversal cost of the chosen path (per Universal P3, Rule B3; Agentic P7).
4. **Produce an ADR on the invalidation strategy** with explicit consistency contract (max staleness tolerated; behaviour when DB write succeeds and invalidation fails) and an exhaustive writer audit.
5. **Confirm dependency owners in writing** for platform/SRE, security, observability, every catalog-write team, and FinOps (per Universal Rule B7).
6. **Produce an Operability section** naming SLOs, alerts, rollback path (feature flag with confirmed Postgres headroom), runbook owner, and a user-visible outcome metric that will be observed post-launch (per Universal Rule A6; Product P1).
7. **Declare an appetite** as a fixed cap (not a range) and a sequenced critical path that puts measurement and ADRs before infrastructure provisioning.

If conditions 1–2 cannot be satisfied (i.e., there is no measurable read-latency problem, or the bottleneck is elsewhere), the recommendation upgrades to **KILL** — the plan is solving a problem the data does not support.
