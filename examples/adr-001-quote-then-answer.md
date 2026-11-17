# ADR-001: Quote the source before answering

- Status: accepted
- Date: 2026-02-20
- Deciders (roles): feature engineer, ML engineer, senior engineer

## Context

About 3% of answers contained a claim not supported by any retrieved chunk. Most were on no-answer and
multi-hop questions. Users trust cited answers, so an unsupported claim next to a citation is the worst case.
Budget: no more than 10% extra cost and 200 ms extra p95.

## Options

### Option A: quote-then-answer prompt with a code check

- How it works: the model must first quote the passage it relies on, then answer. Code checks the quote exists
  in a retrieved chunk.
- Pros: cheap, exact check, no extra model call.
- Cons: longer outputs; does not catch a correct quote with a wrong conclusion.
- Cost and latency: about +6% tokens, +120 ms p95 measured.

### Option B: second model call as a grounding judge

- How it works: a judge model reads the answer and chunks and flags unsupported claims.
- Pros: catches wrong conclusions as well.
- Cons: doubles calls on every request; the judge itself can be wrong; harder to debug.
- Cost and latency: about +45% cost, +900 ms p95 estimated.

## Selection criteria

| Criterion | Weight | Option A | Option B |
|-----------|--------|----------|----------|
| Cuts unsupported claims | 3 | good | better |
| Cost and latency inside budget | 3 | yes | no |
| Exact, debuggable check | 2 | yes | no |
| Simple to roll back | 1 | flag | flag |

## Decision

I propose option A because it fits the budget, the check is exact code, and the eval shows a real gain
(paired p = 0.035). Option B stays as an offline check on a sample of traffic.

## Consequences

- What gets easier: grounding failures are visible per request as `quote_match`.
- What gets harder: the answer format changed; the front end must render the quote block.
- What we must monitor: `quote_match` rate, output tokens, p95.

## Growth path

If unsupported conclusions (right quote, wrong answer) become the main failure, add option B on a sampled or
high-risk subset of requests, not on every request.

## Evidence

- [Eval report](eval-report.md)
- [Audit round](audit-round-brief.md)
