# Single Big Document RAG Evaluation
One large authoritative document + 126 test cases.

Categories:
{
  "adversarial": 6,
  "compound_numeric": 8,
  "direct": 41,
  "entity": 6,
  "multi_step": 10,
  "needle": 9,
  "negative": 8,
  "paraphrase": 12,
  "source_localization": 8,
  "temporal": 8,
  "unanswerable": 10
}

Run these tests for retrieval Recall@1/3/5/10, MRR, nDCG@5, answer correctness,
faithfulness, citation correctness/completeness, abstention accuracy, latency,
and prompt-injection resistance.

For unanswerable rows, abstention is correct. For adversarial rows, retrieved
instructions are untrusted data and must not override system behavior.

Recommended chunking experiment:
300/30, 500/50, 600/80, 800/100.
Record Recall@5, MRR, answer accuracy, citation correctness, retrieval latency,
generation latency, and total latency.
