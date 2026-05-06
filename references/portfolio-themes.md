---
name: portfolio-themes
description: >
  Seven-category taxonomy for classifying roadmap items by strategic purpose.
  Source: Shreyas Doshi. Used in roadmap-shape and capacity allocation under Rule B3.
type: reference
cited_by:
  - skills/roadmap-shape/SKILL.md
---

# Portfolio Themes

Portfolio themes are Shreyas Doshi's taxonomy for classifying roadmap items by their strategic purpose. They are not a prioritisation method — they do not produce a rank order. Their purpose is to name what kind of work an item represents so the team can allocate capacity deliberately across the portfolio rather than letting it drift toward whichever category has the loudest advocates.

Rule B3 mandates that every roadmap item is classified into one of the seven themes, and that capacity allocation across themes is made explicit each planning cycle. A roadmap that does not do this will drift — typically toward customer specials and incrementals, at the expense of tech foundation and differentiators.

## The seven themes

| Theme | What it is | The implicit risk if over-indexed |
|---|---|---|
| **Differentiators** | Capabilities competitors don't have that customers care about | High investment without validation becomes expensive waste |
| **Table-stakes** | Capabilities needed just to be taken seriously in the market | Under-investment means customers don't evaluate you; over-investment means parity at high cost |
| **Incrementals** | Improvements to things you already do | Easy to over-invest; improvement signals are noisy and satisfaction rarely jumps |
| **Embarrassments** | Parts of the product the team is quietly ashamed of; broken windows | Ignored, they compound. Addressed, they pay trust dividends internally and externally. |
| **Customer specials** | Features driven by specific accounts or sales relationships | A roadmap that becomes 50%+ customer specials is a sales roadmap; product complexity grows non-linearly |
| **Tech foundation** | Platform, infrastructure, technical debt reduction | Under-investment causes velocity collapse over time; over-investment delays customer value |
| **Speculative bets** | High-risk, high-upside exploration; options on the future | Easy to starve; also easy to let absorb capacity without accountability |

## Using themes at roadmap shape

When building or reviewing a roadmap, classify every item by theme before capacity allocation begins. The classification surfaces the implicit portfolio mix the roadmap represents. Common patterns worth naming explicitly:

**Customer-specials dominance.** If more than a third of capacity is in customer specials, the roadmap is being shaped by deals rather than strategy. This is not automatically wrong — a company in aggressive sales mode may intend it — but it should be a deliberate choice, stated out loud, not an emergent result.

**Tech foundation starvation.** If tech foundation is consistently zero or near-zero, velocity will degrade. The cost of deferred platform work is non-linear; the signal arrives late.

**Differentiators at opinion-level confidence.** Differentiators require experimental or validated confidence before absorbing meaningful build capacity. A roadmap with high differentiator allocation and low average confidence is a roadmap of expensive bets. Route to validation slots first.

**No speculative bets.** A roadmap with nothing in the speculative category is a maintenance roadmap. That may be right for a mature product in a stable market, but it should be a choice, not an oversight.

## Themes and ICE

Portfolio theme classification does not replace ICE scoring (Rule B2). They serve different purposes: ICE scores an individual item's expected return; the theme identifies what category of work it is. A table-stakes item with a high ICE score is still table-stakes — completing it closes a parity gap, not a differentiation opportunity. Treat theme and score as orthogonal inputs to the prioritisation conversation.

## Capacity allocation

At each planning cycle, the explicit commitment is: what percentage of capacity goes to each theme, and what percentage is reserved for KTLO and validation work (Rule C3). The allocation does not need to be equal across themes — it never is. But it must be explicit. Implicit allocation is how roadmaps drift.

## Sources

- Shreyas Doshi — portfolio themes framework
- `rules/PRODUCT_RULES.md` — Rule B3 (classify items by portfolio theme; explicit allocation each cycle)
- `rules/PRODUCT_RULES.md` — Rule C3 (capacity allocation explicit, not implicit)
