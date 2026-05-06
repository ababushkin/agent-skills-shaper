# Engineering principles — agentic (tier 2)

These are the agent-specific engineering principles for the pde-skills pack. "Agent-specific" means: these principles only have force, or only make sense, because the implementer is an AI agent rather than a human. They sit on top of the universal tier (`eng-principles-universal.md`) — they don't replace it.

The test for tier 2: would this principle survive a counterfactual world without AI coding agents? If no, it belongs here. If yes, it belongs in the universal file. Some universal principles (small batches, boring technology, review) bite harder under agents than under humans alone — those are noted at the end as amplifications, not duplicated as new principles.

Skills, hooks, and sub-agent personas trace to principles in either tier; some trace to both. Where a tier-2 principle has a tier-1 ancestor (e.g. agentic Principle 4 amplifies universal Principle 1), the relationship is named.

---

## Part 1 — Guiding principles

These are the seven beliefs specific to agentic engineering. If a decision conflicts with a principle, the principle wins by default — and the burden of justification sits with the person arguing to deviate.

### 1. Context is the asset; loading it is the work

What's in the agent's context window determines output quality more than the underlying model's capability. Anthropic's own guidance puts it bluntly: every new token introduced depletes the agent's attention budget, and the right framing is "find the smallest set of high-signal tokens that maximise the likelihood of your desired outcome." Loading the right files, conventions, prior decisions, and constraints is engineering — not a preamble to engineering. An agent given the wrong context produces wrong work confidently. An agent given a thin slice of the right context produces narrow but accurate work.

**Implication:** Every skill names the context it expects loaded before the work begins — files, principles, prior decisions, conventions. "The agent will figure out what to read" is the same anti-pattern as "we'll figure out the spec in the code" from universal Principle 2.

### 2. Hallucination is the default; sources are the brake

Agents fabricate APIs, library behaviour, and version-specific quirks with high confidence. The fabrications look plausible because they're statistically reasonable continuations of training data — they're just wrong. Treating agent-produced code as trustworthy by default loses time the moment the wrong API call hits production. Every framework or library claim is verified against current docs or actual runtime behaviour, and inferences are flagged as inferences. This is the engineering analogue of universal Principle 4 (name your assumptions). The difference is that agents will assert assumptions as facts unless the skill explicitly forces a citation.

**Implication:** Skills that touch framework or library APIs require source citations — links to current docs, function signatures verified against the actual library version. Unverified claims are flagged in the work product, not silently shipped.

### 3. The shortest path is the failure mode; the spec is the seatbelt

Without an explicit problem statement, an agent optimises for "produce something that compiles," not "solve the stated problem." The agent has no stake in the original problem and no memory of the conversation that produced it; it has only what's in context now, plus a strong gradient toward producing output. Specs aren't ceremony — they're the only thing holding the work to the actual task. This isn't true of human engineers in the same way; humans carry implicit understanding from the conversation, the channel, the team's history. Agents do not.

**Implication:** Every implementation skill restates the problem at the start of its workflow, before any code is written. Skills explicitly forbid jumping to solution language until the problem statement is acknowledged. The restatement is how the agent's first output anchors to the actual task rather than to "what would compile."

### 4. Evidence beats vibes; "seems right" is never sufficient

Agents will report success based on syntax. "It compiled," "tests ran," "no errors logged" are not the same as "the behaviour the user wanted is now true." Every completion claim demands observable evidence: specific test names that passed, specific log lines that confirm, specific output values that match the expected. This is universal Principle 1 ("shipped is not done; observed is done") applied to the agent's own claims about its work, not just to deployments. The failure mode is the same — declaring victory before observing the outcome — but the trigger is different: agents declare victory at green tests, where humans usually wait for some additional signal.

**Implication:** Skills require evidence, not assertions, in completion claims. "The function works" is rejected; "test_user_creation_with_valid_email passed; log shows user_id 42 written to users table" is accepted. The hook `evidence-claim` (Next) enforces this mechanically.

### 5. The rationalisations are predictable; pre-rebut them

"I'll add tests later," "this is a quick fix so I'll skip the spec," "the existing code does it this way so I won't change it," "the type system is too strict, let me cast to any" — these patterns are in training data and the agent will reach for them when the work gets hard. They are not novel rationalisations the agent invents; they are the catalogue of excuses humans have produced in code review for thirty years, now reflected back. Skills that don't pre-rebut them get bypassed at exactly the moments they were most needed.

