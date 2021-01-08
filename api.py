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

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)


'''






'''