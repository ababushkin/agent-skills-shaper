---
name: writing-refinement
description: Refine plans, engineering design docs, OKRs, milestones, user stories, and task lists into clear, minimal, high-impact prose. Use this skill whenever the user is drafting, writing, reviewing, or refining a plan, design doc, RFC, project proposal, OKR set, milestone list, ticket, user story, or any project/engineering writeup — even if they don't explicitly ask for "refinement" or "editing". Also use when the user asks to "clean up", "tighten", "make this clearer", or "rewrite" technical or planning text.
---

# Writing Refinement

Turn loose thinking into a document that moves an idea exactly from one mind to another: logically sound, ruthlessly concise, and humanly readable.

Work through the five phases **in order**. Each phase produces a checkable intermediate artifact — do not advance until the current phase's "Done when" holds. For a short document (a single ticket, a few OKRs) the intermediates can live in your head or a few scratch lines; for a design doc or plan, write them out before drafting prose.

## Two modes: author and review

Run this skill in one of two modes. Pick the mode first; the routing table and five phases apply to both.

- **Author mode** — you are producing the document. Run Phases 1→5 forward.
- **Review mode** — you are refining a document that already exists (another agent's draft, or your own from an earlier turn). The author who wrote it cannot see its prose failures: the meaning is in their head, so the page reads clearer to them than it is. You hold no such investment. **Load `references/style-rules.md` and the matching type reference *before* you read the draft** — form the standard first, then test the draft against it, so you judge the prose rather than rationalise it.

Review-mode output is a verdict plus line-level fixes, not a rewrite-in-place:

- **Verdict:** `accept` / `accept with notes` / `reject`.
- **Findings:** each numbered, with the exact quoted span, the rewrite, and the one rule it breaks.
- **Verdict rule:** `reject` when a load-bearing span fails a Phase-1–3 rule (a goal, milestone, heading, or task that reads as a label or names no work product). `accept with notes` when only Phase-4 vocabulary/polish findings remain. `accept` only when no finding survives — and a clean `accept` with zero findings on a substantial draft is itself a signal the read was shallow, so re-scan before declaring it.

Review mode runs Phases 1–5 as **checks against the draft**, not as drafting steps: Phase 1 — does an SCQA spine exist and do R1/R2 carry a number or visualizable end product? Phases 2–3 — MECE groups, achievement headings, point-first sections, old-before-new? Phase 4 — the `style-rules.md` line sweep. Phase 5 — the final gate, reported as the verdict above.

For a heavier fresh-context review — an adversarial sub-agent dispatched automatically before a draft reaches the user — use the companion persona `agents/writing-editor/AGENT.md`, which adds the adversarial review posture and the author's-rationalisations table on top of these phases. The two share one source of rules: this skill's `references/`.

## Before Phase 1: route by document type

Identify what is being written, then read the matching reference file for its templates and bad/good examples:

| Document type | Reference |
|---|---|
| Project plan, goals, OKRs, milestones | `references/plans-okrs.md` |
| Engineering design doc / RFC | `references/design-docs.md` |
| Tasks, user stories, bugs, refactors | `references/tasks.md` |
| Plan-mode plan, idea one-pager, proposal | `references/plans-and-ideas.md` |
| **Anything else** | **No type reference — run Phases 1–5 with `style-rules.md` only.** |

Read `references/style-rules.md` in every case — it governs Phase 4 for all document types. The five phases are type-agnostic; only the templates and examples are type-specific. Never refuse a document for lacking a dedicated reference — fall through to the default row and run the same five phases.

## Phase 1 — Architectural definition (the "why")

Before writing any prose, define the document's logical boundary as a four-line SCQA block:

1. **Situation** — a noncontroversial fact about the subject the reader will immediately accept as true.
2. **Complication** — what disturbed that stability. This reveals the Undesired Result (**R1**) and its palpable cost.
3. **Desired Result (R2)** — the success state, stated quantifiably or as a visualizable end product.
4. **Question → Answer** — the specific question the complication raises, and a one-sentence answer. The answer is the document's Main Point.

**Done when:** the SCQA block exists; R1 and R2 each contain a number or a concrete, visualizable end product; the Answer is one sentence.

**If the source material lacks a number the workflow requires, never invent one.** Insert a bracketed placeholder the owner must fill — "from [current P95: __ ms] to under 800ms" — or, in an interactive session, ask. A plausible fabricated metric is worse than a visible gap.

## Phase 2 — Logical synthesis (the pyramid)

Organize the supporting ideas under the Answer:

1. **Build the key line.** Group the ideas that support the Answer. Every item in a group must be the same kind of idea — all reasons, all steps, or all problems, never a mix.
2. **Apply MECE.** Groups must be Mutually Exclusive (no overlaps — "Security" and "Authentication" overlap; "Identity Management" and "Data Encryption at Rest" do not) and Collectively Exhaustive (no gaps).
3. **Declare an ordering principle** for each group: **Time** (sequential steps), **Structure** (parts of a whole, e.g. frontend/backend), or **Degree** (ranked by impact).

**Done when:** an outline exists; each group has one declared ordering principle; no two groups overlap; every sub-point answers "How?" or "Why?" about its parent's summary effect.

## Phase 3 — Global coherence (the narrative flow)

1. **Write the SCQ introduction.** Lead the reader from known (Situation) to unknown (Complication) to your solution (Answer) — as flowing prose. **Never use "Situation", "Complication", "Question", "SCQ", "MECE", "R1", or "R2" as headers or terms in the output document.** These are scaffolding; the reader must never see them.
2. **Open every unit with a point sentence.** Each section and paragraph starts with a short sentence stating its summary effect; complexity follows.
3. **Headings are achievements, not labels.** "Migrated user records to a sharded Postgres cluster", not "Phase 2" or "Data". A heading should contain a verb or a result.
4. **Old before new.** Start sentences with information the reader already has; place new or complex technical information at the end, where the stress position gives it emphasis.

**Done when:** the intro flows problem → solution with no framework vocabulary; every heading states a result; each section's first sentence is its point.

## Phase 4 — Sentence-level pruning (clarity and precision)

Apply `references/style-rules.md` line by line:

1. **Characters as subjects, actions as verbs.** Make the doer (system, user, or developer) the grammatical subject and its activity a specific verb. "The load balancer drops requests above 1k RPS", not "Request dropping occurs at high utilization."
2. **Reverse nominalizations.** Turn *utilization, implementation, optimization, investigation* back into *use, implement, optimize, investigate*.
3. **Delete clutter.** Remove little qualifiers (*basically, actually, quite, a bit, virtually*), redundant pairs (*full and complete*), and throat-clearing (*It should be noted that…*). Sweep the vocabulary watchlist in `style-rules.md`.
4. **Prune without amputating.** Concision must never remove essential dependencies, risks, assumptions, or constraints. If a "wordy" sentence carries an operational fact, compress it — don't cut it.

**Done when:** zero watchlist words remain; no nominalizations where a verb works; every task or goal passes the hand-product test (the reader can visualize a tangible end product).

## Phase 5 — Final review gate

Run the cheap mechanical checks first, then the judgment checks:

**Mechanical:**
- [ ] No framework vocabulary (SCQ, MECE, R1/R2, "Complication") appears in the output.
- [ ] No watchlist words survive.
- [ ] Every heading contains a verb or a result.
- [ ] Every task has a "Done when" with a visualizable, verifiable end product.
- [ ] The newest or most important technical term in each key sentence sits in its final clause (stress position).

**Judgment:**
- [ ] **Narrative:** the document flows from problem to solution as one story of "where we are" and "what we are doing", not a sterile list of data points.
- [ ] **Logic:** sub-points answer "How?" or "Why?" about their parents.
- [ ] **Completeness:** assumptions, risks, and dependencies survived the pruning.
- [ ] **So what:** every section states the cost of the status quo, so the reader is motivated to care.
- [ ] **Human:** it reads like a professional talking to a colleague, not a machine generating "communication facilitation".

If any check fails, return to the relevant phase, fix it, and re-run the gate.
