# Shaping pipeline — one path from idea to shipped work

**Status:** Proposed (awaiting your confirmation on the four items marked _Proposed_)
**Date:** 2026-06-03
**Reverses:** the §17 decision (task-shape at pickup time), which lived on the now-closed PR #11 branch and never reached main

---

## What you asked for

Three things, in your words:

1. Shape lots of tickets quickly in a consistent format — from a pile of ideas or from a single idea, whether or not a goal exists yet.
2. Size the work so your agents never pick up a ticket that is too big.
3. Read the result in product language, sliced so you can review it easily.

And one complaint underneath all three: the skills overlap, and the overlap is confusing.

## The problem: two jobs wearing one coat

The confusion has a single root. Every shaping skill today does the same job — break work into pieces — but each one writes for **agents** and demands a **rigid input**:

- `delivery-shape` needs a committed goal with key results before it runs.
- `planning-and-task-breakdown` needs an accepted design document.
- `task-shape` needs a single ticket already sitting in the tracker.

So when you arrive with a raw idea and want clean tickets you can review, none of them fit. You end up forcing product-shaped input through agent-shaped tools and finishing the job by hand.

The fix is to separate two artefacts that have been mashed together:

- **The thing you review** — tickets written in customer and business language, sliced so you can read down them and judge the work. Audience: you.
- **The thing your agents build** — an engineering breakdown into stacked pull requests, each tagged with the model that should run it. Audience: agents.

One artefact, two audiences. Pull them apart and the overlap disappears.

## The decision: split the work by who reads it

```
YOU (product language)                      AGENTS (engineering)
──────────────────────                      ────────────────────
idea-triage       should we?  (optional)
initiative-shape  goal + KRs? (optional)
delivery-shape ──→ right-sized tickets ───→  execution-breakdown ──→ drain-cycle
  • single OR bulk ideas         (at pickup) • stacked PRs + model tiers   builds it
  • goal optional                            • runs right before the build
  • product language, easy to review
  • size-gated: no oversized tickets
```

Two shapers, divided by who reads the output:

- **`delivery-shape` becomes the shaper you use.** It takes a single idea or a whole pile, with or without a goal attached, and returns right-sized tickets in product language. It owns the size gate. This is the everyday workhorse.
- **`execution-breakdown` is the agent's tool** (renamed from `planning-and-task-breakdown`). It runs the moment an agent picks up a ticket, turns that ticket into a stack of pull requests, and tags each one with the model that should build it. You never drive it by hand.

Two more moves clean up the rest:

- **`task-shape` is retired** (pull request #11 is closed). "Shape one ticket" is simply `delivery-shape` with a single idea — it never needed its own skill.
- **The rename ends a name clash.** `planning-and-task-breakdown` shares its name with a skill in the upstream pack we derived it from. `execution-breakdown` is unmistakably ours, and the name says what it is: the breakdown that happens at execution time, for an agent, right before the build.

## How you'll use it day to day

You bring ideas. That is the only input that matters.

- **A single idea, no goal in sight.** Run `delivery-shape` on it. You get one or more tickets, each a bounded chunk of customer value, sized to be picked up safely.
- **A backlog of ideas after a planning session.** Run `delivery-shape` over the set. You get a consistent ticket for each, grouped however the ideas cluster.
- **An idea that belongs to a goal.** Attach the goal and the tickets trace back to its key results. Skip the goal and the tickets simply stand on their own.

In every case the output reads the same way and slices the same way, so review feels familiar no matter where the idea came from.

## What a ticket looks like _(Decided: keep the five-section body, softened to product language)_

Each ticket keeps `delivery-shape`'s existing five-section body — **What / Why / Completion / Assumptions / Key Risks** — so the format stays consistent with every plan already shaped and the enforcement gate (`bin/check-plan-framing`) is untouched. What changes is the *voice*: the sections are written in customer and business language, not engineering language.

- **What** — the outcome: who gets what value, in plain language. ("A returning customer sees their saved addresses at checkout.")
- **Why** — the bet this ticket makes and what it unlocks.
- **Completion** — the finish line in business terms, not code terms.
- **Assumptions / Key Risks** — what we're taking on faith and what could go wrong, stated so a product reader follows them.

The fine-grained engineering detail — the order of pull requests, the per-slice model tier — is *not* in the ticket; it's produced by the agent's `execution-breakdown` at pickup. Your ticket stays a product artefact.

## The size gate: nothing too big reaches an agent _(Proposed)_

A ticket is too big when either test fails:

- It would break into **more than three to five slices**, or
- It covers **more than one customer outcome**.

When a ticket fails, `delivery-shape` splits it into sibling tickets before you ever see it as one lump. The measure is slice count, never hours or days — size is about how much there is to verify, not how long it takes. This gate is the guarantee you asked for: your agents pick up bounded work every time.

## When there's no goal _(Proposed)_

The goal link is optional, and the ticket format does not change when you drop it:

- **With a goal** — tickets group under the outcomes they serve, and each traces back to a key result.
- **Without a goal** — tickets stand alone, with no grouping layer and no key-result trace.

A pile of ideas becomes a set of ticket groups in one pass. The shaper never invents a goal to justify the structure; it shapes only what you bring it.

## The handoff to your agents _(Proposed)_

Each shaped ticket carries two things across the line to your agents:

- A **rough size signal** (the expected slice count) so you can read capacity at a glance before any build starts.
- A standing instruction: **when picked up, expand through `execution-breakdown`.**

An agent picks up the ticket, runs `execution-breakdown` to produce the stacked pull requests and their model tiers, and builds. The fine-grained breakdown happens on fresh context at the last responsible moment — so it reflects what is true at build time, not what was guessed weeks earlier.

## What changes in the pack

| Artefact | Change |
|---|---|
| `delivery-shape` | Accept single or bulk ideas; make the goal optional; rewrite output to product language; add the size gate. |
| `planning-and-task-breakdown` → `execution-breakdown` | Rename the directory, the command, and the frontmatter name. Reposition as the agent's just-in-time breakdown. |
| `task-shape` (PR #11) | Closed. Folded into `delivery-shape`'s single-idea mode. |
| `docs/design-decisions.md` | Record this decision; supersede §17. |
| References to the old name | Update `delivery-shape`, `references/task-sizing.md`, `design-doc`, `README.md`, `using-this-pack`, `install.sh`. |

## Open questions to confirm

The four sections marked _Proposed_ above are my best defaults, not settled calls:

1. **Ticket format** — ~~resolved~~: keep the five-section body (What / Why / Completion / Assumptions / Key Risks), softened to product language. No gate change.
2. **Size gate** — is "three to five slices, or one outcome" the right line?
3. **No-goal mode** — flat standalone tickets when no goal exists: right, or do you want a lighter grouping?
4. **Handoff** — does the slice-count signal give you the capacity view you want, or do you need a cost or model-mix estimate up front too?

One question sits outside this doc: **`drain-cycle`** is not defined in this pack. Its contract — what it reads from a ticket and how it runs the build — decides whether the handoff above is complete. Confirm whether `drain-cycle` lives in the verify-flow project, or whether we define it here.

## Decision record (supersedes §17)

§17 placed ticket shaping at **pickup time**, inside the agent session, as `task-shape`. This doc reverses that. Shaping you can review happens at **shape time**, in product language, in `delivery-shape`. The engineering breakdown happens at pickup, in `execution-breakdown`, for the agent. The two jobs were never the same job, and §17's mistake was treating them as one.
