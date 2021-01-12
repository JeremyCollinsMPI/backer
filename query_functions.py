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
  print(result)
  result = [x[0] for x in result if x[1] > threshold]
  response = {'result': result}
  return response

def is_relevant_document(query, documents, threshold=0.2, use_api=False):
  if use_api:  
    r = requests.post(url + ':8080/is_relevant_document', data=json.dumps({'query': query, 'documents': documents}))
    return r.json()
  embeddings = Embeddings({"method": "transformers", "path": "sentence-transformers/bert-base-nli-mean-tokens"}) 
  sources_dictionary = {}
  for i in range(len(documents)):
    document = documents[i]
    document = document.replace('!', '.')
    sentences = document.split('.')
    for sentence in sentences:
      sources_dictionary[sentence] = i
  sources = list(sources_dictionary.keys())
  is_relevant_response = is_relevant(query, sources, threshold=0.2, use_api=False)
  is_relevant_result = is_relevant_response['result']
  print(is_relevant_result)
  indices_result = [sources_dictionary[source] for source in is_relevant_result]
  indices_result = np.unique(indices_result)
  print(indices_result)
  result = [documents[index] for index in indices_result]
  response = {'result': result}
  return response

'''
writing one which only returns most relevant
'''  

def is_most_relevant(query, sources, threshold = 0.2, use_api=False):
  if use_api:  
    r = requests.post(url + ':8080/is_most_relevant', data=json.dumps({'query': query, 'sources': sources}))
    return r.json()
  embeddings = Embeddings({"method": "transformers", "path": "sentence-transformers/bert-base-nli-mean-tokens"})
  sections = sources
  similarities = embeddings.similarity(query, sections)
  result = zip(sources, similarities)
  result = sorted(result, key = lambda x: x[1], reverse=True)
  print(result)
  result = [x for x in result if x[1] > threshold]
  if result == []:
    return  {'result': result}
  result = [result[0][0]]
  response = {'result': result}
  return response

def is_most_relevant_document(query, documents, threshold=0.2, use_api=False):
  if use_api:  
    r = requests.post(url + ':8080/is_most_relevant_document', data=json.dumps({'query': query, 'documents': documents}))
    return r.json()
  embeddings = Embeddings({"method": "transformers", "path": "sentence-transformers/bert-base-nli-mean-tokens"}) 
  sources_dictionary = {}
  for i in range(len(documents)):
    document = documents[i]
    document = document.replace('!', '.')
    sentences = document.split('.')
    for sentence in sentences:
      sources_dictionary[sentence] = i
  sources = list(sources_dictionary.keys())
  is_most_relevant_response = is_most_relevant(query, sources, threshold=0.2, use_api=False)
  is_most_relevant_result = is_most_relevant_response['result']
  indices_result = [sources_dictionary[source] for source in is_most_relevant_result]
  indices_result = np.unique(indices_result)
  print(indices_result)
  result = [documents[index] for index in indices_result]
  response = {'result': result}
  return response
