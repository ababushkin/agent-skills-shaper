# Engineering Design Docs / RFCs

This file governs **how each section reads**, not which sections exist or their order. Inside the Shaper shape:design skill (design-doc track), that skill owns the section set, the gates, and the NFR taxonomy (`references/nfr-categories.md`); this file only refines the prose within whatever structure it mandates. Used standalone, treat the sections below as the conventional shape, not a gate.

Map the six-phase workflow onto the design-doc sections. The reader should experience a story — where we are, what broke, what we will do — never a framework.

## Section-by-section guidance

**## Problem**
Open with the stable, accepted fact (the situation), then the disturbance and its cost. The undesired current state must be concrete: a number, an incident, a failing metric. End the section with the one-sentence answer — the recommended move — so the reader holds the conclusion before the detail.

> Bad: "Latency has been a concern for some time and various stakeholders have expressed interest in improvements."
> Good: "Checkout completes in 1.2s today. Since the loyalty service launched in March, P95 has climbed to 4.1s, and conversion is down 6%. We will move loyalty lookups to an async path, restoring sub-1.5s checkout."

**## Context**
Anchor the reader in stable, known facts before introducing anything new. Old before new applies at the section level: architecture the reader knows first, the recent change last.

**## Constraints / NFRs**
Order by degree (most binding first) or by structure (latency / cost / compliance). Each constraint gets a number where one exists.

**## Alternatives**
The set of alternatives must be MECE — no two options that partially overlap, no obvious option missing. Open each alternative with its summary effect ("Buys 5x headroom at 2x infra cost"), then the detail. State why each loses to the recommendation.

**## Recommended Approach**
Old before new: start from the system as it is, walk to the proposed change. The newest component lands at the ends of sentences, where the stress position emphasizes it. Headings within this section are achievements ("Route loyalty calls through the event bus"), not labels ("Architecture").

**## Operability / Rollout Plan**
Every gate gets a verifiable "Done when": "Done when canary error rate holds under 0.1% for 24h", not "monitor and proceed if healthy". Rollback criteria are operational facts — never prune them.

## Design-doc review additions

Beyond the universal Phase 6 gate, check:

- Does the Problem section state the cost of the status quo in numbers?
- Is the recommendation stated in one sentence before the detail begins?
- Are alternatives genuinely exclusive and exhaustive?
- Do rollout gates have visualizable, verifiable end states?
- Did assumptions, risks, and dependencies survive pruning?
