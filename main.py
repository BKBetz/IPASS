from backend.permission import *
from backend.request import *
from backend.user_input import *
from flask import *
from machine import check_if_possible

app = Flask(__name__)
app.register_blueprint(location)
app.register_blueprint(question)
app.secret_key = "secret"


@app.route("/home", methods=["POST", "GET"])
def home():
    if 'location' not in session:
        return redirect(url_for('location.getlocation'))
    else:
        if 'questions' not in session:
            session['questions'] = []

        if 'answers' not in session:
            session['answers'] = []

        print(session['questions'])
        print(session['answers'])
        print(session['location'])
        cw = filter_current_weather(session['location'])
        print(cw)
        if cw == "not found":
            flash('De gegeven locatie is niet gevonden')
            return redirect(url_for('location.getcity'))
        else:
            return render_template("index.html", weather=cw, len=len(session['questions']) , questions=session['questions'], answers=session['answers'])


@app.route("/answer<qt>")
def get_answer(qt):
    if 'location' in session:
        if 'questions' in session:
            fq = remove_stopwords(qt)
            date = check_date(fq)
            forecast = get_correct_forecast_day(date, session['location'])
            advice = check_if_possible(fq, forecast)
            add_to_session(advice)

            return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('location.getlocation'))


def add_to_session(advice):
    all_answers = session['answers']
    all_answers.append(advice)
    session['answers'] = all_answers


if __name__ == '__main__':
    app.run()
