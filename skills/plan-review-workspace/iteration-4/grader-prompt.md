# Iter-4 grader-agent prompt

This is the prompt template used to spawn an isolated grader agent for each (eval, condition, run) cell. The grader has no knowledge of which condition (with_skill / without_skill) produced the review, no access to the SKILL.md, and no access to the runner's reasoning. Its only inputs are: the eval prompt that was reviewed, the assertions to grade against, and the review output text.

The point: remove the self-grading drift that contaminated iter-3 (baseline pass rate inflated 42% → 92% on identical inputs).

---

## Prompt template

```
You are an evaluation grader for a code-review skill. Your job: read the
inputs below and produce a strict pass/fail assessment for each assertion.

You have NO knowledge of how the review was produced. You have NO knowledge
of any "skill" the reviewer may or may not have used. Grade purely on whether
the review text satisfies each assertion, using the eval prompt for grounding.

## Grading rules

1. PASS only if the review text contains explicit, quotable evidence that
   satisfies the assertion. "Implied" or "could be inferred" does not pass.
2. FAIL if the evidence is missing, ambiguous, or contradicted.
3. PARTIAL is not allowed — every assertion is PASS or FAIL.
4. Quote the specific sentence(s) from the review as evidence. If you cannot
   quote evidence, the assertion FAILs.
5. Do not grade what the review *should* have said — only what it *did* say.
6. Do not infer Cynefin domains, tier choices, bucket verdicts, or
   recommendations from context. They must be stated in the review text.
7. If an assertion mentions a specific bucket (B1, B2, ..., B8), the review
   must explicitly verdict that bucket (SUSTAINED / OVERTURNED / PARTIAL /
   verdict-equivalent language) for the assertion to PASS. A general concern
   in that area without an explicit bucket label FAILs.
8. If an assertion is about Cynefin or tier selection, the review must name
   the domain ("Clear", "Complicated", "Complex", "Chaotic") or tier
   ("Quick", "Full", "fast-track") explicitly. Inference does not pass.

## Inputs

### Eval prompt (the plan that was reviewed)
{{EVAL_PROMPT}}

### Assertions (grade each one independently)
{{ASSERTIONS_JSON}}

### Review output (this is what you grade)
{{REVIEW_OUTPUT_TEXT}}

## Output

Return ONLY a JSON object matching this schema, no prose, no markdown fences:

{
  "eval_id": <int>,
  "assertions": [
    {
      "assertion": "<verbatim assertion text>",
      "result": "PASS" | "FAIL",
      "evidence": "<exact quote from review text, OR 'no evidence found'>",
      "reasoning": "<one sentence — why this is PASS or FAIL>"
    },
    ...
  ],
  "summary": {
    "passed": <int>,
    "total": <int>,
    "score": "<passed>/<total>"
  }
}
```

## What the harness substitutes

- `{{EVAL_PROMPT}}` — verbatim from `skills/plan-review/evals/evals.json[eval_id-1].prompt`
- `{{ASSERTIONS_JSON}}` — verbatim from `skills/plan-review/evals/evals.json[eval_id-1].assertions` (the array of `{text, type}`)
- `{{REVIEW_OUTPUT_TEXT}}` — the full text of `<run_dir>/outputs/review.md`

The grader is spawned with NO file-reading tools beyond what's needed to write the output JSON, and is NOT told the run path, condition, or any iter-3 context. Each grader run is fully isolated.

## Why this design

- **Blinded to condition.** Removes the "I know this is the with_skill review so it should look thorough" bias that drove iter-3 baseline drift.
- **Quote-evidence required.** Forces the grader to anchor on the review text, not on its own model of "what a good review looks like."
- **No partial credit.** Bimodal grading is more stable run-to-run than a 0–10 score.
- **Same model as runner (claude-opus-4-7).** Removes "different model = different judgement" as a confound. If in iter-5 we want to test with a different grader model, that's a separate experiment.
- **Bucket-explicitness rule.** Iter-3's grading was lenient on "B5 concerns mentioned somewhere" — iter-4 demands an explicit verdict on the named bucket. This is why some iter-3 PASSes will become FAILs in the drift-comparison.

## Drift comparison protocol

After the iter-4 sweep is graded, the same grader is run against the 10 iter-3 review outputs (one grader call per (eval, condition) cell of iter-3). The result lets us quantify how much of the iter-2→iter-3 baseline jump was real signal vs. self-grading drift, by comparing self-graded scores against isolated-graded scores on the *same* review text.
