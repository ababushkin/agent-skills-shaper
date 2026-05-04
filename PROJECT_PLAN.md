# pde-skills — Project Plan v1.6

**Owner:** Anton Babushkin (`ababushkin`)
**Repo:** `pde-skills` (public, MIT licensed)
**Tagline:** Workflow skills for the small product-design-engineering team — including the team of one.
**Status:** ready for kickoff

A multi-agent project to author an open-source skill pack covering product and engineering workflow disciplines, grounded in the owner's authored principles. Soft fork of [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills): inherits structural conventions, improves where the owner's principles demand. Where a skill has a counterpart in addy's, the relationship is named explicitly; where it's new, it stands alone. Design pack is out of scope for v0.1.

The pack ships three artefact categories. **Skills** are workflows agents invoke when triggered. **Hooks** are mechanical checks that run on events (commit, PR, completion claim) to catch failure modes the agent has every reason not to flag against itself. **Sub-agent personas** are adversarial review passes with fresh context and no investment in the original work. The principle-to-artefact mapping is many-to-many: a single principle may be embedded across several skills, enforced by a hook, and verified by a sub-agent.

This file is the operational spine — the roadmap, structure, and rules an agent needs to execute the build. Owner-side content (strategic framing, OKRs, risks, deliverables checklist, triage rationales) lives in `PROJECT_GOVERNANCE.md`. Authoring specs live under `docs/`. Both are referenced where relevant.

---

## 1. Each artefact must

- Trace to one or more named principles in source documents (`roadmap_principles`, `eng-principles-universal`, `eng-principles-agentic`, PM rules-of-engagement). Engineering principles are two-tier: tier 1 universal, tier 2 agentic.
- Match the voice and register of the source documents — direct, dense, opinionated, citation-bearing. Plain language, no jargon-as-rigor.
- Stay stack-agnostic, with placeholder commands where stack-specific behaviour is needed.
- Produce its outputs under `docs/` in artefact-appropriate subdirectories.
- Land in the size range appropriate to its category (see `docs/skill-anatomy.md`, `docs/hook-anatomy.md`, `docs/sub-agent-anatomy.md`).
- Honestly declare its relationship to addy's pack — predecessor, what was kept, what was changed.
- Be honest about *when* it should and shouldn't be invoked.

Most principles end up *embedded* inside existing skills as red flags, rationalisation rebuttals, or gates — not as their own artefact. A principle earns its own standalone artefact only when it has a workflow (skill), a mechanically-verifiable failure mode (hook), or a structural reason the original agent won't catch its own failure (sub-agent). One skill traces to multiple principles; one principle is enforced across multiple skills, hooks, and sub-agents.

---

## 2. Non-goals

- Stack-specific tooling — no `npm`, `tsc`, `pip`, or other concrete commands baked in. Placeholders only.
- Slash commands and runtime wiring — hooks ship as specs, not as integrations.
- Hook runtime integration testing — verifying hooks catch what they claim is v0.2 work.
- Direct copy of addy's skill content — read it as input, author fresh.
- Multi-language support — English only.
- Tooling for the pack itself — no CLI, validator, or installer.
- Later items — only Now and Next from §3 are in scope.

(Owner-decision non-goals — trial use during project, design pack scope, hard fork choice, visual identity — are recorded in `PROJECT_GOVERNANCE.md`.)

---

## 3. Roadmap

Now / Next / Later format. Phase-and-quarter framing is the false-precision pattern Roadmap Principle 7 was written to replace.

**Predecessor relations:**
- `derivative` — addy has a counterpart we're improving on.
- `adjacent` — addy has loosely related material; we're authoring something he doesn't really have.
- `new` — no counterpart in addy's pack.

Addy's pack has skills only. Most hooks and sub-agents are therefore `new` or `adjacent`, not `derivative`.

### Now (8 items — the Now budget is set at 8; appetite is a cap, not a target)

| # | Artefact | Category | Pack | Lifecycle | Length | Predecessor |
|---|---|---|---|---|---|---|
| 1 | `PRODUCT_RULES.md` | rules | product (root) | reference | ~200 | `new` |
| 2 | `idea-triage` | skill | product | define | 200–280 | `adjacent` |
| 3 | `eng-principles-universal.md` | rules | engineering (root) | reference | ~250 | `new` |
| 4 | `eng-principles-agentic.md` | rules | engineering (root) | reference | ~150 | `new` |
| 5 | `design-doc` | skill | engineering | define | 250–300 | `derivative` (improves on `spec-driven-development`) |
| 6 | `incremental-implementation` | skill | engineering | build | 180–230 | `derivative` (refinement: walking-skeleton-first) |
| 7 | `stop-the-line` | hook | engineering | build/verify | 60–100 | `new` |
| 8 | README routing section | meta | meta | meta | n/a | derivative of `using-agent-skills` philosophy |

