from .query_functions import *
import os

def find_most_relevant_products(query, product_names, product_descriptions, use_api=False):
  relevant_descriptions = is_most_relevant_document(query, product_descriptions, use_api=use_api)['result']
  to_search_through = zip(product_names, product_descriptions)
  result = [x[0] for x in to_search_through if x[1] in relevant_descriptions]
  if result == []:
    print('here1')
    return '[transfer to agent]', []
  elif len(result) == 1:
    print('here2')
    return '我們可以推薦' + result[0], result[0]
  elif len(result) > 1:
    print('here3')
    return '我們可以推薦' + result[0], result[0]

