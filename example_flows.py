from query_functions import *

def find_most_relevant_products(query, product_names, product_descriptions):
  relevant_descriptions = is_relevant(query, product_descriptions)['result']
  to_search_through = zip(product_names, product_descriptions)
  result = [x[0] for x in to_search_through if x[1] in product_descriptions]
  if result == []:
    return "Sorry, we don't have any products matching that query."
  return "We can recommend the following products: \n" + "\n".join(result)
   