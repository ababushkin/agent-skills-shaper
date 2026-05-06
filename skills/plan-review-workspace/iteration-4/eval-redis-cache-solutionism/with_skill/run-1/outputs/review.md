# Plan review: redis-cache-product-catalog

## Plan reference

Pasted plan (verbatim): "Introduce Redis as a caching layer in front of Postgres for product catalog reads. We'll add a Redis cluster, write a thin client, add cache-invalidation on writes. Approve?"

## Inputs

- **Appetite**: NOT STATED. Owner did not declare a time budget. Implied scope (provision a Redis cluster, build a client, design + implement invalidation) is materially > 1 week on any realistic team. Treating as > 1 week for tier selection.
- **Cynefin domain**: Complicated. Caching + invalidation is knowable with expertise but has well-documented emergent failure modes (stale reads, thundering herd, dual-write races). Not Clear (cache invalidation is "one of the two hard things" for a reason); not Complex (the failure space is enumerable).
- **Tier**: Full — selected because (a) the plan introduces a new piece of production infrastructure (Redis cluster) which is an architecture-level one-way door; (b) it touches the read path of the product catalog, which is production data; (c) implied appetite > 1 week. Any one of these triggers Full per the auto-select rules.

## Step 1 — Trigger check

Triggers fired: explicit ("Approve?" + "Review this plan"); auto-fire (architecture choice — new infrastructure component; vendor/topology change — Redis cluster; production data — catalog read path). Proceeding.

## Step 1a — Fast-track gate

Does NOT fire. Failed precondition #1 (not KTLO/maintenance — this is net-new infrastructure) and #2 (not fully reversible — once writers depend on the invalidation path and reads have been re-pointed at the cache, a one-commit revert does not restore prior latency/load characteristics, and any production data drift during the cutover is not undone by the revert). Falling through to normal flow.

## B0 — Cynefin classification

Complicated (see Inputs). Review emphasises dependencies, reversibility, and operability.

## B1 — Problem framing

**Verdict: SUSTAINED.** The plan opens with a solution ("introduce Redis as a caching layer"), not a problem. There is no statement of:

- What is wrong today. Are catalog reads slow? At which percentile? For which user segment? On which endpoints?
- What measurable outcome we expect to move (p95 latency target? DB CPU? cost? page-load LCP for catalog pages?)
- Why caching is the right intervention vs. alternatives (read replicas, query optimisation, materialised views, Postgres-native result caching, CDN/edge caching for catalog responses, application-level memoisation, denormalisation).

This is the textbook solution-first plan that Universal P2 exists to block. The plan must be sent back with a problem statement of the form: "For [users/segment], [observed metric] is [current value], target is [target value], by [date], because [business reason]." Without it, success is undefined and the team will declare victory at "Redis is deployed."

