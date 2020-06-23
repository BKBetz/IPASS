from flask import *
import json
import random


def get_activities(option):
    try:
        with open('backend/activities.json') as json_file:
            data = json.load(json_file)
            activities = data['activities'][option]

        return activities

    except KeyError:
        print("Wrong value given to function")


def search_activities(question):
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


def check_if_possible(question, forecast):
    info = search_activities(question)
    for y in forecast:
        if len(info) > 0:
            for x in info:
                if forecast[y] >= info[x][0] and forecast[y] <= info[x][1]:
                    return "possible"
                else:
                    return give_inside_activity(y, x)
        else:
            return "No activity was found"


def give_inside_activity(date, activity):
    inside_activities = get_activities('inside')
    random.choice(inside_activities)
    str = "op {} is het geen goede dag om de volgende activiteit uit te voeren: {} een leuke activiteit zou {} zijn"

    return 'Not possible'
