from backend.permission import *
from backend.request import *
from flask import *

app = Flask(__name__)
app.register_blueprint(location)


@app.route("/<location>")
def home(location):
    if location is None:
        return redirect(url_for(getlocation))
    else:
        cw = filter_current_weather(location)
        return render_template("index.html", content=cw)


if __name__ == '__main__':
    app.run()
