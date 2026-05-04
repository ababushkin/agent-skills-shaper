# Plan: `plan-review` skill for pde-skills (v2)

> **v2 supersedes v1** (2026-05-04). v1 inherited a four-pattern devil's-advocate
> structure from `phase4-devils-advocate` (investment research). Meta-review
> against three frames (domain transfer, MECE, self-audit of assumptions and
> constraints) surfaced: (a) MECE failure on both axes — A1–A4 overlap at
> boundaries and miss key PDE defect categories (operability, success metrics,
> dependencies, sequencing); (b) empirical evidence (Nemeth meta-analysis) that
> assigned devil's-advocate dissent is less effective than framework-based
> questioning; (c) seven unstated assumptions and four unflagged constraints in
> the v1 spec. v2 is a full rebuild: eight MECE attack buckets + a Cynefin
> Step 0, framework-based questioning (not role-play), and an explicit
> "Known limits + revisit triggers" section in the shipped SKILL.md.

## Context

User identified plan-review as a current weakness: approves coherent-looking
plans that contain unstated assumptions or scope drift, then pays for it in
mid-execution rework. Two recent failures share root cause — plan looked
plausible, user green-lit, mismatch surfaced after work began:

1. Roadmap shaped without running idea-triage on candidates → forced redo.
2. Vue removal task picked PrizeCategorySelector, which touched competition
   code user had abandoned → mid-task re-scope.

Existing pde-skills cover plan *creation* (`design-doc`,
`planning-and-task-breakdown`, `idea-triage`) but no skill covers plan
*review before execution*. Backlog item #14 reserves this gap. The AI thesis
project's `phase4-devils-advocate` agent was the structural starting point —
verdict format (SUSTAINED / OVERTURNED / PARTIAL with named falsifying
condition) survives; the role-play framing does not.

Outcome: a single skill the user runs (or gets prompted to run) on any
plan / spec / design before approving it, that catches plan defects across
eight MECE-disjoint categories with high diagnostic value and low ceremony.

---

## Recommended approach

Build **one** new skill at `pde-skills/skills/engineering/plan-review/`. Two
intensity tiers (Quick / Full) auto-selected by plan attributes — not user
choice. No hook in v1; run manually via `/pde:plan-review` until adoption is
established. Reassess hook after 1–2 weeks of real use.

### Scope (in)

- New skill: `skills/engineering/plan-review/SKILL.md`
- New wrapper: `.claude/commands/plan-review.md`
- New evals: `evals/evals.json` with five drafted test cases
- Update `install.sh` to publish `/pde:plan-review`
- Update `PROJECT_PLAN.md`: mark item #14 in-progress, downgrade #19
- Update `skills/using-this-pack/SKILL.md` routing

### Scope (out)

- ExitPlanMode auto-fire hook (deferred to v2)
- Separate `roadmap-review` skill (deferred per v1 — partially absorbed here)
- Sub-agent extraction (deferred — independence trade-off documented under
  Known Limits)
- `references/` split (only if SKILL.md exceeds 400 lines)
- Description-optimization eval loop (`run_loop.py`) — deferred to post-v1

---

## Skill specification

### Frontmatter (drafted in full)

