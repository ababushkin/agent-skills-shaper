# Plan review: redis-cache-product-catalog

## Plan reference

Pasted excerpt (no path supplied):

> "Review this plan: introduce Redis as a caching layer in front of Postgres for product catalog reads. We'll add a Redis cluster, write a thin client, add cache-invalidation on writes. Approve?"

## Inputs

- **Appetite**: Not stated. Plan declares no time-box. Inferred floor from scope (stand up Redis cluster + client + invalidation) ≥ 2 weeks; treated as >1 week for tier selection.
- **Cynefin domain**: Complicated. Caching is a knowable problem-space with well-understood expert practice (TTL, stampede, invalidation, consistency). The defects appear in dependency and operability detail, not in emergent dynamics.
- **Tier**: **Full** — selected because the plan introduces a one-way-door decision (new vendor / new datastore in production: Redis cluster). Auto-select rule fires on "≥1 one-way-door decision" regardless of appetite. Plan also touches production data path (catalog reads), reinforcing Full.

## B1 — Problem framing

**Verdict: SUSTAINED.**

The plan opens with a solution ("introduce Redis as a caching layer"), not a problem. There is no statement of:

- Who the affected user is (end-customer? internal service consumer?)
- What outcome is degraded today (read latency? Postgres load? cost? throughput ceiling?)
- A measurable target ("p95 catalog read < 50ms," "halve Postgres read QPS," "support 5× catalog traffic without scale-up")

Per Universal P2, design starts with the problem, not the stack. The plan as written is a stack choice in search of a problem. Until the problem and target are written down, any subsequent verdict on whether Redis is the right answer is unfounded — the alternatives (read replicas, materialised views, Postgres `pg_prewarm`/buffer tuning, CDN at the edge, in-process LRU, denormalised read model) cannot be compared without a target.

**Falsifying condition** (what would prove this verdict wrong): the plan contains, or is amended to contain, an explicit problem statement of the form "For [segment], [outcome] is currently [number]; we want it to be [number] by [date], because [business reason]." Absent that text, this verdict stands.

## B2 — Scope clarity

The plan declares scope of three items: Redis cluster, thin client, cache-invalidation on writes. Three undeclared touches and three vague in-scope items follow.

| Item | Verdict | Falsifying condition |
|---|---|---|
| Write path (every catalog writer) must be modified to invalidate cache — touches every service or job that writes catalog rows, not just the read path | SUSTAINED | Plan enumerates every write entry-point (services, batch jobs, admin UI, ETL, replication-driven writes) and confirms each is in scope and owned. |
| Cache-key schema is a new public-ish contract between every reader and writer; effectively a schema migration without an ADR | SUSTAINED | Plan documents the cache-key schema, evolution rules (versioning prefix), and ADR-pairs the decision. |
| Operational surface: Redis cluster needs deploy pipeline, secrets, network policy, backup-or-don't decision, version pinning, on-call rotation, capacity model | SUSTAINED | Plan names each of these and identifies the platform team and owner for each. |
| "Thin client" — undefined. Resilience behaviour (timeout, fallback to Postgres on Redis miss/error, circuit breaker, retry policy) is not specified | SUSTAINED | Plan specifies failure semantics: on Redis unavailability, behaviour is X (e.g., transparent fallback to Postgres with bounded latency budget) and is verified by chaos test. |
| "Cache-invalidation on writes" — invalidation strategy is undefined: write-through, write-behind, TTL-only, key-deletion, versioned keys? Stale-window tolerance is not stated | SUSTAINED | Plan picks one strategy with named consistency contract (e.g., "reads are eventually consistent within 2s of write; that bound is monitored"). |
| "Product catalog reads" — which read paths? List endpoint, detail endpoint, search, faceted browse, internal admin, partner API? Each has different cardinality, hit-rate, and invalidation cost | PARTIAL | Plan enumerates the specific read paths in scope and names hit-rate assumptions per path. |

Six SUSTAINED-or-PARTIAL items on a six-row scan is consistent with B2's expectation that clean plans are rare. The scope statement is doing the work of three sentences for what is in fact a multi-system change.

## B3 — Assumptions + evidence quality

