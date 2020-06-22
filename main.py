from backend.permission import *
from backend.request import *
from backend.user_input import *
from flask import *

app = Flask(__name__)
app.register_blueprint(location)
app.register_blueprint(question)
app.secret_key = "secret"


@app.route("/home", methods=["POST", "GET"])
def home():
    if 'location' not in session:
        return redirect(url_for('location.getlocation'))
    else:
        if 'question' not in session:
            session['question'] = []
        cw = filter_current_weather(session['location'])
        if cw == "not found":
            return render_template("index.html", errormessage="De ingevoerde plek is niet gevonden, probeer opnieuw", weather=[0, 0, 0, 0])
        else:
            return render_template("index.html", weather=cw, content=session['question'])


if __name__ == '__main__':
    app.run()
