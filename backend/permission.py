import geocoder
from flask import *

location = Blueprint("location", __name__, static_folder="static", template_folder="templates")


@location.route('/', methods=["POST", "GET"])
@location.route('/permission', methods=["POST", "GET"])
def getlocation():
    if request.method == "POST":
        permission = request.form["option"]
        if permission == 'ja':
            location = geocoder.ip('me')
            loc = location.city
            return redirect(url_for("home", location=loc))
        else:
            return redirect(url_for("location.getcity"))
    else:
        return render_template('location.html')


@location.route('/city', methods=["POST", "GET"])
def getcity():
    if request.method == "POST":
        loc = request.form["city"]
        if len(loc) == 0:
            return render_template('city.html', extra="Geen locatie ingevuld")
        else:
            return redirect(url_for("home", location=loc))
    else:
        return render_template('city.html')


