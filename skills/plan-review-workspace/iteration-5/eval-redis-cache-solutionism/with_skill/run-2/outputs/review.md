# Plan review: redis-cache-product-catalog

## Plan reference

> "Introduce Redis as a caching layer in front of Postgres for product catalog reads. We'll add a Redis cluster, write a thin client, add cache-invalidation on writes. Approve?"

## Inputs

- **Appetite**: Unstated — extracted implication is >1 week (new cluster provisioning, client authoring, invalidation logic, testing, rollout)
- **Cynefin domain**: Complicated — cache-aside is a known pattern, but cache invalidation is a famously hard sub-problem; cause-effect is knowable with expertise, not obvious
- **Tier**: Full — selected because the plan contains ≥1 one-way-door decision (adding a Redis cluster as a production infrastructure dependency; changing the product catalog read path)

**Fast-track gate**: Did not fire. Precondition 1 failed (not KTLO — this is new infrastructure). Precondition 2 failed (not fully reversible — a Redis cluster, client code, and invalidation logic scattered across write paths cannot be reverted in one commit without coordinated rollback).

---

## B1 — Problem framing

**SUSTAINED.**

The plan opens with a solution: "introduce Redis as a caching layer." There is no stated problem. No user or business outcome appears. The plan does not say:

- What latency is currently observed on product catalog reads
- Whether latency is causing a measurable user or business impact (abandonment, SLA breach, support volume, revenue effect)
- What the target latency is after the change
- Why Postgres is the bottleneck rather than the application layer, network, or an absent query index

A plan that begins with a stack choice rather than a problem statement has pre-committed to a solution before the problem is understood. This is the most common vector for building the wrong thing correctly.

**Falsifying condition**: The plan is shown to contain a measurable outcome statement — e.g. "p95 product catalog read latency currently 850ms; SLA requires 200ms; Postgres EXPLAIN shows sequential scan on catalog table; index addition has been ruled out because X" — with a target metric that will be observed post-launch. If that statement exists and was simply omitted from the summary, the verdict is OVERTURNED. If it does not exist, the verdict stands.

---

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| Cache stampede / thundering-herd on cold start or TTL expiry | SUSTAINED | Plan explicitly names and mitigates cache stampede (probabilistic early expiry, request coalescing, or warm-up procedure) |
| Multi-region or multi-instance invalidation coherence | SUSTAINED | Plan either (a) states the deployment is single-region single-instance so this does not apply, or (b) names the invalidation propagation mechanism across nodes |
| Read-your-own-writes consistency after invalidation | SUSTAINED | Plan names the consistency model it accepts (eventual vs. read-after-write) and names any user-visible flows where stale reads would be harmful |
| "Thin client" scope is undefined | SUSTAINED | Plan defines what the thin client does and explicitly does not do — connection pooling, serialisation format, error fallback behaviour, timeout budget |
| Cache key schema | PARTIAL | Plan names the key schema and versioning strategy, or explicitly defers with a named owner and date |
| What "writes" trigger invalidation | PARTIAL | Plan enumerates all write paths that touch catalog data (direct DB writes, bulk imports, price updates, admin tools, data migrations) — not just "writes" in the abstract |

**Note on zero-hit concern**: Six items surfaced. B2 is not lenient.

---

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| Postgres is the bottleneck — removing it from the read path will meaningfully improve latency | 0.1 — pure assertion; no profiling evidence in the plan | Run `EXPLAIN ANALYZE` on the top-5 product catalog queries; pull p95/p99 from existing APM or add a one-day sampling run | SUSTAINED — blocks APPROVE |
| Cache invalidation on writes is tractable — all write paths are known and enumerable | 0.1 — assertion; no audit of write paths | Audit all write entrypoints touching catalog tables (app code, admin tools, migrations, batch jobs, direct DB access) and count them | SUSTAINED — blocks APPROVE |
| Redis cluster adds acceptable operational overhead for this team | 0.1 — assumption; no stated ops capacity or prior Redis experience | Owner names who will operate the cluster (paging, patching, failover), or a managed service (ElastiCache, Upstash) is explicitly chosen | SUSTAINED — blocks APPROVE |

All three critical assumptions sit at Confidence 0.1 (opinion/assertion). None have a named validation path in the plan. Per B3 rules, untested assumptions with Confidence < 5 block APPROVE.

---

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Infrastructure / platform team (Redis cluster provisioning, networking, security group rules) | Not named | Not confirmed | SUSTAINED |
| Security review (Redis without TLS/auth is a common misconfiguration; new network component needs review) | Not named | Not confirmed | SUSTAINED |
| On-call / SRE (who pages for Redis failures; runbook existence) | Not named | Not confirmed | SUSTAINED |
| All teams / services that write to catalog tables (must coordinate on invalidation) | Not named | Not confirmed | SUSTAINED |

Four unconfirmed dependencies. Universal Rule B7 applies: cross-team dependencies are surfaced and de-risked before commitment. None of these are confirmed in the plan.

---

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Adding Redis as a production infrastructure dependency (all services now require Redis availability to serve catalog reads) | No alternatives named | No ADR exists or committed | SUSTAINED |
| Cache-aside invalidation model (alternatives: write-through, read-through, CDN-level caching, query result caching at DB layer, materialised views, index optimisation) | No alternatives named | No ADR exists or committed | SUSTAINED |
| "Thin client" as bespoke code (alternatives: use existing Redis client library directly; use an HTTP proxy cache; use Postgres connection pooling + read replica) | Not named | Not committed | SUSTAINED |

