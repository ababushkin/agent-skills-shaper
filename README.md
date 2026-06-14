# Shaper

**Robust, scalable patterns for modern agentic engineering**

Vibe coding is fun on a small project. Over a longer one, your prompts drift — methodical and rigorous one day, rushed or forgetful the next - and the quality of the output drifts with them. Shaper encodes the engineering discipline that strong teams have relied on for decades into ready-to-go skills, so an agent applies it the same way on every project, every turn — instead of taking the shortcut.

- 

```
  SHAPE              DESIGN            PLAN              BUILD             VERIFY            SHIP
 ┌────────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
 │ triage     │ ───▶ │ design   │ ───▶ │ delivery │ ───▶ │ build    │ ───▶ │ verify   │ ───▶ │ prepare  │
 │ roadmap    │      │ doc +    │      │ shape +  │      │ debug    │      │ exec     │      │ + finish │
 │ initiative │      │ spikes   │      │ review   │      │ simplify │      │ review   │      │ PRs      │
 └────────────┘      └──────────┘      └──────────┘      └──────────┘      └──────────┘      └──────────┘
  what's worth      how to build      ordered,          green, small      does it match     small PRs,
  building, and     it soundly        verifiable        increments        the spec?         routed for
  what's the bet                      task list                                              merge
```

Every artefact is plain Markdown — a design doc, a delivery plan, a review verdict — so a human can read it and a machine can act on it.

---

## Why you'd want it

- **Consistent execution.** The same checks fire every time. The agent doesn't skip the design doc because the task "looked small," doesn't mark a ticket Done before the acceptance criteria are met, and doesn't merge a PR it never read.
- **Smarter routing.** Each skill knows what comes next. Triage routes a low-confidence idea to a spike instead of the roadmap; a failing build escalates to root-cause debugging; a finished branch routes each PR to auto-merge or human review by an explicit rule. The work flows to the right step without you steering every turn.
- **Orchestrator-ready.** Shaper's outputs are structured for execution engines like [drain-cycle](#works-with-orchestrators). Hand a delivery plan to an orchestrator and each node carries the framing — acceptance criteria, verification gate, review step — that the engine needs to drive a build unattended.

---

## Get started

Install the plugin from GitHub:

```
/plugin install github@ababushkin/agent-skills-shaper
```

Restart Claude Code. That's it — you now have:

- **18 skills**, auto-invoked when the task matches (e.g. say *"how should we build this?"* and `design-doc` fires).
- **Slash commands** for the core skills, namespaced `/shape:` (e.g. `/shape:idea-triage`, `/shape:design-doc`).
- A **SessionStart hook** that loads the navigator skill so the agent always knows which step it's on.

Prefer to drive it yourself? Type the slash command. Prefer the agent to choose? Just describe what you're doing — the skills trigger on natural phrases.

---

## How to use it

Start anywhere in the arc and follow the chain. A typical run looks like this:

1. **An idea arrives.** *"A customer asked for bulk export."* → `idea-triage` scores it, classifies it, and routes it — to the idea bank if it's strong, to a quick spike if the bet is unproven.
2. **It's worth doing.** → `roadmap-shape` and `initiative-shape` turn the idea into a committed initiative with a goal and measurable key results.
3. **Time to design.** → `design-doc` lays out the approach, the trade-offs, and the operability plan. Unsure about a risky unknown first? `product-spike` or `backend-spike` answers the one question before you commit.
4. **Plan the build.** → `delivery-shape` decomposes the initiative into an ordered, verifiable task list. `plan-review` reads it adversarially and catches what's missing *before* a line of code is written.
5. **Build it.** → `build` runs a gated red/green/commit loop, one small increment at a time. Stuck? `debugging` finds the root cause. Heavy? `simplify` trims it once it's green.
6. **Prove it's done.** → `verify-implementation` checks the diff against the ticket's acceptance criteria; `execution-review` runs spec, security, and quality passes. A fail is a halt, not a suggestion.
7. **Ship it.** → `pr-prepare` writes each PR body and routes it for merge or human review; `pr-finishing` submits the stack, one small PR per slice.

You don't have to run the whole arc. Each skill stands alone — invoke just the one you need. But when work spans several steps, following the chain is what keeps the thread from breaking.

Not sure which skill applies? Ask, or run `/shape:using-this-pack` — the navigator maps your task to the right step.

---

## The skills

