# Audit round brief: prompt v14

- Change: quote-then-answer prompt step, plus a grounding check that compares the quote with the source chunk
- Frozen commit: 9f8e7d6
- Scope (in): prompt v14, grounding check, two new log fields (`quote_found`, `quote_match`)
- Out of scope: new judge rubric, index rebuild, model upgrade
- Round number: 1 of max 6
- Due: 2026-02-27

## Reviewers

| Lens | What to look for | Reviewer (role) |
|------|------------------|-----------------|
| Correctness | Quote matching logic, empty retrieval path | backend engineer |
| Evals | Golden set coverage of no-answer cases, judge independence | ML engineer |
| Security | Can a document force a fake quote? | security engineer |
| Operations | New fields on the dashboard, rollback as a flag | on-call engineer |
| Interface | Answer format change for the chat front end | front-end engineer |

## Findings table

| # | Lens | Location | Finding | Severity | Fix | Status |
|---|------|----------|---------|----------|-----|--------|
| 1 | Correctness | `grounding.py:48` | Quote match is case sensitive; a capitalised quote fails a correct answer | blocker | normalise case and whitespace before matching | fixed in 4c3b2a1 |
| 2 | Correctness | `grounding.py:61` | Same pattern in the table-cell matcher (sibling defect) | blocker | same normalisation | fixed in 4c3b2a1 |
| 3 | Evals | golden set v7 | Only 18 no-answer cases; the change targets them | should-fix | add 12 no-answer cases | fixed, now 30 |
| 4 | Security | prompt v14 | A document saying "quote: ..." could inject a fake quote | blocker | quotes must match a retrieved chunk byte range, not model text | fixed in 4c3b2a1 |
| 5 | Operations | dashboard | `quote_match` not on the release dashboard | should-fix | add panel | fixed |
| 6 | Interface | front end | Quote block renders as plain text | follow-up | style quote block next release | open, ticket filed |
| 7 | Evals | judge | Suggest a new rubric for partial answers | follow-up | out of scope: next release | open |

## Confirm round

- Fix commit: 4c3b2a1
- Each finding re-checked: yes
- New findings: none
- Decision: ship. Two follow-ups carried to the next release.