`eng-principles-agentic.md` is sequential dependency on universal. `idea-triage` absorbs the problem-reframe gate (Roadmap A2/A3). `stop-the-line` traces primarily to Eng Agentic Principle 6 and is the pack's first hook.

### Next (11 items)

| # | Artefact | Category | Pack | Lifecycle | Length | Predecessor |
|---|---|---|---|---|---|---|
| 9 | `using-this-pack` | skill | meta | meta | 130–180 | `derivative` |
| 10 | `planning-and-task-breakdown` | skill | engineering | plan | 200–260 | `derivative` |
| 11 | `roadmap-shape` | skill | product | define | 150–220 | `new` |
| 12 | `small-batch` | hook | engineering | ship | 60–100 | `new` |
| 13 | `evidence-claim` | hook | meta | verify | 60–100 | `new` |
| 14 | `plan-review` (was `problem-first-reviewer`) | skill | engineering | define | 320–400 | `derivative` (predecessor: internal phase4-devils-advocate) — **in-progress** |
| 15 | `prototype-to-validate` | skill | engineering | define (discovery) | 180–240 | `new` |
| 16 | `spike` | skill | engineering | build (discovery) | 130–180 | `new` |
| 17 | `deploy` | skill | engineering | ship | 200–280 | `derivative` |
| 18 | `post-launch-impact-review` | skill | engineering | verify-outcome | 150–200 | `new` |
| 19 | `roadmap-review` | skill | product | review | 180–230 | `new` (partially absorbed by `plan-review` #14 — revisit after ≥5 plan-review uses against roadmaps) |

Promotion criteria: capacity opens, item still earns its slot against current evidence at promotion time, no Now item displaces it. Hooks promote in order — `small-batch` and `evidence-claim` only after `stop-the-line` proves the failure-mode-detection pattern works. `problem-first-reviewer` promotes when `design-doc` has enough usage to know whether the embedded constraint catches problem-first violations on its own.

### Later

Tracked in `POST_V0.1_BACKLOG.md`. Not pre-committed. Each entry carries its triage rationale (in `PROJECT_GOVERNANCE.md` §8.3).

### References

Stored under `references/`, cited by skills, authored alongside their citing skills:
- `confidence-meter.md`, `ice-scoring.md`, `kano-classification.md`, `portfolio-themes.md`, `nfr-categories.md`, `dora-metrics.md`

---

## 4. Repository structure

```
pde-skills/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LEARNINGS.md
├── POST_V0.1_BACKLOG.md
├── docs/
│   ├── skill-anatomy.md
│   ├── hook-anatomy.md
│   ├── sub-agent-anatomy.md
│   ├── brief-template.md
│   └── authoring-learnings.md
├── references/
│   ├── confidence-meter.md
│   ├── ice-scoring.md
│   ├── kano-classification.md
│   ├── portfolio-themes.md
│   ├── nfr-categories.md
│   └── dora-metrics.md
├── skills/
│   ├── product/
│   │   ├── PRODUCT_RULES.md
│   │   └── idea-triage/SKILL.md
│   └── engineering/
│       ├── eng-principles-universal.md
│       ├── eng-principles-agentic.md
│       ├── design-doc/SKILL.md
│       └── incremental-implementation/SKILL.md
├── hooks/
│   └── stop-the-line/HOOK.md
└── agents/   # populated when sub-agents promote
```

During authoring, each artefact directory contains `_workspace/` with brief, draft, review, consistency notes. Deleted before merge.

---

## 5. Authoring conventions

### 5.1 Anatomy

See:
- `docs/skill-anatomy.md` — for skills, including `SKILL.md` frontmatter
- `docs/hook-anatomy.md` — for hooks
- `docs/sub-agent-anatomy.md` — for sub-agent personas

Root rules files (`PRODUCT_RULES.md`, `eng-principles-universal.md`, `eng-principles-agentic.md`) mirror the shape of their source principles documents.

The v0.1 rules files are direct conversions of existing principles documents (`roadmap_principles`, `eng_principles`) into pack voice and structure, not original authoring work. The substantive principles are settled. Authoring effort is voice-matching, the tier-1/tier-2 carve-out for the engineering files, and structural alignment with the rest of the pack. These artefacts take the fast-path workflow (see §7).

### 5.2 Voice and register

- Direct, dense, opinionated. No hedging language.
- Plain language. No jargon-as-rigor — "structured placement act" instead of "putting things on the roadmap" is the failure mode.
- Citations to canonical sources where claims are made. Match the citation style of the source documents.
- Sentence-case headings.
- Prose over bullets where prose works.
- No emoji.
- Short sentences where possible. Long sentences where the idea actually requires them.

The voice is the owner's own (matched to source documents), not a continuation of addy's voice. Where an artefact is derivative, structure may inherit but voice does not.

### 5.3 Content rules

- Every claim about practice traces to either a source document principle or a citable external authority.
- Every workflow step is concrete enough that an agent or human could execute it without further interpretation.
- Every gate is testable.
- Stack-agnostic. Placeholders: `<test-command>`, `<lint-command>`, `<deploy-command>`.
- Artefact paths under `docs/` are explicit and consistent.

### 5.4 Length discipline

- Skills: 100–300 lines target. Hard cap 350. Beyond that, split.
- Hooks: 60–100 lines target. Beyond 100, likely a skill in disguise.
- Sub-agent personas: 150–200 lines target. Hard cap 250.
- Root rules files: mirror source principles documents. No hard cap.

### 5.5 Relationship to prior art

For derivative and adjacent artefacts:
- Author reads predecessor as input before drafting.
- Brief identifies what's worth keeping conceptually and what's being changed.
- Frontmatter `kept_from_predecessor` and `changed_from_predecessor` populated honestly.
- No paragraph is a verbatim copy of the predecessor.
- Editor verifies relationship is honest and no copy-paste.

For `new` artefacts: predecessor.relation = `new`, `kept`/`changed` = `n/a`.

### 5.6 Size-the-work rubric

Canonical home is `README.md`. Until `using-this-pack` promotes from Next, `README.md` is the only place the rubric lives. No artefact invents the rubric — they reference the README copy.

---

## 6. Team structure

Five agent roles. Defined by responsibility, not by which model runs them. Implementation via Claude Code subagents/teams.

### 6.1 Supervisor

- Owns `PROJECT_STATE.md` — source of truth for which artefacts are in flight, in review, accepted, blocked.
- Dispatches authors when a brief is ready.
- Dispatches editors when a draft is ready.
- Dispatches the consistency checker when an editorial pass is complete.
- Decides escalations (when editor and author disagree, breaks the tie or escalates to owner).
- Runs final integration pass at end of project.

### 6.2 Author (2 agents in parallel across disciplines)

- Reads the brief in `_workspace/brief.md` if one exists. For artefacts whose substance is already settled (rules files derived from existing principles documents, or any artefact where a brief would be theatre), reads the relevant sections of `PROJECT_PLAN.md`, the source principles documents, and prior conversation context directly. The supervisor flags which path applies at dispatch.
- Reads relevant source documents and prior accepted artefacts.
- Reads the relevant anatomy spec under `docs/`.
- For derivative or adjacent artefacts: reads predecessor in addy's pack.
- Writes `_workspace/draft-v1.md` conforming to anatomy.
- Responds to editor feedback in `_workspace/draft-v2.md`, etc.

Constraints: two authors run in parallel only on different artefacts. Within a discipline, authoring is sequential (each artefact informs the next). Across disciplines, parallel.

### 6.3 Editor

Reads `_workspace/draft-vN.md` against the brief and the relevant anatomy spec. Writes `_workspace/editor-notes.md` with structured findings. Returns `accept`, `accept with notes`, or `reject`. Max 3 editorial rounds before escalating to supervisor.

**Reject triggers (automatic):**

- Artefact does not trace to ≥1 named principle (with bucket assignment).
- Voice does not match source documents.
- Jargon-as-rigor — formal-sounding prose that obscures a simple idea.
- Required section missing from anatomy.
- Stack-prescriptive content where stack-agnostic is expected.
- Over the length cap for the artefact category with no justification.
- Predecessor relation declared but `kept`/`changed` fields empty.
- Verbatim text from addy's pack found in the draft.
- Skill silent on its triggers / when not to fire.
- Hook fail criteria not deterministic (uses "probably", "usually", "consider whether").
- Hook over 100 lines without justification.
- Sub-agent missing the "review posture" or "context to load" sections.
- Embedded-everywhere principles (Eng Universal 5, Eng Agentic 5) not naming three load-bearing homes.
- Two artefacts duplicate the same workflow without explicit `Out of scope` boundaries.
- Confidence claims in triage records that don't cite specific personal-usage evidence.

### 6.4 Consistency checker

Runs after editorial accept. Reads new artefact against all previously-accepted ones. Writes `_workspace/consistency-notes.md` checking:

- Redundancy with existing artefacts.
- Boundary clarity in `Out of scope` sections.
- Cross-references actually linked.
- Vocabulary consistency.
- Coverage gaps.
- Routing consistency with the size-the-work rubric.

Returns `accept` or `revise`.

### 6.5 Owner

Final acceptance on every artefact, brief authoring, escalation resolution, PR merges. (Detailed bottleneck management: see `PROJECT_GOVERNANCE.md` §5.)

### 6.6 Handoff pattern

Filesystem-as-message-bus, git-as-state-machine.

- One git branch per artefact (`skill/<name>`, `hook/<name>`, `agent/<name>`).
- One `_workspace/` directory per artefact during authoring.
- State transitions are git commits with structured messages:
  - `[author] draft v1 ready for editorial`
  - `[editor] notes ready for author revision`
  - `[editor] accepted, ready for consistency check`
  - `[consistency] accepted, ready for owner sign-off`
  - `[supervisor] merged to main`
- Supervisor watches the latest commit on each in-flight branch and dispatches the next agent.
- One PR per artefact at the end. Owner is the only person who merges.

---

## 7. Workflow per artefact

Two paths. The supervisor decides at dispatch which applies.

**Default path** — substance not yet settled. Most skills, hooks, and sub-agents.

```
1. BRIEF       owner approves brief drafted by agent (substance from owner,
                 drafting by agent — see §10), commit
2. AUTHOR v1   author reads brief (and predecessor if derivative/adjacent),
                 writes draft-v1.md, commits
3. EDITOR      editor reviews, writes editor-notes.md, commits
                 → if reject: back to AUTHOR for v2 (max 3 rounds)
                 → if accept: continue
4. CONSISTENCY consistency checker reviews against pack, commits
                 → if revise: back to AUTHOR for v_next
                 → if accept: continue
5. PROMOTE     supervisor promotes draft-vN to <ANATOMY>.md, deletes _workspace/, commits
6. PR          supervisor opens PR
7. SIGN-OFF    owner reviews PR, merges
```

**Fast-path** — substance already settled. v0.1 rules files (direct conversions of existing principles documents) and any artefact whose content was produced during scoping conversations.

```
2. AUTHOR v1   author reads source principles + plan + prior conversation,
                 writes draft-v1.md, commits
3. EDITOR      → as default
4. CONSISTENCY → as default
5. PROMOTE     → as default
6. PR          → as default
7. SIGN-OFF    → as default
```

The fast-path skips step 1 (BRIEF) only. Editorial review, consistency check, promote, PR, and sign-off all still apply — quality gates aren't conditional on whether a brief was needed.

Average rounds: 2 author + 1 editor + 1 consistency + 1 owner = 5 turns (default path; fast-path is the same minus the brief step).

---

## 8. Authoring order

**Sequential within a discipline, parallel across disciplines.** Reason: vocabulary propagation. Each artefact in a discipline reads the previous accepted one as input so language stays consistent. Parallelising within a discipline produces drift the consistency checker has to catch later, which is more expensive than authoring sequentially.

### 8.1 Now

**Product track (sequential):**
1. `PRODUCT_RULES.md`
2. `idea-triage`

**Engineering track (sequential):**
1. `eng-principles-universal.md`
2. `eng-principles-agentic.md` (depends on universal)
3. `design-doc`
4. `incremental-implementation`

**Hook track (parallel with engineering, gated on agentic principles draft):**
- `stop-the-line` — authored once `eng-principles-agentic.md` is at draft stage.

**Meta (owner work during M6):**
- README routing section.

**References (parallel):**
- All `references/*.md` files written as their citing skills come up. Editor batches reviews.

### 8.2 Next

Authored only on promotion to Now. Each promotion gets a written decision (criteria in §3). Brief authored at promotion time, not pre-emptively.

---

## 9. Milestones

- **M1 — Project setup complete.** Repo initialised, anatomy specs accepted, `PROJECT_STATE.md` initialised, agent roles tested on a throwaway hello-world artefact.
- **M2 — Root rules files accepted.** `PRODUCT_RULES.md`, `eng-principles-universal.md`, `eng-principles-agentic.md` merged.
- **M3 — Now complete.** All 8 Now artefacts accepted, coverage matrix audit done.
- **M4 — References complete.** All 6 reference files merged.
- **M5 — Promotion review (optional).** Re-evaluate Next items against current evidence. Default: no promotion; ship in v0.2.
- **M6 — Ship.** v0.1.0 tagged, project closed.

(Detailed milestone audit checklists in `PROJECT_GOVERNANCE.md` §6.)

---

## 10. Briefs

Most Now artefacts get a brief written before authoring begins. Format: see `docs/brief-template.md`.

Briefs are agent-drafted from the plan, the triage records, and the source principles documents; owner reviews and approves. Owner contributes substance — decisions, gotchas, scope clarifications, anything specific the agent can't infer from the plan and source materials. Owner does not draft the YAML or write the prose. The pattern is conversational: owner tells the agent (or supervisor) what's important in plain language; agent drafts the brief in template format; owner reviews and either approves or corrects.

Briefs are skipped for artefacts whose substance is already settled — typically v0.1 rules files derived from existing principles documents (`PRODUCT_RULES.md`, `eng-principles-universal.md`, `eng-principles-agentic.md`), or artefacts whose content was produced during scoping conversations. The supervisor decides at dispatch whether a brief is needed (default path) or skipped (fast-path) — see §7.

Briefs for Next items are drafted only at promotion time, not pre-emptively.

---

## 11. Triage records

The pack's first principles (`idea-triage`, `roadmap-shape`) demand every accepted item carry a written triage record. Confidence scale (Gilad): opinion 0.1, anecdote 0.5, market data/surveys 2-5, smoke tests/experiments 5-8, validated launches 8-10. See `references/confidence-meter.md` for calibration guidance and `docs/authoring-learnings.md` for the calibration warnings.

### 11.1 Now

| # | Artefact | Category | Confidence | Evidence basis |
|---|---|---|---|---|
| 1 | `PRODUCT_RULES.md` | rules | 8 | source content exists, reformatting work |
| 2 | `idea-triage` | skill | 7 | strong principle backing; v0.1 scoping demonstrated need |
| 3 | `eng-principles-universal.md` | rules | 8 | source content exists; tier-1 carve-out work |
| 4 | `eng-principles-agentic.md` | rules | 7 | tier-2 derived in scoping; sequential dependency on universal |
| 5 | `design-doc` | skill | 6 | personal usage on real work; 6 universal-tier principles route through it |
| 6 | `incremental-implementation` | skill | 6 | personal usage of addy's version; most-fired skill |
| 7 | `stop-the-line` | hook | 6 | felt-pain evidence (any-cast, .skip, lint suppression); deterministic checks |
| 8 | README routing section | meta | 6 | replaces using-this-pack at v0.1 scale |

### 11.2 Next

| # | Artefact | Category | Confidence | Evidence basis |
|---|---|---|---|---|
| 9 | `using-this-pack` | skill | 6 | cut from Now; promotes when pack grows |
| 10 | `planning-and-task-breakdown` | skill | 6 | cut from Now; team-shape concern, low for engineer-of-one |
| 11 | `roadmap-shape` | skill | 2 | cut from Now; bootstrapping argument weak; principle-only |
| 12 | `small-batch` | hook | 4 | mechanical (PR size, branch age); promote after stop-the-line proves pattern |
| 13 | `evidence-claim` | hook | 4 | mechanical (scan for evidence references); promote after stop-the-line |
| 14 | `plan-review` (was `problem-first-reviewer`) | skill | 5 | reframed from sub-agent to skill; predecessor `phase4-devils-advocate` already in real use; meta-reviewed against MECE + Nemeth findings before authoring |
| 15 | `prototype-to-validate` | skill | 5 | recent personal usage; gap between idea-triage and design-doc |
| 16 | `spike` | skill | 3 | principle-backed; informal personal usage |
| 17 | `deploy` | skill | 3 | end-to-end coherence; partial personal practice |
| 18 | `post-launch-impact-review` | skill | 1.5 | highest principle-weight, lowest personal evidence |
| 19 | `roadmap-review` | skill | 1 | partially absorbed by `plan-review`; revisit only if ≥5 plan-review runs against roadmaps yield <30% bucket hit rate (per plan-review Known Limits section) |

Triage rationales (the prose justifications behind each row) are in `PROJECT_GOVERNANCE.md` §8.

---

## See also

- `PROJECT_GOVERNANCE.md` — strategic goals, OKRs, risks, deliverables checklist, owner-side rationales, plan version history.
- `docs/authoring-learnings.md` — calibration guidance and failure modes for authors and editors.
- `docs/skill-anatomy.md`, `docs/hook-anatomy.md`, `docs/sub-agent-anatomy.md` — anatomy specs.
- `docs/brief-template.md` — brief format.