```yaml
---
name: plan-review
description: >
  Review a plan, spec, design, or roadmap before approval to catch scope
  drift, unstated assumptions, missing operability, unaddressed one-way
  doors, and predictable failure modes. Use whenever the user is about to
  approve a plan — even if they haven't asked for review explicitly.
  Trigger phrases: "review this plan", "is this plan ok", "before I
  approve", "should we go with this", "what's missing here", "any concerns",
  "look this over", "thoughts on this approach". Auto-fire conditions: any
  plan that exceeds one day of effort, touches code the user has not
  personally read recently, or contains a one-way-door decision (architecture
  choice, schema migration, public API, vendor lock-in, auth or production-data
  touch).
pack: engineering
lifecycle_stage: define
principles_implemented:
  - source: eng-agentic
    id: P3       # spec is the seatbelt
    bucket: standalone
  - source: eng-agentic
    id: P4       # evidence beats vibes
    bucket: embedded
  - source: eng-agentic
    id: P5       # rationalisations are predictable; pre-rebut
    bucket: embedded
  - source: eng-agentic
    id: P6       # stop the line; never silence the signal
    bucket: embedded
  - source: eng-agentic
    id: P7       # memory lives in artefacts (ADR pairing)
    bucket: embedded
  - source: eng-universal
    id: P2       # design starts with the problem, not the stack
    bucket: standalone
  - source: eng-universal
    id: P3       # architecture is the set of expensive-to-change decisions
    bucket: embedded
  - source: eng-universal
    id: P4       # name your assumptions; test the risky ones
    bucket: standalone
  - source: eng-universal
    id: P6       # operability is a functional requirement
    bucket: embedded
  - source: eng-universal
    id: P9       # Conway's Law is a law
    bucket: embedded
  - source: eng-universal
    id: Rule A2  # design doc structure (used as scope-check baseline)
    bucket: embedded
  - source: eng-universal
    id: Rule A6  # operability section is required
    bucket: embedded
  - source: eng-universal
    id: Rule B3  # name blast radius and reversibility cost
    bucket: embedded
  - source: eng-universal
    id: Rule B7  # cross-team dependencies surfaced before commitment
    bucket: embedded
  - source: product
    id: P1       # outcomes, not outputs
    bucket: embedded
  - source: product
    id: P4       # confidence must be made explicit
    bucket: embedded
length_target: 320–400
author: Anton Babushkin
predecessor:
  repo: internal/ai-thesis-research
  skill: phase4-devils-advocate
  relation: derivative
kept_from_predecessor:
  - SUSTAINED / OVERTURNED / PARTIAL verdict format
  - Named-falsifying-condition discipline (no generic critiques accepted)
  - Pre-mortem framing as prospective hindsight, not forward critique
  - Time-boxed adversarial sweep with tier selection by complexity
changed_from_predecessor:
  - Replaced four investment-thesis attack patterns with eight MECE attack
    buckets covering PDE defect categories (B1–B8)
  - Added Cynefin Step 0 to right-size review depth
  - Dropped devil's-advocate role-play framing — replaced with framework-based
    questioning (Heilmeier-style). Empirical: Nemeth meta-analysis shows
    assigned dissent < authentic dissent
  - Added Confidence scoring (Gilad scale) per surfaced assumption (B3)
  - Added operability + success-metrics bucket (B6) — was missing entirely
  - Added cross-team dependency bucket (B4) — was partial in A3 only
  - Added ADR-pairing requirement to reversibility bucket (B5)
  - Added "Known limits + revisit triggers" subsection to make spec-level
    assumptions and locked constraints explicit
  - APPROVE / REVISE / KILL recommendation replaces investment-thesis verdicts
  - Common rationalisations table per Agentic P5
  - Artefact template files review at docs/plan-reviews/<slug>/review.md
---
```

### Body section list

1. **Purpose** — what review-before-approve catches; why review of a plan is
   cheaper than review of work built on a wrong plan; trace to Agentic P3
   (spec is the seatbelt).
2. **When to use** — three triggers (any one fires) plus auto-fire conditions
   for one-way-door decisions, production-data touches, auth changes.
3. **When not to use** — typo / single-line / read-only; in-progress work
   (use kill-switch review instead); already-reviewed plans in current session.
4. **Inputs** — plan artefact (path / pasted text / in-conversation); plan
   appetite (extracted or asked); optional prior reviews for pattern continuity.
5. **Outputs** — review record at `docs/plan-reviews/<slug>/review.md` +
   inline summary with APPROVE / REVISE / KILL.
6. **Tier selection [auto, not user-pick]** — Quick (≤8 min) vs. Full
   (≤30 min). Auto-select Full when ANY of: appetite >1 week, ≥1 one-way-door
   decision, ≥3 external dependencies, touches production data / schema /
   auth. **"Production data" defined**: any system reachable from the
   production database, secrets vault, or auth identity store. User can
   override with `--quick` / `--full`. Why auto: user-pick produces skip rate.
