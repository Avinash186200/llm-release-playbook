# Postmortem: grounding failures after index refresh

```text
Title: Grounding failures rose from 3% to 11% after the weekly index refresh
Severity: SEV2
Start / detect / mitigate / resolve: 02:00 / 02:40 / 03:05 / next day 11:00 (UTC)
What users saw: answers about the travel policy cited old rates or said "I don't know"
What changed: weekly index refresh; a new PDF export put the travel policy tables into images
Root cause: the text extractor skipped images, so the rate tables were missing from the new index
What went well: the grounding-failure alert fired in 40 minutes; rollback was one flag (index policies-v2)
What went badly: the refresh job had no check that chunk counts per document stayed close to the last run
Actions:
  - Refresh job fails if any document loses more than 20% of its chunks (owner: data engineer; proof: test)
  - Add 6 travel-rate questions to the golden set (owner: ML engineer; proof: golden set v8)
  - Run the golden set against a new index before switching it live (owner: feature engineer; proof: CI step)
```

Lesson: an index refresh is a release. It gets the same eval gate as a prompt change.