| Stage | Skill | What it does |
|---|---|---|
| **Shape** | [idea-triage](skills/idea-triage/SKILL.md) | Score, classify, and route an incoming idea — to the idea bank or a validation spike. |
| | [app-calibrate](skills/app-calibrate/SKILL.md) | Capture app-specific context so triage Impact scores are grounded, not generic. |
| | [backlog-manage](skills/backlog-manage/SKILL.md) | Curate the idea bank — promote, kill, re-score, track KTLO. |
| | [roadmap-shape](skills/roadmap-shape/SKILL.md) | Build a Now/Next/Later roadmap with explicit portfolio mix and capacity. |
| | [initiative-shape](skills/initiative-shape/SKILL.md) | Shape an idea into a committed initiative — goal, key results, appetite, kill condition. |
| **Design** | [design-doc](skills/design-doc/SKILL.md) | Structure significant work before building: problem, approach, NFRs, operability. |
| | [product-spike](skills/product-spike/SKILL.md) | Throwaway artefact to answer one product question before committing. |
| | [backend-spike](skills/backend-spike/SKILL.md) | Time-boxed investigation of a backend correctness question, with rejected alternatives. |
| **Plan** | [delivery-shape](skills/delivery-shape/SKILL.md) | Decompose an initiative into an ordered, verifiable delivery hierarchy. |
| | [plan-review](skills/plan-review/SKILL.md) | Adversarial review of a plan before approval — scope drift, one-way doors, missing operability. |
| **Build** | [build](skills/build/SKILL.md) | Gated red/green/commit loop for one task — every increment lands verified, smallest first. |
| | [debugging](skills/debugging/SKILL.md) | Find root cause before proposing fixes — hypothesis and evidence, not guess-and-check. |
| | [simplify](skills/simplify/SKILL.md) | Reduce complexity after code is green, preserving exact behaviour. |
| **Verify** | [verify-implementation](skills/verify-implementation/SKILL.md) | Check the diff against the ticket's acceptance criteria — pass/fail, one finding per gap. |
| | [execution-review](skills/execution-review/SKILL.md) | Multi-persona review — spec compliance, security, quality — into one GO/NO-GO verdict. |
| **Ship** | [pr-prepare](skills/pr-prepare/SKILL.md) | Write each PR body and route it to auto-merge or human review by the carve-out rule. |
| | [pr-finishing](skills/pr-finishing/SKILL.md) | Submit a green branch as a stack of small PRs, one per commit slice. |
| **Meta** | [using-this-pack](skills/using-this-pack/SKILL.md) | The navigator — maps any task to the right skill. Loads at session start. |
| | [render-html](skills/render-html/SKILL.md) | Convert a Markdown doc into a single self-contained HTML file for human review. |

---

<details>
<summary><strong>Deeper details</strong> — tracker bindings, orchestrators, hooks, other agents, benchmarks</summary>

### Tracker-agnostic by default

Initiatives, key results, and the idea bank are plain Markdown out of the box — every artefact is a paste-ready shape. Install the **Workflow pack** (plugin `workflow`) to record them in a Linear-based initiative/cycle model instead; its SessionStart hook injects the governance and indexes Shaper's principle files for lazy loading. Shaper itself never assumes a tracker is present.

### Works with orchestrators

Shaper shapes the work; an execution engine can drive it. Outputs are structured so an orchestrator like **drain-cycle** can walk a delivery plan node-by-node and run each one unattended — every node carries its acceptance criteria, verification gate (`verify-implementation`), and review step (`execution-review`) inline. The skill pack and the engine compose: Shaper decides *what good looks like* at each step; the engine decides *when to run it*.

### Persistent rules

Three rule files load as context, not as skills, and apply across every step:

| File | Covers |
|---|---|
| [PRODUCT_RULES.md](rules/PRODUCT_RULES.md) | Idea filtering, roadmap discipline, capacity allocation. |
| [eng-principles-universal.md](rules/eng-principles-universal.md) | Design before build, small batch, explicit contracts, technical quality. |
| [eng-principles-agentic.md](rules/eng-principles-agentic.md) | Scope discipline, no speculative refactoring, confirm before destructive action. |

They're lazy-loaded — the SessionStart hook injects the navigator, which tells the agent when to read each one. No manual `@`-imports needed.

### Hooks

Mechanical checks that fire on events and catch failure modes the agent has every reason not to flag against itself.

| Hook | Catches | Fires |
|---|---|---|
| [stop-the-line](hooks/stop-the-line/HOOK.md) | Type suppressions, compiler directives, test skips, deleted assertions. | When the agent signals work is done. |
| [task-annotation-check](hooks/task-annotation-check/HOOK.md) | Task blocks missing their model-tier routing annotation. | On task-file changes. |

### References

Short files cited by skills, loaded on demand: [confidence-meter](references/confidence-meter.md), [ice-scoring](references/ice-scoring.md), [kano-classification](references/kano-classification.md), [portfolio-themes](references/portfolio-themes.md), [nfr-categories](references/nfr-categories.md), [dora-metrics](references/dora-metrics.md), [app-context-schema](references/app-context-schema.md).

### Benchmarks

The `plan-review` skill catches **93%** of the issues a senior reviewer should catch on a 5-scenario benchmark, versus **19%** without the skill loaded (n=3, Claude Sonnet 4.6). The methodology is reusable; benchmarking the other skills is on the roadmap. [Full methodology and per-eval breakdown.](docs/benchmarks.md)

### Local-dev install

To edit skills and have changes propagate live:

```
git clone https://github.com/ababushkin/agent-skills-shaper.git
cd agent-skills-shaper
./install.sh
```

The script writes slash-command wrappers, symlinks each skill into `~/.claude/skills/shape-<name>`, and installs the SessionStart hook. Re-run after a `git pull` — it's idempotent and prunes stale symlinks.

### Other agents (Cursor, Gemini CLI, Windsurf, …)

Skills are plain Markdown. Paste the relevant `rules/*.md` or `skills/<name>/SKILL.md` into your agent's instructions. Load rule files persistently; load skills situationally — loading all at once wastes context.

### Attribution

Inspired by [superpowers](https://github.com/obra/superpowers) and [agent-skills](https://github.com/addyosmani/agent-skills).

</details>

---

## License

MIT — see [LICENSE](LICENSE).
