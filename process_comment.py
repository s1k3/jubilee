import nltk
from autocorrect import spell
from nltk.stem import WordNetLemmatizer


def make_data():
    nounTags = ['NN', 'NNP', 'NNS', 'NNPS']
    verbTags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    adjectiveTags = ['JJ', 'JJR', 'JJS']
    adverbTags = ['RB', 'RBS', 'RBR']
    filters = [["Sentence,Noun,Verb,Adverb,Adjective"]]
    stop_words = []
    trainings = [["Sentence,data,class"]]
    classes = []
    file = open("stop_words.txt", "r+")
    for line in file:
        stop_words += [line.lower().rstrip().lstrip()]
    file.close()

    lemmatizer = WordNetLemmatizer()
    file = open("comment.csv", "r")
    for line in file:
        data = line.split(",")
        if data[1].lower().rstrip().lstrip() not in classes:
            classes += [data[1].lower().rstrip().lstrip()]
        sentence = data[0].lower().rstrip().lstrip()
        nouns = []
        verbs = []
        adverbs = []
        adjectives = []
        tokens = nltk.word_tokenize(sentence)
        tags = nltk.pos_tag(tokens)

        for tag in tags:
            word = spell(tag[0].lower().rstrip().lstrip())
            lemmatizedWord = lemmatizer.lemmatize(word)
            if word not in stop_words:
                if tag[1] in nounTags:
                    nouns += [lemmatizedWord]
                elif tag[1] in verbTags:
                    verbs += [lemmatizer.lemmatize(word, "v")]
                elif tag[1] in adverbTags:
                    adverbs += [lemmatizedWord]
                elif tag[1] in adjectiveTags:
                    adjectives += [lemmatizedWord]
        nounText = ' '.join(nouns)
        verbText = ' '.join(verbs)
        adverbText = ' '.join(adverbs)
        adjectiveText = ' '.join(adjectives)
        filters += [[sentence + "," + nounText + "," + verbText + "," + adverbText + "," + adjectiveText]]
        trainings += [[sentence + "," + nounText + " " + verbText + " " + adverbText + " " + adjectiveText + "," + data[
            1].lower().rstrip().lstrip()]]
    file.close()

    file = open("filter.csv", "w+")
    for line in filters:
        file.write(line[0] + "\n")
    file.close()

    file = open("training.csv", "w+")
    for line in trainings:
        file.write(line[0] + "\n")
    file.close()

    file = open("classes.txt", "w+")
    file.write(','.join(classes))
    file.close()


def get_classes():
    file = open("classes.txt", "r+")
    line = file.readline()
    file.close()
    return line.split(",")
