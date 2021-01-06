from txtai.embeddings import Embeddings
import numpy as np

def is_relevant(query, sources, threshold=0.2, use_api=False):
  if use_api:
    return 'hello'
  embeddings = Embeddings({"method": "transformers", "path": "sentence-transformers/bert-base-nli-mean-tokens"})
  sections = sources
  similarities = embeddings.similarity(query, sections)
  result = zip(sources, similarities)
  result = sorted(result, key = lambda x: x[1], reverse=True)
  result = [x[0] for x in result if x[1] > threshold]
  return result
  
  