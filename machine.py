from flask import *
import json
from datetime import *
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
    answers = []
    for y in forecast:
        if forecast[y] == "none":
            answers.append("De datum/dag waarvoor u advies wou hebben is niet gevonden.")
        else:
            if len(info) > 0:
                for x in info:
                    if forecast[y] >= info[x][0] and forecast[y] <= info[x][1]:
                        answers.append(pretty_answer(y, forecast[y], x, True))
                    else:
                        answers.append(pretty_answer(y, forecast[y], x, False))
            else:
                answers.append("De gevraagde activiteit is niet gevonden, check op spellingsfouten. Als het goed is gespeld zit de activiteit niet in de database.")

    return answers


def pretty_answer(date, temp, activity, possible):
    date_step = datetime.strptime(date, "%Y-%m-%d")
    clean_date = date_step.strftime("%d-%m-%Y")
    if possible:
        str = "Je kunt {} de volgende activiteit uitvoeren: {}."
        return str.format(clean_date, activity)
    else:
        replacement = find_replacement(temp)
        str = "Op {} is het gemiddeld {} graden en is het geen goede dag om de volgende activiteit uit te voeren: {}. Een leuke activiteit zou {} zijn."
        return str.format(clean_date, temp, activity, replacement)


def find_replacement(temp):
    outside_activities = get_activities('outside')
    replacements =[]
    for x in outside_activities:
        if temp >= outside_activities[x]['min_temp'] and temp <= outside_activities[x]['max_temp']:
            replacements.append(x)

    if len(replacements) == 0:
        return give_inside_activity()

    else:
        return random.choice(replacements)


def give_inside_activity():
    inside_activities = get_activities('inside')
    return random.choice(inside_activities)
