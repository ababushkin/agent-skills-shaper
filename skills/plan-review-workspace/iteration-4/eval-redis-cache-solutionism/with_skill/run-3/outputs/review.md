# Plan review: redis-cache-product-catalog

## Plan reference

Pasted from prompt: "Introduce Redis as a caching layer in front of Postgres for product catalog reads. We'll add a Redis cluster, write a thin client, add cache-invalidation on writes. Approve?"

## Inputs

- **Appetite**: Not stated in plan. Assumed >1 week (Redis cluster provisioning + client + invalidation logic + rollout). Owner must confirm a fixed cap.
- **Cynefin domain**: Complicated — known cause-effect with expertise required (cache coherence, invalidation patterns, failure modes). Phil Karlton: "There are only two hard things in Computer Science: cache invalidation and naming things."
- **Tier**: **Full** — selected because the plan contains multiple one-way-door decisions (vendor topology / Redis cluster, cache-coherence semantics, write-path coupling) and touches production data path (catalog reads serve user traffic).

**Trigger fired**: Auto-fire #4 (one-way-door: vendor lock-in + production-data-path architecture choice). Also trigger #2 (work clearly exceeds one day) and trigger #3 (touches production read path).

**Step 1a — Fast-track gate**: Did NOT fire. Precondition #1 fails (this is a net-new architectural component, not KTLO). Precondition #2 fails (not one-commit reversible — once writes route through invalidation, removing Redis means re-validating that Postgres alone serves load). Falls through to Full.

## B0 — Cynefin

Complicated. Cache invalidation is a knowable-with-expertise problem with well-documented failure modes (stale reads, thundering herd, split-brain on cluster failover, dual-write inconsistency). Review emphasises dependencies, reversibility, and failure-mode enumeration.

## B1 — Problem framing [GATE]

**Verdict: SUSTAINED.** The plan opens with a solution ("introduce Redis as a caching layer") not a problem. There is no stated user or business outcome, no measured baseline, no target metric. We do not know:

- What Postgres latency or throughput is today (p50/p95/p99 on catalog reads)
- Whether Postgres is actually the bottleneck (vs. application layer, network, N+1 queries, missing indexes)
- What user-visible problem this solves (page load time? cost? read scaling for a launch?)
- What success looks like in numbers

This is a textbook Universal P2 violation: design starts with the stack, not the problem. It is also a Product P1 violation: outputs (Redis cluster shipped) are framed as the goal, not outcomes.

**Falsifying condition**: Owner produces a problem statement of the form "For [segment], catalog read [latency|throughput|cost] is [measured value], causing [outcome]; we need it to be [target] by [date]," with the baseline measured against current Postgres telemetry.

**Until B1 is resolved, every other bucket is reviewing a solution in search of a problem.** A common alternative — adding a missing index, fixing an N+1, enabling Postgres's own query cache, or putting a CDN in front of catalog responses — may be cheaper, more reversible, and sufficient. None of these have been considered in writing.

## B2 — Scope clarity [GATE]

| Item | Verdict | Falsifying condition |
|---|---|---|
| **Cache-invalidation on writes** is named but undefined — does it cover bulk imports, admin tools, background jobs, replication-stream events, partial updates, multi-row transactions? | SUSTAINED | Plan enumerates every write path that mutates catalog data and specifies the invalidation contract for each. |
| **"Thin client"** — undefined. Is it a wrapper around `redis-rb`/`ioredis`/equivalent, or a new abstraction with read-through/write-through semantics? Where does it live (per-service library? sidecar? gateway?)? | SUSTAINED | Plan names the client surface, the language/runtime, the location, and which services depend on it. |
| **"Product catalog reads"** — which reads? Detail page only, or list/search/filter/recommendation endpoints too? Are personalised reads in scope? | SUSTAINED | Plan lists the specific read endpoints in scope and explicitly excludes the rest. |
| Out-of-scope but touched: **observability stack** — Redis adds new metrics, new alerts, new on-call surface. Not declared. | SUSTAINED | Plan has a B6 operability section naming Redis-specific metrics, alerts, and runbooks. |
| Out-of-scope but touched: **deployment topology** — Redis cluster needs network, IAM, TLS, secrets, backup, failover, capacity planning. Not declared. | SUSTAINED | Plan names the deployment substrate, HA topology, failover behaviour, and who operates it. |
| Out-of-scope but touched: **data-consistency contract with consumers** — "eventually consistent reads" is a public behavioural change for any internal/external consumer who currently assumes read-after-write. | SUSTAINED | Plan documents the new consistency guarantee and identifies consumers that need to be informed/migrated. |

