---
name: debugging
description: >
  Find root cause before proposing fixes. Use when stuck on a failing test, build, or system
  behavior — hypothesis and evidence instead of guess-and-check. Phase 1 complete, blocker
  named, before any fix attempt.
pack: engineering
lifecycle_stage: debugging
principles_implemented:
  - source: eng-agentic
    id: P4
    bucket: embedded
  - source: eng-agentic
    id: P6
    bucket: embedded
  - source: eng-universal
    id: Rule A1
    bucket: embedded
length_target: 280–320
author: Anton Babushkin
predecessor:
  repo: https://github.com/obra/superpowers
  skill: systematic-debugging
  relation: port
kept_from_predecessor: "Four-phase root-cause methodology; iron law framing; common rationalisations table; red flags and verification checklist (superpowers); Phase 1-4 structure and diagnostics; multi-component tracing pattern"
changed_from_predecessor: "[GATE] root-cause-note marker requiring written root cause before any fix attempt; anatomy-compliant section order; per-phase gate markers; integration with build skill escalation path"
---

# Debugging

## Purpose

debugging is the root-cause investigation skill for broken builds and unexpected behaviour. It enforces
the IRON LAW — no fixes before understanding root cause — and makes that understanding explicit by
requiring a written root-cause note that names the blocker before any fix attempt. The dominant failure
it guards against: looping on retries without diagnosis, producing thrashing commits and masked underlying issues.

## When to use

- After three consecutive build failures without narrowing the error (escalation from `build` skill).
- When a test fails and the cause is unclear — before attempting any fix.
- Production bugs, unexpected behaviour, performance problems, integration failures.
- Especially when under time pressure, when "just try changing X" seems obvious, or after multiple
  failed fix attempts.

## When not to use

- **Clear cause, clear fix** — if you understand the root cause and can write a failing test for it,
  open `build` directly, not this skill. This skill is for diagnosis, not implementation.
- **Feature or refactoring** — open `build`. This skill does not add behaviour.
- **Architecture decision** — open `design-doc` first. Debugging assumes the design is sound.

## Inputs

- The failing check: command that goes RED, its output verbatim.
- Evidence of failure: stack traces, error messages, system state at failure time.
- Prior fix attempts and why they failed (if this is escalation from `build`).

## Outputs

- Root-cause note: written statement of what is wrong and why (not a fix, not a hypothesis—
  the diagnosis).
- Blocker hypothesis: if cause is unknown after Phase 1 investigation, the narrowest statement
  of what must be learned or resolved before a fix can be attempted.
- Ready-to-hand-off state: evidence and diagnosis for `build` skill to proceed with Phase 4
  (implementation) or for architectural escalation if the cause points to design.

## Workflow

**1. [GATE] Verification command and current state.**

Record the failing check command exactly. Run it; observe the failure. Collect:
- Full error output and stack trace
- System state at failure time (env vars, file state, recent changes, git log)
- Previous fix attempts (what was tried, what output did each produce)

**2. [GATE] Phase 1 — Root Cause Investigation.**

Complete before moving to Phase 2. Do NOT propose fixes until Phase 1 is complete.

**2.1 Read Error Messages Carefully**
- Don't skim. Read the full stack trace and all warnings.
- Note line numbers, file paths, error codes, exact failure message.
- Error messages often contain the solution.

**2.2 Reproduce Consistently**
- Can you trigger the failure reliably?
- What are the exact steps?
- If not reproducible: gather more data, don't guess.

**2.3 Check Recent Changes**
- What changed that could cause this?
- Run `git diff`, `git log --oneline`, check recent commits.
- New dependencies, config changes, environment differences.

**2.4 Gather Evidence in Multi-Component Systems**

When the system has multiple layers (CI → build → signing, API → service → database):

Before proposing a fix, add diagnostic instrumentation at each component boundary:
- What data enters this component?
- What data exits this component?
- Is environment/config propagated correctly?

Run once to gather evidence showing WHERE the failure occurs, then investigate
that specific component, not the entire system.

**2.5 Trace Data Flow Backward**

When error is deep in a call stack:
- Where does the bad value originate?
- What called this function with bad input?
- Keep tracing up until you find the source.
- Fix at source, not at symptom.

**3. [GATE] Phase 2 — Pattern Analysis.**

Find the pattern before fixing.

**3.1 Find Working Examples**
- Locate similar working code in the same codebase.
- What works that's similar to what's broken?

**3.2 Compare Against References**
- If implementing a pattern, read the reference implementation COMPLETELY.
- Don't skim; read every line.
- Understand the pattern fully before comparing.

**3.3 Identify Differences**
- What's different between working and broken?
- List every difference, however small.
- Don't assume "that can't matter."

**3.4 Understand Dependencies**
- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

**4. [GATE] Phase 3 — Hypothesis and Testing.**

