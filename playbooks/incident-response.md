# Incident response for LLM applications

LLM incidents look different from normal outages. The service is often "up" and returning 200s while it gives
wrong answers, leaks data, or burns money. This page covers the four I plan for, plus the common steps.

## Common steps for every incident

1. **Declare it.** Name an incident lead. One person decides; others investigate.
2. **Stop the harm first.** Roll back, switch the flag, or disable the tool. Find the cause second.
3. **Record the exact state.** Running version (digest, prompt version, model id, index version), the time it
   started, and the first signal that showed it.
4. **Keep evidence.** Save sample traces and request ids before log retention removes them.
5. **Communicate.** A short status every 30 minutes: what we know, what we did, next update time.
6. **Close with a test.** Every incident ends with a new golden case, a new alert, or a new standing rule.

## Severity

| Level | Meaning | Example |
|-------|---------|---------|
| SEV1 | Data leak, harmful output at scale, or full outage | System prompt or another user's data in answers |
| SEV2 | Wrong answers or cost growth affecting many users | Grounding failures up 3x after a release |
| SEV3 | Limited impact, workaround exists | One tool failing, answers still grounded |

## 1. Hallucination spike

**Signals:** grounding failure rate up, thumbs-down up, citation-missing rate up, support tickets quoting wrong
facts.

**Triage**

1. Check what changed: prompt, model id (providers update aliases), retrieval index, chunking, document set.
2. Pull 20 failing traces. Is retrieval returning the right chunks?
   - Wrong or empty chunks: retrieval problem (index, embeddings, filters, stale documents).
   - Right chunks, wrong answer: generation problem (prompt, model, context too long, truncation).
3. Check context length. Truncated context often drops the very chunk that held the answer.
4. Check a pinned model version against the alias. A silent provider update can shift behaviour.

**Contain:** roll back the last change. If nothing changed on your side, pin the previous model version, or
raise the grounding check to refuse unsupported answers until fixed.

**Close:** add the failing questions to the golden set with their correct sources.

## 2. Prompt injection

**Signals:** answers that follow instructions from document content, unexpected tool calls, the system prompt
appearing in output, outbound requests to unknown hosts, a user report.

**Triage**

1. Find the source of the injected text: user input, an uploaded document, a web page, a tool result.
2. List every tool call made in the affected sessions. Did any write, send or delete?
3. Check whether data from other users or other tenants appeared in any answer.

**Contain**

- Disable the affected tool or ingest path. Quarantine the poisoned document.
- If data left the system, treat it as a security incident and follow your data-breach process.
- Rotate any secret that may have been exposed.

**Close:** add the payload to the injection suite. Tighten the tool policy (allow list, confirmation step).
Treat all retrieved text as data, never as instructions, and test that.

## 3. Cost blow-up

**Signals:** spend alert, tokens per request up, request count up without user growth, retry counts up.

**Triage**

1. Split cost by route, tenant, model and prompt version. Find the one that moved.
2. Look for loops: agent steps or repair retries without a cap.
3. Look for context growth: conversation history not trimmed, too many chunks retrieved.
4. Look for abuse: one key or one user sending a large share of traffic.
5. Check cache hit rate. A prompt change that edits the shared prefix can drop it to zero.

**Contain:** lower the per-request token cap, cap agent steps, rate-limit the heavy key, or route to a cheaper
model for non-critical paths. Roll back the change that moved cost.

**Close:** add a cost-per-request alert at 1.5 x baseline and a hard daily cap.

## 4. Provider outage or degradation

**Signals:** timeouts, 429 or 5xx from the provider, latency up, provider status page.

**Triage**

1. Confirm it is the provider: check their status page and a direct test call.
2. Check whether it is one region, one model or all.
3. Check your own rate limits and quota first. A 429 is often your quota, not their outage.

**Contain**

- Fail over to a fallback model or region if you have one, and say so in the answer metadata.
- Turn on a degraded mode: cached answers for common questions, or a clear "try again later" message.
- Back off retries with jitter. Retry storms make outages longer.

**Close:** note the time to detect and the time to fail over. Test the fallback path every release, because a
fallback that is never exercised does not work when you need it.

## Postmortem template

```text
Title:
Severity:
Start / detect / mitigate / resolve times:
What users saw:
What changed:
Root cause:
What went well:
What went badly:
Actions (each with an owner role and a test or alert that proves it is done):
```

Write it blameless. The question is what let the defect reach users, not who wrote it.