The plan names no alternatives. It is a solution statement, not a decision record. Per B5 rules, an undocumented one-way door must either record alternatives or be sent back. Three one-way doors with zero alternatives documented.

**Additional note — quick wins not considered**: The plan skips the obvious lower-cost alternatives that should be eliminated before adding a new infrastructure component: adding missing Postgres indexes, adding a read replica, enabling Postgres query caching, using a CDN for public catalog data, or enabling HTTP-level caching (ETags, Cache-Control). These are reversible and require no new infrastructure. The plan provides no evidence they were evaluated.

---

## B6 — Operability + success metrics

- **Metrics**: Absent. No cache hit rate, cache miss rate, Redis memory usage, eviction rate, or latency delta targets named.
- **Alerts**: Absent. No alerts for Redis unavailability, high eviction rate, memory pressure, or connection pool exhaustion.
- **Rollback path**: Absent. What happens when the Redis cluster fails? Does the application fall back to Postgres reads or does it error? The plan does not state a fallback strategy. (This is the most operationally dangerous gap — a Redis outage could take down product catalog reads entirely if the fallback is not designed.)
- **Runbook**: Absent.
- **Capacity headroom**: Absent. No estimate of cache size needed, memory provisioning, or eviction policy named.
- **User-visible outcome metric**: Absent. The plan contains no measurable user or business outcome — not latency target, not conversion improvement, not SLA compliance target.

All six operability sub-items are absent. This is a complete operability gap. Per B6 rules, absence on either half blocks APPROVE.

---

## B7 — Sequencing + capacity

- **Critical path**: Not surfaced. The plan lists three work items (Redis cluster, thin client, cache-invalidation) without naming dependencies between them or which is the blocking item.
- **Appetite**: Not stated. "We'll add a Redis cluster, write a thin client, add cache-invalidation on writes" is a scope statement, not an appetite. There is no time cap.
- **FTE consistency**: Cannot be assessed — no appetite, no team size stated.

The Shape Up rule applies: an appetite of "however long it takes" is not an appetite; it is an open-ended commitment. The plan cannot be approved without a fixed time cap.

---

## B8 — Pre-mortem

The plan shipped and failed within its appetite. Top three reasons ranked by likelihood:

**1. Cache invalidation is incomplete — stale catalog data serves to users (highest likelihood)**

The plan says "add cache-invalidation on writes" without enumerating all write paths. In practice: bulk import jobs, admin price-update tools, data migrations, and direct-DB writes from other services will all miss the invalidation hook. Users see stale prices, unavailable products shown as available, or sold-out items still purchasable. This surfaces in production 2–4 weeks post-launch when a batch job runs and the cache is not purged.

**Kill-switch condition**: Before launch, run a full audit of all write paths touching catalog tables. If any path cannot have invalidation added before launch, the launch is blocked.

**2. Redis becomes a single point of failure — catalog reads error during Redis downtime (second highest)**

If the application does not implement graceful degradation (fall back to Postgres on Redis miss/error), a Redis cluster failure or network partition takes product catalog reads down entirely. The plan does not mention a fallback path.

**Kill-switch condition**: Chaos test before launch — simulate Redis unavailability and verify product catalog reads degrade gracefully (fall back to Postgres, not error). If the chaos test fails, the launch is blocked.

**3. The performance problem was not Postgres — cache adds latency instead of removing it**

Without profiling evidence that Postgres is the bottleneck, adding a Redis round-trip (network + serialisation) to every read may increase p95 latency rather than decrease it — especially on a well-indexed table where Postgres already caches hot pages in shared_buffers. The "performance improvement" is real only if the assumption in B3 is true.

---

## Recommendation

**KILL**

The plan's core premise fails B1: no problem statement exists, so there is no measurable target that would tell us whether the change succeeded. Every downstream bucket (B3, B5, B6) amplifies this: the assumptions supporting the solution have Confidence 0.1, no alternatives were considered, and the operability plan is entirely absent. The plan is a solution in search of a problem.

This is not a REVISE because the defects are not cosmetic — the plan would need to be substantially rewritten as a problem statement with profiling evidence, alternatives analysis, operability plan, and appetite before it could be reviewed as a plan rather than as a proposal.

### Conditions for a future APPROVE

If the team wishes to proceed, the replacement plan must satisfy all of the following before approval:

1. **B1**: State the measured current latency (p95), identify the bottleneck via profiling (not assumption), state the target latency, and tie the target to a user or business outcome.
2. **B3**: Provide profiling evidence that Postgres is the bottleneck. Document an evaluation of lower-cost alternatives (index tuning, read replica, CDN) with the reason each was ruled out.
3. **B3**: Audit all write paths touching catalog tables and name them explicitly in the plan.
4. **B5**: Document the alternatives considered (write-through vs cache-aside vs CDN vs materialised views) and produce an ADR naming the chosen approach and reversal cost.
5. **B6**: Name the fallback behaviour on Redis failure (circuit breaker to Postgres or explicit error), the cache hit rate target, eviction policy, memory provisioning, and success metric.
6. **B4**: Confirm infrastructure, security, and on-call owners in writing before committing the build slot.
7. **B7**: State a fixed time appetite (cap, not range) and name the critical path.