**Implication:** Every skill includes a "Common rationalisations" section — a table of typical excuses with documented counter-arguments. This isn't decoration: it's the operational form of the principle. If the skill doesn't name the rationalisation, the agent will use it.

### 6. Stop the line on first failure; never silence the signal

Failing tests get changed, type errors get `any`'d, lint failures get suppressed, assertions get deleted. The default response to a failing signal is investigation, not silencing. This deserves its own principle because the failure mode is so consistent: agents are optimised to make errors disappear, and silencing achieves that faster than fixing. The line between "fix the test that's wrong" and "delete the test that's correct" is a judgement call humans make routinely; agents collapse it almost every time without a hard rule.

**Implication:** Casts to `any`, `// @ts-ignore`, `.skip`, suppression of lint warnings, and deletion of assertions are flagged at the PR level by the `stop-the-line` hook (Now). When the hook fires, the agent's work is sent back for investigation, not for re-suppression.

### 7. Memory lives in artefacts, not in agents

Agents have no continuity between sessions. The ADR, the design doc, the postmortem, the README are how reasoning persists. Doc drift is fatal in agentic contexts in a way it isn't in human-only ones, because there's no human carrying the implicit knowledge from one session to the next. When the next agent reads the codebase, what it sees is the artefacts; what it doesn't see is anything not written down. Rule D3 in eng-principles-universal.md says ADRs are living documents that get superseded rather than ignored. In agentic contexts, that rule is load-bearing — silent drift means the next agent has the wrong model and confidently produces wrong work from it.

**Implication:** Every architectural change updates or supersedes its corresponding ADR or design doc in the same PR. The hook `artefact-pair` (Later) flags code changes without doc updates. Skills that produce design artefacts treat the artefact as the deliverable, not the code.

---

## Part 2 — How universal principles bite harder under agents

The universal-tier principles still apply. Four of them apply with extra force when the implementer is an agent.

**Small batches matter MORE.** The 2024 DORA report found that AI-assisted coding raises individual output but degrades stability when batch size grows. The discipline of universal Principle 8 is the brake on this. Without it, the productivity gains evaporate. The same DORA work also notes that AI-assisted teams that hold batch size constant see the gains compound rather than offset.

**Boring technology matters MORE.** Agents have seen every framework and every fad in training and reach for the most "interesting" solution unless constrained. Innovation-token budgets shrink: an agent given free choice will burn three tokens where a human would burn one, because every framework looks plausibly applicable. Universal Principle 10 needs harder enforcement in agentic contexts — the default must explicitly be the existing stack, not "what the model thinks is appropriate."

**Review matters MORE.** When an agent generates code at scale, human review is the only place asymmetric judgement is applied. Volume changes the math: a human writing 100 lines an hour is reviewed in proportion to that volume; an agent writing 1000 lines an hour cannot be reviewed by a human at the same proportion. Sub-agent review personas (the third artefact category in this pack) exist because mechanical hooks and embedded skill constraints aren't sufficient — some judgement requires fresh context and an adversarial second pass.

**Operability matters MORE.** An agent thinks it's done at green tests. Universal Principle 1 ("shipped is not done; observed is done") is harder to enforce when the implementer can't observe the production system. The agent needs skills that explicitly include the observation step in their workflow, because there's no on-call instinct to fall back on.

---

## Part 3 — Quick reference

The agentic tier is: an agent's failure modes are predictable, structural, and largely solved by writing them down before the agent encounters them.

The agentic tier is not: a list of complaints about agents, or a denial of how much they accelerate the work.

The seven principles in one line each:

1. Context is the asset; loading it is the work
2. Hallucination is the default; sources are the brake
3. The shortest path is the failure mode; the spec is the seatbelt
4. Evidence beats vibes; "seems right" is never sufficient
5. The rationalisations are predictable; pre-rebut them
6. Stop the line on first failure; never silence the signal
7. Memory lives in artefacts, not in agents

Cross-references to universal-tier principles that amplify under agents are in Part 2 above.
See `eng-principles-universal.md` for the full tier-1 principles set.
