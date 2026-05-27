# Shaper

**The shaping layer for product and engineering — including the team of one.**

> *Shape the work before you build it.*

Shaper turns a fuzzy idea into something bettable, sound, and ready to build — before a line of code exists. It covers two shapes and deliberately stops before execution:

- **Product shaping** — which problems are worth solving, what the bet is, what "done" means.
- **Technical shaping** — how to build it soundly: the design, the de-risking spike, the task breakdown, the pre-build review.

Execution — implement, test, ship — is delegated to an execution pack of your choice. That's a scope decision, not a gap: Shaper's job is to hand that pack a clean, de-risked, bettable spec.

Shaper is **tracker-agnostic** — initiatives, key results, and the idea bank are plain markdown by default. Install the [Workflow pack](#how-to-install) (plugin `workflow`) to record them in a Linear-based initiative/cycle model; without it, every artefact is a paste-ready markdown shape.

Skills encode the discipline experienced teams apply at each decision point, packaged so AI agents follow them consistently instead of taking shortcuts.

```
  DISCOVER         CURATE          DECIDE          DESIGN            PLAN
 ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
 │  idea    │──▶ │ backlog  │──▶ │  roadmap │──▶ │ design   │──▶ │ planning │
 │  triage  │    │  manage  │    │  shape   │    │  doc     │    │ + task   │
 └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
  creates          promotes/        reads            how to           tasks for
  idea bank        kills items      idea bank        build it         your build
  records          updates scores   builds roadmap                    skill
```

Calibrated where it counts: the [`plan-review`](skills/plan-review/SKILL.md) skill catches **93%** of the issues a senior reviewer should catch on a 5-scenario benchmark, vs **19%** without the skill loaded (n=3, Claude Sonnet 4.6). [Methodology and per-eval breakdown.](docs/benchmarks.md)

---

## Skills

### Product shaping

| Skill | What it does | Use when |
|---|---|---|
| [PRODUCT_RULES.md](rules/PRODUCT_RULES.md) | Rule set covering idea filtering (P2–P4), roadmap discipline (B1–B5), and capacity allocation (C1–C3). | Load persistently for product work |
| [idea-triage](skills/idea-triage/SKILL.md) | Interrogates incoming ideas through confidence gates, ICE scoring, and Kano classification. Routes to idea bank (Confidence ≥ 5) or validation slot (Confidence < 5). | Any proposal arrives |
| [app-calibrate](skills/app-calibrate/SKILL.md) | Captures app-specific context (audience, value props, constraints) so Impact scores in `idea-triage` are grounded in this product, not a generic one. | Before running `idea-triage` for the first time on a product; product context shifts |
| [backlog-manage](skills/backlog-manage/SKILL.md) | Maintains the idea bank between triage and planning. Promotes validated items, kills stale ones, updates confidence scores with new evidence, and tracks KTLO work. Run before `roadmap-shape` so it reads a clean input. | Idea bank needs curation; validation result arrived; adding KTLO work; feeding post-launch evidence back |
| [roadmap-shape](skills/roadmap-shape/SKILL.md) | Reads the curated idea bank and builds a Now/Next/Later roadmap with explicit portfolio-theme mix and capacity allocation. Assumes the idea bank is clean. | Planning cycle; roadmap review |
| [initiative-shape](skills/initiative-shape/SKILL.md) | Shapes a vague idea or roadmap item into a properly formed initiative — goal, 3 measurable key results, affected repos, appetite, kill condition, project type — gated by an 11-rule quality rubric. Records it via your tracker if a binding is installed (e.g. the Workflow pack), else emits a paste-ready markdown shape. | Committing to goal-directed work; preparing initiatives for cycle planning |

### Technical shaping

| Skill | What it does | Use when |
|---|---|---|
| [eng-principles-universal.md](rules/eng-principles-universal.md) | Rule set: design before build (A1–A5), small batch (B1), explicit contracts (C1–C3), technical quality (D1–D4). | Load persistently for engineering work |
| [eng-principles-agentic.md](rules/eng-principles-agentic.md) | Agentic-specific constraints: scope discipline, no speculative refactoring, confirmation before destructive action. | Load alongside universal for agent-driven work |
| [product-spike](skills/product-spike/SKILL.md) | Throwaway artefact (narrative, clickable, or code) to answer one product question before committing to a design. Time-boxed; exits with a written finding: proceed / reshape / kill. | Idea approved; dominant unknown is product feel or interaction |
| [backend-spike](skills/backend-spike/SKILL.md) | Time-boxed investigation of a backend correctness question (detection threshold, substitution strategy, algorithmic safeguard). Produces a recommendation with a rejected-alternatives table and a named follow-up implementation ticket. | Design-doc stalls on a correctness sub-question; ≥2 plausible approaches with different edge-case behaviour |
| [planning-and-task-breakdown](skills/planning-and-task-breakdown/SKILL.md) | Decomposes a design doc or spec into small, verifiable tasks with acceptance criteria and dependency order. | Design accepted; ready to implement |
| [design-doc](skills/design-doc/SKILL.md) | Structures significant work before building: problem statement, approach options, chosen design, NFR constraints, operability plan. | Work exceeds 4 weeks, reused capability, or meaningful user/cost/compliance impact |
| [plan-review](skills/plan-review/SKILL.md) | Reviews a plan, spec, or design before approval. Eight MECE attack buckets plus a Cynefin classifier; surfaces unstated assumptions, missing alternatives, and reversibility blind spots. Calibrated against a [5-scenario benchmark](docs/benchmarks.md): 93% with-skill vs 19% baseline (n=3, Sonnet 4.6). | Plan/spec/design needs a second pass before commitment |
| [render-html](skills/render-html/SKILL.md) | Converts a markdown design doc, plan, ADR, or roadmap into a single self-contained HTML file for human review. Preserves spatial content (alternatives tables, dependency graphs, timelines) that flat markdown collapses. | Artefact is about to go to review or sign-off and reviewer experience matters |

### Meta

| Skill | What it does | Use when |
|---|---|---|
| [using-this-pack](skills/using-this-pack/SKILL.md) | Meta-skill that maps a task to the right pack skill. Loads first when the agent is unsure which workflow applies. | Starting a session; task arrives and you don't know which skill fits |

---

## Pairing with an implementation pack

Shaper owns shaping — discover, curate, decide, design, review-before-build — and its deliverable is a clean, de-risked, bettable spec. Execution — test, debug, build UI, harden, ship — is a separate job by design. Pair Shaper with an execution pack built for that job, or drive execution with your own prompting. Either way, what Shaper hands off is a spec that's ready to build.

[`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) is the worked example throughout this section because three of Shaper's skills trace their lineage from it (`predecessor` declarations in frontmatter). It's not a required pair — it's one option among the implementation packs that exist or will exist.

### What an implementation pack covers

Using addy's pack as the example. Empty cells on Shaper's side aren't gaps to be filled — they're scope decisions. Shaper will never ship a TDD or CI/CD skill; that's not its job.

| Phase | Shaper (shaping) | Implementation pack (e.g. `agent-skills`) |
|---|---|---|
| Discover / curate | `idea-triage`, `app-calibrate`, `backlog-manage` | — |
| Decide / plan | `roadmap-shape`, `initiative-shape`, `planning-and-task-breakdown` | — |
| Design | `design-doc`, `product-spike`, `backend-spike` | — |
| Pre-build review | `plan-review` (calibrated, [benchmarks](docs/benchmarks.md)) | — |
| Build | — | `incremental-implementation`, `frontend-ui-engineering`, `source-driven-development`, `context-engineering`, `api-and-interface-design` |
| Verify | — | `test-driven-development`, `debugging-and-error-recovery`, `browser-testing-with-devtools` |
| Review | — | `code-review-and-quality`, `security-and-hardening`, `performance-optimization`, `code-simplification` |
| Ship | — | `git-workflow-and-versioning`, `ci-cd-and-automation`, `documentation-and-adrs`, `shipping-and-launch`, `deprecation-and-migration` |
| Persistent rules | `PRODUCT_RULES`, `eng-principles-universal`, `eng-principles-agentic` | — |
| Hooks | `stop-the-line` | (varies by pack) |

### Where the two intentionally overlap

Three Shaper skills have direct counterparts in addy's pack. They diverge intentionally; the divergences are declared in each skill's frontmatter (`predecessor`, `kept_from_predecessor`, `changed_from_predecessor`).

| Shaper skill ↔ addy skill | What Shaper changed | Why |
|---|---|---|
| `idea-triage` ↔ `idea-refine` (adjacent) | Mandatory ICE scoring + Confidence Meter gates; Kano classification; routes low-confidence ideas to a validation slot, not the roadmap. | The product principles in `PRODUCT_RULES.md` demand evidence before commitment — `idea-refine` accepts framed ideas; `idea-triage` gates them. |
| `design-doc` ↔ `spec-driven-development` (derivative) | NFRs as numbered measurable targets, not adjectives; mandatory Operability section (metrics, alerts, rollback); ADR pattern enforced. | Universal eng principles A1–A6 require this rigour; `spec-driven-development` is more permissive. |
| `planning-and-task-breakdown` ↔ `planning-and-task-breakdown` (derivative) | Acceptance criteria required per task; explicit dependency-order surfacing before commitment. | Eng principle B7 requires cross-team dependency surfacing pre-commitment; addy's version leaves it implicit. |

If you install both packs, the namespace prefix (`shape-*` vs the implementation pack's namespace) means both versions coexist; pick which one fires by which trigger language you use, or by loading only one.

Install commands for both packs are in [How to install](#how-to-install).

---

## Hooks

Hooks are mechanical checks that fire on events. They catch failure modes the agent has every reason not to flag against itself.

| Hook | What it catches | Fires when |
|---|---|---|
| [stop-the-line](hooks/stop-the-line/HOOK.md) | Type suppressions, compiler directives, test skips, deleted assertions, static-analysis suppressions in a diff | Agent signals work is done |

---

## Benchmarks

One skill (`plan-review`) has been calibrated against a 5-scenario eval set with isolated blinded grading and n=3 per cell. Headline: **93% pass rate with-skill vs 19% without** (delta +0.74) on Claude Sonnet 4.6. Full methodology, per-eval results, the trajectory across five iterations, and caveats: [docs/benchmarks.md](docs/benchmarks.md).

The methodology is reusable; benchmarking the other eight skills is on the roadmap.

---

## References

Short reference files cited by skills. Load on demand.

| Reference | What it contains | Cited by |
|---|---|---|
| [confidence-meter](references/confidence-meter.md) | Gilad 1–5 evidence quality scale | idea-triage, roadmap-shape |
| [ice-scoring](references/ice-scoring.md) | ICE = Impact × Confidence × Ease formula and scoring guide | idea-triage |
| [kano-classification](references/kano-classification.md) | Five-category feature taxonomy (must-be → excitement) with decay behaviour | idea-triage |
| [portfolio-themes](references/portfolio-themes.md) | Doshi's seven strategic themes with capacity allocation guidance | roadmap-shape |
| [nfr-categories](references/nfr-categories.md) | NFR taxonomy: category, measurable target, fitness function type | design-doc |
| [dora-metrics](references/dora-metrics.md) | Four DORA metrics with elite / high / medium / low benchmarks | post-launch-impact-review, deploy |
| [app-context-schema](references/app-context-schema.md) | Schema for capturing app-specific context (audience, value props, constraints) used to ground Impact scoring | app-calibrate, idea-triage |

---

## How to install

Shaper installs and runs on its own. To pair it with an implementation pack, see the [optional step](#optional--pair-with-an-implementation-pack) below.

### Claude Code — marketplace install (recommended)

Install the plugin directly from GitHub:

```
/plugin install github@ababushkin/agent-skills-shaper
```

This gives you:

- The 11 slash commands (`/shape:idea-triage`, `/shape:design-doc`, …)
- The 12 auto-invocable Skills, namespaced as `shape-<name>` (model-triggered via the Skill tool)

Restart Claude Code after install. To load the rule files persistently, add three `@` references to your `~/.claude/CLAUDE.md`:

```
@/path/to/agent-skills-shaper/rules/PRODUCT_RULES.md
@/path/to/agent-skills-shaper/rules/eng-principles-universal.md
@/path/to/agent-skills-shaper/rules/eng-principles-agentic.md
```

Where `/path/to/agent-skills-shaper` is the install path printed by Claude Code, typically under `~/.claude/plugins/cache/...`.

The tracker workflow — the Linear initiative/cycle cadence, the code-review-before-Done gate, and the issue-comment standard — lives in the **Workflow pack** (plugin `workflow`), not in Shaper. Install it for the tracker workflow; its SessionStart hook then loads that governance and points at the three principle files above, making these manual imports optional. Shaper installed on its own keeps the three principle `@`-refs as its persistent-load path.

### Claude Code — local-dev install (`install.sh`)

If you've cloned the repo and want edits to propagate live without re-installing the plugin, run:

```
git clone https://github.com/ababushkin/agent-skills-shaper.git
cd agent-skills-shaper
./install.sh
```

The script:

1. Generates wrapper command files in `~/.claude/commands/shape/` (slash commands).
2. Symlinks each skill dir into `~/.claude/skills/shape-<name>` (auto-invocable Skills, edits propagate live).
3. Appends `@`-refs for the three principle rule files to `~/.claude/CLAUDE.md` (persistent rule loading; idempotent — old-layout refs and any ref to a rule file Shaper no longer ships are pruned automatically).

Re-run the script after a `git pull` or after adding a new skill — it's idempotent and prunes stale symlinks.

### Optional — pair with an implementation pack

`addyosmani/agent-skills` is the worked example for the implementation half (build, verify, review, ship — see [Pairing with an implementation pack](#pairing-with-an-implementation-pack)). Install it alongside Shaper:

```
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

Either pack works on its own; both work together. For local-dev co-install, run each pack's installer independently — namespacing (`shape-*` vs the implementation pack's namespace) prevents symlink collisions in `~/.claude/skills/`.

### Other agents (Cursor, Gemini CLI, Windsurf, …)

Skills are plain Markdown. Paste the content of the relevant `rules/*.md` or `skills/<name>/SKILL.md` into your agent's rules/instructions file for the project. Load rule files persistently; load skills situationally — loading all of them at once wastes context.

---

## Attribution

This pack is a soft fork of [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) by Addy Osmani. It inherits the structural conventions (skill frontmatter, anatomy specs, the `SKILL.md` pattern). Where an artefact has a counterpart in addy's pack, the relationship is declared explicitly in the artefact's frontmatter (`predecessor`, `kept_from_predecessor`, `changed_from_predecessor`). Where an artefact is new, it stands alone. No paragraph in this pack is a verbatim copy of the source.

---

## License

MIT — see [LICENSE](LICENSE).
