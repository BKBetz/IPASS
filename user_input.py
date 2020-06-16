from nltk import *


def get_question():
    question = input("Stel je vraag ")

    while len(question) == 0:
        question = input("Je hebt geen vraag ingevuld...probeer opnieuw")

    return question


def remove_stopwords():
    sentence = get_question()
    sent_array = word_tokenize(sentence)

    language = corpus.stopwords.words('dutch')
    new_sentence = []

    for x in sent_array:
        if x not in language:
            new_sentence.append(x)

    return new_sentence