**Falsifying condition (would prove SUSTAINED wrong):** the owner produces an existing, dated problem statement (latency report, DB load graph, cost line item, customer complaint cluster) that names the metric, current value, and target, and that has been used to rule out at least two cheaper alternatives.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| **Out-of-scope touch #1: Write path.** Plan says "cache-invalidation on writes" — every product-catalog writer (admin tool, import jobs, supplier feeds, price updates, inventory sync) now has a new failure mode and a new dependency. This is not declared in scope. | SUSTAINED | Owner names the complete enumerated list of writer call-sites that will be modified, with owners and estimated effort per site. |
| **Out-of-scope touch #2: Deploy + secrets + network topology.** A Redis cluster requires: provisioning (IaC), VPC/subnet placement, security group rules, secret rotation, TLS, backup policy, monitoring stack integration. None declared. | SUSTAINED | Owner provides the IaC change set or an explicit dependency on a platform team that has agreed to do the provisioning within the plan's appetite. |
| **Out-of-scope touch #3: On-call + runbook.** Adding a stateful prod component changes the on-call surface area. The team that gets paged at 3am for a Redis OOM or split-brain is not declared. | SUSTAINED | Plan names the on-call team, the new runbook entries, and the capacity (people-hours/week) absorbed. |
| **In-scope-but-vague #1: "thin client".** "Thin" is undefined. Does it handle: connection pooling, pipelining, retries, circuit-breaking, fallback-to-DB on Redis unavailability, key versioning, TTLs, serialization format/version, observability hooks? Each is a design decision that can silently expand. | SUSTAINED | Plan enumerates which of these the client handles, which it explicitly does not, and what the fallback behaviour is on Redis unreachable. |
| **In-scope-but-vague #2: "cache-invalidation on writes".** The hardest problem in the plan is described in five words. Strategies (write-through, write-around, write-back, TTL-only, event-driven via CDC, dual-write with compensating reconciliation) are not chosen, and each has materially different failure modes and engineering cost. | SUSTAINED | Plan names the chosen invalidation strategy, the consistency guarantee it provides (read-your-writes? eventual? bounded staleness?), and the failure mode when invalidation fails (stale read for how long? alert? auto-recovery?). |
| **In-scope-but-vague #3: "product catalog reads".** Which reads? List, detail, search, faceting, pricing, inventory, related-products, personalised ranking? Each has different cardinality, hit-rate, and invalidation cost. | SUSTAINED | Plan enumerates the specific read endpoints/queries to be cached, with estimated hit rate and key cardinality per endpoint. |

Note: B2 returned six SUSTAINED items on a five-line plan. This is the dominant signal in the review — the plan is roughly 5% of the artefact it needs to be before it can be approved.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| Catalog reads are the bottleneck (not writes, not search, not auth, not network egress, not application CPU). | 0.1 — opinion | Pull last 7 days of APM/DB metrics; identify the top-5 slowest endpoints by p95 × QPS. If catalog reads are not in the top 3, the premise is wrong. | SUSTAINED |
| Redis will materially improve the metric. Implies cache hit rate will be high (>80%?) and Postgres latency is the dominant component of end-to-end response time. | 0.1 — opinion | Run `EXPLAIN ANALYZE` on the top catalog queries and check whether DB time is >50% of end-to-end. Pull current QPS distribution by catalog key to estimate hit rate ceiling. | SUSTAINED |
| Cache-invalidation on writes is achievable with acceptable consistency. Implies: writers are enumerable; all writers can be modified; no out-of-band writes (DB-direct admin scripts, replication from upstream systems, CDC from another service) will bypass invalidation. | 0.1 — opinion | List every system or tool that writes to the catalog tables in the last 90 days (audit log, DB user query, deploy history). If the list contains anything not under the plan's control, the assumption fails. | SUSTAINED |
| The team has Redis operational experience (or the platform team does, and is available). | 0.1 — opinion | Owner names two engineers who have run Redis in prod before, or a platform team with a documented Redis-as-a-service offering. | SUSTAINED |
| Adding Redis is cheaper (TCO: infra + on-call + dev time + future debugging) than the alternatives that were not considered. | 0.1 — opinion | Cost out the cheapest alternative (typically: read replica + query tuning, or HTTP/CDN caching of catalog endpoints) and compare. | SUSTAINED |

All five top assumptions sit at 0.1 (opinion). Per Step 6: untested assumptions with Confidence < 5 block APPROVE.

## B4 — Dependencies

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Platform/SRE team for Redis cluster provisioning, secrets, network, backup, monitoring integration | NO | NO | SUSTAINED |
| Every team that writes to product-catalog tables (likely: catalog mgmt, pricing, inventory, supplier integrations, admin tooling) | NO | NO | SUSTAINED |
| Observability team / on-call rota changes (new alerts, new runbooks, paging policy) | NO | NO | SUSTAINED |
| Security review for new in-cluster service holding (potentially) PII-adjacent data and new credentials | NO | NO | SUSTAINED |
| Finance / cost approval for new infra line item if material | NOT NAMED | NOT NAMED | PARTIAL |

