# A Practical Guide to Reliable Retrieval-Augmented Generation

Retrieval-augmented generation (RAG) combines a retrieval component with a language model. A useful evaluation strategy must separate retrieval failures from generation failures.

A retrieval system can fail because the relevant document was never indexed, because the query representation is poor, because the candidate set is too small, because ranking is weak, or because access control removed an otherwise relevant document. Generation can fail even when retrieval succeeds: the model may ignore evidence, combine facts incorrectly, cite the wrong chunk, or answer a question that the corpus does not support.

## Retrieval evaluation

Recall measures whether relevant items were retrieved. Precision measures how much of the retrieved set is relevant. MRR emphasizes the rank of the first relevant result. nDCG accounts for graded relevance and rank position.

Recall@k is especially useful for RAG because downstream generation cannot use a relevant passage that retrieval omitted. However, a high recall score does not guarantee a good answer: the context may be noisy or contradictory.

## Generation evaluation

Faithfulness asks whether claims in the answer are supported by the retrieved evidence. Citation correctness asks whether citations actually support the claims they are attached to. Completeness asks whether the answer covers the important supported parts of the question.

Unanswerable questions are important because a system should abstain when evidence is missing. A confident answer to an unsupported question is a hallucination even if the answer sounds reasonable.

## Multi-hop evaluation

A multi-hop question requires multiple pieces of evidence. For example, if one document identifies the owner of Project Cedar and another document states the owner's team, the question may require joining both facts. A system that retrieves only one document has incomplete evidence.

## Chunking

Small chunks can improve retrieval precision but may lose surrounding context. Large chunks preserve context but can dilute ranking signals and increase generation cost. Overlap helps preserve facts that cross chunk boundaries, but excessive overlap can create duplicate evidence.

## Evaluation design

Use a held-out question set with known supporting documents. Include paraphrases, entity aliases, temporal questions, multi-hop questions, negative/unanswerable questions, and adversarial prompt-injection examples. Store expected source IDs so retrieval can be evaluated independently of generation.

A robust RAG evaluation should report both aggregate scores and failure examples. A single score can hide systematic weaknesses such as poor performance on long documents, historical facts, or questions requiring abstention.
