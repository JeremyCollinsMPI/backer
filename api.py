from flask import Flask, request, send_file
from query_functions import *
from flask_cors import CORS
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)

CORS(app)

fake_database = {}

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
  return {'result': open('data/moose.txt', 'r').read().split('.')}
#   return 'hello'
  
@app.route('/search_for', methods=['POST'])
def search_for_path():
  content = request.get_json(force=True) 
  sentences = content['sentences']
  string = content['string']
  return {'result': search_for(sentences, string)}

def set_step_input(dictionary, step, file):
  '''
  structure is {'inputs': [{'type': 'file or directory', 'file': x}]}
  
  '''
  print(dictionary)
  step = int(step)
  dictionary['inputs'][step]['file'] = file
  return dictionary

def store_data(id, data):
  fake_database[id] = data

def load_data(id):
  return fake_database[id] 

@app.route('/accept_steps', methods=['POST'])
def accept_steps_path():
  content = request.get_json(force=True)
  id = request.args.get('id')
  store_data(id, content['state'])
  print(fake_database)
  return {'result': 'success'}

@app.route('/accept_file', methods=['POST'])
def accept_file_path():
  file = request.files['file']
  filename = secure_filename(file.filename)
  extension = filename.split('.')[1]
  id = request.args.get('id')
  step = request.args.get('step')
  Path("data/" + str(id) + '/' + str(step)).mkdir(parents=True, exist_ok=True)
  file.save("data/" + str(id) + '/' + str(step) + '/' + 'file' + '.' + extension)
  dictionary = load_data(id)
  dictionary = set_step_input(dictionary, step, "data/" + str(id) + '/' + str(step) + '/' + 'file' + '.' + extension)
  store_data(id, dictionary)
  print(fake_database[id])
  return {'result': 'success'}

def prepare_for_display(list_result):
  list_result = '\n'.join(list_result)
  return list_result

def get_result(id):
  '''
  you then need to look up that id in the fake database
  
  '''
  
  
  return ['hello', 'mate', 'goodbye']
  

@app.route('/run', methods=['GET'])
def run_path():
  '''
  you need an id here
  
  you need to work out where the data is saved
  
  
  will make a fake database at the moment
  
  this database has ids as attributes.
  the value is a dict.  functions is a list.  inputs is a list.  additionalinputs.  
  
  
  '''
  id = request.args.get('id')
  result = get_result(id)
#   if isinstance(result, list):
#     result = prepare_for_display(result)
  return {'result': result}
  
  
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)