7. **Workflow [GATE]s** —
   - **Step 1 [GATE] Trigger check.** Confirm at least one trigger fires.
   - **Step 2 — Tier selection.** Apply auto-select; state chosen tier and
     attribute that selected it.
   - **Step 3 — B0 Cynefin classification.** One line: plan domain =
     Clear / Complicated / Complex / Chaotic. Adjusts review depth: Clear =
     checklist coverage; Complicated = dependency + risk emphasis; Complex =
     verify the plan includes feedback loops, not deterministic milestones;
     Chaotic = stop, recommend stabilising before planning.
   - **Step 4 [GATE] — B1 Problem framing.** Does the plan open with a problem
     (user/business outcome) or a solution (stack/feature)? If solution-first,
     SUSTAINED; demand a problem statement before approval. (univ P2)
   - **Step 5 [GATE] — B2 Scope clarity.** Name three things the plan touches
     that it has NOT declared in scope. Name three things it declares in-scope
     that are vague enough to expand silently. VERDICT per item.
   - **Step 6 [GATE] — B3 Assumptions + evidence quality.** Extract every
     "we assume…" / "X will…" / "the system can…". List the three riskiest.
     **For each, assign a Confidence score (Gilad 0.1–10)** and a 5-min test
     or named owner. Untested assumptions with Confidence <5 block APPROVE.
   - **Step 7 [GATE] — B4 Dependencies (Full only).** List every internal,
     external, and cross-team dependency. For each: named owner confirmed in
     writing? capacity available within plan appetite? (Rule B7)
   - **Step 8 [GATE] — B5 Reversibility + ADR pairing (Full only).** List
     every one-way door. For each: Alternatives section present in plan?
     ADR exists or committed to be written? (univ P3, Rule B3; agentic P7)
   - **Step 9 [GATE] — B6 Operability + success metrics (Full only).**
     Plan names: metrics, alerts, rollback path, on-call runbook, capacity
     headroom? Plan names a user-visible outcome metric that will be observed
     post-launch? Absence on either side blocks APPROVE. (univ P6, Rule A6;
     product P1)
   - **Step 10 — B7 Sequencing + capacity (Full only).** Critical-path risk
     surfaced? Appetite is fixed (days / weeks cap, not range)? Team-FTE
     consistent with appetite?
   - **Step 11 — B8 Pre-mortem (cross-cutting, both tiers).**
     - Quick: assume failure by end-of-week. Top 1 reason. Kill-switch.
     - Full: assume failure within appetite. Top 3 reasons ranked by
       likelihood. Kill-switch for top 2.
   - **Step 12 [GATE] — Recommendation.** APPROVE / REVISE / KILL with named
     conditions. APPROVE blocked by any unresolved SUSTAINED verdict.
   - **Step 13 — File review record.** Write to
     `docs/plan-reviews/<plan-slug>/review.md` per artefact template.
8. **Artefact template** — markdown code block.
   - Plan reference + appetite + Cynefin domain + selected tier +
     tier-selection reason
   - One section per bucket run (B0–B8 conditional on tier)
   - Each item: claim → verdict → falsifying condition → Confidence (B3 only)
   - Final recommendation with conditions
9. **Common rationalisations** (per Agentic P5) — at least 7 entries:
   - "I already read it"
   - "It's a small plan, review is overkill"
   - "The LLM considered alternatives"
   - "Quick mode is fine for this"
   - "Pre-mortem is theatre"
   - "I don't have time for the full mode"
   - "We can revise mid-execution if we hit issues"
10. **Red flags** — verdict given without falsifying condition; B2 returns
    zero items on >1-day plan; pre-mortem reasons all generic; one-way door
    identified but plan APPROVED without Alternatives + ADR; B6 absent on
    Full-tier plan; Confidence scores missing on B3 items; user runs skill
    but discards REVISE recommendations without addressing them.
11. **Worked example** — apply plan-review retroactively to the
    PrizeCategorySelector failure (~30 lines). B2 SUSTAINS "competition code
    touched but out-of-scope unstated"; B6 SUSTAINS "no rollback path named";
    recommendation REVISE; user re-scopes before execution = avoided rework.
12. **Verification / exit criteria** (per skill *run* — not skill *build*):
    - Tier explicitly selected with selecting attribute named
    - Cynefin domain stated
    - All required buckets for the tier ran and produced verdicts
    - Every verdict has a named falsifying condition
    - B3 items each carry a Confidence score
    - APPROVE only with zero unresolved SUSTAINED items
    - Review record filed at `docs/plan-reviews/<plan-slug>/review.md`