Six SUSTAINED items on a one-paragraph plan. This is the expected B2 hit pattern when a plan is solution-stated without scope decomposition.

## B3 — Assumptions + evidence quality [GATE]

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| Postgres is the bottleneck for catalog reads | **0.1** (assertion, no baseline cited) | Pull current p95/p99 latency and CPU/IO utilisation from Postgres telemetry; check pg_stat_statements for catalog query cost. Owner: data/platform on-call. | SUSTAINED |
| Catalog read patterns are cacheable (hot keys, high read:write ratio, low cardinality) | **0.1** (asserted by choice of Redis) | 5-min test: aggregate access logs for top-N catalog SKU read frequency over 24h and compute hit-rate ceiling at typical TTL. | SUSTAINED |
| Cache invalidation on writes will preserve correctness | **0.5** (anecdotal — "we'll add it") | Karlton's law applies. Owner must specify the invalidation strategy (write-through, write-around, TTL-only, event-driven via CDC) and the consistency guarantee. No 5-min test — needs design. | SUSTAINED |
| Redis cluster operational cost (people + infra) is justified by the gain | **0.1** (no number on either side) | Owner: platform/SRE produces a cost estimate (monthly infra + on-call load); product owner produces the expected gain in $ or user-experience terms. | SUSTAINED |
| The team has Redis cluster operational experience | **0.5** at best — not addressed | Owner: name the on-call rota that will respond to a 3am Redis failover incident; if no one, this is an Inverse Conway / Universal P9 problem. | SUSTAINED |

Every assumption sits at Confidence ≤0.5. **Per Step 6, untested assumptions with Confidence <5 block APPROVE.** This alone forces REVISE.

## B4 — Dependencies [GATE, Full]

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| Platform/SRE — provision and operate Redis cluster | Not named | Not confirmed | SUSTAINED |
| Security — review of new in-memory cache (TLS, auth, secrets, data-at-rest if catalog has any sensitive fields) | Not named | Not confirmed | SUSTAINED |
| Finance — approve incremental cloud spend for Redis cluster + replicas | Not named | Not confirmed | SUSTAINED |
| Every consumer of the catalog read API — must accept the new consistency contract | Not named | Not confirmed | SUSTAINED |
| Observability — dashboards, alerts, log pipeline for Redis | Not named | Not confirmed | SUSTAINED |

Universal Rule B7: unconfirmed cross-team dependencies are the single most common cause of missed commitments. Five SUSTAINED.

## B5 — Reversibility + ADR pairing [GATE, Full]

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Add Redis cluster as new operational dependency | No alternatives named (Memcached, in-process LRU, Postgres pgbouncer + better indexes, read replicas, CDN at edge, application-layer cache, materialised view) | None | SUSTAINED |
| Cache-invalidation strategy (write-through vs. event-driven vs. TTL) | Not named — "add cache-invalidation" treats it as one option | None | SUSTAINED |
| Coupling write path to cache-invalidation logic | Not named — once writes call invalidation, removing Redis requires write-path refactor | None | SUSTAINED |
| Public consistency contract for catalog reads (read-after-write → eventual) | Not named | None | SUSTAINED |

Universal P3 + Rule B3 violation in four places. Each one-way door must record the alternatives considered and produce an ADR (Nygard) before approval. Universal Principle 5 ("code is a liability; the best change is often the one you don't make") demands the alternatives be ruled out, not skipped.

## B6 — Operability + success metrics [GATE, Full]

- **Metrics**: Absent. Required: cache hit rate, Redis memory pressure, eviction rate, command latency p95/p99, replication lag, key count, post-launch Postgres load delta, post-launch p95 catalog read latency delta.
- **Alerts**: Absent. Required: hit-rate floor, memory headroom ceiling, replication lag ceiling, cluster-node failure, invalidation queue depth.
- **Rollback path**: Absent. Required: feature-flag to bypass cache and serve directly from Postgres; verified procedure to disable Redis without data loss; verified Postgres can absorb full read load (the failure mode that bites here is "Redis went down, Postgres falls over from the thundering herd").
- **Runbook**: Absent. Required: how on-call diagnoses cache stampede, stale reads, split-brain, full memory.
- **Capacity headroom**: Absent. Required: Postgres headroom assuming Redis is unavailable (this is the failure mode); Redis cluster headroom for traffic peaks.
- **User-visible outcome metric**: Absent. The plan names no observable user outcome. Per Product P1, "Redis cluster deployed" is an output, not an outcome. Required: e.g. "catalog page p95 TTFB reduced from Xms to Yms," "Postgres CPU on read-replicas reduced from X% to Y%," "$Z/month infra cost reduction," or whatever the actual goal is.

