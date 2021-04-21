from transformers import pipeline
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")



if __name__ == '__main__':      
  sequence_to_classify = "one day I will see the world"
  candidate_labels = ['travel', 'cooking', 'dancing']
  result = classifier(sequence_to_classify, candidate_labels)
  print(result)
#{'labels': ['travel', 'dancing', 'cooking'],
# 'scores': [0.9938651323318481, 0.0032737774308770895, 0.002861034357920289],
# 'sequence': 'one day I will see the world'}



# multiple classes
# candidate_labels = ['travel', 'cooking', 'dancing', 'exploration']
# classifier(sequence_to_classify, candidate_labels, multi_class=True)

#{'labels': ['travel', 'exploration', 'dancing', 'cooking'],
# 'scores': [0.9945111274719238,
#  0.9383890628814697,
#  0.0057061901316046715,
#  0.0018193122232332826],
# 'sequence': 'one day I will see the world'}

