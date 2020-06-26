from nltk import *
from datetime import *
from flask import *

"""
    This file gets the user input (or question) and filters the sentence given with nltk and dictionaries.
    The asked question gets saved in the session for later usage and the function redirects immediately to the function 
    that gives the answer. Which could be advice or an "OK".
    If no activity was given it returns The temperature of the asked day so that the user can decide for him/herself.
"""


question = Blueprint("question", __name__, static_folder="static", template_folder="templates")


@question.route("/get", methods=["POST", "GET"])
def get_question():
    if request.method == "POST":
        # get question from userinput
        question = request.form['question']
        # if only button has been pressed return to homepage
        if len(question) == 0:
            return redirect(url_for('home'))
        else:
            # can't just append to session so we make a var that saves current session
            all_questions = session['questions']
            # append the question to this question
            all_questions.append(question)
            # make the session equal to updated list
            session['questions'] = all_questions

            # immediatly get answer to save in session
            return redirect(url_for('get_answer', qt=question))


def remove_stopwords(sentence):
    # remove all unnecessary words in a sentence with nltk libary
    sent_array = word_tokenize(sentence)

    language = corpus.stopwords.words('dutch')
    new_sentence = []

    for x in sent_array:
        if x not in language:
            new_sentence.append(x)

    return new_sentence


def check_date(words):
    # check if there has been asked for a date to get correct forecast
    today = date.today()
    possible_dates = {'vandaag': 0, 'morgen': 1, 'overmorgen': 2, 'overovermorgen': 3,
                      'week': 7, 'maand': 30, 'jaar': 365,
                      'maandag': get_count('Mon'), 'dinsdag': get_count('Tue'), 'woensdag': get_count('Wed'),
                      'donderdag': get_count('Thu'), 'vrijdag': get_count('Fri'), 'zaterdag': get_count('Sat'),
                      'zondag': get_count('Sun')}

    # dict used for plural of words to use in the numeric check
    possible_numeric = {'dagen': 1, 'overmorgens': 2, 'overovermorgens': 3,'weken': 7, 'maanden': 30, 'jaren': 365}

    dates_asked = set()
    for word in words:
        d = word.lower()
        dt = ""
        # if it is in dict. add value to today to get correct date
        if d in possible_dates:
            dt = today + timedelta(days=possible_dates[d])
            dates_asked.add(dt.strftime('%Y-%m-%d'))
        # if it isn't a word but a number instead give forecast for number
        elif d.isnumeric():
            index = words.index(d)
            next = words[index + 1]
            if next.lower() in possible_numeric:
                # check if the next word is in possible numeric and multiply it by the value in possible dates
                # if next == overmorgen and d = 3 sum = 2 * 3 = 6
                dt = today + timedelta(days=int(d) * possible_numeric[next])
                dates_asked.add(dt.strftime('%Y-%m-%d'))

    # if not found give date for today
    if len(dates_asked) == 0:
        dates_asked.add(today.strftime('%Y-%m-%d'))

    return dates_asked


def get_count(day):
    # check what day it is today
    today = date.today()
    date_name = today.strftime('%a')
    c = 0
    # keep adding 1 to c while new_date isn't equal to asked
    while day != date_name:
        c += 1
        new_date = today + timedelta(days=c)
        date_name = new_date.strftime('%a')

    return c

