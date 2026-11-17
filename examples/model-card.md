# Model card: document Q&A assistant

## Summary

- What it does: answers staff questions about internal policy documents, with citations
- Who uses it: staff, through the internal chat page
- Version: app a1b2c3d, prompt qa-v14, model model-large-2026-01-15, index policies-v3
- Release date: 2026-03-03
- Owner (role): feature engineer

## System

- Base model and provider: a hosted large language model, pinned version
- Pinned model version: model-large-2026-01-15
- Fallback model: model-medium-2025-12-01 (answers flagged as degraded)
- Retrieval: hybrid BM25 + dense, 400-token chunks with 50 overlap, top-k 6, reranked to 4
- Tools and their permissions: `search_documents`, read-only
- Guards: injection detector on retrieved chunks, output redaction, quote-match grounding check

## Intended use

- In scope: questions answered by the policy documents
- Out of scope: legal advice, questions about individual cases, anything not in the documents
- Users should not rely on it for: final decisions on expenses or leave; the cited policy is the authority

## Evaluation

- Golden set version and size: v7, 120 cases
- Split: 100 dev, 20 held-out
- Repeats (k): 3, metric pass^3
- Results: all 111/120 (95% 86.4% to 96.0%); dev 93/100 (86.3% to 96.6%); held-out 18/20 (69.9% to 97.2%)
- Paired comparison with v13: only_v13 3, only_v14 12, p = 0.035
- Judge model and calibration: different family from the answer model; 91% agreement, kappa 0.79 on 80 labels

## Known limits and failure modes

- Tables split across chunks can lose their header row; answers about table values are less reliable.
- Questions that combine three or more documents fail more often (multi_hop 26/30).
- Policies updated in the last 24 hours may not be indexed yet.

## Safety

- Injection suite result: 40/40 blocked or ignored
- Refusal and over-refusal results: 30/30 out-of-scope refused; 2 of 200 normal questions over-refused
- Data handling: prompts and answers kept 30 days, redacted; no user identifiers in prompts

## Cost and latency

- Tokens per request: median 3,300 in / 220 out; p95 5,900 in / 480 out
- Cost per 1,000 requests: $6.15
- p50 / p95 latency: 1.7 s / 2.7 s

## Monitoring

- Dashboard link: https://dash.example.org/qa/release
- Alerts: error rate, p95, cost per request, daily spend, grounding failures, refusal rate, guard spikes

## Change history

| Version | Date | Change | Eval result |
|---------|------|--------|-------------|
| qa-v13 | 2026-01-20 | Added no-answer instruction | 102/120 pass^3 |
| qa-v14 | 2026-03-03 | Quote-then-answer step and quote-match check | 111/120 pass^3 |
