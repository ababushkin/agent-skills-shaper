# Style Rules (all document types)

Apply these during Phase 5. The goal is the shortest path to the reader's mind without losing operational facts.

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

## Plain English by default — replace live metaphors, keep conventional terms

Write the literal mechanism. This is a technical document, not a story: use no metaphor, analogy, or figurative jargon unless the author explicitly asked for one. Default to the plain word for the thing.

Two kinds of word look alike and must be told apart:

- A **conventional technical term** is the field's normal name for the thing. It is a dead metaphor — no reader still hears the picture. Keep it; there is no plainer word. `thread`, `stream`, `tree`, `branch`, `queue`, `cache`, `handshake`, `mutex`, `P99`, `idempotent` all earn their place.
- A **live decorative metaphor** is a sport, war, building, finance, or nature word standing in for an abstract idea the author could have named directly. Replace it with the literal mechanism.

**The test:** is this the only ordinary name for the thing (keep), or did the writer reach for a colourful word when a plain one exists (replace)? When unsure, ask whether a new engineer would search the codebase for this word. They would search `mutex` and `queue`; they would not search `north-star` or `blast radius`.

A word used literally is not a metaphor. "The staging config **drifted** from prod" is literal — the values genuinely diverged over time; keep it. "Scope **drift**" standing in for "the scope grew" is decorative; write "the scope grew".

| Live metaphor (replace) | Literal mechanism (write this) |
|---|---|
| "The seam lives in the orchestrator." | "The recovery points are in the orchestrator." |
| "This change has a large blast radius." | "This change touches the auth, billing, and session modules." |
| "Edge caching is our north-star." | "The goal is to serve 95% of reads from the edge cache." |
| "Rate limiting is the brake on runaway cost." | "Rate limiting caps cost by rejecting requests above 1k RPS." |
| "We surface the error to the user." | "We show the error to the user." |
| "This is a risky bet." | "This approach may not work, because [reason]." |

### Decorative-jargon ban-list

Flag each of these and replace with the literal mechanism. The right replacement depends on what the word stands in for, so name the actual thing rather than swap one vague word for another.

| Banned (decorative) | Usually means — write that instead |
|---|---|
| bet | approach / option / the assumption being tested |
| gate | check / required condition (name the condition) |
| brake | limit / what stops X (name the limiter) |
| cap (figurative) | upper limit / maximum (a literal `rate cap` is fine) |
| blast radius | the modules or systems a change touches (list them) |
| north-star | goal / objective / target metric (state it) |
| keystone | the part the rest depends on (name the dependency) |
| spine | the structure or main path (name it) |
| seam | the boundary / integration point / recovery point |
| shepherd (as verb) | guide / route / move through |
| drift (figurative) | grew / diverged / went stale (literal config drift is fine) |
| lever | control / input / what we change to affect X |
| surface (as verb) | show / expose / report / return |

Do not over-correct conventional terms — these are the field's normal names and have no plainer word: thread, stream, tree, branch, queue, cache, handshake, mutex, fork, pipeline, backpressure, throttle.

## The pruning safety rule

Concision serves clarity, never the reverse. Before deleting a sentence, ask: does it carry a dependency, risk, assumption, or constraint? If yes, compress it into fewer words — do not remove it. A short document that omits the rollback plan is worse than a longer one that keeps it.
