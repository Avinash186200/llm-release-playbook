# Metrics and instrumentation spec

What I log for every request, what I aggregate, and what I alert on. If it is not logged, you cannot debug it
and you cannot prove a release was safe.

## 1. Per request

| Field | Type | Notes |
|-------|------|-------|
| `request_id` | string | Unique, returned to the caller |
| `trace_id` | string | Links all spans for the request |
| `timestamp` | ISO 8601 UTC | Start time |
| `route` | string | Endpoint or feature name |
| `tenant_id` | string | Hashed if needed |
| `app_version` | string | Commit or image digest |
| `prompt_version` | string | Versioned prompt id |
| `model_id` | string | Exact model version, not only the alias |
| `index_version` | string | Retrieval index version, if any |
| `input_tokens` | int | From the provider response |
| `output_tokens` | int | From the provider response |
| `cached_tokens` | int | Prompt cache hits |
| `cost_usd` | float | Computed from a versioned price table |
| `latency_ms` | int | End to end |
| `ttft_ms` | int | Time to first token, if streaming |
| `tool_calls` | int | Count |
| `tool_errors` | int | Count |
| `repairs` | int | Retries to fix invalid output (bad JSON, schema failures) |
| `refused` | bool | The model or a guard refused |
| `refusal_reason` | string | Guard name or model refusal |
| `grounding_failed` | bool | At least one claim without support |
| `citations` | int | Count of sources cited |
| `status` | string | `ok`, `error`, `timeout`, `degraded` |
| `error_type` | string | Null when ok |
| `feedback` | string | `up`, `down` or null, joined later |

Never log raw secrets. Log prompt text and outputs only with redaction and a retention limit.

## 2. Per step (spans)

One span per retrieval, model call and tool call, with `trace_id`, `span_id`, `parent_id`, `name`,
`latency_ms`, `status` and step-specific fields (chunk ids and scores for retrieval, tool name and argument hash
for tools).

## 3. Per eval run

| Field | Notes |
|-------|-------|
| `run_id`, `timestamp` | |
| `golden_set_version` | |
| `app_version`, `prompt_version`, `model_id`, `judge_model_id` | |
| `k` | Repeats per case |
| `cases[]` | `id`, `tag`, `split`, `passes`, `runs` |
| `summary` | `passed`, `total`, Wilson interval, gate decision |

## 4. Event schema examples

Request event:

```json
{
  "event": "llm_request",
  "request_id": "req_7f3a",
  "trace_id": "tr_91c2",
  "timestamp": "2026-03-04T10:15:22Z",
  "route": "/ask",
  "app_version": "a1b2c3d",
  "prompt_version": "qa-v14",
  "model_id": "model-large-2026-01-15",
  "index_version": "policies-v3",
  "input_tokens": 3120,
  "output_tokens": 210,
  "cached_tokens": 2048,
  "cost_usd": 0.0061,
  "latency_ms": 1840,
  "ttft_ms": 420,
  "tool_calls": 1,
  "tool_errors": 0,
  "repairs": 0,
  "refused": false,
  "grounding_failed": false,
  "citations": 2,
  "status": "ok"
}
```

Tool span:

```json
{
  "event": "tool_call",
  "trace_id": "tr_91c2",
  "span_id": "sp_04",
  "parent_id": "sp_01",
  "tool": "search_documents",
  "args_sha256": "5e88...",
  "latency_ms": 230,
  "status": "ok",
  "result_items": 5
}
```

Guard event:

```json
{
  "event": "guard",
  "trace_id": "tr_91c2",
  "guard": "injection_detector",
  "action": "blocked",
  "source": "retrieved_chunk",
  "chunk_id": "doc12#p4"
}
```

## 5. Dashboards

One release dashboard, split by version so canary and baseline sit side by side:

- Requests per minute, error rate, timeout rate.
- Latency p50, p95, p99 and time to first token.
- Tokens per request (input, output, cached) and cache hit rate.
- Cost per request and cost per day, with forecast.
- Tool calls per request, tool error rate, repairs per request.
- Refusal rate, grounding failure rate, citations per answer.
- Thumbs-down rate.
- Guard blocks by guard name.

## 6. Alerts

| Alert | Condition | Severity |
|-------|-----------|----------|
| Error rate | > 2% for 10 min | page |
| p95 latency | > 1.3 x 7-day baseline for 15 min | page |
| Cost per request | > 1.5 x baseline for 30 min | page |
| Daily spend | > 80% of daily cap | ticket, page at 100% |
| Grounding failures | > baseline + 2 points for 30 min | page |
| Refusal rate | > 2 x baseline for 30 min | ticket |
| Repairs per request | > 0.3 for 15 min | ticket |
| Guard blocks | sudden spike, > 5 x baseline | page |
| Provider errors | 429 or 5xx > 5% for 5 min | page |

Every alert links to the matching section of `../playbooks/incident-response.md`.
