from txtai.embeddings import Embeddings
import numpy as np
import requests
import os
import json

try:
  url = 'http://' + os.environ['backer_ip']
except:
  url = 'http://0.0.0.0'

def is_relevant(query, sources, threshold=0.2, use_api=False):
  if use_api:
  
    r = requests.post(url + ':8080/is_relevant', data=json.dumps({'query': query, 'sources': sources}))
    return r.json()
  embeddings = Embeddings({"method": "transformers", "path": "sentence-transformers/bert-base-nli-mean-tokens"})
  sections = sources
  similarities = embeddings.similarity(query, sections)
  result = zip(sources, similarities)
  result = sorted(result, key = lambda x: x[1], reverse=True)
  result = [x[0] for x in result if x[1] > threshold]
  response = {'result': result}
  return response
  
  