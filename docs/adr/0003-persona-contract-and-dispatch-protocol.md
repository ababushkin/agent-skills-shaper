# ADR 0003 — Persona contract and dispatch protocol

- **Status:** Accepted
- **Date:** 2026-06-10
- **Serves:** Initiative D1 / KR2 — execution-review quality gate proven on seeded defects (N02).
- **Premise for:** Initiative C — thin supervisor that fans persona reviews out and merges their findings.

## Context

D1 builds a persona-driven review gate. To run the gate the same way across the worker surfaces this pack targets, two things must be pinned: how a persona is authored, and how it is dispatched. The surfaces differ materially:

- **Claude Code** — has an `Agent` tool that fans out a prompt-file persona into a subagent, returning the subagent's final text.
- **codex / kimi / other non-Claude workers** — no equivalent fan-out tool; the worker is one process running one prompt at a time.

A persona that hard-codes Claude-Code dispatch mechanics would strand the other workers and break initiative C's portability premise. A persona that hard-codes inline-sequential mechanics would forfeit the parallelism Claude Code already affords. The pack also needs a finding format the N01 grader can match on without parsing free prose; the grader looks for `file · defect class · severity` triples.

Two contract shapes were considered:

1. **Prompt-file personas + protocol in this ADR.** Persona prose lives in a plain `.md` file with frontmatter; dispatch rules live here, not in the personas. Portable; Claude-Code-native dispatch is preserved as the default branch.
2. **Claude-Code-native agent definitions** (`.claude/agents/*.md` with agent-tool metadata). Richer dispatch ergonomics on Claude Code but no usable form on codex/kimi; would require a second authoring track for non-Claude surfaces.

Shape 1 is taken. The Agent tool can dispatch a plain prompt-file persona directly — its content is the prompt — so the Claude-Code ergonomics loss is small, and the non-Claude surface stays first-class.

## Decision

**Persona file format and location.** Personas live at `personas/<name>.md`. Each file is a self-contained prompt with YAML frontmatter:

```yaml
---
name: <kebab-case>
description: <one-line role + when to invoke>
defect_classes: [<class>, <class>, ...]   # the classes this persona is responsible for catching
---
```

The body is plain prose: role, what to look for, what to ignore, and the finding format (below). No dispatch mechanics in the persona — those are this ADR's job.

**Structured finding format.** Each finding the persona emits is one line:

```
<file>:<line?> · <defect_class> · <severity>
```

`severity ∈ {critical, required, suggestion}`. `defect_class` is one of the persona's declared classes. Lines may be followed by indented free-prose context, but the leading triple is what the N01 grader matches on. The persona's prompt body restates this format verbatim.

**Dispatch protocol.**

- **Claude Code (default).** The supervisor reads `personas/<name>.md` and dispatches each persona via the `Agent` tool, passing the file content as the prompt and running personas in parallel (one `Agent` tool call per persona, batched in a single message). The Agent's returned text is the persona's findings list.
- **Non-Claude fallback (codex, kimi, others without fan-out).** The supervisor runs personas **inline-sequentially** in the same worker: for each persona, load `personas/<name>.md`, treat its body as a self-review instruction over the same diff, capture findings, then move to the next persona. The persona prose is identical to the Claude Code path; only the harness differs.

Both branches return findings in the same triple format, so the N01 grader and the supervisor's merge step are dispatch-agnostic.

## Consequences

**Positive**
- One persona authoring surface serves both dispatch worlds; initiative C builds against a stable contract.
- The N01 grader and any future merger consume the same finding triples regardless of dispatch path.
- Adding a persona is a single-file change with no harness coupling.

**Negative / costs**
- The non-Claude fallback gives up parallelism — review latency on codex/kimi scales linearly with persona count. Accepted because the alternative is a second authoring track.
- Finding-format discipline now lives in persona prose. Drift (a persona forgetting the triple) is silent until the grader sees it; N03 must verify the format holds during its iteration loop and add a lint check if drift recurs.
- Claude-Code-native agent affordances (named agent metadata, model pinning per agent) are not used. Re-evaluate if a future persona genuinely needs them.

## Scope

This ADR pins the contract only. N03 authors the personas against it and is the first consumer; the N01 fixture corpus and grader (already landed) are the acceptance harness. Any change to the finding triple or the dispatch branches requires a follow-up ADR.