Universal Rule B7: unconfirmed cross-team dependencies are the single most common cause of missed commitments. Five dependencies, zero confirmed.

## B5 — Reversibility + ADR pairing

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Adopting Redis as a stateful prod component (vs. read replica, materialised views, CDN/edge caching, query tuning, app-level memoisation, Postgres logical replication to a denormalised store) | NO | NO | SUSTAINED |
| Choice of cache-invalidation strategy (write-through vs. CDC-driven vs. TTL-only vs. event-bus) — once writers depend on a strategy, switching strategies is a coordinated migration | NO | NO | SUSTAINED |
| Cache key schema and serialization format — once cached data is in production and clients depend on it, key/format changes require dual-writing or full flushes | NO | NO | SUSTAINED |
| Coupling read path to a non-Postgres service — reverts are not one-commit once readers have been migrated and the DB has been right-sized down for cache-hit-adjusted load | NO | NO | SUSTAINED |

Per Universal P3 / Rule B3 and Agentic P7: every item here needs alternatives named and an ADR committed. None present.

## B6 — Operability + success metrics

- **Metrics**: not named. Required at minimum: cache hit rate per endpoint, Redis p99 latency, Redis memory utilisation, eviction rate, key cardinality, invalidation lag (write-to-cache-coherent time), fallback-to-DB rate, end-to-end catalog-read p95.
- **Alerts**: not named. Required: Redis unavailable, hit rate drop >X%, eviction rate spike, invalidation backlog, memory >80%, replication lag (if clustered), elevated stale-read rate.
- **Rollback path**: not named. The plan must specify how to disable cache reads at the flip of a flag (per-endpoint feature flag with default=off during rollout, fallback-to-DB code path tested), and what the DB capacity headroom is to absorb 100% of reads if Redis is taken out.
- **Runbook**: not named. Required entries: "Redis is down", "hit rate is low", "stale reads reported", "memory is full", "invalidation is failing".
- **Capacity headroom**: not named. Has Postgres been sized for the cold-cache and full-cache-miss-storm cases (e.g. after a flush, after a deploy, after a cluster failover)? Cache-induced thundering herd is a documented production failure mode.
- **User-visible outcome metric**: not named. Per Product P1: the plan must name the user-facing metric (e.g. p95 catalog page latency for logged-out users on mobile, or catalog API p99 for the storefront) and the target movement, and commit to observing it post-launch.

**Verdict: SUSTAINED on all six sub-items.** This alone blocks APPROVE under Step 9.

## B7 — Sequencing + capacity

- **Critical path**: not surfaced. Likely critical path is: platform-team provisioning → client library → invalidation strategy decision (ADR) → writer instrumentation (across N teams) → shadow-read validation → progressive rollout per endpoint behind flag. None of this is in the plan.
- **Appetite**: not stated. "Add a Redis cluster, write a thin client, add cache-invalidation on writes" is not an appetite; it is a checklist with no time budget. Per Universal Rule C1 and Singer's Shape Up: appetite is a cap set up-front. Without one, the work will expand to consume all available capacity — exactly the failure mode the rule exists to prevent.
- **FTE consistency**: cannot be assessed without an appetite or a team size.

## B8 — Pre-mortem

Adopting prospective hindsight: assume the plan shipped and failed within its (implied) appetite.

**Top 3 reasons the plan failed, ranked by likelihood:**

1. **Stale reads in production caused a real customer incident.** A writer was missed during invalidation instrumentation (most likely an out-of-band path: a nightly import, a CDC stream from an upstream ERP, a one-off admin script, a replicated table from another service). Customers saw stale prices, stale inventory ("in stock" when sold out), or stale product descriptions. The cost of trust loss exceeded any latency win. *Kill-switch: a continuous shadow-read test in production that reads from cache and from DB in parallel for a sampled fraction of traffic, asserts equality within bounded staleness, and pages on divergence > threshold. Run this from day one of rollout, not after.*

