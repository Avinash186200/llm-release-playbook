# Senior review: prompt v14 change

## Change basics

- [x] Description says what changed, why, and how it was tested | status: PASS | evidence: https://repo.example.org/qa/pull/57
- [x] Diff is against the current target branch, not a stale base | status: PASS | evidence: https://repo.example.org/qa/pull/57/files
- [x] Docstrings and comments match what the code now does | status: PASS | evidence: https://repo.example.org/qa/pull/57#discussion-3

## Pattern checks

- [x] Sibling defects: the same bug pattern searched for in other files and fixed or listed | status: PASS | evidence: https://repo.example.org/qa/pull/57#discussion-5
- [x] Replies match code: each "fixed" reply checked against the actual diff | status: PASS | evidence: https://repo.example.org/qa/pull/57#discussion-8
- [x] Dead switches: every new flag or config value is read somewhere and changes behaviour | status: PASS | evidence: https://repo.example.org/qa/pull/57#discussion-9
- [x] Cross-PR coupling: no hidden dependency on another open change merging first | status: PASS | evidence: https://repo.example.org/qa/pull/57#discussion-10
- [x] Pending decisions: no open question left unanswered in the thread | status: PASS | evidence: https://repo.example.org/qa/pull/57
- [x] Changed return value meaning traced to every call site | status: N/A | evidence: no function signatures changed
- [x] Claims in the description (for example "closes X", "no behaviour change") verified | status: PASS | evidence: https://repo.example.org/qa/pull/57#discussion-11

## LLM-specific checks

- [x] Prompt change scored on the golden set with an interval | status: PASS | evidence: [eval report](eval-report.md)
- [x] Judge or rubric not changed in the same change as the prompt | status: PASS | evidence: [eval report](eval-report.md)
- [x] Tool permissions not widened without reason | status: N/A | evidence: no tool change
- [x] New retrieved or user text treated as data, never as instructions | status: PASS | evidence: https://ci.example.org/qa/runs/412#injection
- [x] Token caps and retry limits present on new loops | status: N/A | evidence: no new loops
- [x] New fields logged per the metrics spec | status: PASS | evidence: https://repo.example.org/qa/pull/57#discussion-12

## Before approval

- [x] CI fully green on the latest commit, every check explained | status: PASS | evidence: https://ci.example.org/qa/commit/a1b2c3d
- [x] Approval is for the latest commit, not an earlier one | status: PASS | evidence: https://repo.example.org/qa/pull/57#review-2
- [x] No blockers open. Non-blocking items recorded as follow-ups | status: PASS | evidence: https://repo.example.org/qa/pull/57#follow-ups
