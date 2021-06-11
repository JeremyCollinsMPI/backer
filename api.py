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
import random
import string

app = Flask(__name__)

CORS(app)

fake_database = {}

@app.route('/wake_up_gcp', methods=['GET'])
def wake_up_gcp_path():
  url = gcp_ip + '/status'
  r = requests.get(url)
  return {'result': r.json()}

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

def generate_api_id(context):
  return {'result': context['ip'] + ':8080/api/' + context['id'] + '_' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))}


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

def get_input(context):
  data = context['data']
  step_number = context['step_number']
  if data['inputs'][step_number]['type'] == 'Output':
    output_to_use = data['inputs'][step_number]['index']
    input = data['outputs'][output_to_use]
  elif data['inputs'][step_number]['type'] == 'Api input':
    input = data['api_inputs'][str(step_number)]
  elif data['inputs'][step_number]['type'] == 'file or directory':
    input = data['inputs'][step_number]['file']
  else:
    input = None
  return {'result': input}

def get_result(context):
  if not 'mode' in context.keys():
    context['mode'] = 'normal'
  id = context['id']
  current_result = ''
  data = fake_database[id]
  print(data)
  data['outputs'] = []
  if 'Make api link' in data['functions']:
    if not context['mode'] == 'within api':
      context['ip'] = "http://103.102.44.216"
      context['id'] = id
      api_id = generate_api_id(context)['result']  
      data['api_id'] = api_id
      current_result = [api_id]
      return {'result': current_result}
  for step_number in data['stepNumbers']:
    step_number = int(step_number)
    get_input_result = get_input(context | {'data': data, 'step_number': step_number})
    input = get_input_result['result']
    if data['functions'][step_number] == 'Get sentences from CSV':
      sentences = get_sentences_from_csv(input, data['additionalInputs'][step_number]['text'])
      current_result = sentences
      data['outputs'].append(deepcopy(current_result))
    if data['functions'][step_number] == 'Semantic search':
      query = data['additionalInputs'][step_number]['text']
      current_result = semantic_search(input, query)
      data['outputs'].append(deepcopy(current_result))
    if data['functions'][step_number] == 'Entails':
      query = data['additionalInputs'][step_number]['text']
      current_result = entails(input, query)
      data['outputs'].append(deepcopy(current_result)) 
    if data['functions'][step_number] == 'Ask question':
      print('matey')
      query = data['additionalInputs'][step_number]['text']
      current_result = ask_question(input, query)
      data['outputs'].append(deepcopy(current_result))  
    if data['functions'][step_number] == 'Get sentences from url':
      sentences = get_sentences_from_url(data['additionalInputs'][step_number]['text']) 
      current_result = sentences
      data['outputs'].append(deepcopy(current_result)) 
  return {'result': current_result}

def submit_files_for_running_with_api(context):
  if context['files'] == None:
    return {'result': 'no files'}
  id = context['id']
  if not 'api_inputs' in fake_database[id]:
    fake_database[id]['api_inputs'] = {}
  for item in context['files'].items():
    step = item[0]
    file = item[1]
    filename = secure_filename(file.filename)
    extension = filename.split('.')[1]
    Path("data/" + str(id) + '/' + str(step)).mkdir(parents=True, exist_ok=True)
    file_path = "data/" + str(id) + '/' + str(step) + '/' + 'file' + '.' + extension
    file.save(file_path)
    fake_database[id]['api_inputs'][step] = file_path 
  return {'result': 'success'}

@app.route('/api_accept_files/<string:api_id>', methods=['POST'])
def api_accept_files_path(api_id):
  files = request.files
  id = api_id.split('_')[0]
  submit_files_for_running_with_api_result = submit_files_for_running_with_api({'id': id, 'files': files})
  return submit_files_for_running_with_api_result 
  
@app.route('/api/<string:api_id>', methods=['POST'])
def api_path(api_id):
  content = request.json
  id = api_id.split('_')[0]
  data = fake_database[id]
  if not 'api_inputs' in fake_database[id]:
    fake_database[id]['api_inputs'] = {}
  for key in content['api_inputs']:
    data['api_inputs'][key] = content['api_inputs'][key]
  get_result_context = {'id': id, 'mode': 'within api', 'content': content}
  return {'result': get_result(get_result_context)['result']}

@app.route('/run', methods=['GET'])
def run_path():
  id = request.args.get('id')
  get_result_context = {'id': id}
  result = get_result(get_result_context)
  return {'result': result['result']}
  
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)


