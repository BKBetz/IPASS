from user_input import remove_stopwords
from request import *
import json
import random

question = remove_stopwords()
weather = get_current_weather()
forecast = get_forecast()


def get_activities(option):
    try:
        with open('activities.json') as json_file:
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
    if len(info) > 0:
        for x in info:
            if weather[1] >= info[x][0] and weather[1] <= info[x][1]:
                print("possible")
            else:
                give_inside_activity()
    else:
        print("No activity was found")


def give_inside_activity():
    inside_activities = get_activities('inside')
    print(random.choice(inside_activities))



check_if_possible()