---
name: writing-refinement
description: Refine plans, engineering design docs, OKRs, milestones, user stories, and task lists into clear, minimal, high-impact prose. Use this skill whenever the user is drafting, writing, reviewing, or refining a plan, design doc, RFC, project proposal, OKR set, milestone list, ticket, user story, or any project/engineering writeup — even if they don't explicitly ask for "refinement" or "editing". Also use when the user asks to "clean up", "tighten", "make this clearer", or "rewrite" technical or planning text.
---

# Writing Refinement

## Purpose

Turn loose thinking into a document that moves an idea exactly from one mind to another: logically sound, ruthlessly concise, and humanly readable.

Work through the six phases **in order**. Each phase produces a checkable intermediate artifact — do not advance until the current phase's "Done when" holds. For a short document (a single ticket, a few OKRs) the intermediates can live in your head or a few scratch lines; for a design doc or plan, write them out before drafting prose. Each phase is a single objective with its own "Done when"; do not collapse several phases into one "refine this" pass — a single broad pass satisfices, fixing a few obvious words and stopping there.

## Two modes: author and review

Run this skill in one of two modes. Pick the mode first; the routing table and six phases apply to both.

- **Author mode** — you are producing the document. Run Phases 1→6 forward.
- **Review mode** — you are refining a document that already exists (another agent's draft, or your own from an earlier turn). The trap is that prose reads clearer to whoever holds the meaning in their head than it does on the page; reading the draft first lets it set your standard. **Load `references/style-rules.md` and the matching type reference *before* you read the draft** — form the standard first, then test the draft against it, so you judge the prose rather than rationalise it.

Review-mode output is a verdict plus line-level fixes, not a rewrite-in-place:

- **Verdict:** `accept` / `accept with notes` / `reject`.
- **Findings:** each numbered, with the exact quoted span, the rewrite, and the one rule it breaks.
- **Verdict rule:** `reject` when *any* load-bearing span fails a Phase-1–4 rule — a goal, milestone, heading, or task that reads as a label or names no work product, a missing SCQA spine, a fact restated across three or more sections, or no 30-second main point. One such failure is enough; these are the spans the document is built on. `accept with notes` when no Phase-1–4 failure survives and only Phase-5 vocabulary/polish findings remain — an isolated awkward sentence or a watchlist word is a note, not a rejection. `accept` only when no finding survives. A clean `accept` with zero findings on a draft longer than a few lines is itself a signal the read was shallow, so re-scan before declaring it.

Review mode runs Phases 1–6 as **checks against the draft**, not as drafting steps — transpose each phase into the question it answers:

- Phase 1 — does an SCQA spine exist, and do R1/R2 each carry a number or a visualizable end product? (For a task/bug, only the Answer need survive — see Phase 1.)
- Phases 2–3 — are the groups MECE, the headings achievements, every section point-first, every sentence old-before-new?
- Phase 4 — the redundancy pass: build the fact ledger, emit one finding per restated fact (see Phase 4).
- Phase 5 — the `style-rules.md` line sweep.
- Phase 6 — the final gate, reported as the verdict above.

The matching type reference adds its own review checklist on top of these — read it before judging.

For a heavier fresh-context review — an adversarial sub-agent dispatched automatically before a draft reaches the user — use the companion persona `agents/writing-editor/AGENT.md`, which adds the adversarial review posture and the author's-rationalisations table on top of these phases. The two share one source of rules: this skill's `references/`.

## Long documents: run the passes as distinct steps

For anything longer than roughly two pages, do not attempt one combined refinement. Run the objectives as separate passes, each to its own "Done when":

1. Phases 1–3 once, on the whole document (structure).
2. **Phase 4 once, on the whole document** — the redundancy pass needs the entire draft in view; never chunk it.
3. Phase 5 chunkable — sweep the line rules section by section.
4. Phase 6 once, as the final gate.

For a very long draft, dispatch Phase 4 to the `agents/writing-editor/AGENT.md` sub-agent, whose sole instruction is the redundancy pass — a fresh context cannot satisfice on structure or wording and call the document done.

## Before Phase 1: route by document type

Identify what is being written, then read the matching reference file for its templates and bad/good examples:

| Document type                            | Reference                                                          |
| ---------------------------------------- | ------------------------------------------------------------------ |
| Project plan, goals, OKRs, milestones    | `references/plans-okrs.md`                                         |
| Engineering design doc / RFC             | `references/design-docs.md`                                        |
| Tasks, user stories, bugs, refactors     | `references/tasks.md`                                              |
| Plan-mode plan, idea one-pager, proposal | `references/plans-and-ideas.md`                                    |
| **Anything else**                        | **No type reference — run Phases 1–6 with `style-rules.md` only.** |

Read `references/style-rules.md` in every case — it governs Phase 5 for all document types. The six phases are type-agnostic; only the templates and examples are type-specific. Never refuse a document for lacking a dedicated reference — fall through to the default row and run the same six phases.

## Phase 1 — Architectural definition (the "why")

Before writing any prose, define the document's logical boundary as a four-line SCQA block:

1. **Situation** — a noncontroversial fact about the subject, anchored in time or place, that the reader will immediately accept as true.
2. **Complication** — what disturbed that stability. This reveals the Undesired Result (**R1**) and its palpable cost.
3. **Desired Result (R2)** — the success state, stated quantifiably or as a visualizable end product.
4. **Question → Answer** — the specific question the complication raises, and a one-sentence answer. The answer is the document's Main Point.

**Done when:** the SCQA block exists; R1 and R2 each contain a number or a concrete, visualizable end product (the *hand-product test* — the reader can picture a tangible result; it recurs in Phases 4 and 5 under the same name); the Answer is one sentence.

**If the source material lacks a number the workflow requires, never invent one.** Insert a bracketed placeholder the owner must fill — "from [current P95: __ ms] to under 800ms" — or, in an interactive session, ask. A plausible fabricated metric is worse than a visible gap.

**For a single task, bug, or refactor, collapse SCQA to its Answer.** These artefacts inherit the SCQA of the plan or ticket above them; re-deriving a Situation and Complication for each one is busywork. Keep only the Answer — the one-sentence statement of the work and its verifiable end product (the "Done when"). Do not reject a task or bug for lacking a Situation/Complication block. Full SCQA applies to documents that stand alone: plans, design docs, OKR sets, one-pagers.

## Phase 2 — Logical synthesis (the pyramid)

Organize the supporting ideas under the Answer:

1. **Build the key line.** Group the ideas that support the Answer. Every item in a group must be the same kind of idea — all reasons, all steps, or all problems, never a mix.
2. **Apply MECE.** Groups must be Mutually Exclusive (no overlaps — "Security" and "Authentication" overlap; "Identity Management" and "Data Encryption at Rest" do not) and Collectively Exhaustive (no gaps).
3. **Declare an ordering principle** for each group: **Time** (sequential steps), **Structure** (parts of a whole, e.g. frontend/backend), or **Degree** (ranked by impact).
4. **State each fact once, at outline time.** Give every fact, number, and decision exactly one home in the outline. If two groups both want the same fact, the groups overlap — fix the MECE split, do not copy the fact into both. A first draft that states each fact once needs far less cutting in Phase 4.

**Done when:** an outline exists; each group has one declared ordering principle; no two groups overlap; no fact is assigned to more than one group; every sub-point answers "How?" or "Why?" about its parent's summary effect.

## Phase 3 — Global coherence (the narrative flow)

1. **Write the SCQ introduction.** Lead the reader from known (Situation) to unknown (Complication) to your solution (Answer) — as flowing prose. **Never use "Situation", "Complication", "Question", "SCQ", "MECE", "R1", or "R2" as headers or terms in the output document.** These are scaffolding; the reader must never see them. The introduction *reminds* the reader of facts they already accept before it reveals the problem — it brings in no new data or exhibit the reader must verify to accept the premise.
2. **Open every unit with a point sentence.** Each section and paragraph starts with a short sentence stating its summary effect; complexity follows.
3. **Headings are achievements, not labels.** "Migrated user records to a sharded Postgres cluster", not "Phase 2" or "Data". A heading should contain a verb or a result.
4. **Old before new.** Start sentences with information the reader already has; place new or complex technical information at the end, where the stress position gives it emphasis.

**Done when:** the intro flows problem → solution with no framework vocabulary; every heading states a result; each section's first sentence is its point.

## Phase 4 — Redundancy and concision (the whole-document pass)

This is the single most valuable pass on a long draft, and the one a per-paragraph sweep cannot do: you cannot tell a fact is restated unless you hold the whole document at once. Run it on the complete draft, in one objective — cut everything that earns no new work — before the line-level sweep. Do not interleave it with Phase 5; a paragraph you are about to delete is not worth polishing.

1. **Build a fact ledger.** Read the whole draft and list every distinct claim, decision, number, and definition once, with every location it appears: "P95 is 4.1s → §Problem, §Constraints, §Rollout". The ledger makes restatement visible that prose hides.
2. **Merge to one home.** For each fact stated in more than one place, pick the single section where the reader most needs it and cut it everywhere else. Replace a needed back-reference with a pointer ("see §Problem"), not a restatement. The first place a fact appears is usually not its best home — put it where the reader uses it.
3. **Cut to the standard, not to a line count:**
   - The main point must be graspable in 30 seconds — the Answer and the shape of the solution, before any detail.
   - Expect to cut roughly half of a first draft. If you have cut almost nothing, you have not looked hard enough.
   - Every word must do new work. A sentence that restates the previous one, gives an example the reader already inferred, or hedges a claim already made is clutter — delete it.
   - One fact, stated once.

**Guard against over-cutting.** This pass removes *repetition*, not *content*. The unit of redundancy is the **fact**, not the **sentence**: a dependency, risk, assumption, or constraint stated once is never redundant, however cuttable it looks — keep it (see `references/style-rules.md`, the pruning safety rule). Two sections that each state the rollback criteria are redundant; merge to one home. A section stating the rollback criteria and another stating the monitoring thresholds are two facts; keep both.

**Done when:** the fact ledger shows no claim with more than one home (back-references excepted); the main point is graspable in the first 30 seconds of reading; no paragraph survives that a reader could delete without losing a fact; and every dependency, risk, assumption, and constraint from the ledger is still present, exactly once.

**In review mode, this pass emits findings, not a rewrite.** For each restated fact, emit one finding: the quoted span at each location, the recommended single home, and the rule ("one fact, one home"). Example: *"P95 = 4.1s appears in §Problem, §Constraints, and §Rollout → keep in §Problem, replace the other two with 'see §Problem'."* A document carrying any fact with three or more homes, or with no 30-second main point, is `reject` — these are structural failures, the same severity tier as a missing SCQA spine.

## Phase 5 — Sentence-level pruning (clarity and precision)

Sweep `references/style-rules.md` over the draft line by line — that file owns the rules, examples, and watchlist. It covers characters-as-subjects, reversing nominalizations, deleting clutter and throat-clearing, the vocabulary watchlist, and the one rule that overrides the rest: **prune without amputating** — concision must never remove an essential dependency, risk, assumption, or constraint. If a "wordy" sentence carries an operational fact, compress it; don't cut it.

**Done when:** zero watchlist words remain; no nominalizations where a verb works; every task or goal passes the hand-product test (the reader can visualize a tangible end product).

## Phase 6 — Final review gate

Run the cheap mechanical checks first, then the judgment checks:

**Mechanical:**

- [ ] No framework vocabulary (SCQ, MECE, R1/R2, "Complication") appears in the output.
- [ ] No watchlist words survive.
- [ ] No fact, number, or decision is stated in more than one place (back-references excepted).
- [ ] The main point is graspable in the first 30 seconds — the Answer and solution shape come before the detail.
- [ ] No live decorative metaphor survives (`style-rules.md` ban-list); conventional technical terms are left alone.
- [ ] Every heading contains a verb or a result.
- [ ] The newest or most important technical term in each sentence sits in its final clause (stress position).
- [ ] *(task/plan docs only)* Every task has a "Done when" with a visualizable, verifiable end product.
- [ ] *(task/plan docs only)* Every task with more than three distinct moves is split, unless the moves must ship atomically.

**Judgment:**

- [ ] **Narrative:** the document flows from problem to solution as one story of "where we are" and "what we are doing", not a sterile list of data points.
- [ ] **Logic:** sub-points answer "How?" or "Why?" about their parents.
- [ ] **Completeness without repetition:** every assumption, risk, and dependency survived the cut — and appears exactly once, not restated across sections.
- [ ] **So what:** every section states the cost of the status quo, so the reader is motivated to care.
- [ ] **Human:** it reads like a professional talking to a colleague, not a machine generating "communication facilitation".

If any check fails, return to the relevant phase, fix it, and re-run the gate.
