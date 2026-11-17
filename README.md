# LLM Release Playbook

[![tests](https://github.com/Avinash186200/llm-release-playbook/actions/workflows/ci.yml/badge.svg)](https://github.com/Avinash186200/llm-release-playbook/actions/workflows/ci.yml)

How I release an LLM application safely. This repo holds the standard, checklists, playbooks and templates I use
when a model, a prompt, a retrieval change or a tool change goes to production.

It is not a framework. It is a set of short documents you copy into your own repo and fill in, plus three small
scripts that check the filled-in documents, the eval numbers and the links.

## Who it is for

- Engineers who ship features built on a language model: chat, retrieval Q&A, agents with tools.
- Reviewers who need to say "yes, this can go out" with evidence, not a feeling.
- Small teams that do not have a release process yet and want one that fits on a few pages.

## How to use it

1. Read `standards/release-standard.md`. It is the definition of done. Agree on it with your team once.
2. For each release, copy `checklists/go-no-go.md` and `checklists/rollout.md` into your change folder.
3. Fill each line with a status and an evidence link. Run the linter:

   ```bash
   python tools/checklist_lint.py path/to/your/go-no-go.md
   ```

4. Run your evals, write the results as JSON (see `examples/eval-results.json`) and run the gate:

   ```bash
   python tools/release_gate.py examples/eval-results.json --threshold 0.85
   ```

   It prints `pass`, `fail` or `unsure` and exits 0, 1 or 2.
5. Keep `playbooks/incident-response.md` open during the rollout. Abort criteria are written down before you start.
6. Record decisions with `templates/adr.md` and the model with `templates/model-card.md`.

The `examples/` folder has every template filled in for one fictional product: a document Q&A assistant that
answers questions from a set of internal policy PDFs. Read an example before you fill a template.

## Map

| Path | What it is |
|------|------------|
| [`standards/release-standard.md`](standards/release-standard.md) | Definition of done for an LLM feature |
| [`checklists/go-no-go.md`](checklists/go-no-go.md) | Pre-release gate with sign-off fields |
| [`checklists/rollout.md`](checklists/rollout.md) | Canary, staged, full, with abort criteria |
| [`playbooks/evaluation.md`](playbooks/evaluation.md) | Golden sets, repeats, judges, statistics |
| [`playbooks/incident-response.md`](playbooks/incident-response.md) | Hallucination spike, injection, cost blow-up, provider outage |
| [`specs/metrics-instrumentation.md`](specs/metrics-instrumentation.md) | What to log per request, event schemas, dashboards, alerts |
| [`templates/audit-round-brief.md`](templates/audit-round-brief.md) | Running a multi-reviewer audit |
| [`templates/review-checklist.md`](templates/review-checklist.md) | Senior review checks |
| [`templates/model-card.md`](templates/model-card.md) | Model card |
| [`templates/adr.md`](templates/adr.md) | Architecture decision record |
| [`examples/`](examples/) | Worked examples for a fictional document Q&A assistant |
| [`tools/checklist_lint.py`](tools/checklist_lint.py) | Checks that every checklist item has a status and evidence |
| [`tools/release_gate.py`](tools/release_gate.py) | Pass, fail or unsure from eval results, using a Wilson interval |
| [`tools/check_links.py`](tools/check_links.py) | Checks that every relative link in the Markdown files resolves |
| `tools/check_links.py` | Offline check of relative links in the Markdown files |

## Running the checks

```bash
pip install pytest
pytest -q
python tools/check_links.py .
```

Standard library only for the tools. Python 3.10 or newer.

## Principles behind it

- Measure before you claim. A score without an interval is a guess.
- Write the abort criteria before the rollout, not during it.
- Every checklist line needs evidence a reviewer can open.
- Rollback must be a redeploy of a known version, never a rebuild.
- One fix batch per review round. New ideas wait for the next release.

## License

MIT. See `LICENSE`.
