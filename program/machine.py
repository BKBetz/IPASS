from flask import *
import json
from datetime import *
import random


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
                        answers.append(pretty_answer(y, forecast[y], x, True))
                    else:
                        answers.append(pretty_answer(y, forecast[y], x, False))
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
        return str.format(clean_date, activity)
    else:
        replacement = find_replacement(temp)
        str = "Op {} is het gemiddeld {} graden en is het geen goede dag om de volgende activiteit uit te voeren: {}. Een leuke activiteit zou {} zijn."
        return str.format(clean_date, temp, activity, replacement)


def find_replacement(temp):
    # check the current temp
    outside_activities = get_activities('outside')
    replacements =[]
    for x in outside_activities:
        # find all activities that are okay to do with these weather circumstances
        if temp >= outside_activities[x]['min_temp'] and temp <= outside_activities[x]['max_temp']:
            replacements.append(x)

    if len(replacements) == 0:
        # no activity found.. give inside activity
        return give_inside_activity()

    else:
        # pick random outside activity that can act as a replacement
        return random.choice(replacements)


def give_inside_activity():
    # return random inside activity
    inside_activities = get_activities('inside')
    return random.choice(inside_activities)