The three riskiest implicit assumptions in the plan, each with Gilad-scale confidence and the 5-minute test that would raise it.

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| Postgres is the bottleneck — i.e., catalog read latency or load is dominated by DB work that a cache would actually relieve | 0.1 (assertion only — no profiling data cited) | Pull the last 7 days of p50/p95/p99 catalog read latency from APM and decompose into DB time vs. app time vs. network. If DB time is <30% of total, the cache will not move the metric. | SUSTAINED |
| Catalog read traffic has a hit-rate profile that justifies a cache (high read:write ratio, high key concentration, tolerable staleness) | 0.1 (assumed by analogy to "product catalogs are cacheable") | Sample 1 hour of catalog read keys from production logs; compute key cardinality and top-N concentration. If top 1% of keys is <50% of traffic, ROI is marginal. | SUSTAINED |
| The organisation can operate Redis at production quality — on-call coverage, version upgrades, failover testing, capacity planning, observability parity with Postgres | 0.1 (no platform-team confirmation cited) | Named owner from the platform / SRE team signs off on operability ownership before the cluster is provisioned. | SUSTAINED |

All three are at Confidence 0.1 (opinion / assertion). Per B3, untested assumptions with Confidence < 5 block APPROVE. Each has a 5-minute or 1-hour test that would raise confidence cheaply — there is no excuse for committing build effort before they are run.

## B4 — Dependencies (Full)

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Platform / SRE — Redis cluster provisioning, network, secrets, backups, on-call rotation | No | No | SUSTAINED |
| Every team that writes to the product catalog — must adopt the invalidation contract | No | No | SUSTAINED |
| Observability team — metrics, dashboards, alerts, log pipelines for the new component | No | No | SUSTAINED |
| Security — vendor / new-datastore review, threat model, secrets handling, encryption-in-transit/rest posture | No | No | SUSTAINED |
| Finance / procurement — Redis cluster cost (managed vs. self-hosted), budget approval | Not addressed | Not addressed | SUSTAINED |

Per Universal Rule B7, unconfirmed cross-team dependencies are the single most common cause of missed commitments. The plan names zero owners. Five SUSTAINED dependency verdicts on a single plan is a structural signal — this is platform work disguised as a feature.

## B5 — Reversibility + ADR pairing (Full)

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Introducing a new datastore vendor (Redis) into the production runtime — adds an operational surface, a failure mode, a hiring/skills cost, a budget line | No alternatives listed | No ADR | SUSTAINED |
| Cache-key schema as cross-service contract — once N services adopt key format X, changing it is an N-way migration | Not addressed | No ADR | SUSTAINED |
| Invalidation strategy choice (TTL vs. key-delete vs. versioned-keys vs. write-through) — locks the consistency contract every reader and writer relies on | Not addressed | No ADR | SUSTAINED |

Three one-way doors, none paired with an ADR, none accompanied by an alternatives section. Per Universal P3 and Rule B3, expensive-to-reverse decisions require deliberation proportional to reversal cost; introducing a new datastore is at the high end of that cost. Per Universal P10 (boring tech / innovation tokens) and the universal Rule B4, novel infrastructure requires written justification: which problem does Redis uniquely solve that the existing stack cannot, what is the total cost of ownership, which innovation token is being spent. None of this is in the plan.

Plausible alternatives that the plan must consider in writing before this verdict is OVERTURNED: Postgres read replicas, a materialised view + refresh job, application-layer in-process cache (LRU/TTL), HTTP/CDN cache at the edge, denormalised read model in the existing DB, query-level optimisation (index review, plan analysis).

## B6 — Operability + success metrics (Full)

- **Metrics**: absent. Plan names no SLI for the cache (hit-rate, p95 latency, error rate, eviction rate) and no SLI for the read path it is intended to improve.
- **Alerts**: absent. No threshold for Redis unavailability, no alert for hit-rate collapse, no alert for stale-read escalation.
- **Rollback path**: absent. Plan does not describe how to disable the cache (feature flag? environment switch? client-side bypass?) and does not specify the latency/load posture once disabled.
- **Runbook**: absent. No 3am on-call procedure for Redis-down, hit-rate-zero, or invalidation-storm.
- **Capacity headroom**: absent. No memory sizing model, no key-cardinality estimate, no eviction policy decision.
- **User-visible outcome metric**: absent. No statement of "catalog read p95 will move from X to Y" or "catalog-related conversion / cart-abandon will move by Z." Per Product P1 and Universal P1, "shipped is not done; observed is done" — without an outcome metric, the plan has no completion criterion beyond deployment.

Per Universal Rule A6, absence on either operability or success-metrics blocks APPROVE. Both halves are absent. Verdict: SUSTAINED.

## B7 — Sequencing + capacity (Full)

