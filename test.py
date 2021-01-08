from query_functions import *
from example_flows import *

def test1():
  sources = ["US tops 5 million confirmed virus cases",
            "Canada's last fully intact ice shelf has suddenly collapsed, forming a Manhattan-sized iceberg",
            "Beijing mobilises invasion craft along coast as Taiwan tensions escalate",
            "The National Park Service warns against sacrificing slower friends in a bear attack",
            "Maine man wins $1M from $25 lottery ticket",
            "Make huge profits without work, earn up to $100,000 a day"]
  query = "feel good story"
  result = is_relevant(query, sources)
  print(result)
  
def test2():
  query = 'What do you have for oily skin?'
  product_descriptions = ['Neutrogena is good for oily skin and acne']
  product_names = ['Neutrogena']
  answer = find_most_relevant_products(query, product_names, product_descriptions)
  print(answer)

def test3():
  sources = ["US tops 5 million confirmed virus cases",
            "Canada's last fully intact ice shelf has suddenly collapsed, forming a Manhattan-sized iceberg",
            "Beijing mobilises invasion craft along coast as Taiwan tensions escalate",
            "The National Park Service warns against sacrificing slower friends in a bear attack",
            "Maine man wins $1M from $25 lottery ticket",
            "Make huge profits without work, earn up to $100,000 a day"]
  query = "feel good story"
  result = is_relevant(query, sources, use_api=True)
  print(result)

test3()