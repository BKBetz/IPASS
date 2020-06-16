import requests
from permission import getlocation


def get_current_weather(location):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=nl&appid=df791e0435796b142477640396f9ef61"

    response = requests.get(url.format(location))
    data = response.json()

    while data['cod'] != 200:
        location = input("De ingevoerde locatie is niet gevonden. Controleer op spellingsfouten of voer een andere plek in de buurt in")
        response = requests.get(url.format(location))
        data = response.json()

    return data


def get_forecast(location):
    url = "https://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&lang=nl&appid=df791e0435796b142477640396f9ef61"

    response = requests.get(url.format(location))
    data = response.json()

    while data['cod'] != '200':
        location = input("De ingevoerde locatie is niet gevonden. Controleer op spellingsfouten of voer een andere plek in de buurt in")
        response = requests.get(url.format(location))
        data = response.json()

    return data


def get_correct_forecast_day(dates, location):
    data = get_forecast(location)
    for date in dates:
        for x in data['list']:
            datetime = x['dt_txt']
            dt = datetime.split(" ")
            if date == dt[0]:
                print(dt)


def filter_current_weather(location):
    data = get_current_weather(location)

    filtered = []

    temp = data['main']['temp']
    fl = data['main']['feels_like']
    weather = data['weather'][0]['description']
    location = data['name']

    filtered.append(temp)
    filtered.append(fl)
    filtered.append(weather)
    filtered.append(location)

    return filtered