13. **Known limits + revisit triggers** — *new section*. Each entry: limit →
    measurable trigger → action.
    - **Tier auto-select drift.** Limit: rules may not match user's risk
      model. Trigger: override rate >20% over first 10 runs. Action: revisit
      attribute set.
    - **Artefact-consumer reality.** Limit: review files assume a reader.
      Trigger: zero references to `docs/plan-reviews/` in subsequent work
      after 1 month. Action: migrate to inline-only or Slack rollup.
    - **Time-box overflow.** Limit: Full mode caps at 30 min. Trigger: Full
      runs exceed 30 min on >25% of cases. Action: split skill or expand cap.
    - **No-sub-agent independence loss.** Limit: review runs in same context
      as plan author. Trigger: evals show review adopts plan-author framing
      (false-OVERTURN rate >10%). Action: extract to sub-agent.
    - **Single-skill bottleneck.** Limit: roadmap-specific moves not covered.
      Trigger: ≥5 reviews against roadmaps yield <30% bucket hit rate.
      Action: split off `roadmap-review`.
    - **Phase4 transfer hypothesis.** Limit: bucket structure was designed,
      not piloted. Trigger: any bucket has <10% SUSTAINED hit rate after
      5 real runs. Action: prune / merge buckets.
14. **References**
    - `skills/engineering/eng-principles-agentic.md` — P3, P4, P5, P6, P7
    - `skills/engineering/eng-principles-universal.md` — P2, P3, P4, P6, P9,
      Rule A2, Rule A6, Rule B3, Rule B7
    - `skills/product/PRODUCT_RULES.md` — P1, P4
    - `references/confidence-meter.md` — Gilad scale for B3
    - `phase4-devils-advocate` (internal/ai-thesis-research) — predecessor
    - Klein, Gary — "Performing a Project Premortem" (HBR 2007)
    - Nemeth, Charlan — "Authentic dissent vs. devil's advocate"
      (peer-reviewed meta-analysis: assigned dissent fails)
    - Snowden, Dave — Cynefin framework
    - Heilmeier, George — DARPA Catechism (8 questions, structural reference)
    - Nygard, Michael — ADR Alternatives section discipline
    - Singer, Ryan — Shape Up appetites + reversibility framing

---

### Critical files

- New: `/Users/anton/src/pde-skills/skills/engineering/plan-review/SKILL.md`
- New: `/Users/anton/src/pde-skills/.claude/commands/plan-review.md`
- New: `/Users/anton/src/pde-skills/skills/engineering/plan-review/evals/evals.json`
- Edit: `/Users/anton/src/pde-skills/install.sh`
- Edit: `/Users/anton/src/pde-skills/PROJECT_PLAN.md`
- Edit: `/Users/anton/src/pde-skills/skills/using-this-pack/SKILL.md`

### Existing patterns to reuse

- **Frontmatter shape**: `skills/engineering/design-doc/SKILL.md` lines 1–65
- **Body ordering + `[GATE]` discipline**: same file, workflow section
- **Wrapper command shape**: `.claude/commands/design-doc.md`
- **Verdict + falsifying-condition discipline**:
  `/Users/anton/src/ai-thesis-research/.claude/agents/phase4-devils-advocate.md`
- **Common rationalisations table**: `idea-triage/SKILL.md` lines 178–187
- **Artefact template**: `idea-triage/SKILL.md` lines 141–175
- **Heilmeier Catechism** (8 questions): structural reference for B1–B7
- **Cynefin classification**: structural reference for B0
- **Confidence Meter (Gilad)**: `references/confidence-meter.md`

---

### Evals (drafted — five test cases)

`skills/engineering/plan-review/evals/evals.json`. Run after implementation
per skill-creator's eval loop.

