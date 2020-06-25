from program.backend.permission import *
from program.backend.request import *
from program.backend.user_input import *
from flask import *
from program.machine import check_if_possible

app = Flask(__name__)
app.register_blueprint(location)
app.register_blueprint(question)
app.secret_key = "secret"


@app.route("/home", methods=["POST", "GET"])
def home():
    # location has to exist in order to go to this page
    if 'location' not in session:
        return redirect(url_for('location.getlocation'))
    else:
        # create following sessions if they don't exist yet
        if 'questions' not in session:
            session['questions'] = []

        if 'answers' not in session:
            session['answers'] = []

        print(session['questions'])
        print(session['answers'])
        print(session['location'])
        # get current weather
        cw = filter_current_weather(session['location'])
        print(cw)
        if cw == "not found":
            # location hasn't been found.. return to city page
            flash('De gegeven locatie is niet gevonden')
            return redirect(url_for('location.getcity'))
        else:
            return render_template("index.html", weather=cw, len=len(session['questions']) , questions=session['questions'], answers=session['answers'])


@app.route("/answer<qt>")
def get_answer(qt):
    # this is basically the function that makes combines all the functions into one big algorithm
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
    # add to session
    all_answers = session['answers']
    all_answers.append(advice)
    session['answers'] = all_answers


if __name__ == '__main__':
    app.run()
