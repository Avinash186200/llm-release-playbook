# Rollout checklist: document Q&A assistant, prompt v14

The prompt version is a config value, so rollout and rollback are flag changes, not deploys.

## Before you start

- [x] Abort criteria below are filled in with numbers | status: PASS | evidence: see table below in rollout.md
- [x] Baseline metrics captured for the current version (last 7 days) | status: PASS | evidence: https://dash.example.org/qa/baseline/2026-03-03
- [x] Rollback command written and tested on staging | status: PASS | evidence: https://ci.example.org/qa/staging/rollback-2026-03-02
- [x] On-call person named and available for the whole window | status: PASS | evidence: https://oncall.example.org/qa/2026-03-03
- [x] Exact version recorded (image digest or commit, prompt version, model id, index version) | status: PASS | evidence: https://ci.example.org/qa/commit/a1b2c3d

Rollback command:

```text
flagctl set qa.prompt_version qa-v13 --env prod
```

## Abort criteria

Baseline (qa-v13, last 7 days): error rate 0.4%, p95 2.6 s, cost $0.0058 per request, grounding failures 3.1%,
refusals 4.0%, thumbs-down 6%.

| Signal | Abort when |
|--------|------------|
| Error rate | above 1.4% |
| p95 latency | above 3.4 s |
| Cost per request | above $0.0087 |
| Grounding failure rate | above 5.1% |
| Refusal rate | above 8% |
| Thumbs-down rate | above 12% |
| Any data-correctness issue | immediately |
| Any confirmed injection or data leak | immediately |

## Stage 1: canary (5%)

- [x] Deploy with no traffic and run the smoke test | status: PASS | evidence: https://ci.example.org/qa/smoke/881
- [x] Send one real request end to end and read the answer | status: PASS | evidence: https://trace.example.org/tr_91c2
- [x] Send one request that should fail cleanly | status: PASS | evidence: https://trace.example.org/tr_91c5
- [x] Route canary share and hold at least 1 hour | status: PASS | evidence: https://dash.example.org/qa/release?from=10:00&to=11:30
- [x] Compare all abort signals with baseline | status: PASS | evidence: https://dash.example.org/qa/release/compare/canary
- [x] Read 20 sampled traces by hand | status: PASS | evidence: https://trace.example.org/qa/samples/canary-2026-03-03

## Stage 2: staged (25%, then 50%)

- [x] Raise to 25% and hold at least 4 hours or one peak period | status: PASS | evidence: https://dash.example.org/qa/release/compare/25
- [x] Compare abort signals again | status: PASS | evidence: https://dash.example.org/qa/release/compare/25
- [x] Raise to 50% and hold | status: PASS | evidence: https://dash.example.org/qa/release/compare/50
- [x] Spend tracking matches the forecast | status: PASS | evidence: https://dash.example.org/qa/cost?v=qa-v14

## Stage 3: full (100%)

- [x] Raise to 100% | status: PASS | evidence: https://dash.example.org/qa/release/compare/100
- [x] Watch the first hour of full traffic | status: PASS | evidence: https://dash.example.org/qa/release/compare/100
- [ ] Keep the previous version deployable for at least 7 days | status: FAIL | evidence: https://registry.example.org/qa/prompts/qa-v13 (in progress, day 2 of 7)

## After the release

- [x] Next-day review of sampled traces for wrong-tool and ungrounded answers | status: PASS | evidence: https://trace.example.org/qa/samples/day1
- [x] New failure cases added to the golden set | status: PASS | evidence: https://repo.example.org/qa/golden/v8
- [x] Surprises written down as a test or a standing rule | status: PASS | evidence: [ADR-001](adr-001-quote-then-answer.md)

Note: one item is still open on purpose. It shows that the linter accepts an honest `FAIL` on an unticked box.