Critical path is not surfaced. Implied ordering — provision cluster → ship client → modify writers — is plausible but undocumented; in particular, the writer-side invalidation work is the longest pole and depends on every writing team's roadmap, not the catalog team's.

Appetite is not stated — see Inputs. An undeclared appetite is not an appetite; it is an open-ended commitment, which is the failure mode Shape Up exists to prevent (Universal P8 / Rule C5 / Rule B1 in the engineering principles, mirroring Product Rule C1).

FTE is not declared. Multi-team coordination across at least three teams (catalog, platform, observability) plus N writer-owning teams is not consistent with the plan's framing as three small bullets.

Verdict: SUSTAINED — fix appetite, surface the critical path, and confirm FTE before approval.

## B8 — Pre-mortem (Full)

Adopting prospective hindsight: assume the plan shipped, ran for the duration of its (unstated) appetite, and failed. Top three reasons ranked by likelihood.

1. **Cache hit-rate was lower than assumed; latency did not move.** The "Postgres is the bottleneck" assumption was never tested. Catalog reads turned out to be dominated by application-layer work (serialization, N+1 queries, fanout to other services), not DB time. Cache went live, hit-rate stabilised at a respectable number, but end-to-end p95 moved by <5%. The team shipped the feature; the outcome did not move. (Direct Universal P1 / Product Rule D4 failure mode.)

   **Kill-switch condition**: before any client integration, an offline analysis shows DB-time is <30% of total catalog-read p95, OR after the first 1% canary the observed p95 reduction is <half of the projected target. Either condition triggers stop-and-reassess.

2. **Invalidation bugs caused stale reads in production; trust in the catalog data degraded.** A writer team missed the invalidation contract on a write path (batch ETL, replication-driven write, or admin UI), causing customer-visible stale data — wrong price, wrong availability — for hours before being caught. Recovery required cache flush, which spiked Postgres load and cascaded into a partial outage.

   **Kill-switch condition**: a staleness SLI (cache-key age vs. last-write timestamp on a sampled subset) is in place before launch, with an alert at a defined staleness bound. If the staleness SLI cannot be defined or instrumented before launch, the plan does not ship.

3. **Operational burden landed on a team that didn't sign up for it.** Platform / SRE was not consulted at plan time; the catalog team stood up the Redis cluster informally; six months in, a Redis incident at 3am had no clear owner, no runbook, and resolution took 4× longer than a comparable Postgres incident.

   (No kill-switch required at the Full tier for the third reason — but the dependency confirmation in B4 already covers this.)

## Recommendation

**REVISE** — strong tendency toward **KILL-as-currently-framed**. Approval is blocked by SUSTAINED verdicts in B1, B2, B3, B4, B5, B6, and B7. The plan as written is a stack choice without a problem statement; until the problem and target are written down, the question "is Redis the right answer?" is unanswerable and approving the plan would be approving a decision the plan does not actually contain.

### Conditions

The plan must be amended to satisfy each of the following before re-review:

1. **Problem statement (B1)**: who, what outcome, current number, target number, business reason. Until this is written, the alternatives in B5 cannot be compared on merit.
2. **Tested assumptions (B3)**: profile catalog read latency to confirm DB-time dominance; sample read-key distribution to confirm cacheable hit-rate; confirm operational ownership with platform / SRE. All three are <1 hour of work and gate the rest of the plan.
3. **Alternatives + ADR (B5)**: written comparison of at least Postgres read-replica, materialised view, application-layer cache, and edge/CDN cache against the chosen approach. ADR committed to be authored in the same PR as the implementation.
4. **Scope expansion (B2)**: enumerate every write path that must adopt the invalidation contract; specify the resilience behaviour of the "thin client"; pick an invalidation strategy and state its consistency contract; enumerate the read paths in scope.
5. **Dependencies (B4)**: named owner sign-off from platform / SRE, observability, security, and finance. Each writer-owning team confirms capacity within the appetite.
6. **Operability + outcome metric (B6)**: SLIs, alerts, rollback (feature-flag bypass), runbook, capacity model, AND a user-visible outcome metric with a target value and observation window.
7. **Appetite (B7)**: a fixed time-box for the work, not a range. If the plan cannot be shaped to a fixed appetite, that is itself a kill signal.

If conditions 1 and 2 are run and the evidence shows Postgres is not the bottleneck or hit-rate is unfavourable, the recommendation escalates to **KILL** — not because Redis is a bad technology but because the plan would be solving a problem the data does not support.
