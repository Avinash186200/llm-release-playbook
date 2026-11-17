# Evaluation playbook

A golden set is a small sample. Every number from it has noise. This page is how I build the set, score it, and
decide whether a change is really better.

## 1. Golden sets

- Start with 50 to 200 cases. Take them from real traffic when you can, not from your own imagination.
- Cover the main tasks, the edge cases, and every bug you have fixed. A fixed bug becomes a case.
- Each case has: an id, the input, the expected behaviour (an answer, a cited source, a refusal), and a tag.
- Keep the set in the repo, versioned. A change to the set is a reviewed change, like code.
- Tag cases by type (lookup, multi-hop, no-answer, adversarial) so you can see where a change helps or hurts.
- Include "no answer" cases. A system that always answers will look great until it meets one.

## 2. Held-out cases

- Split off 20 to 30% as held-out. Nobody looks at these while tuning prompts.
- Tune on the dev slice. Report on both. If dev goes up and held-out does not, you overfit the prompt.
- Refresh the held-out slice from new traffic every few releases. Retire cases that leaked into prompts.

## 3. Repeats and pass^k

Model outputs vary between runs, even at temperature 0 on many providers.

- Run each case k times (k = 3 or 5 is usually enough).
- pass@k: the case passes if any run passes. Good for "can it do this at all".
- pass^k: the case passes only if all k runs pass. This is what users feel, because they get one run.
- Report pass^k for release decisions. If pass@k is high and pass^k is low, the feature is flaky, not good.
- Estimate pass^k from n runs with c passes as `C(c, k) / C(n, k)`.

## 4. LLM judges

A judge is a model that scores another model's output. It is useful and easy to fool yourself with.

**Independence**

- Use a different model, or at least a different model family, from the one being judged. Models favour their
  own style.
- Give the judge the reference answer and the source text, not only the candidate.
- Hide which version produced which output. Randomise order in pairwise comparisons to remove position bias.
- Never let the judge prompt change in the same release as the system prompt. Change one thing at a time.

**Calibration**

- Label 50 to 100 outputs by hand. Run the judge on the same outputs.
- Report agreement (percent agreement and Cohen's kappa). Below about 0.6 kappa, do not trust the judge alone.
- Look at the disagreements. They usually show a rubric gap, not a judge bug.
- Recalibrate when the judge model, the rubric or the product domain changes.

Prefer exact checks where they exist: string match on ids, JSON schema checks, citation present, number within
tolerance. Use the judge only for what code cannot check.

## 5. Statistical significance

**Wilson interval for one pass rate**

For `x` passes out of `n` cases, the 95% Wilson interval is

```text
p = x / n, z = 1.96
centre = (p + z^2 / (2n)) / (1 + z^2 / n)
half   = z * sqrt(p(1 - p)/n + z^2 / (4n^2)) / (1 + z^2 / n)
range  = [centre - half, centre + half]
```

It behaves well for small `n` and for pass rates near 100%, where the normal approximation fails.
Example: 10/10 gives a range of about 72% to 100%. Ten passes out of ten is not proof.

**Gate decision**

- `pass` if the low end of the interval is at or above the threshold.
- `fail` if the high end is below the threshold.
- `unsure` otherwise. The fix for `unsure` is more cases, not a lower threshold.

`tools/release_gate.py` implements this.

**Sign test for two versions on the same cases**

- Run A and B on the same cases. Count `only_a` (A passed, B failed) and `only_b` (B passed, A failed).
- Cases where both pass or both fail carry no information about the difference.
- Under "no difference", each disagreement is a coin flip. The two-sided exact p-value is
  `2 * P(X <= min(only_a, only_b))` with `X ~ Binomial(only_a + only_b, 0.5)`, capped at 1.
- Example: 50 cases, A passes 40, B passes 46, with only_a = 2 and only_b = 8. The p-value is about 0.11.
  Six points better on 50 cases is still within noise.

## 6. When an improvement is real

I call an improvement real only when all of these hold:

1. The paired sign test gives p < 0.05 on the full set, or the gate moves from `unsure` to `pass`.
2. The held-out slice moves in the same direction.
3. No tag group got worse by more than its own noise. A gain on lookups that hides a loss on no-answer cases
   is not a gain.
4. pass^k improved, not only pass@k.
5. The judge was not changed in the same release, or the result also holds on exact checks.
6. Cost and latency did not get worse beyond budget.

If a result looks too good, check for leakage first: golden cases copied into few-shot examples, the judge seeing
the reference in the candidate, or the test set used to choose between many prompt variants.

## 7. Reporting template

```text
Version: prompt v14, model id X, index v3
Golden set: v7, 180 cases (140 dev, 40 held-out), k = 3
pass^3 dev:      121/140 = 86.4% (95% 79.8% to 91.1%)
pass^3 held-out:  33/40  = 82.5% (95% 68.0% to 91.3%)
Paired vs previous: only_prev 4, only_new 15, p = 0.019
Gate at 0.75 (dev): pass   (at 0.80 it would be unsure: low end 79.8%)
Worse tag groups: none beyond noise
Cost per 1k requests: +3%   p95 latency: +40 ms
```
