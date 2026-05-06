---
name: dora-metrics
description: >
  The four DORA metrics for engineering delivery performance — deployment frequency, lead time
  for changes, change failure rate, and time to restore. Source: Forsgren, Humble, Kim —
  "Accelerate" (2018). Used in post-launch impact review and deploy skills.
type: reference
cited_by:
  - skills/post-launch-impact-review/SKILL.md
  - skills/deploy/SKILL.md
---

# DORA Metrics

DORA (DevOps Research and Assessment) metrics are the four delivery performance indicators identified by Nicole Forsgren, Jez Humble, and Gene Kim in their multi-year research programme, published as "Accelerate" (2018). They are the most empirically grounded set of engineering delivery metrics available. The research covers thousands of organisations across industries, team sizes, and technology stacks. The core finding: teams that perform well on all four metrics simultaneously deliver more software, with fewer outages, at higher quality.

Rule D4 mandates that DORA metrics are tracked and reviewed on a fixed cadence — not discussed informally as feelings ("our delivery is slow"), but measured.

## The four metrics

### 1. Deployment frequency

**What it measures:** How often the team deploys to production (or releases to end users).

**Why it matters:** Deployment frequency is a proxy for batch size. High-frequency deployment means small batches, which means faster feedback, lower merge risk, and cheaper rollback. Low-frequency deployment means large batches, which compounds risk and delay.

**Elite benchmark:** Multiple times per day. High: once per day to once per week. Medium: once per week to once per month. Low: less than once per month.

**Fitness function:** Count of production deployments per day/week in CI/CD tooling or deployment log.

---

### 2. Lead time for changes

**What it measures:** The time from code commit to code running in production.

**Why it matters:** Long lead times mean feedback on decisions is delayed. A 30-day lead time means a mistake made today is not visible in production for a month. Short lead times create tight feedback loops between changes and their effects.

**Elite benchmark:** Less than one hour. High: one day to one week. Medium: one week to one month. Low: one to six months.

**Fitness function:** Timestamp delta: commit time to production deploy time, averaged over the period. Tracked in CI/CD pipeline or deployment metadata.

---

### 3. Change failure rate

**What it measures:** The percentage of production changes that result in a degradation requiring remediation (hotfix, rollback, patch).

**Why it matters:** High change failure rate signals that changes are not validated before they reach production. It is not the same as incident rate — it measures the fraction of changes that cause problems. A team deploying 50 times a day with a 2% failure rate has more incidents than a team deploying 5 times a day with the same rate.

**Elite benchmark:** 0–15%. High: 16–30%. Medium: 31–45%. Low: 46–60%.

**Fitness function:** (Count of deployments requiring rollback or hotfix) / (Total deployments) over the measurement period. Sourced from incident log and deployment log.

---

### 4. Time to restore service (MTTR)

**What it measures:** How long it takes to recover from a production failure — from detection (or start of impact) to restoration of normal service.

**Why it matters:** Systems fail. The variable within a team's control is how fast they detect and recover. Short time-to-restore reflects good observability, practiced runbooks, and small-batch changes that are easy to reason about and roll back. Long time-to-restore reflects the opposite.

**Elite benchmark:** Less than one hour. High: less than one day. Medium: one day to one week. Low: one week to one month.

**Fitness function:** Time from incident opened to incident resolved, by severity tier. Sourced from incident tracker. Review outliers: a single long incident can skew the mean; track median and p90 together.

---

## Cluster, not cherry-pick

Elite teams perform well on all four metrics, not three out of four. Teams that optimise for deployment frequency alone (without improving change failure rate) ship problems fast. Teams that optimise for change failure rate alone (without improving deployment frequency) slow down until the feedback loop breaks. The four metrics form a coherent cluster. If one is strong and the others are weak, the measurement is being gamed rather than the system being improved.

## Applying DORA in a post-launch review

After a feature or change ships, DORA metrics provide the baseline for evaluating delivery health during and after the release. Relevant questions:

- Did deployment frequency change during this release window? (Did the team slow down to manage risk, or maintain cadence?)
- What was lead time from feature-complete to production? Was it within the team's normal range?
- Did this change contribute to any incidents? What was the change failure rate for the release period?
- For any incidents triggered: what was time-to-restore? Was a rollback needed, and how long did it take?

These questions connect the specific release to the team's delivery system health, not just the feature's business outcomes.

## Sources

- Forsgren, Humble, Kim — "Accelerate: The Science of Lean Software and DevOps" (2018)
- DORA State of DevOps Report (annual)
- `rules/eng-principles-universal.md` — Rule D4 (technical quality measured, not discussed)
