# Release standard: definition of done for an LLM feature

A feature is done when every section below is met and the evidence is linked. "It worked when I tried it" is not
evidence. If a section does not apply, write why in one line.

## 1. Evals

- A golden set exists, is versioned in the repo, and covers the main user tasks plus known failure cases.
- A held-out slice exists that nobody tuned prompts against.
- The new version is scored on the full set, with repeats if outputs are not deterministic.
- The pass rate is reported with a 95% Wilson interval, not as a bare number.
- If this replaces an older version, a paired comparison on the same cases is reported (sign test).
- The release gate (`tools/release_gate.py`) returns `pass`. `unsure` means add cases, not ship.

See `../playbooks/evaluation.md`.

## 2. Grounding

- For answers built on retrieved content, every factual claim cites a source chunk.
- A grounding check runs on each answer: claims without support are flagged or the answer is refused.
- The grounding failure rate on the golden set is below the agreed limit.
- When retrieval returns nothing useful, the feature says "I don't know" instead of guessing.

## 3. Safety

- Prompt injection tests pass: instructions inside documents, tool results and user text do not change the
  system behaviour.
- Tools follow least privilege. Write or delete tools need explicit confirmation or an allow list.
- Output is checked for secrets and personal data before it leaves the service.
- Refusal behaviour is tested both ways: harmful asks are refused, normal asks are not over-refused.
- Secrets come from environment variables or a secrets manager. Logs never print their values.

## 4. Cost

- Expected tokens per request and cost per 1,000 requests are written down, from a real run.
- A per-request token cap and a daily spend alert exist.
- Retries and repair loops have a hard limit.
- Caching is used where the same prompt prefix repeats, and the hit rate is measured.

## 5. Latency

- p50 and p95 end-to-end latency are measured on realistic inputs, and time to first token for streaming.
- Each external call has a timeout. The user sees a clean error, not a hang.
- The budget is written down per step (retrieval, model, tools).

## 6. Observability

- Each request logs the fields in `../specs/metrics-instrumentation.md`.
- Traces link the request, the retrieved chunks, the prompt version, the model version and each tool call.
- Dashboards and alerts exist before launch, not after the first incident.
- Logs are redacted. Prompts with user data have a retention limit.

## 7. Rollback

- The previous version (image, prompt, model id, index) is still deployable.
- The rollback command is written in the rollout checklist and was tested on staging.
- Prompt and model changes sit behind a flag or a config value, so rollback does not need a deploy.
- Data changes are backward compatible. Index rebuilds keep the old index until the new one is confirmed.

## 8. Documentation

- A model card is filled in (`../templates/model-card.md`).
- Each non-obvious decision has an ADR (`../templates/adr.md`).
- The change log says what changed for users.

## Done means

All eight sections met, the go/no-go checklist signed, and the rollout checklist ready with abort criteria.
