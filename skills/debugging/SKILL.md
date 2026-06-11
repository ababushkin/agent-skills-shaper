---
name: debugging
description: >
  Find root cause before proposing fixes. Use when stuck on a failing test, build, or
  system behaviour — hypothesis and evidence instead of guess-and-check. Trigger phrases:
  "why is this failing", "I can't figure out", "tried everything", "build keeps breaking",
  "escalate from build".
---

# Debugging

## Purpose

Diagnose broken builds and unexpected behaviour by root cause, not by guessing. The one thing that must hold: no fix is attempted before a written root-cause note names what is broken and why.

## When to use

- After three consecutive build failures without narrowing the error (escalation from `build`).
- A test fails and the cause is unclear, before attempting any fix.
- Production bugs, unexpected behaviour, performance problems, integration failures.
- Under time pressure, when "just try changing X" seems obvious, or after multiple failed fix attempts.

## Do not use when

- Cause and fix are both clear — open `build` and write the failing test directly; this skill is for diagnosis, not implementation.
- Adding a feature or refactoring — open `build`; this skill adds no behaviour.
- The cause points at the design — open `design-doc`; debugging assumes the design is sound.

## Inputs

- The failing check: the command that goes RED, and its output verbatim.
- Evidence of failure: stack traces, error messages, system state at failure time.
- Prior fix attempts and why they failed (when escalated from `build`).

## Outputs

- A root-cause note (see Artefact template): what is broken, where, why, with supporting evidence.
- A blocker hypothesis when the cause is still unknown after investigation — the narrowest statement of what must be resolved before a fix.
- A hand-off state: diagnosis ready for `build` to implement the fix, or for `design-doc` if the cause is architectural.

## Workflow

### 1. Gate: record the verification command and current state

Record the failing check command exactly and run it. Collect the full error output and stack trace, the system state at failure (env vars, file state, recent changes, `git log`), and every previous fix attempt with the output it produced.

### 2. Gate: Phase 1 — root-cause investigation

Complete this before proposing any fix.

- **Read the error fully.** Don't skim. Note line numbers, file paths, error codes, the exact message — it often contains the solution.
- **Reproduce consistently.** Find the exact steps that trigger the failure. If you can't reproduce it, gather more data; don't guess.
- **Check recent changes.** `git diff`, `git log --oneline`, new dependencies, config or environment differences.
- **Instrument component boundaries.** In multi-layer systems (CI → build → signing, API → service → DB), add diagnostics at each boundary to show what enters and exits, then investigate the component where the failure actually occurs — not the whole system.
- **Trace data flow backward.** When the error is deep in a call stack, find where the bad value originates and fix at the source, not the symptom.

### 3. Gate: Phase 2 — pattern analysis

Find the pattern before fixing. Locate similar working code in the same codebase. If implementing against a reference, read it completely. List every difference between working and broken, however small — don't assume "that can't matter." Confirm the broken code's dependencies, config, and assumptions.

### 4. Gate: Phase 3 — hypothesis and test

State one hypothesis: "I think X is the root cause because Y." Test it with the smallest possible change, one variable at a time. If it works, proceed to the note. If not, form a new hypothesis — don't stack fixes. If you don't understand something, say so rather than pretend.

### 5. Gate: write the root-cause note

Before any fix, write the note (Artefact template below). A note that says "I don't know" is valid — it names the blocker for escalation. A missing note means Phase 1 is incomplete. Do not proceed to a fix without it.

### 6. After three failed fixes, escalate to design

If each fix reveals a new problem in a different layer, requires massive refactoring, or creates new symptoms, the problem is architectural, not a diagnosis failure. Write the root-cause note naming the architectural issue and hand off to `design-doc` or your human partner — do not attempt a fourth fix.

## Artefact template

No file artefact. Produce:

```
ROOT CAUSE NOTE
Verification: <command>

What is broken: <observable symptom and its impact>
Where it breaks: <component / layer / function>
Why it's broken: <root cause — the deepest reason, not a symptom>
Evidence: <diagnostics, stack traces, or diffs that prove the cause>
Blocker: <"none — fix ready" or "requires X to resolve">

Ready for: build (implement fix) | design-doc (architectural escalation)
```

## Red flags

- Proposing a fix before Phase 1 investigation is written down.
- Root-cause note missing, or "I don't know" with no evidence of what was investigated.
- A failing check deleted or skipped to "move on."
- Multiple fixes attempted in sequence without narrowing the error.
- Each fix reveals a new problem in a different component, with no architectural issue named.
- A "fix" that masks a symptom (adding retry logic instead of fixing the source).

## Exit criteria

1. Phases 1–3 complete and a root-cause note written.
2. The note names the symptom and its location, the root cause (not a symptom), the evidence, and the blocker if the cause is unknown.
3. The note is specific enough for `build` to implement the fix, or architectural escalation is triggered.
4. After three failed fixes, the note names the architectural issue rather than a new fix hypothesis.

## Related

- `skills/build/SKILL.md` — escalates here after three RED loops without narrowing; receives the root-cause note as input.
- `skills/design-doc/SKILL.md` — escalation target when the cause is architectural.
- Ported from `superpowers/systematic-debugging` (MIT): four-phase root-cause methodology and the no-fix-before-understanding rule.
