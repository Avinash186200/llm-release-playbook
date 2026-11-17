# Go / no-go checklist: document Q&A assistant, prompt v14

## Release

- Release name: qa-assistant 2026.03.1
- Change summary: prompt v14 adds a quote-then-answer step to reduce ungrounded answers
- Release owner: (role) feature engineer
- Date: 2026-03-03

## Quality

- [x] Golden set pass rate meets the threshold with the Wilson low bound | status: PASS | evidence: [eval report](eval-report.md)
- [x] Held-out slice scored and not worse than the previous version | status: PASS | evidence: [eval report](eval-report.md)
- [x] Paired comparison against the previous version reported | status: PASS | evidence: [eval report](eval-report.md)
- [x] Grounding failure rate below the limit | status: PASS | evidence: https://ci.example.org/qa/runs/412#grounding
- [x] Judge calibrated against human labels for this release | status: PASS | evidence: https://ci.example.org/qa/calibration/2026-03

## Safety

- [x] Prompt injection suite passes | status: PASS | evidence: https://ci.example.org/qa/runs/412#injection
- [x] Tool permissions reviewed (least privilege) | status: N/A | evidence: no tool change; search_documents stays read-only
- [x] Output redaction for secrets and personal data tested | status: PASS | evidence: https://ci.example.org/qa/runs/412#redaction
- [x] Over-refusal check on normal questions | status: PASS | evidence: https://ci.example.org/qa/runs/412#over-refusal

## Cost and latency

- [x] Cost per 1,000 requests measured and within budget | status: PASS | evidence: https://dash.example.org/qa/cost?v=qa-v14
- [x] p95 latency within budget | status: PASS | evidence: https://dash.example.org/qa/latency?v=qa-v14
- [x] Token cap and spend alert configured | status: PASS | evidence: https://dash.example.org/qa/alerts

## Operations

- [x] Dashboards and alerts live | status: PASS | evidence: https://dash.example.org/qa/release
- [x] Rollback tested on staging | status: PASS | evidence: https://ci.example.org/qa/staging/rollback-2026-03-02
- [x] Previous version still deployable | status: PASS | evidence: https://registry.example.org/qa/prompts/qa-v13
- [x] CI fully green on the release commit | status: PASS | evidence: https://ci.example.org/qa/commit/a1b2c3d
- [x] Rollout checklist filled with abort criteria | status: PASS | evidence: [rollout](rollout.md)

## Decision

- Decision: GO
- Open risks accepted: held-out slice alone is `unsure` (18/20); 30 new held-out cases planned for golden set v8.

## Sign-off

| Role | Name | Decision | Date |
|------|------|----------|------|
| Release owner | (feature engineer) | GO | 2026-03-03 |
| Reviewer | (senior engineer) | GO | 2026-03-03 |
| Operations | (on-call engineer) | GO | 2026-03-03 |