```json
{
  "skill_name": "plan-review",
  "evals": [
    {
      "id": 1,
      "name": "roadmap-without-triage",
      "prompt": "Review this plan: shape next-quarter roadmap with shareable shortlist + push notifications + onboarding rewrite, allocate 60/30/10. Approve?",
      "expected_output": "B1 OVERTURNED (problem framing present at portfolio level). B2 SUSTAINED on 'shareable shortlist scope vague — no triage record exists'. B3 SUSTAINED on assumed customer demand for push notifications, Confidence ≤2. Recommendation: REVISE.",
      "files": []
    },
    {
      "id": 2,
      "name": "prizecategoryselector-vue-removal",
      "prompt": "Review this plan: remove unused Vue components, starting with PrizeCategorySelector under app/javascript/components/. Approve?",
      "expected_output": "B2 SUSTAINED 'PrizeCategorySelector lives in competition/ — out-of-scope unstated. Falsifying condition: grep PrizeCategorySelector returns hits in competition/ directory.' Recommendation: REVISE.",
      "files": []
    },
    {
      "id": 3,
      "name": "clean-gem-bump",
      "prompt": "Review this plan: bump rubocop dependency from 1.60 to 1.65 in Gemfile, run bundle update, run full test suite, commit. Approve?",
      "expected_output": "B0 = Clear. Quick tier selected (appetite <1hr, no one-way doors). Most buckets OVERTURNED. B8 pre-mortem identifies 'rubocop rule changes break CI' as low-likelihood. Recommendation: APPROVE.",
      "files": []
    },
    {
      "id": 4,
      "name": "schema-migration-no-rollback",
      "prompt": "Review this plan: add NOT NULL column user_tier to users table (50M rows), backfill from subscription_status, deploy in next release. Approve?",
      "expected_output": "Full tier (touches production data + schema migration is one-way door). B5 SUSTAINED 'no Alternatives section, no ADR for migration approach'. B6 SUSTAINED 'no rollback path named, no metrics for backfill progress'. Recommendation: REVISE.",
      "files": []
    },
    {
      "id": 5,
      "name": "redis-cache-solutionism",
      "prompt": "Review this plan: introduce Redis as caching layer in front of Postgres for product catalog reads. Approve?",
      "expected_output": "B1 SUSTAINED 'plan opens with solution (Redis) — no problem statement, no latency target, no current-pain measurement'. B6 SUSTAINED 'no success metric named'. Recommendation: REVISE — demand problem statement + measurable target before approving.",
      "files": []
    }
  ]
}
```

---

### Verification (implementation-side)

After implementation, verify in this order:

1. **Install correctness**
   - `bash /Users/anton/src/pde-skills/install.sh`
   - `~/.claude/commands/pde/plan-review.md` exists with absolute `@/Users/...` path
   - `/pde:plan-review` appears in restart message

2. **Skill loads in fresh session**
   - Restart Claude Code
   - `/pde:plan-review` with no args asks for the plan, doesn't error
   - Run `/pde:plan-review` against a real plan (e.g., the AI thesis project's
     `PHASE5-KICKOFF.md`) as a dry-run

3. **Catches the flagged failures retrospectively (evals 1, 2, 4, 5)**
   - Each eval should SUSTAIN its target finding. If any fails to catch,
     revise the relevant bucket prompt before shipping.

4. **No false positive on clean plan (eval 3)**
   - Should APPROVE. If REVISE / KILL, buckets are over-aggressive.

5. **Tier auto-selection works**
   - Eval 1 (roadmap, 1-quarter appetite, multiple themes) → Full
   - Eval 2 (Vue removal, ~1-day appetite, no one-way doors) → Quick
   - Eval 3 (gem bump, <1hr, fully reversible) → Quick
   - Eval 4 (schema migration, prod data, one-way door) → Full
   - Eval 5 (Redis intro, vendor + cache layer = one-way door) → Full
   - User-override flag works in both directions

6. **MECE self-test on the 8 buckets**
   - For each pair (B1↔B2, B2↔B3, B3↔B4, B4↔B5, B5↔B6, B6↔B7), name a
     candidate finding and confirm exactly one bucket owns it. If a finding
     lands cleanly in two, tighten the bucket boundary in SKILL.md.

7. **Documentation**
   - `using-this-pack/SKILL.md` includes routing line: "I have a plan, should
     I trust it?" → `plan-review`
   - `PROJECT_PLAN.md` reflects #14 in-progress and #19 deferred

8. **Optional — skill-creator eval loop**
   - Run with-skill + baseline runs in parallel for 5 evals
   - Generate `benchmark.json` + viewer per skill-creator workflow
   - Capture iteration-1 results in
     `pde-skills/skills/engineering/plan-review-workspace/iteration-1/`

### Out of scope (explicitly)

- ExitPlanMode auto-fire hook (deferred to v2)
- Sub-agent extraction (deferred — Known Limits has the revisit trigger)
- Roadmap-review split (deferred — Known Limits has the revisit trigger)
- `references/` subdirectory (only if SKILL.md crosses 400 lines)
- Description-optimization eval loop (deferred to post-v1)
