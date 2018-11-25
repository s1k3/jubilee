import nltk
import csv
from nltk.tokenize import word_tokenize
import process_comment

process_comment.make_data()
classes = process_comment.get_classes()
# Reading the training data
train = []
with open('training.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        comment = row['data']
        output = row['class']
        train += [(comment, output)]
# Tokenizing and reading all the words
all_words = set(word.lower() for passage in train for word in word_tokenize(passage[0]))
# Create the training set naive bayes
t = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in train]
# Train the classifier
classifier = nltk.NaiveBayesClassifier.train(t)
# Creating a test case
outputs = [["Sentence,output," + ','.join(classes)+","+"age"]]
with open('test.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        test_sentence = row['test']
        test_age = row['age']
        test_sent_features = {word.lower(): (word in word_tokenize(test_sentence.lower())) for word in all_words}
        print(test_sentence + "," + classifier.classify(test_sent_features))
        percentage = {}
        for c in classes:
            percentage[c] = "{0:.2f}".format(classifier.prob_classify(test_sent_features).prob(c) * 100)
        outputs += [
            [test_sentence + "," + classifier.classify(test_sent_features) + "," + ','.join(
                list(percentage.values())) + "," + test_age]]
file = open("output.csv", "w+")
for line in outputs:
    file.write(line[0] + "\n")
file.close()
