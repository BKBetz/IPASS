import geocoder
from flask import *

location = Blueprint("location", __name__, static_folder="static", template_folder="templates")


@location.route('/', methods=["POST", "GET"])
@location.route('/permission', methods=["POST", "GET"])
def getlocation():
    # first page.. if there are sessions while on this page..reset them
    if 'answers' in session:
        flash('Locatie en vragen gereset')
        session.pop('answers')
    if 'questions' in session:
        session.pop('questions')
    if 'location' in session:
        session.pop('location')

    # check if method is post
    if request.method == "POST":
        permission = request.form.get("option")
        if permission == 'ja':
            # this is used to get your current location
            loc = geocoder.ip('me')
            session['location'] = loc.city
            return redirect(url_for("home"))
        elif permission == 'nee':
            return redirect(url_for("location.getcity"))
        # only button has been pressed
        else:
            flash('Geen antwoord gegeven')
            return redirect(url_for('location.getlocation'))
    else:
        return render_template('location.html')


@location.route('/city', methods=["POST", "GET"])
def getcity():
    # if someone goes here by changing url...also reset
    if 'answers' in session:
        flash('Locatie en vragen gereset')
        session.pop('answers')
    if 'questions' in session:
        session.pop('questions')
    if 'location' in session:
        session.pop('location')
    # enter city name for weather api
    if request.method == "POST":
        loc = request.form["city"]
        if len(loc) == 0:
            flash("Geen locatie ingevuld")
            return render_template('city.html')
        else:
            session['location'] = loc
            return redirect(url_for("home"))
    else:
        return render_template('city.html')


