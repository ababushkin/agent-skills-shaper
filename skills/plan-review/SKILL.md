---
name: plan-review
description: >
  Review a plan, spec, design, or roadmap before approval to catch scope drift,
  unstated assumptions, missing operability, unaddressed one-way doors, and
  predictable failure modes. Use whenever someone is about to approve a plan —
  even if they haven't asked for review explicitly. Trigger phrases: "review
  this plan", "is this plan ok", "before I approve", "should we go with this",
  "what's missing here", "any concerns", "look this over", "thoughts on this
  approach". Auto-fire conditions: any plan that breaks into more than a single
  independently verifiable slice, touches code the user has not personally read
  recently, or contains a one-way-door decision (architecture choice, schema
  migration, public API, vendor lock-in, auth or production-data touch).
---

# Plan review

## Purpose

This skill catches plan defects before approval. A plan that looks coherent can still touch out-of-scope code, rest on unstated assumptions, or commit to a one-way door without recording the alternatives that were considered. By the time those defects surface in execution, the cost of correction is the cost of rework, not the cost of revision. The skill is the operational form of Agentic P3 (the spec is the seatbelt): it forces a structured pass over the plan against eight MECE attack buckets — problem framing, scope, assumptions, dependencies, reversibility, operability, sequencing, pre-mortem — so the categories of defect that actually appear in PDE work each get an explicit check. The deliverable is a review record with a final APPROVE / REVISE / KILL recommendation. The skill replaces the role-play "play the skeptic" framing of its predecessor with framework-based questioning, because empirical evidence (Nemeth meta-analysis) shows assigned dissent is less reliable than structured coverage.

## When to use

Run plan-review when at least one trigger fires. Any single trigger is sufficient.

1. An LLM (or a human) has just produced a plan, spec, design doc, or roadmap, and the owner is about to approve it.
2. The plan breaks into more than one independently verifiable slice (see Agentic P8 — slices, not calendar time).
3. The plan touches code or systems the owner has not personally traced this week.
4. **Auto-fire**: the plan contains a one-way-door decision — architecture choice, schema migration, public API, vendor lock-in, auth change, or any touch of production data (defined: any system reachable from the production database, secrets vault, or auth identity store).

If a trigger is ambiguous, run it. The Quick tier is short; the cost of skipping a needed review is not.

## Do not use when

- **Typo fixes, single-line changes, pure read-only exploration.** Review overhead exceeds value.
- **Plans for work already in progress.** Use a kill-switch review instead — different question (should we stop?), different output.
- **Plans already reviewed and revised in the current session.** Re-review only if material new evidence arrived.
- **The plan itself doesn't exist yet.** Use **shape:design** or **shape:idea** to produce a plan first.

## Inputs

- The plan artefact: file path, pasted text, or plan stated in conversation
- Plan appetite — estimated time-to-completion. Extract from the plan; if absent, ask the owner before proceeding (appetite drives tier selection)
- Optional: prior plan-review records for related work (loaded for pattern continuity per Agentic P1)
- Access to `eng-principles-universal.md`, `eng-principles-agentic.md`, `PRODUCT_RULES.md`, and `references/confidence-meter.md`

## Outputs

An inline review record in the conversation, structured per the artefact template below and ending with the APPROVE / REVISE / KILL recommendation plus named conditions for any non-APPROVE verdict. The review is conversation-only — no file is written; any change the owner accepts lands back in the reviewed plan or design doc itself.

## Tier selection — auto, not user-pick

Two tiers. The skill selects the tier from plan attributes; the owner can override with `--quick` or `--full`.

**Quick** (≤8 minutes). Runs B0, B1, B2, B3, and a short B8.

**Full** (≤30 minutes). Runs all of B0–B8.

**Auto-select Full when ANY of these holds:**

- Plan appetite > ~5 slices (the design-doc threshold from Rule A1 / Agentic P8)
- Plan contains ≥1 one-way-door decision
- Plan has ≥3 external dependencies (other teams, vendors, third-party APIs)
- Plan touches production data, schema migrations, or auth

**Why auto and not user-pick.** User-pick tiering produces a skip rate. Under deadline pressure, the owner picks Quick on plans that warrant Full, defeating the skill's purpose. Auto-select removes the discretion at the moment it is least reliable.

## Workflow

**Step 1 — Trigger check [GATE]**
Confirm at least one trigger from the When-to-use section fires. State which one. If none holds, recommend skipping or downgrading to a read-and-acknowledge. Do not proceed past this gate.

