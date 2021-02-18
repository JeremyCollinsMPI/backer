from flask import Flask, request, send_file
from query_functions import *
from flask_cors import CORS

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
  dictionary['inputs'][step-1]['file'] = file
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
  id = requests.args.get('id')
  step = requests.args.get('step')
  '''
  the idea is that you also want an id.
  you also need to know which step you are talking about.
  so you can set these as parameters in the url.
  
  you need to load the dictionary for that id
  and set the input
  '''
  dictionary = load_data(id)
  dictionary = set_step_input(dictionary, step, file)
  store_data(id, dictionary)
  print(fake_database[id])
  return {'result': 'success'}

@app.route('/run', methods=['GET'])
def run_path():
  '''
  you need an id here
  
  you need to work out where the data is saved
  
  
  will make a fake database at the moment
  
  
  
  
  '''
  return {'result': ['hello']}
  
  
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)


'''
remaining tasks

the idea is that you choose the options in the interface
you click the button.
it submits the whole state.
it submits the files.
it then submits a get request for the pipeline to run.

check that the first step is finished first - done
now need to check that submitting files is working






'''