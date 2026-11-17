# Audit round brief

Use this when a change is big enough that one reviewer will miss things: a new feature, a model switch, a new
tool with write access. The method is simple. Many specialist reviewers look at once, you fix in one batch, one
reviewer confirms, and the scope is frozen.

## How it works

1. **Freeze the scope.** Write down what is in the change. Nothing new joins during the audit.
2. **Wide round.** Run several specialist reviewers in parallel, each on one lens. Each reviews the same frozen
   commit without seeing the others' findings, so they are not anchored.
3. **Triage.** Merge findings, remove duplicates, mark each as blocker, should-fix or follow-up.
4. **One fix batch.** Fix all blockers and should-fixes together. No new mechanisms in the fix batch. If a fix
   needs a new design, it becomes a follow-up.
5. **Confirm round.** A fresh reviewer checks each finding against the new commit and looks for regressions.
6. **Stop.** If the confirm round finds nothing new, ship. Hard limit of 5 to 6 rounds. If you hit the limit,
   the scope was too big; split it.

## Brief

- Change:
- Frozen commit:
- Scope (in):
- Out of scope:
- Round number: 1 of max 6
- Due:

## Reviewers

| Lens | What to look for | Reviewer (role) |
|------|------------------|-----------------|
| Correctness | Logic errors, edge cases, wrong defaults | |
| Evals | Golden set coverage, leakage, statistics, judge independence | |
| Security | Injection paths, tool permissions, secrets, data exposure | |
| Operations | Rollback, observability, timeouts, cost caps | |
| Interface | API and output format changes, backward compatibility | |

## Instructions for each reviewer

- Review the frozen commit only.
- For each finding give: file and line, what is wrong, why it matters, a proposed fix, and severity.
- Check sibling places: if a defect is in one file, search for the same pattern in the others.
- Do not propose new features. Note them as follow-ups.

## Findings table

| # | Lens | Location | Finding | Severity | Fix | Status |
|---|------|----------|---------|----------|-----|--------|
| 1 | | | | | | |

## Confirm round

- Fix commit:
- Each finding re-checked: yes / no
- New findings: (none means ship)
- Decision: ship / another round / split scope
