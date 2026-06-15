---
name: thin-supervisor-contract
status: accepted
authors: Anton Babushkin
created: 2026-06-16
last_updated: 2026-06-16
supersedes: none
namespace_record: extends `docs/design-docs/execution-workflow/design-doc.md` (A/N04). Schema v2 amends A/N04's inter-skill handoff table in place; supervisor-seam columns added here.
---

# Thin-supervisor contract — prompt-segment allocation, handoff schema v2, process/workflow boundary

## Problem

The drain-cycle supervisor's worker prompt today inlines the workflow it wants the worker to follow: a preamble names the worktree and base branch, then a tail script enumerates "review → fix → commit → push → comment → transition to Done." `drain_cycle/prompt.py` emits ~80–120 lines depending on stack mode, and `flow.py` branches the tail on the `verify` label. The same procedure is also owned by this pack's `exec:*` skills — two sources of truth for one workflow.

Affected parties: the drain-cycle supervisor (one prompt template per state; rewrites every time a skill changes its trail artefacts), pack-skill authors (cannot evolve `exec:finish` without a coordinated edit in the supervisor repo), and non-Claude workers (codex, kimi) that today either re-implement the inlined procedure or skip steps silently. The handoff file `.drain-handoff.json` v1 carries `pr_urls`, `final_linear_state`, and `exit_code` — enough to grade a run but not enough to inspect *why* a worker halted or *which AC items* it failed (KR2's commit).

Current behaviour: the prompt prescribes the workflow; the pack's skills also prescribe it; drift between them is silently absorbed by the worker. Desired behaviour: the supervisor names one skill pointer and the operational facts the worker needs to run (worktree, base branch, stack mode, resume marker, labels); the pack owns every workflow step; the handoff file records the verdicts the supervisor needs to grade and the operator needs to inspect.

## Context

**Initiative A's design doc (`docs/design-docs/execution-workflow/design-doc.md`) is the predecessor of this one.** A/N04 reserved the `exec:*` namespace, pinned the skill graph (`exec:pickup → exec:breakdown → exec:build → … → exec:finish`), and defined `pickup-envelope.json` as the in-flight carrier across skills. This doc extends A/N04 with the *supervisor-seam* contract — what the supervisor passes in and what the run leaves behind — without re-deciding the skill graph or the envelope.

The migration consequence is bounded. A/N04's supervisor-binding audit found that `drain_cycle/prompt.py` currently emits exactly two execution-side verbs literally: `/code-review-and-quality` (4 string locations) and `/shape:task` (verify-flow directive). The remaining completion-sequence prose (commit/push, review-summary comment, Linear Done transition) is inlined as prose, not delegated. Per A/N10, the literal `/code-review-and-quality` swap to `/exec:review` happens via `exec:finish`/`exec:pickup` taking ownership; this doc decides the *shape* of the prompt that survives the swap and the schema the verdicts land in.

`drain_cycle/orchestrator.py:505` resolves the per-run `stack` flag from the `--no-stack` CLI flag and the `push_to_main_repos` config. Today this fact picks the preamble variant emitted (normal vs stack). After collapse, the worker still needs to know which mode it is in to delegate to `shape:pr-finishing` correctly (Graphite stack vs gh PR). The signal must survive.

`drain_cycle/flow.py` routes the supervisor preamble on the issue's `verify` label, choosing between the build-and-finish tail and a verify-only tail. After collapse, the label remains a process-readable fact (it sits on the Linear issue payload), but *what verify-only means* is a workflow concern (it parses the issue body for a Task-Shaper block and only calls `/shape:task` when missing). Allocation is governed below.

Predecessors and adjacent decisions: ADR 0003 (persona-dispatch contract; locates vendor-specific branching inside `exec:review` only), ADR 0004 (`exec:*` verb namespace), KR3's measurement clause (`wc -l` on the worker prompt template ≤15; grep for procedure-verb slash-commands over `drain_cycle/` returns empty).

## Constraints

**Functional.**

- The worker prompt template must transmit *only* process facts and a single skill pointer. No procedure prose. No conditional branches inside the prompt body.
- The `stack` mode and the issue's `labels[]` are supervisor-resolved facts; they must reach the worker via the prompt template (not via files the skill loads).
- `.drain-handoff.json` must carry the verdict fields the supervisor reads at run-end to (a) grade the run, (b) build the run-log entry KR2 promises, and (c) name the halt reason on any non-Done exit. Every field has a named writer and a named reader.
- The schema must extend A/N04's `pickup-envelope.json` rather than duplicate it. `pickup-envelope.json` is the in-flight carrier *between skills*; `.drain-handoff.json` is the exit record *from the worker back to the supervisor*.
- A non-Claude worker reading the prompt must be able to follow it. No Claude-Code-only tool names. No SDK-specific framings.

**Non-functional.**

| NFR | Target | Fitness function |
|---|---|---|
| Worker prompt template size | ≤15 lines including blanks | `wc -l drain_cycle/prompt_template.txt` ≤ 15 on the rendered template skeleton (before issue-body substitution) |
| Procedure-verb absence | No execution slash-command in the supervisor source other than `/exec:pickup` | `git grep -nE '/(code-review\|shape:(pr-\|verify-\|task)\|exec:(build\|review\|verify\|finish\|breakdown\|debug\|simplify))' drain_cycle/` returns empty |
| Schema-v2 fitness | `.drain-handoff.json` produced by any worker exit parses against the JSON Schema in `references/drain-handoff-schema-v2.md` and every required field is present per its writer's exit gate | Extract the fenced JSON Schema from `references/drain-handoff-schema-v2.md`, validate every `~/.drain-cycle/runs/*.json` against it; exit 0 on every fixture and every live run |
| Vendor portability | The prompt template contains zero references to `Claude`, `Anthropic`, `Skill` (capitalised), `Agent` (capitalised), or any tool-search call | `grep -iE '(claude\|anthropic\|toolsearch\|agent tool)' drain_cycle/prompt_template.txt` returns empty |
| Handoff parse cost | `jq` parse of `.drain-handoff.json` completes in <50 ms on a tens-of-runs `~/.drain-cycle/runs/` directory | KR2 schema-check one-liner finishes in <1 s wall-clock over the directory |

## Alternatives considered

This doc presents two decisions, each with its own alternative set.

### Decision 1 — Prompt-segment allocation (≤15-line template)

**Alt P1 — Process facts + minimal context + one pointer (chosen).**

Template carries: issue id + title (1), issue URL (1), worktree path (1), base branch (1), stack mode (1), labels (1), resume marker (1, optional but always present — `"none"` on fresh runs), issue-body header (1), issue-body placeholder (1), pointer prose (1), pointer (1). Total fixed skeleton: 11 lines, expandable to 13 with two blank separators, under the 15-line cap.

*Blast radius if wrong.* Low. A miss surfaces immediately: KR3's `wc -l` clause fails the brake. Worker behaviour degrades gracefully because the skill — not the prompt — owns the procedure; recovery is a one-line template edit, not a coordinated cross-skill migration.

*Reversal cost.* Low. The template lives in one file (`drain_cycle/prompt_template.txt`); reverting to a fatter template restores prior behaviour without touching the pack.

**Alt P2 — Process facts + minimal context + pointer, with resume directive inlined as prose.**

Same as P1 but on resumed runs the supervisor injects 2–3 lines of prose: "this worktree may be dirty; the branch already exists; inspect existing state before continuing." Two prompt-template variants (fresh, resume).

*Blast radius if wrong.* Medium. Resume prose is exactly the shape KR3's grep is hunting for ("inspect → decide → continue"). Two templates to keep in sync. The resume case is already representable as a structured marker (`resume: true|false`) that the skill consumes — inlining the prose pushes a workflow concern back into the supervisor.

*Reversal cost.* Medium — requires deleting one variant *and* moving the resume semantics into `exec:pickup`.

**Alt P3 — Pointer-only; every fact carried in env vars or sidecar files.**

Prompt is "`/exec:pickup`" plus the branch and URL; the rest of the operational context (worktree path, stack mode, labels) is materialised into env vars or a temp file that the skill reads.

*Blast radius if wrong.* High. Env-var conventions vary by worker runtime (codex's env exposure ≠ Claude Code's). Readability of the prompt log drops: an operator inspecting a halted run can no longer see what the worker knew. The skill must now treat the absence of a file as a recoverable case, which spreads supervisor-coupling into the pack.

*Reversal cost.* High — once one runtime binds to env-var names, the others have to be retrofitted.

**Decision: Alt P1.** P1 wins the brake (template stays under cap), the portability NFR (no runtime-specific assumptions), and the prompt-log inspectability constraint (operators see the facts that drove the run). P2's resume prose is the cleanest counter-argument refused: the resume marker is a process *fact*, not a workflow step.

### Decision 2 — `.drain-handoff.json` schema v2

**Alt H1 — Flat extension of v1 (chosen).**

v1 already carries `pr_urls`, `final_linear_state`, `exit_code`. v2 adds four fields: `outcome_verdict`, `prep_verdict`, `flow`, and `halt_reason`. No `schema_version` field; no nested envelopes. The reader (supervisor) treats a missing v2 field as v1 — backwards compatible by absence.

*Blast radius if wrong.* Low. New fields are additive; v1 readers tolerate them. A renamed field is caught immediately by the schema-fitness check (which exists). A missing required field on the exit path is caught by the writer's exit gate.

*Reversal cost.* Low. The schema is a JSON file in `references/`; updates are a one-line edit.

**Alt H2 — Versioned envelope (`schema_version: 2`, nested `v1` + `v2` records).**

Top-level `schema_version` plus separate `v1` and `v2` sub-objects. The reader switches on the version field.

*Blast radius if wrong.* Medium. Forces every writer to set the version field; mismatched values silently route to the wrong reader. Speculative: there is no current divergence between readers — the supervisor is the only one — so the envelope encodes a problem we do not have.

*Reversal cost.* Medium — flattening later means re-walking every existing run file.

**Alt H3 — Per-skill handoff files (`.exec-verify.json`, `.exec-finish.json`, etc.).**

Each skill writes its own handoff; the supervisor merges them at run-end.

*Blast radius if wrong.* High. The supervisor now depends on a *set* of files existing in a known order; partial writes (e.g., halt between `exec:verify` and `exec:finish`) leave the supervisor inspecting a torn state. KR2's "every worker exit produces a run-log entry" loses its single grade-point.

*Reversal cost.* High — once skills write to separate paths, consolidating them requires re-authoring each.

**Decision: Alt H1.** Flat extension; one file, additive fields, single grade-point.

## Recommended approach

### Prompt-segment allocation (the ≤15-line budget, line by line)

The worker prompt template, with placeholders in `{BRACES}`:

```
Issue {ISSUE_ID} — {ISSUE_TITLE}                                        [1]
URL: {ISSUE_URL}                                                        [2]
Worktree: {WORKTREE_PATH}                                               [3]
Base branch: {BASE_BRANCH}                                              [4]
Stack mode: {STACK_MODE}                                                [5]
Labels: {LABELS_CSV}                                                    [6]
Resume: {RESUME_MARKER}                                                 [7]
                                                                        [8] blank
Issue body:                                                             [9]
{ISSUE_BODY}                                                            [10]
                                                                        [11] blank
Pick up this issue and drain it to Done by invoking the skill below.    [12]
/exec:pickup                                                            [13]
```

13 lines. Two-line margin under the cap absorbs future single-line additions (e.g., a `Cycle: ` line if cycle context starts to matter) without rebreaching the brake.

**Segment classification:**

| Line | Segment | Class | Source |
|---|---|---|---|
| 1 | Issue id + title | context | Linear payload |
| 2 | URL | context | Linear payload |
| 3 | Worktree path | process | supervisor (worktree manager) |
| 4 | Base branch | process | supervisor (run config) |
| 5 | Stack mode (`stack`\|`no-stack`) | process | supervisor (`orchestrator.py:505` resolution) |
| 6 | Labels csv | process | Linear payload, passed through |
| 7 | Resume marker (`none`\|`true`) | process | supervisor (continuation detector) |
| 9–10 | Issue body | context | Linear payload |
| 12–13 | Pointer prose + slash-command | pointer | template constant |

**Process segments are counted inside the budget** (per the assumption verified in N01). Lines 3–7 are five of the thirteen — the brake forces every process fact to earn its line.

**The procedure-verb grep (pinned).** KR3 measures the supervisor source for procedure-verb leakage with:

```
git grep -nE '/(code-review|shape:(pr-|verify-|task)|exec:(build|review|verify|finish|breakdown|debug|simplify))' drain_cycle/
```

Expected output: empty. The only execution slash-command named in `drain_cycle/` is `/exec:pickup` (in `prompt_template.txt` line 13). The pattern catches every current and future execution verb the pack might author; new verbs add to the regex, never to the supervisor.

### `.drain-handoff.json` schema v2

```json
{
  "pr_urls": ["https://github.com/…/pull/123"],
  "final_linear_state": "Done",
  "exit_code": 0,
  "outcome_verdict": {
    "result": "pass",
    "failed_ac": []
  },
  "prep_verdict": {
    "route": "auto-merge",
    "reasoning": "additive; passes carve-out; CI green"
  },
  "flow": "build",
  "halt_reason": null
}
```

**Writer / reader allocation:**

| Field | Type | Writer | Reader | Required |
|---|---|---|---|---|
| `pr_urls` | `string[]` | `shape:pr-finishing` (invoked by `exec:finish`) | supervisor (grade); review-summary commenter | yes on Done exit |
| `final_linear_state` | `string` | `shape:pr-finishing` | supervisor (grade); run-log writer | yes |
| `exit_code` | `int` | supervisor (on worker exit) | supervisor (grade); inspector | yes |
| `outcome_verdict` | `{result: "pass"\|"fail", failed_ac: string[]}` | `exec:verify` (via `shape:verify-implementation`) | supervisor (run-log); inspector | yes once verify has run; absent on halts before verify |
| `prep_verdict` | `{route: "auto-merge"\|"human-review", reasoning: string}` | `shape:pr-prepare` (invoked by `exec:finish`) | supervisor (run-log); inspector | yes on Done exit; absent on halts before finish |
| `flow` | `"build"\|"verify-only"\|"shape-task"` | `exec:pickup` (writes on entry) | supervisor (run-log); fixture grader | yes |
| `halt_reason` | `string \| null` | supervisor (on non-Done halt) | supervisor (run-log); inspector | required when `final_linear_state != "Done"`; `null` otherwise |

**This table amends A/N04's inter-skill handoff table in place.** A/N04 stops at `exec:finish`'s emits column (review verdict + verify result + PR body); this row carries those verdicts forward into `.drain-handoff.json` so the supervisor — which never reads `pickup-envelope.json` — can grade the run from one file.

**Halt-reason taxonomy** (the closed set `halt_reason` draws from):

| Code | Meaning | Set by |
|---|---|---|
| `worker-exit-1` | Worker process exited non-zero before reaching `exec:finish` | supervisor |
| `timeout` | Wall-clock budget exhausted | supervisor |
| `repeated-exit-1` | Consecutive-failure escalation tripped | supervisor |
| `verify-fail-noloop` | `outcome_verdict.result == "fail"` and `exec:build`'s remediation budget exhausted | `exec:verify` (passed up); supervisor records |
| `pr-blocked` | `shape:pr-finishing` could not submit (Graphite/gh error, base diverged) | `shape:pr-finishing` (passed up); supervisor records |
| `human-review-requested` | `prep_verdict.route == "human-review"`; run halts before merge | `shape:pr-prepare` (passed up); supervisor records |

### Process-vs-workflow boundary chart

| Concern | Today's location | After contract | Class |
|---|---|---|---|
| Worker spawn (subprocess invocation) | `orchestrator.py` | unchanged | process |
| Worktree creation / cleanup | `orchestrator.py` | unchanged | process |
| Halt on timeout / repeated exit-1 | `orchestrator.py` | unchanged | process |
| Resume detection (continuation marker) | `orchestrator.py` | unchanged; surfaces as line 7 | process |
| Grade the run (read `.drain-handoff.json`) | `grade.py` | unchanged; new fields available | process |
| Per-run `stack` flag resolution | `orchestrator.py:505` | unchanged; surfaces as line 5 | process |
| Per-issue label list | `flow.py` (used to branch tail) | passed through to line 6; routing moves into `exec:pickup` | process |
| Pickup envelope creation | inlined in prompt preamble | `exec:pickup` | workflow |
| Breakdown into tasks | `/shape:task` directive in tail | `exec:breakdown` (invoked by `exec:pickup`) | workflow |
| RED/GREEN/commit loop | inlined in tail | `exec:build` | workflow |
| Code review fan-out | `/code-review-and-quality` (4 sites) | `exec:review` | workflow |
| AC verification | inlined in tail | `exec:verify` | workflow |
| PR submission (Graphite vs gh) | two preamble variants | `shape:pr-finishing` (invoked by `exec:finish`); supervisor signals mode via line 5 | workflow |
| Review-summary comment + Linear Done transition | numbered prose in tail | `exec:finish` | workflow |
| Verify-flow routing (verify-label check) | `flow.py` | `exec:pickup` reads labels (line 6) and routes | workflow |
| Run-log entry writing | n/a (KR2 commit) | supervisor reads `.drain-handoff.json` and appends to `~/.drain-cycle/runs/*.json` | process |

**The ambiguous edges, named:**

1. *Verify-flow routing.* The label list is a process-readable fact (supervisor reads Linear). The decision *what verify-only means* (parse body for Task-Shaper block, call `/shape:task` only if missing) is a workflow fact. **Allocation: supervisor passes labels through line 6; `exec:pickup` reads them and routes.** `flow.py`'s branching code deletes. The `flow` field on `.drain-handoff.json` records which path was taken so the supervisor can grade without re-parsing.
2. *`/shape:task` directive.* The verb is workflow (it is a pack skill). The decision *whether to invoke it* depends on issue-body parsing, also workflow. **Allocation: folds entirely into `exec:pickup`'s breakdown step.** The current verify-flow directive deletes from the supervisor.
3. *Stack-mode signal.* The decision *that the user runs in stack mode* is operational policy (CLI flag, config), so it is process. The decision *what stack mode means at PR-submission* (Graphite vs gh code path) is workflow. **Allocation: supervisor emits the flag on line 5; `shape:pr-finishing` switches on it.**

### Vendor-agnostic prose constraints

- The prompt template contains no instance of `Claude`, `Anthropic`, `Skill` (capitalised tool name), `Agent` (capitalised tool name), `ToolSearch`, or any SDK identifier. The pointer is a slash-command name; its expansion is the worker runtime's responsibility.
- All pack-skill workflow sections, except `exec:review`'s persona-dispatch block, are written in vendor-neutral imperative prose (no "use the Agent tool", no "via `claude -p`"). ADR 0003 is the single locus of vendor-specific branching.
- All artefacts (`pickup-envelope.json`, `.drain-handoff.json`, `build-log.md`) are POSIX-path text files written via plain filesystem APIs.
- Slash-command syntax `/<namespace>:<verb>` is treated as the worker's responsibility to resolve; the prompt only *names* it. A worker without a slash-command runtime maps it to whatever its command registry is — the prompt does not care.

## Consequences

**Positive.**

- One contract that the prompt template, the schema, and the pack-skill workflows all bind to. Drift between them surfaces at one of three named fitness checks (template `wc -l`, supervisor grep, schema parse).
- KR3 brake becomes mechanical: `wc -l` and `git grep`. No interpretive call at acceptance.
- The handoff carries enough to build the run-log KR2 promises *and* enough to drive a future "post review-summary to Linear" automation off one file.
- A non-Claude worker can be pointed at this prompt and the published `exec:*` skills with no further glue; the only Claude-Code-specific code path is the persona-dispatch branch inside `exec:review`, which has a documented inline-sequential fallback.
- `pickup-envelope.json` and `.drain-handoff.json` are separated by lifetime: the envelope flows skill→skill in memory of the worker; the handoff is the exit record the supervisor reads. Each has one writer per field; readers are named.

**Negative.**

- The 13-line template has two lines of margin to absorb future facts. If a sixth process segment appears (e.g., a per-run sandbox identifier), the brake must be re-negotiated — not silently raised.
- `flow.py`'s deletion concentrates more routing logic inside `exec:pickup`. If that skill grows past the 200-line NFR A/N04 imposed, it will need a one-step delegation to a `exec:route` helper. Flagged as a future scope check, not blocking.
- The `halt_reason` taxonomy is a closed set. A halt cause outside the taxonomy must extend it before the run-log will validate, which costs a one-line schema edit and a writer change. Acceptable cost; speculative additions are explicitly out of scope.

**Walking skeleton.** Not separately required: the design surface is one file (the prompt template) plus one schema file. N02's pointer-only template smoke-drained through one issue *is* the walking skeleton for the broader initiative; that node is flagged `skeleton: true` in D1's deliverable. This doc unblocks it.

## Operability plan

**Metrics.** Per drained run, recorded in `~/.drain-cycle/runs/<run-id>.json` from the handoff:

- `flow` distribution (build vs verify-only vs shape-task) — confirms verify-flow routing is reaching the right path.
- `outcome_verdict.result` rate — verify-pass rate.
- `prep_verdict.route` distribution — auto-merge vs human-review split.
- `halt_reason` histogram — surfaces which halt path dominates.
- Wall-clock time per `flow` value — for cycle-throughput grading.

**Structured logs.** The supervisor emits one stderr JSON line per run boundary (`{event: "run-start" | "run-end", run_id, issue_id, flow, exit_code, halt_reason}`). No vendor SDK in the log line.

**Traces.** Not required at this stage — drain volume is low and single-user. If volume grows past ~10 drains/day, add a span per `exec:*` skill invocation parented to the pickup span (deferred to a later initiative).

**Alerts.** None — single-user CLI; halts surface on stderr and in the run-log. The N09 validation drain (initiative A) is the alert surface for any contract drift.

**Rollback plan.**

1. If the pointer-only prompt template causes 3 consecutive halts that the inlined preamble would have completed, revert `drain_cycle/prompt_template.txt` to the prior inlined tail. Verification gate: re-run one of the failed issues with the reverted template; expect Done.
2. If schema v2 fields are written but the run-log parser breaks, revert the parser to the v1 field set and accept that the verdict columns show `null` until the parser is fixed. Verification gate: KR2's schema-check one-liner returns 0 on every existing run file.
3. If the halt-reason taxonomy is missing a code that a halt path needs, extend the closed set with one entry and re-run. Verification gate: the next halted run writes a non-null `halt_reason` in the new code.

Each step is independently reversible without coordinated cross-repo work; the contract change is structurally two-way for the prompt and additive for the schema.

**Capacity headroom.** `.drain-handoff.json` per run: ≤4 KB. `pickup-envelope.json`: ≤2 KB per drain (per A/N04). Run-log file (`~/.drain-cycle/runs/*.json`) growth: one file per run; trim after one year. No capacity concern at present volume.

**Known failure modes.**

| Failure | Surface | Mitigation |
|---|---|---|
| Template re-grows past 15 lines | KR3 brake fails | template `wc -l` runs in pre-merge check; no merge while red |
| Procedure verb leaks into supervisor source | KR3 grep fails | the pinned grep runs in the same pre-merge check |
| Writer/reader allocation drifts (a field written nowhere) | run-log shows `null` where required | schema fitness check parses live handoffs; absence of a required field on a Done exit is a CI failure |
| Halt-reason taxonomy outgrown | unrecognised code in run-log | schema validates against closed set; an unknown code fails parse, forcing the taxonomy edit before merge |
| `pickup-envelope.json` and `.drain-handoff.json` confused | a field written to the wrong file | A/N04 owns the envelope columns, this doc owns the handoff columns; one table cites the other |

**Upstream dependencies.** Linear API (reads labels for line 6; reads issue body for lines 9–10). Failure: supervisor halts with a comment naming the API as the blocker; no run starts. **Downstream dependencies.** `drain_cycle/prompt.py` consumes only the template + the per-issue facts; the pack consumes only the slash-command name `/exec:pickup`.

## Open questions

| Q | Owner | Resolution gate |
|---|---|---|
| **Q1.** Does `prep_verdict.route == "human-review"` materialise to a supervisor-level halt (the worker exits non-zero so the operator must merge), or is it a Done-state outcome with a different Linear status? | N04 author | Resolved at N04 wiring time. Default: halt with `halt_reason: human-review-requested`; the supervisor records Done-equivalent outcome on the run-log but does not transition the issue. |
| **Q2.** Does the per-task model annotation belong on the handoff (so the run-log can grade model-tier coverage) or only on `pickup-envelope.json`? | N03 author | Resolved at N03 schema-test authoring. Default: envelope-internal; the handoff records only verdict-level facts. Re-open if a grader needs model-tier columns. |
| **Q3.** Does `exec:pickup` need a publicly-named `--verify-only` entry point, or is the verify-flow routing entirely internal to it (based on the `labels[]` argument)? | N02 author | Resolved at N02 authoring. Default: internal — one slash-command, internal routing on labels. Add a public sub-command only if a non-drainer caller appears. |
| **Q4.** Does the `flow` value `"shape-task"` survive after `exec:breakdown` is published? (`/shape:task` is the current verb; the pack should rename to `/exec:breakdown` per A/N04.) | N03 author | Resolved at N03 authoring. Default: the `flow` enum updates to `"breakdown"` if the breakdown verb renames; the supervisor reads the value as opaque. |

## Review hand-off

Accepted through the `plan-review` exit gate at `docs/plan-reviews/thin-supervisor-contract/review.md`. The plan-review on the initiative's *delivery plan* (`docs/plan-reviews/drain-cycle-thin-supervisor/review.md`) approved this node's framing during plan acceptance; this review covers the *design doc itself* against design-doc anatomy.
