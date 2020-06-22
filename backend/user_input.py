from nltk import *
from datetime import *
from flask import *

question = Blueprint("question", __name__, static_folder="static", template_folder="templates")


@question.route("/get", methods=["POST", "GET"])
def get_question():
    if request.method == "POST":
        question = request.form['question']
        all_questions = session['question']
        all_questions.append(question)
        session['question'] = all_questions

    return redirect(url_for('home'))


def remove_stopwords():
    sentence = get_question()
    sent_array = word_tokenize(sentence)

    language = corpus.stopwords.words('dutch')
    new_sentence = []

    for x in sent_array:
        if x not in language:
            new_sentence.append(x)

    return new_sentence


def check_date(words):
    today = date.today()
    possible_dates = {'vandaag': 0, 'morgen': 1, 'overmorgen': 2, 'overovermorgen': 3, 'week': 7, 'maand': 31, 'jaar': 365,
                      'maandag': get_count('Mon'), 'dinsdag': get_count('Tue'), 'woensdag': get_count('Wed'),
                      'donderdag': get_count('Thu'), 'vrijdag': get_count('Fri'), 'zaterdag': get_count('Sat'),
                      'zondag': get_count('Sun')}

    dates_asked = set()
    for word in words:
        d = word.lower()
        dt = ""
        if d in possible_dates:
            dt = today + timedelta(days=possible_dates[d])
            dates_asked.add(dt.strftime('%Y-%m-%d'))
        elif d.isnumeric():
            dt = today + timedelta(days=int(d))
            dates_asked.add(dt.strftime('%Y-%m-%d'))

    if len(dates_asked) == 0:
        dates_asked.add(today.strftime('%Y-%m-%d'))

    return dates_asked


def get_count(day):
    today = date.today()
    date_name = today.strftime('%a')
    c = 0
    while day != date_name:
        c += 1
        new_date = today + timedelta(days=c)
        date_name = new_date.strftime('%a')

    return c

