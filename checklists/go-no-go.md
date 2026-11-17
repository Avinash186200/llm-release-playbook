# Go / no-go checklist

Copy this file for each release. Each item needs a status and an evidence link.

Status values: `PASS`, `FAIL`, `N/A`. An `N/A` still needs a one-line reason in the evidence field.
Format of each line: `- [x] Item | status: PASS | evidence: <link>`. Use `[ ]` until the item is done.

Run `python tools/checklist_lint.py <this file>` before asking for sign-off.

## Release

- Release name:
- Change summary:
- Release owner: (role)
- Date:

## Quality

- [ ] Golden set pass rate meets the threshold with the Wilson low bound | status: | evidence:
- [ ] Held-out slice scored and not worse than the previous version | status: | evidence:
- [ ] Paired comparison against the previous version reported | status: | evidence:
- [ ] Grounding failure rate below the limit | status: | evidence:
- [ ] Judge calibrated against human labels for this release | status: | evidence:

## Safety

- [ ] Prompt injection suite passes | status: | evidence:
- [ ] Tool permissions reviewed (least privilege) | status: | evidence:
- [ ] Output redaction for secrets and personal data tested | status: | evidence:
- [ ] Over-refusal check on normal questions | status: | evidence:

## Cost and latency

- [ ] Cost per 1,000 requests measured and within budget | status: | evidence:
- [ ] p95 latency within budget | status: | evidence:
- [ ] Token cap and spend alert configured | status: | evidence:

## Operations

- [ ] Dashboards and alerts live | status: | evidence:
- [ ] Rollback tested on staging | status: | evidence:
- [ ] Previous version still deployable | status: | evidence:
- [ ] CI fully green on the release commit | status: | evidence:
- [ ] Rollout checklist filled with abort criteria | status: | evidence:

## Decision

- Decision: GO / NO-GO
- Open risks accepted:

## Sign-off

| Role | Name | Decision | Date |
|------|------|----------|------|
| Release owner | | | |
| Reviewer | | | |
| Operations | | | |