Scientific method: form hypothesis, test minimally, verify.

**4.1 Form Single Hypothesis**
- State clearly: "I think X is the root cause because Y."
- Write it down.
- Be specific, not vague.

**4.2 Test Minimally**
- Make the SMALLEST possible change to test hypothesis.
- One variable at a time.
- Don't fix multiple things at once.

**4.3 Verify Before Continuing**
- Did it work? Yes → Phase 4.
- Didn't work? Form NEW hypothesis, return to 4.1.
- DON'T add more fixes on top.

**4.4 When You Don't Know**
- Say "I don't understand X."
- Don't pretend to know.
- Ask for help or research more.

**5. [GATE] Root-Cause Note — Write it before proceeding.**

Before implementing any fix, write a root-cause note that states:
- **What is broken:** The observable symptom and its impact.
- **Where it breaks:** The component, layer, or function where the failure occurs.
- **Why it's broken:** The root cause — the deepest reason, not a symptom.
- **Evidence:** Reference to diagnostics, stack traces, or diffs that prove the cause.

Example:
```
ROOT CAUSE NOTE
===============
Symptom: Build fails with "identity not found" in codesign step
Where: In signing layer (step 3: codesign script)
Why: Environment variable IDENTITY is not propagated from CI workflow to build script
Evidence: Diagnostic output shows IDENTITY:UNSET in build script (step 2.4),
but IDENTITY:SET in workflow (step 1). Check workflow → build bridge: env vars
not exported in build-script.sh line 42 (git blame shows added in commit abc123).

Blocker: None identified. Fix is ready (add `export IDENTITY` to line 42).
```

**[GATE] — Do NOT proceed to fix without this written note. A note that says "I don't know"
is valid; it names the blocker for escalation. A missing note means Phase 1 is incomplete.**

**6. If 3+ Fix Attempts Failed (Architectural Escalation)**

If investigation shows each fix reveals a new problem in a different layer:
- Each fix uncovers shared state/coupling/problem elsewhere
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms

This indicates architectural problem, not diagnosis failure.

**STOP and escalate:** Write the root-cause note naming the architectural issue, then
hand off to `design-doc` or your human partner for architecture discussion.

## Artefact template

No file artefact. Produce:

```
Verification: <command>

[PHASE 1 — INVESTIGATION]
Evidence gathered:
- Error message and stack trace
- Recent changes (git log, diff)
- System state at failure (env, files, config)
- Multi-component diagnostics (if applicable)

[PHASE 2 — PATTERN]
Working example found: <location>
Differences from working code: <list>

[PHASE 3 — HYPOTHESIS & TEST]
Hypothesis: <statement>
Test result: <passed/failed>

[ROOT CAUSE NOTE]
Symptom: <observable failure>
Where: <component/layer>
Why: <root cause>
Evidence: <reference to diagnostics>
Blocker: <"none" or "requires X to resolve">

Ready for: build skill (implement fix) OR design-doc (architectural escalation)
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "Issue is simple, don't need process" | Simple bugs have root causes too. Diagnosis is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this fix, then investigate if it fails" | First fix sets the pattern. Diagnose before implementing. |
| "I'll write root-cause note after the fix works" | Untested hypotheses don't stick. Diagnose first; implement after. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. Trace to source. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

## Red flags

- Proposing a fix before Phase 1 investigation is written down.
- Root-cause note missing or says "I don't know" without evidence of what was investigated.
- A failing check is deleted or skipped to "move on."
- Multiple fixes attempted in sequence without narrowing the error.
- Each fix reveals a new problem in a different component (architectural issue not named).
- A "fix" that is really a symptom mask (adding retry logic instead of fixing the source).

## Verification / exit criteria

The skill has run correctly when:

1. All four phases are complete (Phase 1–3 investigation, Phase 4 root-cause note).
2. A written root-cause note exists that names:
   - The observable symptom and its location
   - The root cause (not just a symptom)
   - Evidence (diagnostics, stack traces, diffs) that supports the diagnosis
   - The blocker (if cause is unknown: what must be resolved)
3. The note is specific enough that a `build` skill invocation can proceed with Phase 4 (implement fix) or architecture escalation is triggered if the cause points to design.
4. If three consecutive fix attempts failed without narrowing the error: the root-cause note names the architectural issue, not a new fix hypothesis.

## References

- `skills/build/SKILL.md` — escalation source when three consecutive RED attempts fail without narrowing; receives root-cause note as input
- `skills/design-doc/SKILL.md` — escalation target when investigation reveals architectural issue
- `rules/eng-principles-agentic.md` — P4 (evidence beats vibes), P6 (stop the line)
- `rules/eng-principles-universal.md` — Rule A1 (diagnosis before remedy)
- Predecessor: `superpowers/systematic-debugging` (MIT) — four-phase root-cause methodology, iron law framing
