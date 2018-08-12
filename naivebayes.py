import nltk
import csv
from nltk.tokenize import word_tokenize

# Reading the training data
train = []
with open('training.csv', 'r') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    comment = row['comment']
    output = row['value']
    train += [(comment, output)]
# Tokenizing and reading all the words
all_words = set(word.lower() for passage in train for word in word_tokenize(passage[0]))
# Create the training set naive bayes
t = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in train]
# Train the classifier
classifier = nltk.NaiveBayesClassifier.train(t)
# Creating a test case
outputs = []
outputs+=[["Sentence,Result,Positive,Negative"]]
with open('test.csv', 'r') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    test_sentence = row['test']
    test_sent_features = {word.lower(): (word in word_tokenize(test_sentence.lower())) for word in all_words}
    print(test_sentence + "," + classifier.classify(test_sent_features))
    positive="{0:.2f}".format(classifier.prob_classify(test_sent_features).prob('pos')*100)
    negative="{0:.2f}".format(classifier.prob_classify(test_sent_features).prob('neg')*100)
    outputs += [[test_sentence + "," + classifier.classify(test_sent_features)+","+positive+","+negative]]
file = open("output.csv", "w+")
for line in outputs:
  file.write(line[0] + "\n")
file.close()
