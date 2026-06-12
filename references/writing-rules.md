---
name: writing-rules
description: >
  Prose ruleset for the artefacts Shaper writes — initiatives, OKRs, milestones, tasks,
  and design docs. Governs how the words read, not which fields exist. Cited at each
  skill's synthesis step and carried as the lens for the writing-editor persona.
type: reference
cited_by:
  - skills/initiative-shape/SKILL.md
  - skills/roadmap-shape/SKILL.md
  - skills/delivery-shape/SKILL.md
  - skills/design-doc/SKILL.md
  - agents/writing-editor/AGENT.md
---

# Writing rules

Use these rules for the software-engineering and product-management writing Shaper produces. They govern **prose** — the sentences inside a goal, a milestone, a task, a design-doc section. They do not govern **structure**: which fields a skill emits and in what order is the skill's job, not this file's. Where a rule below would re-mandate a section a skill already gates, the rule keeps only its prose guidance and drops the structural part.

## Core rules

- Put the actor in the subject and the action in the verb. Prefer "The API caches responses" over "Caching is implemented by the API."
- Use concrete verbs. Replace nominalizations such as "implementation," "utilization," and "optimization" with "implement," "use," and "optimize."
- Make each goal, milestone, or task produce a visible work product: a shipped change, design doc, verified fix, report, migration, test, or decision.
- Start with known context and end with the new or important information.
- Cut filler, but keep assumptions, risks, constraints, dependencies, owners, dates, and success criteria.
- Write like a professional colleague. Prefer a clear story over a list of disconnected facts.

## Project goals and OKRs

- Explain the gap between the current state, the desired state, and the cost of staying where you are.
- Use Situation, Complication, Question, Answer logic internally, but do not use those labels as headings.
- Make success measurable.

Bad: "Improve the efficiency of our API and utilize better caching."
Good: "Our API serves 1k RPS today. The Q3 launch requires 10k RPS, which will exceed current capacity. We will re-architect the load balancer to support 15k RPS."

Bad: "Significantly improve dashboard speed."
Good: "Reduce P95 dashboard load time from 4.5s to under 800ms using Edge Workers."

## Design docs

This section governs the prose inside a design doc. Which sections a design doc contains, and their order, is owned by the `design-doc` skill's gates — do not restate that here.

- Problem: name the current state and the cost of the status quo, not just the desired feature.
- Context: anchor the reader in stable facts before introducing the change or conflict.
- Constraints: state each non-functional requirement in concrete, checkable terms.
- Alternatives: compare distinct options and state the practical effect of each one, not a list of properties.
- Recommended approach: start with what the team already knows, then introduce the proposed change.
- Operability: state rollback gates, monitoring signals, and ownership as verifiable conditions, not intentions.

## Milestones and deliverables

- Use milestones as summary achievements, not labels such as "Phase 1" or "Research."
- Group work into non-overlapping containers.
- Order groups by sequence, system structure, or impact.

Bad: "Frontend; Data; Implementation."
Good: "Built responsive React components; Migrated user records to a sharded Postgres cluster."

Bad: "Security; Authentication; Login Page."
Good: "Identity management; Data encryption at rest."

## Tasks, stories, bugs, and refactors

- Every task needs a concrete "done when" state.
- Avoid blank tasks such as "Investigate latency" unless the output is named.
- Use active voice.

Bad: "Perform an investigation into the latency situation."
Good: "Done when: the report identifies the three highest-latency queries in the /orders endpoint."

Bad: "As a user, I want the utilization of an automated system."
Good: "As a user, I want to reset my password through an email link so I can regain access in under 2 minutes."

## Vocabulary

- Use exact technical terms when they are accurate. Replace metaphors only when they hide the cause.
- Prefer "essential" or "required" over vague intensifiers such as "vital."
- Replace "bottleneck" with the specific shortage, delay, queue, lock, or capacity limit when known.
- Prefer "plan" or "spec" over "blueprint" unless discussing an actual final design.
- Prefer "limit" or "maximum" over "ceiling."
- Prefer "use" over "utilization."
- Prefer "implement" over "implementation" when describing action.
- Prefer "communicate with," "connect to," or "call" over "interface with."
- Prefer "affect" over "impact" as a verb.
- Delete "basically," "actually," "quite," "it should be noted that," and similar throat-clearing.
- Replace "at this point in time" with "now."

## Agent review checklist

Before returning an artefact, check:

- Does it move from problem to solution in a clear order?
- Do subtasks explain how to achieve the milestone or why the milestone matters?
- Did pruning preserve assumptions, risks, dependencies, constraints, and success criteria?
- Is every task's done state visible and verifiable?
- Do important terms or conclusions appear where readers will notice them?
- Does it sound like a capable colleague wrote it?
