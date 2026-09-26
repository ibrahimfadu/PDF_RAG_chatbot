# Document Ingestion Standard

The ingestion pipeline has five stages: extraction, normalization, chunking, embedding, and indexing.

Extraction supports PDF, Markdown, HTML, and plain text. During normalization, repeated whitespace is collapsed, Unicode is normalized to NFC, and page headers can be removed when they match a configured template.

The reference chunking policy is 500 tokens with 75-token overlap. A heading is kept with the following paragraph when possible. Tables are converted into row-oriented text before chunking.

Scanned PDFs require OCR. If OCR confidence is below 0.82 for a page, the page is flagged for review rather than silently accepted.

Every indexed chunk stores: document_id, chunk_id, source_path, page_or_section, text, token_count, embedding_model, and ingestion_timestamp.

A document is not considered searchable until indexing completes successfully. Failed embedding jobs are retried twice with exponential backoff. After the second failure, the document enters the `embedding_failed` queue.
