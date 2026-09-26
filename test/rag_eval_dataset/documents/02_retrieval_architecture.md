# Aurora Retrieval Platform

Aurora is NRL's internal retrieval platform. Version 3.2 uses a hybrid retrieval pipeline: lexical BM25 retrieval runs first, followed by dense-vector retrieval. The candidate sets are merged, duplicate chunks are removed, and a cross-encoder reranker selects the final context.

Default production settings for Aurora 3.2:
- BM25 candidates: 40
- Dense candidates: 40
- Maximum merged candidates before reranking: 60
- Reranker candidates: 30
- Final context chunks: 8
- Chunk size: 500 tokens
- Chunk overlap: 75 tokens

The embedding model used by the reference deployment is `aurora-embed-768`, which produces 768-dimensional vectors. The reranker is `aurora-rerank-base`.

A query is considered "retrieval-supported" when at least one final context chunk directly supports the answer. The system must not invent a source when no chunk supports the answer.

Version 3.2 introduced reciprocal-rank fusion. Version 3.1 used weighted score addition. Therefore, notes written for 3.1 should not be used to infer the ranking formula for 3.2.
