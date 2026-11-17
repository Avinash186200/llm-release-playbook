# Contributing

I keep this repo small on purpose. Changes are welcome if they make a release safer or a template easier to fill.

## How

1. Open a pull request with a short description: what changed, why, and how you checked it.
2. Keep the writing plain: short sentences, first person, no marketing words.
3. If you change a template, update its filled example in `examples/` in the same pull request.
4. If you change a tool, add or update a test in `tests/`.
5. Run the checks before you push:

   ```bash
   pytest -q
   python tools/check_links.py .
   python tools/checklist_lint.py examples/go-no-go.md examples/rollout.md examples/review-checklist.md
   ```

## Rules

- No real company, product or person names in examples. Use the fictional document Q&A assistant.
- No real links in examples. Use the `example.org` host.
- Tools stay standard library only.
- One idea per pull request.
