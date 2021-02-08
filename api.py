from flask import Flask, request, send_file
from query_functions import *
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

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

@app.route('/classify', methods=['POST'])
def classify_path():
  content = request.get_json(force=True) 
  query = content['query']
  sources = content['sources']
  return classify(query, sources)

@app.route('/text_file_to_sentences', methods=['POST'])
def text_file_to_sentences_path():
  file = request.files['file']
  file.save('data/moose.txt')
#   return {'result': open('data/moose.txt', 'r').read().split('.')}
  return 'hello'
  
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)


'''






'''