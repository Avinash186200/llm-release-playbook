# Eval report: prompt v14

```text
Version: app a1b2c3d, prompt qa-v14, model model-large-2026-01-15, index policies-v3
Judge: judge-model-b-2025-11-01 (different family from the answer model)
Golden set: v7, 120 cases (100 dev, 20 held-out), k = 3, metric pass^3

All cases:  111/120 = 92.5%  (95% 86.4% to 96.0%)   gate at 0.80: pass
Dev:         93/100 = 93.0%  (95% 86.3% to 96.6%)   gate at 0.80: pass
Held-out:     18/20 = 90.0%  (95% 69.9% to 97.2%)   gate at 0.80: unsure

Paired vs v13 (same 120 cases): only_v13 3, only_v14 12, sign test p = 0.035
```

## By tag

| Tag | v13 | v14 | Note |
|-----|-----|-----|------|
| lookup | 28/30 | 29/30 | within noise |
| multi_hop | 24/30 | 27/30 | helped |
| no_answer | 24/30 | 28/30 | helped: fewer guesses |
| adversarial | 26/30 | 27/30 | within noise |

No tag group got worse.

## Judge calibration

Hand-labelled 80 outputs. Agreement 91%, Cohen's kappa 0.79. Most disagreements were partial answers the judge
marked as pass. Rubric updated for the next release, not this one, so the comparison stays fair.

## Is the improvement real?

1. Paired sign test p = 0.035 on the full set. Yes.
2. Held-out moved the same way (17/20 to 18/20). Too small to prove alone, but not against.
3. No tag group worse.
4. pass^3 improved, not only pass@3.
5. Judge unchanged between v13 and v14 runs.
6. Cost per 1,000 requests +6% (longer answers with quotes). p95 latency +120 ms. Both inside budget.

Decision: real improvement. The held-out `unsure` is a sample-size problem, so 30 new held-out cases from last
month's traffic go into golden set v8.
