# RAG Evaluation Standard

NRL evaluates retrieval-augmented generation systems at two levels: retrieval quality and answer quality.

Retrieval metrics include Recall@k, Precision@k, MRR, and nDCG. For the reference benchmark, Recall@5 is the primary retrieval metric. Answer metrics include exact match for short factual answers, citation correctness, faithfulness, and answer completeness.

The benchmark contains 120 questions: 70 single-hop questions, 30 multi-hop questions, and 20 unanswerable questions. The unanswerable set is intentionally included to measure hallucination resistance.

A system passes the reference gate when Recall@5 is at least 0.90, citation correctness is at least 0.95, and the unanswerable hallucination rate is at most 0.05.

For multi-hop questions, all required supporting facts must be retrieved. Retrieving only one half of a two-fact chain does not count as a successful retrieval.

Evaluation should be performed on a fixed corpus snapshot. Comparing scores from different corpus versions without labeling the version is invalid.