Absence on either half of B6 blocks APPROVE. Both halves are absent.

## B7 — Sequencing + capacity (Full)

- **Critical path**: Not surfaced. Likely: measure baseline → confirm Postgres is the bottleneck → choose strategy (cache vs. index vs. replica vs. CDN) → if cache, design invalidation contract → spike → walking skeleton → progressive rollout behind flag → measure → decide.
- **Appetite**: Not fixed. Universal Rule C1 + Shape Up: the appetite is a cap, set up front. "Add a Redis cluster, write a client, add invalidation" is open-ended scope.
- **FTE consistent with appetite**: Cannot evaluate without either.

The plan is not yet shaped — it is a one-paragraph intent. Sequencing should be produced as part of the revision.

## B8 — Pre-mortem (Full: top 3 + kill-switches for top 2)

Adopting prospective hindsight: assume the plan shipped and failed within its appetite.

1. **Cache-invalidation correctness defect leaks stale catalog data** (price, availability, or product info) to users. A bulk import path or admin-tool write path was missed in invalidation. Customers see stale prices; finance/legal incident.
   - **Kill-switch**: pre-launch, write a cross-system audit that compares Redis-served reads against Postgres ground-truth on every write path; ship with the audit running in shadow mode and an alert on divergence >0.1%. Hold rollout until divergence is clean for 7 days.

2. **Postgres was not actually the bottleneck.** Redis is shipped, hit rate is high, but the user-visible latency does not move because the real cost was in the application layer, network, or render path. The team has built and now operates a Redis cluster for no measurable user gain.
   - **Kill-switch**: B1 problem statement gate. Refuse to start build until baseline + target are measured and the bottleneck is profiled. If profiling shows the bottleneck is elsewhere, kill the plan and redirect.

3. **Redis cluster failure causes a worse outage than the original problem.** A failover, a memory-eviction storm, or a network partition takes the cache down; Postgres cannot absorb the un-cached read load and the whole catalog goes down. The cache became a single point of failure.
   - (Kill-switch not required by template, but: load-test Postgres at full read load with cache disabled before declaring the rollout done; size Postgres to survive cache loss. Universal Principle 6 — operability is a functional requirement.)

## Recommendation

**REVISE** — the plan is solution-first with no problem statement, no baseline, no alternatives considered, no operability plan, no success metric, no confirmed dependencies, no ADR for any of four one-way doors, and every named assumption sits at Confidence ≤0.5.

This is not a plan that should be killed — there may well be a real problem here worth solving with caching. But it is not yet a plan that can be approved. The current artefact is an *intent*, and the act of approving an intent locks in a solution before the problem is understood.

### Conditions

Before re-review for APPROVE:

1. **B1**: Produce a problem statement with measured baseline (current p50/p95/p99 catalog read latency, Postgres CPU/IO, throughput) and a target metric. Confirm via profiling that Postgres reads are the actual bottleneck — not application logic, not N+1s, not missing indexes, not a render-path issue.
2. **B5**: Write an ADR enumerating alternatives — at minimum: missing index / query optimisation, Postgres read replicas, materialised view, application-layer in-process cache, CDN at edge, Memcached, Redis. Record the reversal cost of each. Justify Redis specifically against the alternatives, not in isolation.
3. **B2**: Decompose scope. Enumerate every write path that needs invalidation; specify the invalidation contract (write-through, event-driven, TTL-only) and the consistency guarantee published to consumers. List the specific read endpoints in scope.
4. **B3**: Raise Confidence on the top-3 assumptions to ≥5 via the named 5-min tests or owner sign-offs (baseline measurement, read-pattern analysis, invalidation-design review).
5. **B4**: Name and confirm in writing each cross-team owner (platform/SRE for cluster, security for review, observability for stack, finance for spend, every catalog-read consumer for consistency contract).
6. **B6**: Produce the operability section — metrics, alerts, rollback path (feature-flag bypass + verified Postgres can absorb full load if Redis is removed), runbook, capacity headroom on both Redis and Postgres.
7. **B7**: Set a fixed appetite (cap, not range). Surface the critical path with the spike/walking-skeleton steps explicit.
8. **B8 kill-switch**: Ship the cross-system audit (Redis vs. Postgres divergence) in shadow mode before user-visible cutover; hold rollout until divergence is clean.

When these are addressed, re-submit for APPROVE. If the B1 baseline shows Postgres is not the bottleneck, KILL and redirect to whatever the real bottleneck turns out to be.
