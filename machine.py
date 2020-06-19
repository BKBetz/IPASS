from backend.user_input import *
from backend.request import *
from backend.permission import *
from flask import *
import json
import random

location = getlocation()
question = remove_stopwords()
date = check_date(question)
weather = filter_current_weather(location)
forecast = get_correct_forecast_day(date, location)


def get_activities(option):
    try:
        with open('backend/activities.json') as json_file:
            data = json.load(json_file)
            activities = data['activities'][option]

        return activities

    except KeyError:
        print("Wrong value given to function")


def search_activities():
    outside_activities = get_activities('outside')
    activities_asked = {}

    for word in question:
        for activity in outside_activities:
            activity_temp = []
            if word == activity:
                for temp in outside_activities[activity]:
                    activity_temp.append(outside_activities[activity][temp])
                activities_asked[activity] = activity_temp

    return activities_asked


def check_if_possible():
    info = search_activities()
    for y in forecast:
        if len(info) > 0:
            for x in info:
                if forecast[y] >= info[x][0] and forecast[y] <= info[x][1]:
                    print("possible", y)
                else:
                    give_inside_activity(y, x)
        else:
            print("No activity was found")


def give_inside_activity(date, activity):
    inside_activities = get_activities('inside')
    str = "op {} is het geen goede dag om de volgende activiteit uit te voeren: {} een leuke activiteit zou {} zijn"
    print(str.format(date, activity, random.choice(inside_activities)))
