import nltk
sentence="Lg is a crazy bitch"
tokens = nltk.word_tokenize(sentence)
tags = nltk.pos_tag(tokens)
print("Tokens",tokens)
print ("Tags",tags)
