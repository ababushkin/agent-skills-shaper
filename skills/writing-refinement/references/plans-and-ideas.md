# Plan-Mode Plans, Idea One-Pagers, and Proposals

These are the artefacts that fall between an OKR set and a full design doc: the plan you produce in plan mode before touching code, the one-pager that comes out of refining a raw idea, and the lightweight proposal that argues for a direction. None of them is a design doc — they carry no operability gate, no NFR table — but each still tells the same story: where we are, what's wrong with that, and what we will do.

Apply the six phases. The SCQA spine (Phase 1) is the whole value here: a plan that opens with its task list instead of the gap it closes reads as motion without a reason.

## Plan-mode plan

A plan shaped for action: enough that a reader can grade the approach before any code is written, no more.

| Bad | Good |
|---|---|
| "Plan: 1. Look at the auth code. 2. Make changes. 3. Test." | A Context paragraph naming the gap, an Outcome with a Done-when, then subtasks that each name an observable result. |

Output shape:

1. **Context** — the SCQ intro as prose: the stable fact, what disturbed it, the cost of leaving it. No "Situation/Complication" labels.
2. **Outcome** — one sentence stating what is true when the plan is done, with a verifiable end product. This is the Answer from Phase 1.
3. **Subtasks** — each names an observable result and carries its own **Done when**. Ordered by dependency, not by difficulty. A subtask whose Done-when a reviewer cannot check is intellectually blank (see `tasks.md`).
4. **Files** — what gets created or edited, so the reader sees what the change touches.
5. **Risks / Assumptions** — kept through pruning, never cut for concision.
6. **Verification** — how the owner confirms the outcome held.

Headings are achievements, not stages: "Reconcile the rules against existing gates", not "Step 2".

## Idea one-pager

The artefact that comes out of refining a raw idea (e.g. the idea-refine skill). Its job is to make a proposed direction legible and to make the trade-offs explicit — the **Not Doing** list is the most valuable part, because focus is saying no to good ideas.

Output shape:

1. **Problem statement** — one "How might we" sentence. State the cost of the status quo, or the reader has no reason to care.
2. **Recommended direction** — the chosen approach and why it beats the alternatives, in two or three short paragraphs.
3. **Key assumptions to validate** — each with how to test it. An untested assumption is the most common idea-killer; name it, don't bury it.
4. **MVP scope** — the minimum version that tests the core assumption. What's in, what's out.
5. **Not doing (and why)** — the good ideas being declined, each with its reason. Make the trade-off explicit.

| Bad | Good |
|---|---|
| "We should build an AI assistant to help users." | "How might we cut the time a user spends finding the right doc from 4 minutes to under 30 seconds?" |
| "Out of scope: lots of things." | "Not doing: offline mode — every target user is online; building it now would double the sync surface for no current benefit." |

## Number discipline

Phase 1's never-invent-a-number rule applies in full here: a plan or one-pager leans on figures like current latency, today's error rate, or the cost of the status quo, and a fabricated one that makes the proposal look good is the most damaging kind. When the figure is missing, bracket a placeholder for the owner or ask.

## Review additions

Beyond the universal Phase 6 gate, check:

- Does the Context / Problem state the cost of the status quo, not just the change?
- Does every subtask or assumption carry a checkable Done-when or a test?
- Is there a Not Doing / out-of-scope list, and does each entry give its reason?
- Did risks, assumptions, and dependencies survive pruning?
