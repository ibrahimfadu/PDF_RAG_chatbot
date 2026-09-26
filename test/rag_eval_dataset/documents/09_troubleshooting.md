# Troubleshooting Guide

If search returns zero candidates, first verify that indexing completed and that the document is not in the `embedding_failed` queue.

If dense retrieval returns vectors with an unexpected dimension, verify that the configured embedding model is `aurora-embed-768`. The expected dimension is 768.

If answers contain unsupported claims, inspect the final context and citation mapping before changing the language model. A generation problem can actually originate from retrieval.

If a scanned PDF has missing text, check OCR confidence. Pages below 0.82 should be flagged for review.

If retrieval appears to use old ranking behavior, check the corpus and deployment version. Aurora 3.2 uses reciprocal-rank fusion, whereas Aurora 3.1 used weighted score addition.
