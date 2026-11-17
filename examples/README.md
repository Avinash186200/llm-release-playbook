# Worked examples: document Q&A assistant

Every template in this repo, filled in for one fictional product.

**The product.** A document Q&A assistant. Staff ask questions in plain English about a set of internal policy
documents (travel, expenses, leave, security). The assistant retrieves passages, answers with citations, and says
"I don't know" when the documents do not cover the question. It has one read-only tool, `search_documents`.

**The release.** Prompt v14 replaces v13. The change adds a "quote the passage first, then answer" step to cut
ungrounded answers. The model and the index stay the same.

All names, numbers and links here are made up for illustration. The links point to a placeholder host.

| File | Template |
|------|----------|
| [go-no-go.md](go-no-go.md) | `checklists/go-no-go.md` |
| [rollout.md](rollout.md) | `checklists/rollout.md` |
| [eval-results.json](eval-results.json) | Input for `tools/release_gate.py` |
| [eval-report.md](eval-report.md) | Report shape from `playbooks/evaluation.md` |
| [audit-round-brief.md](audit-round-brief.md) | `templates/audit-round-brief.md` |
| [review-checklist.md](review-checklist.md) | `templates/review-checklist.md` |
| [model-card.md](model-card.md) | `templates/model-card.md` |
| [adr-001-quote-then-answer.md](adr-001-quote-then-answer.md) | `templates/adr.md` |
| [incident-postmortem.md](incident-postmortem.md) | Postmortem from `playbooks/incident-response.md` |

Try the tools on them:

```bash
python tools/checklist_lint.py examples/go-no-go.md examples/rollout.md examples/review-checklist.md
python tools/release_gate.py examples/eval-results.json
python tools/release_gate.py examples/eval-results.json --split held_out
```

The last command returns `unsure`: 18 of 20 held-out cases is not enough to prove 80% on its own. The report
explains why the release still went ahead on the full set, and what was added to the held-out slice.
