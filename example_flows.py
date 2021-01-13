from .query_functions import *
import os

def find_most_relevant_products(query, product_names, product_descriptions):
  relevant_descriptions = is_most_relevant_document(query, product_descriptions)['result']
  to_search_through = zip(product_names, product_descriptions)
  result = [x[0] for x in to_search_through if x[1] in relevant_descriptions]
  if result == []:
    return '[transfer to agent]'
  elif len(result) == 1:
    return '我們可以推薦' + result[0]
  elif len(result) > 1:
    return "我們可以推薦一下的產品: \n" + "\n".join(result)

def load_product_descriptions():
  dir_name = 'product_descriptions'
  dir = os.listdir(dir_name)
  result = []
  for i in range(0,10000):
    if str(i) + '.txt' in dir:
      with open(dir_name + '/' + str(i) + '.txt', 'r') as file:
        result.append(file.read())
  return result