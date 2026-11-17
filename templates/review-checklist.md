# Senior review checklist

The checks I run before I approve a pull request. Most of them catch defects that tests do not.

Format of each line: `- [x] Item | status: PASS | evidence: <link>`.

## Change basics

- [ ] Description says what changed, why, and how it was tested | status: | evidence:
- [ ] Diff is against the current target branch, not a stale base | status: | evidence:
- [ ] Docstrings and comments match what the code now does | status: | evidence:

## Pattern checks

- [ ] Sibling defects: the same bug pattern searched for in other files and fixed or listed | status: | evidence:
- [ ] Replies match code: each "fixed" reply checked against the actual diff | status: | evidence:
- [ ] Dead switches: every new flag or config value is read somewhere and changes behaviour | status: | evidence:
- [ ] Cross-PR coupling: no hidden dependency on another open change merging first | status: | evidence:
- [ ] Pending decisions: no open question left unanswered in the thread | status: | evidence:
- [ ] Changed return value meaning traced to every call site | status: | evidence:
- [ ] Claims in the description (for example "closes X", "no behaviour change") verified | status: | evidence:

## LLM-specific checks

- [ ] Prompt change scored on the golden set with an interval | status: | evidence:
- [ ] Judge or rubric not changed in the same change as the prompt | status: | evidence:
- [ ] Tool permissions not widened without reason | status: | evidence:
- [ ] New retrieved or user text treated as data, never as instructions | status: | evidence:
- [ ] Token caps and retry limits present on new loops | status: | evidence:
- [ ] New fields logged per the metrics spec | status: | evidence:

## Before approval

- [ ] CI fully green on the latest commit, every check explained | status: | evidence:
- [ ] Approval is for the latest commit, not an earlier one | status: | evidence:
- [ ] No blockers open. Non-blocking items recorded as follow-ups | status: | evidence:

Never approve with a blocker open. A comment saying "approve once X is fixed" is not an approval.
