from flask import Flask, request
from query_functions import *

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
  return {'statusCode': 200}

@app.route('/is_relevant', methods=['POST'])
def is_relevant_path():
  content = request.get_json(force=True) 
  query = content['query']
  sources = content['sources']
  return is_relevant(query, sources)

@app.route('/is_relevant_document', methods=['POST'])
def is_relevant_document_path():
  content = request.get_json(force=True) 
  query = content['query']
  documents = content['documents']
  return is_relevant_document(query, documents)

@app.route('/is_most_relevant', methods=['POST'])
def is_most_relevant_path():
  content = request.get_json(force=True) 
  query = content['query']
  sources = content['sources']
  return is_most_relevant(query, sources)

@app.route('/is_most_relevant_document', methods=['POST'])
def is_most_relevant_document_path():
  content = request.get_json(force=True) 
  query = content['query']
  documents = content['documents']
  return is_most_relevant_document(query, documents)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)


'''






'''