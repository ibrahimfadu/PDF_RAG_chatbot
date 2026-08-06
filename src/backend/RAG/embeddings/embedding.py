class Embedding:

  def encoding_text(self,chunks : list[str] | str)->list[float]:
        if not chunks:
            raise ValueError("No chunks found..")
        clean_chunks = [ c.encode("utf-8", errors="ignore").decode("utf-8") for c in chunks ]
        try:
            embedded = self.embedding_model.encode(clean_chunks)
            return embedded
        except Exception as e:
            raise RuntimeError(f"Error {e}")