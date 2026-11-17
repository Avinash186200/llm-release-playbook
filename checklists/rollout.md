# Rollout checklist

Copy this file for each release. Write the abort criteria before you start. During a rollout nobody argues
about thresholds; you read them off this page.

Format of each line: `- [x] Item | status: PASS | evidence: <link>`.

## Before you start

- [ ] Abort criteria below are filled in with numbers | status: | evidence:
- [ ] Baseline metrics captured for the current version (last 7 days) | status: | evidence:
- [ ] Rollback command written and tested on staging | status: | evidence:
- [ ] On-call person named and available for the whole window | status: | evidence:
- [ ] Exact version recorded (image digest or commit, prompt version, model id, index version) | status: | evidence:

Rollback command:

```text
(write the exact command here)
```

## Abort criteria

Abort and roll back if any of these hold for 10 minutes or more, compared with the baseline:

| Signal | Abort when |
|--------|------------|
| Error rate | above baseline + 1 point, or above 2% |
| p95 latency | above 1.3 x baseline |
| Cost per request | above 1.5 x baseline |
| Grounding failure rate | above baseline + 2 points |
| Refusal rate | above 2 x baseline |
| Thumbs-down rate | above 2 x baseline (when volume allows) |
| Any data-correctness issue | immediately |
| Any confirmed injection or data leak | immediately |

Adjust the numbers to your product, but never leave them blank.

## Stage 1: canary (1 to 5% of traffic)

- [ ] Deploy with no traffic and run the smoke test | status: | evidence:
- [ ] Send one real request end to end and read the answer | status: | evidence:
- [ ] Send one request that should fail cleanly | status: | evidence:
- [ ] Route canary share and hold at least 1 hour | status: | evidence:
- [ ] Compare all abort signals with baseline | status: | evidence:
- [ ] Read 20 sampled traces by hand | status: | evidence:

## Stage 2: staged (25%, then 50%)

- [ ] Raise to 25% and hold at least 4 hours or one peak period | status: | evidence:
- [ ] Compare abort signals again | status: | evidence:
- [ ] Raise to 50% and hold | status: | evidence:
- [ ] Spend tracking matches the forecast | status: | evidence:

## Stage 3: full (100%)

- [ ] Raise to 100% | status: | evidence:
- [ ] Watch the first hour of full traffic | status: | evidence:
- [ ] Keep the previous version deployable for at least 7 days | status: | evidence:

## After the release

- [ ] Next-day review of sampled traces for wrong-tool and ungrounded answers | status: | evidence:
- [ ] New failure cases added to the golden set | status: | evidence:
- [ ] Surprises written down as a test or a standing rule | status: | evidence:

## If you abort

1. Roll back first. Find the cause second.
2. Confirm the old version is serving (check the digest, not the tag).
3. Open an incident using `../playbooks/incident-response.md`.
4. Do not retry the rollout until the cause is understood and a test covers it.