**Step 1a — Fast-track gate [GATE]**
Before tier selection, check whether the plan qualifies for fast-track. The fast-track gate fires only when **all four** preconditions hold:

1. **Class is KTLO/maintenance.** One of: dependency bump at minor or patch SemVer (any gem/npm/cargo/etc.); lint or format config change (rubocop.yml, eslint, prettier); doc-only change (README, comments, changelog); log/telemetry cleanup (removing unused log lines, renaming); test cleanup (deleting skipped/dead tests, fixture refresh).
2. **Fully reversible.** One-commit revert restores prior state. No production data, schema, auth, or vendor topology touched.
3. **Appetite is a single slice.** If the plan breaks into more than one independently verifiable slice, fall through to normal flow.
4. **No major-version anything.** Any major SemVer bump (1.x → 2.x), any breaking-API call-out, any "we'll need to absorb new features" framing → full flow. Major bumps need a problem statement (what features, why now, what we're absorbing) — they are not KTLO.

If all four hold → emit the fast-track output template (below) and stop. Skip B0–B7 entirely; B8 is folded into the template as a one-liner. Length target 15–25 lines, hard cap 30. Token target ~15k vs ~55k for full Quick-tier flow.

If any of the four fails → fall through to Step 2 (normal flow). Record one line on which precondition failed, so the owner sees why the gate did not fire.

Rationale: this is the operational form of Universal Rule A5 (KTLO carve-out). On a fully-reversible KTLO change, the cost of acting on a flawed plan is bounded by the revert; the cost of running heavy review (and producing token waste plus REVISE-blocked APPROVEs on routine maintenance) exceeds the cost of the worst-case mistake. CI/CD is assumed present and is the runtime safety net for this class.

### Fast-track output template

```markdown
# Plan review: <plan-slug>

**Fast-track gate fired** — KTLO/minor-version class, fully reversible, single slice. CI/CD is the runtime gate; this review is proportionate to that risk.

**Cynefin domain**: Clear
**Tier**: Quick (fast-track sub-form)

## Verdict: APPROVE

## Sanity checks
- <check 1 — typically a scope-narrowing flag, e.g. `bundle update --conservative <gem>` not `bundle update`>
- <check 2 — typically a post-change validation, e.g. run `bundle exec rubocop` after bump, not just the test suite>
- <check 3 if applicable — e.g. confirm related ecosystem gems move in lockstep>

## B8 — Pre-mortem (one line)
Top failure mode: <named, specific>. Kill-switch: <revert | named precheck>.
```

If the gate fires and the produced review exceeds 30 lines, the gate misfired — re-evaluate against the four preconditions before emitting.

**Step 2 — Tier selection**
Apply the auto-select rules. State the chosen tier and the attribute that selected it. If the owner has supplied `--quick` or `--full`, honour the override and record it.

**Step 3 — B0 Cynefin classification**
One line: classify the plan's domain as Clear, Complicated, Complex, or Chaotic (Snowden). The classification adjusts review depth.
- **Clear** — known cause-effect; review is checklist coverage.
- **Complicated** — knowable with expertise; emphasise dependencies and risk.
- **Complex** — emergent; verify the plan includes feedback loops and not deterministic milestones.
- **Chaotic** — no clear cause-effect; stop. Recommend stabilising before planning.

**Step 4 — B1 Problem framing [GATE]**
Does the plan open with a problem (a user or business outcome) or with a solution (a stack choice or feature)? A plan that begins "we will use Redis…" without a problem statement is solution-first; SUSTAINED. Demand a problem statement with measurable target before approval. (Universal P2.)

**Step 5 — B2 Scope clarity [GATE]**
Read the plan against its declared scope. Name three things the plan touches that it has NOT declared in scope. Name three things it declares in-scope that are vague enough to expand silently. For each item, issue a verdict: **SUSTAINED**, **OVERTURNED**, or **PARTIAL**, accompanied by a specific falsifying condition (the observable thing that would prove the verdict wrong). If zero SUSTAINED items surface and the plan exceeds single-slice appetite, re-run B2 more aggressively — clean plans are rare, and zero hits usually means lenient review.

**Step 6 — B3 Assumptions + evidence quality [GATE]**
Extract every "we assume…", "X will…", "the system can…", and "users want…" implicit in the plan. List the three riskiest. **For each, assign a Confidence score on Gilad's scale (`references/confidence-meter.md`):**
- 0.1 — opinion, assertion, assumption
- 0.5 — anecdote, one-off observation
- 2–5 — survey data, market research
- 5–8 — experiment, smoke test, prototype test
- 8–10 — validated launch, sustained behavioural data

Then name a 5-minute test that would validate the assumption before execution begins, or a named owner who must sign off. Untested assumptions with Confidence < 5 block APPROVE. (Universal P4; Product P4.)

**Step 7 — B4 Dependencies [GATE, Full only]**
List every internal, external, and cross-team dependency the plan implies. For each: is the owner named and confirmed in writing? Is capacity available within the plan's appetite? Unconfirmed dependencies are the single most common cause of missed commitments (Universal Rule B7). Verdict per dependency.

**Step 8 — B5 Reversibility + ADR pairing [GATE, Full only]**
List every one-way door — decisions expensive to reverse (architecture, schema, public API, vendor lock-in). For each: does the plan name the alternatives that were considered? Does an ADR exist or has one been committed to be written? An undocumented one-way door is a silent commitment; the plan must either record the alternatives or be sent back to add them. (Universal P3, Rule B3; Agentic P7.)

**Step 9 — B6 Operability + success metrics [GATE, Full only]**
Two halves.
- **Operability**: does the plan name metrics, alerts, rollback path, on-call runbook, and capacity headroom? (Universal Rule A6.)
- **Success metrics**: does the plan name a user-visible outcome metric that will be observed post-launch — not a delivery metric, an outcome metric? (Product P1: outcomes, not outputs.)

Absence on either half blocks APPROVE.

**Step 10 — B7 Sequencing + capacity (Full only)**
Is the critical path surfaced — does the plan name what blocks what? Is the appetite fixed (a cap, not a range)? Is the team's actual FTE consistent with the appetite? An appetite of "2–4 weeks" is not an appetite; it is a hope.

**Step 11 — B8 Pre-mortem (cross-cutting, both tiers)**
Adopt prospective hindsight (Klein): assume the plan has already failed.
- **Quick**: the plan failed by the end of the slice it's executing. Name the top 1 reason. Name a kill-switch condition that would catch it early.
- **Full**: the plan shipped and failed within its appetite. Write the top 3 reasons ranked by likelihood. For the top 2, name kill-switch conditions.

Generic reasons ("things went wrong") are rejected — name the specific failure mode.

**Step 12 — Recommendation [GATE]**
Issue **APPROVE**, **REVISE**, or **KILL** with named conditions.
- **APPROVE** — no unresolved SUSTAINED verdicts; all required buckets ran.
- **REVISE** — at least one SUSTAINED verdict that the owner must address before approval.
- **KILL** — the plan's core premise fails (problem framing absent or false; reversibility cost unbearable; dependencies cannot be secured).

APPROVE is blocked by any unresolved SUSTAINED verdict on a falsifying condition — **except** under the Quick-tier reversibility carve-out below. (When the Step 1a fast-track gate fires, this Step is bypassed entirely — fast-track output is APPROVE by construction.)

**Quick-tier reversibility carve-out.** At Quick tier, when the plan is fully reversible (one-commit revert restores prior state, no production data touched, no schema/auth/vendor changes), SUSTAINED verdicts on B2 (scope) and B3 (assumptions) downgrade from "block APPROVE" to "**APPROVE with named recommendation**." The skill still surfaces the finding — the owner still sees the scope or assumption concern — but the recommendation rides alongside an APPROVE rather than triggering REVISE. Rationale: on a fully-reversible KTLO change (Universal Rule A5), the cost of acting on a flawed plan is bounded by the revert; the cost of REVISE-blocking such a plan exceeds the cost of the worst-case mistake. The carve-out does NOT apply to:
- B5 (reversibility) SUSTAINED — by definition the plan is not fully reversible
- B6 (operability) SUSTAINED — operability concerns survive revert
- Full-tier plans — the auto-select attributes (one-way door, production data, >1wk appetite) already preclude reversibility

When the carve-out applies, write the verdict as `APPROVE — recommend: <named action>` and record the SUSTAINED bucket finding under Conditions for visibility.

**Step 13 — Present review record**
Present the review in the conversation using the artefact template below. The review is inline-only — do not write a file. Any change the owner accepts lands back in the reviewed plan or design doc, not in a separate review record.

## Artefact template

```markdown
# Plan review: <plan-slug>

## Plan reference
<!-- Path or link to the plan being reviewed. Pasted excerpt if no path. -->

## Inputs
- **Appetite**: <slice count — fixed cap, not range; see Agentic P8>
- **Cynefin domain**: <Clear | Complicated | Complex | Chaotic>
- **Tier**: <Quick | Full> — selected because <attribute>

## B1 — Problem framing
<!-- Does plan open with problem or solution? Verdict + falsifying condition. -->

## B2 — Scope clarity
| Item | Verdict | Falsifying condition |
|---|---|---|
| <out-of-scope touch #1> | SUSTAINED / OVERTURNED / PARTIAL | <observable thing that would prove the verdict wrong> |

## B3 — Assumptions + evidence quality
| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|

## B4 — Dependencies (Full only)
| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|

## B5 — Reversibility + ADR pairing (Full only)
| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|

## B6 — Operability + success metrics (Full only)
- Metrics: <named or absent>
- Alerts: <named or absent>
- Rollback path: <named or absent>
- Runbook: <named or absent>
- Capacity headroom: <named or absent>
- User-visible outcome metric: <named or absent>

## B7 — Sequencing + capacity (Full only)
<!-- Critical path surfaced? Appetite fixed? FTE consistent with appetite? -->

## B8 — Pre-mortem
<!-- Quick: top 1 reason + kill-switch. Full: top 3 reasons + kill-switches for top 2. -->

## Recommendation
**APPROVE | REVISE | KILL** — <one-line rationale>

### Conditions
<!-- Named conditions the plan must satisfy before APPROVE. -->
```

## Red flags

- Reviewer notes "LLM considered alternatives" — the LLM produced text that mentions alternatives; B5 requires them named alongside the chosen approach with reversal cost. Pattern-match is not analysis.
- Tier overridden to `--quick` without a written reason on a plan that auto-selects Full.
- A verdict is given without a named falsifying condition.
- B2 returns zero items on a plan whose appetite exceeds a single slice.
- Pre-mortem reasons are all generic ("things might go wrong", "might be slow").
- A one-way door is identified but the plan is APPROVED without alternatives or ADR.
- Confidence scores are missing on B3 items.
- Operability section absent on a Full-tier plan.
- Owner runs the skill but discards REVISE recommendations without addressing them.
- Review presented without a final recommendation.

## Exit criteria

A single review run is complete when all of the following hold:

1. The triggered condition is stated, and the chosen tier is named with the selecting attribute.
2. The Cynefin domain is stated (B0).
3. Every required bucket for the tier ran and produced verdicts.
4. Every verdict has a named falsifying condition.
5. Every B3 item carries a Confidence score (Gilad scale).
6. APPROVE is issued only when zero unresolved SUSTAINED verdicts remain.
7. The review record is presented inline in the conversation, structured per the artefact template and ending with a recommendation.

## Known limits + revisit triggers

The skill carries deliberate limitations. Each one has a measurable trigger that should prompt a revisit.

| Limit | Revisit trigger | Action |
|---|---|---|
| Tier auto-select rules may not match the owner's risk model | Override rate exceeds 20% over the first 10 runs | Revisit the auto-select attribute set |
| Full mode has a 30-minute cap | Full runs exceed 30 minutes on >25% of cases | Split the skill or expand the cap |
| Review runs in main context — same context as the plan author = same blindspots | Evals show the review adopts plan-author framing (false-OVERTURN rate >10%) | Extract review to a sub-agent with isolated context |
| One skill covers all plan types — roadmap-specific moves not specialised | ≥5 reviews against roadmaps yield <30% bucket hit rate | Split off a separate `roadmap-review` skill |
| Bucket structure was designed against PDE failure modes, not piloted | Any bucket has <10% SUSTAINED hit rate after 5 real runs | Prune or merge buckets |

## Related

- `rules/eng-principles-agentic.md` — P3, P4, P5, P6, P7, P8
- `rules/eng-principles-universal.md` — P2, P3, P4, P6, P9, Rule A2, Rule A6, Rule B3, Rule B7
- `rules/PRODUCT_RULES.md` — P1, P4
- `references/confidence-meter.md` — Gilad scale used in B3
- Klein, Gary — "Performing a Project Premortem" (HBR 2007) — B8 source
- Snowden, Dave — Cynefin framework (B0 source)
- Heilmeier, George — DARPA Catechism (structural reference for B1–B7 framework-based questioning)
- Nygard, Michael — ADR alternatives discipline (B5 source)
- Singer, Ryan — "Shape Up" — appetites and reversibility framing
