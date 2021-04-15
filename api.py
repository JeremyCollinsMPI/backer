from flask import Flask, request, send_file
# from query_functions import *
from flask_cors import CORS
from pathlib import Path
from werkzeug.utils import secure_filename
import pandas as pd
from time import sleep
from copy import deepcopy

app = Flask(__name__)

CORS(app)

fake_database = {}

@app.route('/status', methods=['GET'])
def status():
  return {'statusCode': 200}

# @app.route('/is_relevant', methods=['POST'])
# def is_relevant_path():
#   content = request.get_json(force=True) 
#   query = content['query']
#   sources = content['sources']
#   return is_relevant(query, sources)
# 
# @app.route('/is_relevant_document', methods=['POST'])
# def is_relevant_document_path():
#   content = request.get_json(force=True) 
#   query = content['query']
#   documents = content['documents']
#   return is_relevant_document(query, documents)
# 
# @app.route('/is_most_relevant', methods=['POST'])
# def is_most_relevant_path():
#   content = request.get_json(force=True) 
#   query = content['query']
#   sources = content['sources']
#   return is_most_relevant(query, sources)
# 
# @app.route('/is_most_relevant_document', methods=['POST'])
# def is_most_relevant_document_path():
#   content = request.get_json(force=True) 
#   query = content['query']
#   documents = content['documents']
#   return is_most_relevant_document(query, documents)
# 
# @app.route('/classify', methods=['POST'])
# def classify_path():
#   content = request.get_json(force=True) 
#   query = content['query']
#   sources = content['sources']
#   return classify(query, sources)

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
  print('Steps *****')
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
  print('File *****')
  print(fake_database[id])
  return {'result': fake_database[id]}

def prepare_for_display(list_result):
  list_result = '\n'.join(list_result)
  return list_result

def get_sentences_from_csv(filename, column_name):
  df = pd.read_csv(filename)
  return df[column_name].tolist()

def semantic_search(input, query):
  for i in range(len(input)):
    input[i] = query + input[i]
  print('HERE ******')
  print(input)
  print(query)
  return input

def get_result(id):
  '''
  you then need to look up that id in the fake database
  
  '''
  current_result = ''
  print(id)
  print(fake_database)
  data = fake_database[id]
  data['outputs'] = []
  for step_number in data['stepNumbers']:
    step_number = int(step_number)
    use_previous_output = False
    if data['inputs'][step_number]['type'] == 'Output':
      use_previous_output = True
      output_to_use = data['inputs'][step_number]['index']
      print('^^^^^^ true ', output_to_use)
    if data['functions'][step_number] == 'Get sentences from CSV':
      sentences = get_sentences_from_csv(data['inputs'][step_number]['file'], data['additionalInputs'][step_number]['text'])
      current_result = sentences[0:10]
      data['outputs'].append(deepcopy(current_result))
    if data['functions'][step_number] == 'Semantic search':
      if use_previous_output:
        input = data['outputs'][output_to_use]
        query = data['additionalInputs'][step_number]['text']
        current_result = semantic_search(input, query)
        data['outputs'].append(deepcopy(current_result))
  return current_result
  

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
  print(fake_database)
  '''
  example:
{'123': {'stepNumbers': [0], 'currentStepNumber': 0, 'functions': ['Get sentences from CSV'], 'inputs': [{'type': 'undefined'}], 'additionalInputs': [{'type': 'text', 'text': 'hello'}], 'r': {'result': []}, 'id': 123}}  '''
#   if isinstance(result, list):
#     result = prepare_for_display(result)
  print('****')
  print(result)
  return {'result': result}
  
  
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)


