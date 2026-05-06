---
name: nfr-categories
description: >
  Taxonomy of non-functional requirement categories for Rule A4. Each category requires
  a number, a unit, and a named fitness function. Used when completing the Constraints
  section of a design doc.
type: reference
cited_by:
  - skills/design-doc/SKILL.md
---

# NFR Categories

Non-functional requirements (NFRs) express quality targets a system must meet independently of what it does. Rule A4 mandates they are specified up front as measurable targets — numbers with units, not adjectives. This document lists the categories, what an acceptable specification looks like for each, and the fitness function types that make them executable under Rule A5.

A specification that uses adjectives ("fast," "highly available," "scalable") is not an NFR. It is a wish. The fitness function is the mechanism that keeps a specified target from drifting after the design doc is accepted.

## Categories

### Performance — latency

**What to specify:** Response time at p50, p95, and p99 under a named load condition. Specify the operation (read, write, query, render), the measurement point (client, load balancer, service), and the load level (requests per second, concurrent users, batch size).

**Example:** `p95 API response time < 200 ms at 500 RPS on the order-search endpoint, measured at the load balancer`

**Fitness function types:** Load test in CI with threshold assertions; alerting rule on tail latency percentile in production.

---

### Performance — throughput

**What to specify:** Transactions or requests per second the system must sustain, with the time window (sustained vs. burst) and the degradation policy when capacity is exceeded.

**Example:** `≥ 2 000 events/s sustained ingest; degrade gracefully (drop with backpressure signal) above 3 000 events/s`

**Fitness function types:** Load test asserting sustained throughput; chaos test asserting backpressure behaviour.

---

### Availability and reliability

**What to specify:** Availability SLO as a percentage over a rolling window; error budget (how much downtime or error rate is acceptable per period); recovery time objective (RTO) and recovery point objective (RPO) for failure scenarios.

**Example:** `99.9% availability over a 30-day rolling window; RTO < 15 min; RPO < 5 min for the primary data store`

**Fitness function types:** SLO burn-rate alert; chaos experiment verifying RTO; backup restore drill verifying RPO.

---

### Security posture

**What to specify:** Authentication and authorisation model, encryption requirements (at rest, in transit), secrets handling, input validation scope, known threat surface (public-facing vs. internal), and compliance framework if applicable (SOC 2, ISO 27001, GDPR, HIPAA).

**Example:** `All API endpoints require JWT auth with 15-min expiry; data encrypted at rest (AES-256); secrets in vault, never in environment variables; no direct SQL query construction from user input`

**Fitness function types:** Auth integration test; static analysis rule for SQL construction; secret-scanner in CI; pen test or automated DAST scan.

---

### Data residency and retention

**What to specify:** Geographic constraints on where data at rest and in transit may reside; retention period by data class; deletion guarantee (days, mechanism).

**Example:** `All PII must remain in EU regions; user data retained ≤ 90 days post-account deletion; deletion propagated to backups within 30 days`

**Fitness function types:** Infrastructure policy assertion (region tags); automated deletion job with audit log; retention-period test on backup restore.

---

### Accessibility

**What to specify:** Conformance level (WCAG 2.1 AA is the common floor), the user-facing surface in scope, and the assistive technology targets (screen readers, keyboard navigation).

**Example:** `All user-facing UI meets WCAG 2.1 AA; keyboard-navigable without mouse; tested with VoiceOver on macOS and NVDA on Windows`

**Fitness function types:** Automated accessibility lint in CI (axe-core or equivalent); manual screen-reader test in QA checklist.

---

### Cost envelope

**What to specify:** Maximum spend per time period by cost category (compute, storage, egress, third-party APIs), the load assumption the estimate is based on, and the scaling behaviour (linear with users, step function at capacity tiers).

**Example:** `Cloud spend ≤ $800/month at 10 000 MAU; linear scaling assumption; alert at 80% of budget`

**Fitness function types:** Cost anomaly alert; budget alert at threshold; load test + cost projection from usage metrics.

---

### Operational limits

**What to specify:** Storage growth rate and capacity ceiling; connection pool limits; queue depth limits; any hard resource ceilings imposed by the deployment environment.

**Example:** `Database storage growth ≤ 50 GB/year at current retention policy; alert at 80% of provisioned capacity; max 20 DB connections per instance`

**Fitness function types:** Storage growth metric with alert; connection pool saturation alert; capacity headroom calculation in design doc Operability section.

---

## Applying this taxonomy in a design doc

In the Constraints section of a design doc, list each NFR that applies to the change. Not every category applies to every design. Select the categories relevant to the problem. For each:

1. State the category.
2. State the target with a number and a unit.
3. Name the fitness function that will verify it.

An NFR entry without a fitness function is incomplete — it names a target no one is watching. A fitness function that cannot be expressed means the target is not yet well enough understood to protect.

## Sources

- Rule A4 in `rules/eng-principles-universal.md` — NFRs specified up front as measurable targets
- Rule A5 in `rules/eng-principles-universal.md` — fitness functions make A4 targets executable
- Ford, Parsons, Kua — "Building Evolutionary Architectures" (fitness functions)
- Nygard, Michael — "Release It!" (operational NFRs; failure modes)
- `skills/design-doc/SKILL.md` — Constraints section where NFRs are documented
