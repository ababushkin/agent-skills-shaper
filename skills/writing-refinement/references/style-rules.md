# Style Rules (all document types)

Apply these during Phase 4. The goal is the shortest path to the reader's mind without losing operational facts.

## Sentence mechanics

**Characters as subjects, actions as verbs.** Find the doer; make it the subject; make its activity a specific verb.

| Bad | Good |
|---|---|
| "There was a failure in the deployment process due to configuration drift." | "The deploy failed because the staging config drifted from prod." |
| "Request dropping occurs at high utilization." | "The load balancer drops requests above 1k RPS." |
| "It was decided that caching should be utilized." | "We will cache session tokens in Redis." |

**Old before new.** Start with what the reader knows; end with the new term. The end of a sentence is the stress position — the reader emphasizes whatever sits there.

| Bad | Good |
|---|---|
| "Edge Workers, which intercept requests at the CDN layer, will reduce load time." | "To cut load time, we will intercept requests at the CDN layer using Edge Workers." |

**Hand-product test.** Every task, goal, or milestone must imply a tangible end product the reader can visualize. "Investigate latency" fails; "a report naming the three slowest queries in /orders" passes.

## Nominalizations — reverse them

Abstract nouns derived from verbs freeze action. Turn them back into verbs.

| Frozen | Active |
|---|---|
| utilization | use |
| implementation | implement |
| optimization | optimize |
| investigation | investigate |
| facilitation | help / enable |
| determination | decide |
| reduction | reduce / cut |

## Vocabulary watchlist

Sweep the document for these and replace:

| Avoid | Prefer | Why |
|---|---|---|
| load-bearing / vital | essential / required | Overworked metaphor distracts from the technical reality |
| bottleneck | shortage / delay / hold-up | Cliché that hides the specific cause of constriction |
| target | objective / goal / aim | Often "attained" without being "hit" |
| blueprint | plan / scheme / spec | Implies a final design; usually misused for early ideas |
| ceiling | limit / maximum | "Raise the limit" is clearer than "raise the ceiling" |
| interface with | talk to | Jargon for a plain act |
| impact (as verb) | affect | "Impact" blunts a painful truth |
| leverage (as verb) | use | Same |
| basically / actually / quite / virtually / a bit | *(delete)* | Little qualifiers dilute authority |
| "at this point in time" | now | Shortest path to the mind |
| "in order to" | to | Same |
| "It should be noted that…" / "It is important to…" | *(start directly)* | Throat-clearing adds nothing |
| full and complete / each and every | full / each | Redundant pairs |

## Keep the exact term; cut only the hiding metaphor

Use the precise technical term whenever it is accurate — `mutex`, `P99`, `idempotent` earn their place. Replace a metaphor only when it hides the cause the reader needs. A figure of speech that names no mechanism leaves the reader guessing; the concrete noun states it.

| Hides the cause | States it |
|---|---|
| "The seam lives in the orchestrator." | "The recovery points are in the orchestrator." |
| "The missing move is the status check." | "The orchestrator checks the status." |
| "This keeps reviewable work from being stranded." | "This prevents stranded branches." |

## The pruning safety rule

Concision serves clarity, never the reverse. Before deleting a sentence, ask: does it carry a dependency, risk, assumption, or constraint? If yes, compress it into fewer words — do not remove it. A short document that omits the rollback plan is worse than a longer one that keeps it.
