# Plans, Goals, OKRs, and Milestones

## Goals: justify the project by the gap

A goal exists to close the gap between the current state and the success state. State both, with numbers.

| Bad | Good |
|---|---|
| "The goal is to improve the efficiency of our API and utilize better caching." | "Our API serves 1k RPS today. Q3 traffic forecasts 10k RPS. We will re-architect the load balancer to sustain 15k RPS." |

Note what the good version does: noncontroversial fact → disturbance → quantified success state, in three short sentences, with no framework labels.

## OKRs: a specific result that eliminates a palpable cost

Each key result names the current value, the success value, and (where useful) the mechanism.

| Bad | Good |
|---|---|
| "Significantly improve dashboard speed." | "Reduce P95 dashboard load time from 4.5s to under 800ms using Edge Workers." |
| "Increase reliability." | "Cut weekly pager incidents from 12 to under 3 by adding circuit breakers to the payments service." |

If a key result has no number, it is a wish, not a result. If it has no cost attached (what the current state is costing in money, time, or pain), the reader has no reason to care — state the cost in the surrounding prose.

## Milestones: achievements, not labels

Group work into containers that state a **summary effect** — what was accomplished, not where you were on the calendar.

| Bad | Good |
|---|---|
| "1. Frontend; 2. Data" | "1. Built responsive React components; 2. Migrated user records to a sharded Postgres cluster" |
| "Phase 1: Research" | "Identified the three highest-cost queries blocking checkout" |

**MECE check for milestone groups.** Groups must not overlap and must cover the whole project.

| Bad (overlapping) | Good (exclusive) |
|---|---|
| "1. Checkout flow; 2. Payment processing" | "1. Cart and checkout UI; 2. Payment capture and settlement" |

**Ordering.** Pick one principle per list and state it implicitly through structure: time (sequential delivery), structure (frontend / backend / infra), or degree (highest-impact first).

## Output shape for a plan

1. Opening prose paragraph: where we are, what changed, what we will do (the SCQ intro, unlabeled).
2. Goal with quantified current → success state.
3. Key results, each with numbers.
4. Milestones as achievement headings, MECE, in a declared order.
5. Risks, assumptions, and dependencies — kept, even when pruning.

## Plan / OKR review additions

Beyond the universal Phase 5 gate, check:

- Does the goal state both the current state and the success state, each with a number?
- Does every key result carry a number, and does the surrounding prose name the cost of the status quo?
- Are the milestones achievement headings (a result), not calendar or category labels?
- Are the milestone groups MECE — no overlap, no gap — under one declared ordering principle?
- Did risks, assumptions, and dependencies survive pruning?
