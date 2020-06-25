import pytest
from backend.request import *
from backend.user_input import *
from machine import *
from datetime import *


"""
    Er zijn een paar functies die niet getest worden. Hier zijn de redenen:
    
    voor:
    - get_question
    - getlocation
    - getcity
    - home
    - getanswer
    
    geld overal hetzelfde probleem en dat is dat dit flask functies zijn die gebruik maken van post methods of iets
    anders van flask en ik heb geen idee hoe je dit test
    
    voor:
    - findreplacement
    - give_inside_activity
    
    geld dat beide een random waarde meegeven. Om te testen of er echt een vaste waarde uit komt kan dus niet
    
    voor:
    - get_count
    
    geld dat deze functie kijkt naar de datum van vandaag en de dagen van de week. De waarde die je terug krijgt van 
    deze functie zal dus altijd anders zijn omdat de datum constant veranderd de functie heeft als parameter alleen de
    dag die het moet zoeken dus ik kan ook geen vaste datum meegeven.


"""


def test_get_current_weather():
    # simple function.. only test if code is 200 and the name is correct
    weather = get_current_weather('Rotterdam')
    assert weather['cod'] == 200
    assert weather['name'] == 'Rotterdam'


def test_get_forecast():
    # didn't give up a max length so we check the length as well
    weather = get_forecast('Rotterdam')
    assert weather['cod'] == '200'
    assert weather['cnt'] == 40
    assert weather['city']['name'] == 'Rotterdam'


def test_get_correct_forecast_day():
    # forecast api give forecast for up to 5 days so giving a date 6 days or more from now should return none
    weather = get_correct_forecast_day(['2020-06-24', '2020-06-30'], 'Rotterdam')
    assert weather['2020-06-24'] != 'none'
    assert weather['2020-06-30'] == 'none'


def test_get_average_temp():
    # calculates average and returns with 2 decimals instead of complete number
    average = get_average_temp([20, 35, 22, 28, 25])
    average_2_decimal = get_average_temp([12.345, 12.3, 13.24])
    assert average == 26
    assert average_2_decimal == 12.63
    assert average_2_decimal != 12.6283333333


def test_filter_currect_weather():
    # The check if the location has been found is here so we test that as well
    weather = filter_current_weather('Rotterdam')
    wrong_weather = filter_current_weather('hghgdcgshgdf')
    assert weather != 'not found'
    assert weather[3] == 'Rotterdam'
    assert wrong_weather == 'not found'


def test_remove_stopwords():
    # should only keep important words and the first word of the sentence
    sn = "Kan ik morgen gaan basketballen"
    sn_2 = "Ik wil naar het strand"
    rs = remove_stopwords(sn)
    rs_2 = remove_stopwords(sn_2)

    assert rs == ['Kan', 'morgen', 'gaan', 'basketballen']
    assert rs_2 == ['Ik', 'strand']


def test_check_date():
    # check if 'morgen' equals 1 day from now.. same goes with 3 days
    tomorrow = date.today() + timedelta(days=1)
    td = date.today() + timedelta(days=3)
    sn = "Kan ik morgen naar het strand"
    sn_2 = "Kan ik over een 3 dagen naar het strand"
    rs = remove_stopwords(sn)
    rs_2 = remove_stopwords(sn_2)
    # dt & dt_2 are sets so in order to compare to the item in the sets we need to loop through it
    dt = check_date(rs)
    dt_2 = check_date(rs_2)

    for x in dt:
        assert x == tomorrow.strftime("%Y-%m-%d")
    for y in dt_2:
        assert y == td.strftime("%Y-%m-%d")


def test_get_activities():
    # test if the try catch works
    outside = get_activities('outside')
    inside = get_activities('inside')
    wrong = get_activities('dbchegcghcgh')

    assert 'basketballen' in outside
    assert 'voetballen' in outside
    assert 'strand' in outside
    assert 'bordspellen' in inside
    assert 'binnensport' in inside
    assert wrong == 'Wrong value given to function'


def test_search_activities():
    # check if more than one activity can be found
    qt = ['Kan', 'gaan', 'basketballen']
    qt_2 = ['Strand', 'voetballen']
    activities = search_activities(qt)
    activities_2 = search_activities(qt_2)

    assert 'basketballen' in activities
    assert 'voetballen' not in activities
    assert 'strand' in activities_2
    assert 'voetballen' in activities_2
    assert 'basketballen' not in activities_2


def test_check_if_possible():
    # this basically checks the whole algorithm for giving advice
    sn = "Kan ik morgen gaan basketballen"
    sn_2 = "Kan ik over een maand gaan basketballen"
    sn_3 = "Kan ik gaan efvhgefhcvhev"
    qt = remove_stopwords(sn)
    qt_2 = remove_stopwords(sn_2)
    qt_3 = remove_stopwords(sn_3)
    dt = check_date(qt)
    dt_2 = check_date(qt_2)
    dt_3 = check_date(qt_3)
    fc = get_correct_forecast_day(dt, 'Rotterdam')
    fc_2 = get_correct_forecast_day(dt_2, 'Rotterdam')
    fc_3 = get_correct_forecast_day(dt_3, 'Rotterdam')
    advice = check_if_possible(qt, fc)
    advice_2 = check_if_possible(qt_2, fc_2)
    advice_3 = check_if_possible(qt_3, fc_3)

    assert advice[0] != "De datum/dag waarvoor u advies wou hebben is niet gevonden."
    assert advice[0] != "De gevraagde activiteit is niet gevonden, check op spellingsfouten. Als het goed is gespeld zit de activiteit niet in de database."
    assert advice_2[0] == "De datum/dag waarvoor u advies wou hebben is niet gevonden."
    assert advice_3[0] == "De gevraagde activiteit is niet gevonden, check op spellingsfouten. Als het goed is gespeld zit de activiteit niet in de database."
