from flask import Flask, request, send_file
from flask_cors import CORS
from pathlib import Path
from werkzeug.utils import secure_filename
import pandas as pd
from time import sleep
from copy import deepcopy
from conf import *
import requests
from extract_text_from_html import *

app = Flask(__name__)

CORS(app)

fake_database = {}

@app.route('/status', methods=['GET'])
def status():
  return {'statusCode': 200}

@app.route('/text_file_to_sentences', methods=['POST'])
def text_file_to_sentences_path():
  file = request.files['file']
  file.save('data/moose.txt')
  return {'result': open('data/moose.txt', 'r').read().split('.')}
  
@app.route('/search_for', methods=['POST'])
def search_for_path():
  content = request.get_json(force=True) 
  sentences = content['sentences']
  string = content['string']
  return {'result': search_for(sentences, string)}

def set_step_input(dictionary, step, file):
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
  return {'result': fake_database[id]}

def prepare_for_display(list_result):
  list_result = '\n'.join(list_result)
  return list_result

def get_sentences_from_csv(filename, column_name):
  df = pd.read_csv(filename)
  return df[column_name].tolist()[0:100]

def semantic_search(input, query):
  content = {'sentences': input, 'query': query}
  url = gcp_ip + '/run'
  result = requests.post(url, json=content)
  return result.json()['result']

def entails(input, query):
  content = {'sentences': input, 'hypothesis': query}
  url = gcp_ip + '/inference'
  result = requests.post(url, json=content)
  return result.json()['result']

def ask_question(input, query):
  result = []
  for item in input:
    content = {'text': item, 'question': query}
    url = gcp_ip + '/question_answering'
    result.append(requests.post(url, json=content).json()['result'])
  return result

def get_sentences_from_url(url):
  text = extract_text_from_html(requests.get(url).content)
  text = text.replace('\n', ' ')
  texts = text.split('                                                       ')
  return texts

@app.route('/accept_urls', methods=['POST'])
def accept_urls_path():
  content = request.get_json(force=True)
  result = []
  for url in content['urls']:
    text = extract_text_from_html(requests.get(url).content)
    text = text.replace('\n', ' ')
    texts = text.split('                                                       ')
    for item in texts:
      result.append([url, item])
  return {'result': result}

def get_result(id):
  current_result = ''
  data = fake_database[id]
  print(data)
  data['outputs'] = []
  for step_number in data['stepNumbers']:
    step_number = int(step_number)
    use_previous_output = False
    if data['inputs'][step_number]['type'] == 'Output':
      use_previous_output = True
      output_to_use = data['inputs'][step_number]['index']
    if data['functions'][step_number] == 'Get sentences from CSV':
      sentences = get_sentences_from_csv(data['inputs'][step_number]['file'], data['additionalInputs'][step_number]['text'])
      current_result = sentences
      data['outputs'].append(deepcopy(current_result))
    if data['functions'][step_number] == 'Semantic search':
      if use_previous_output:
        input = data['outputs'][output_to_use]
        query = data['additionalInputs'][step_number]['text']
        current_result = semantic_search(input, query)
        data['outputs'].append(deepcopy(current_result))
    if data['functions'][step_number] == 'Entails':
      if use_previous_output:
        input = data['outputs'][output_to_use]
        query = data['additionalInputs'][step_number]['text']
        current_result = entails(input, query)
        data['outputs'].append(deepcopy(current_result)) 
    if data['functions'][step_number] == 'Ask question':
      print('matey')
      if use_previous_output:
        input = data['outputs'][output_to_use]
        query = data['additionalInputs'][step_number]['text']
        current_result = ask_question(input, query)
        data['outputs'].append(deepcopy(current_result))  
    if data['functions'][step_number] == 'Get sentences from url':
      sentences = get_sentences_from_url(data['additionalInputs'][step_number]['text']) 
      current_result = sentences
      data['outputs'].append(deepcopy(current_result))   
  return current_result
  

@app.route('/run', methods=['GET'])
def run_path():
  id = request.args.get('id')
  result = get_result(id)
  return {'result': result}
  
  
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)