2. **The win didn't materialise because catalog reads were not the bottleneck.** After Redis shipped, end-to-end catalog response times improved by single-digit percentages because the dominant cost was application code, network, search ranking, or auth — not the DB query that got cached. The team had spent N weeks and added a permanent operational liability for no measurable user-visible improvement. *Kill-switch: before any code is written, produce a dated APM trace breakdown showing DB time as >50% of end-to-end on the target endpoints. If it isn't, kill the plan and pursue the actual bottleneck.*

3. **Operational cost of the new component exceeded the latency saving in business terms.** Redis on-call incidents, memory tuning, eviction surprises, cluster failover drills, and the engineering time to maintain the invalidation path consumed more team capacity per quarter than the latency improvement was worth — and the team that gets paged is not the team that got the win. (No kill-switch required for top-3, but flagged: Universal Rule C9 — platforms are products. The receiving on-call team needs to be a willing customer of this platform addition, not a victim of it.)

## Recommendation

**REVISE** — The plan as written cannot be approved. It is solution-first (B1 SUSTAINED), has six SUSTAINED scope items on a five-line plan (B2), every top assumption sits at Confidence 0.1 (B3), all dependencies are unconfirmed (B4), every one-way door lacks alternatives and an ADR (B5), and operability is wholly absent (B6). This is not a marginal review — this is a plan that does not yet exist as a plan; it is a solution headline. The Quick-tier reversibility carve-out does not apply (Full tier; production data; one-way doors).

### Conditions

Before this plan can be re-reviewed for APPROVE, the owner must produce:

1. **Problem statement (B1)** in the form "For [segment], [metric] is [current], target is [target], by [date], because [reason]" — sourced from observed production data, not opinion.
2. **At-least-two alternatives considered (B5)** — read replica, query/index tuning, materialised views, CDN/edge caching of catalog responses, application-level memoisation. Cost out each. Document rejection reasons. Pair with an ADR.
3. **Bottleneck evidence (B3 #1, #2)** — APM trace breakdown showing DB time >50% of end-to-end on the named endpoints, and an estimated cache hit rate ceiling from current request distribution.
4. **Enumerated writer inventory (B2 #1; B3 #3)** — every system that writes to catalog tables, named, with the invalidation hook design per writer, including out-of-band writers (CDC, admin scripts, replication).
5. **Chosen invalidation strategy with consistency contract (B2 #5)** — named strategy, named consistency guarantee, named failure mode and detection mechanism.
6. **Enumerated cached read set (B2 #6)** — list of endpoints/queries to cache, with hit-rate estimate and key cardinality per item.
7. **Operability section (B6)** — metrics, alerts, rollback path with feature flag and DB-headroom verification, runbook entries, on-call team confirmed.
8. **User-visible outcome metric and observation commitment (B6; Product P1)** — what user-facing number we expect to move, by how much, and the dated post-launch review at which we will check it.
9. **Cross-team dependencies confirmed in writing (B4)** — platform/SRE, writer-team(s), observability/on-call, security. Owners named, capacity agreed, dependency staged so a slip in one does not block the whole.
10. **Appetite as a fixed cap (B7)** — not "2–4 weeks", a cap. The plan ships what fits in the cap; remainder is dropped or reshaped.
11. **ADRs (B5)** — at minimum: ADR for adopting Redis (vs. alternatives in #2); ADR for invalidation strategy; ADR for key schema + serialization versioning policy.
12. **Continuous shadow-read kill-switch (B8 #1)** — designed and committed before rollout begins, not after the first stale-read incident.

If, after addressing these, the bottleneck evidence (#3) shows catalog reads are not the dominant latency component, the verdict escalates to **KILL**: the core premise fails and the right move is to redirect engineering effort to the actual bottleneck rather than ship infrastructure that solves a non-problem.
