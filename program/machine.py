from flask import *
import json
from datetime import *
import random

"""
    This file reads the json files and checks the forecast and user input to return an answer. This could be advice if the
    activity isn't a good move or it can give a "OK" if the activity is approved.
"""


def get_activities(option):
    # get activities from the json file based on the option.. except keyerror if option not found
    try:
        with open('backend/activities.json') as json_file:
            data = json.load(json_file)
            activities = data['activities'][option]

        return activities

    except KeyError:
        return "Wrong value given to function"


def search_activities(question):
    # checks if activity is in json file
    outside_activities = get_activities('outside')
    activities_asked = {}

    for word in question:
        for activity in outside_activities:
            activity_temp = []
            # all words in json file are with lowercases so all words in the sentence are converted to lowercases
            if word.lower() == activity:
                for temp in outside_activities[activity]:
                    activity_temp.append(outside_activities[activity][temp])
                activities_asked[activity] = activity_temp

    return activities_asked


def check_if_possible(question, forecast):
    info = search_activities(question)
    answers = []
    for y in forecast:
        # if the date wasn't found
        if forecast[y] == "none":
            answers.append("De datum/dag waarvoor u advies wou hebben is niet gevonden.")
        else:
            if len(info) > 0:
                for x in info:
                    if forecast[y] >= info[x][0] and forecast[y] <= info[x][1]:
                        answers.append(pretty_answer(y, forecast[y], info, True))
                    else:
                        answers.append(pretty_answer(y, forecast[y], info, False))
            # if activity wasn't found
            else:
                # change this if extra time
                text = "We hebben u activiteit niet kunnen vinden. De gemiddelde temperatuur is {} graden. Probeer hiermee uw keuze te maken"
                answers.append(text.format(forecast[y]))

    return answers


def pretty_answer(date, temp, activity, possible):
    # just a function to return pretty sentences
    date_step = datetime.strptime(date, "%Y-%m-%d")
    clean_date = date_step.strftime("%d-%m-%Y")
    if possible:
        str = "Je kunt {} de volgende activiteit uitvoeren: {}."
        return str.format(clean_date, list(activity.keys())[0])
    else:
        replacement = find_replacement(activity, temp)
        str = "Op {} is het gemiddeld {} graden en is het geen goede dag om de volgende activiteit uit te voeren: {}. Een leuke activiteit zou {} zijn."
        return str.format(clean_date, temp, list(activity.keys())[0], replacement)


def find_replacement(activity, temp):
    # check the current temp
    outside_activities = get_activities('outside')
    key = list(activity.keys())[0]
    possible_replacements = []
    better_replacements = []
    for x in outside_activities:
        # find all activities that are okay to do with these weather circumstances
        if temp >= outside_activities[x]['min_temp'] and temp <= outside_activities[x]['max_temp']:
            possible_replacements.append([x, outside_activities[x]])

    if len(possible_replacements) == 0:
        # no activity found.. give inside activity
        return give_inside_activity(activity[key][2])

    else:
        # check for activities with the same type
        for y in possible_replacements:
            if activity[key][2] == y[1]['type']:
                better_replacements.append(y[0])
        return random.choice(better_replacements)


def give_inside_activity(type):
    # return random inside activity
    inside_activities = get_activities('inside')
    replacements = []
    for x in inside_activities:
        if inside_activities[x]['type'] == type:
            replacements.append(x)

    if len(replacements) == 0:
        return random.choice(inside_activities)
    else:
        return random.choice(replacements)
