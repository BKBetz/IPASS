import requests
from permission import getlocation


def get_current_weather():
    location = getlocation()
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=nl&appid=df791e0435796b142477640396f9ef61"

    response = requests.get(url.format(location))
    data = response.json()

    while data['cod'] != 200:
        location = input("De ingevoerde locatie is niet gevonden. Controleer op spellingsfouten of voer een andere plek in de buurt in")
        response = requests.get(url.format(location))
        data = response.json()

    return data


def get_forecast():
    location = getlocation()
    url = "https://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&lang=nl&appid=df791e0435796b142477640396f9ef61"

    response = requests.get(url.format(location))
    data = response.json()

    while data['cod'] != '200':
        location = input("De ingevoerde locatie is niet gevonden. Controleer op spellingsfouten of voer een andere plek in de buurt in")
        response = requests.get(url.format(location))
        data = response.json()

    return data


def filter_current_weather():
    data = get_current_weather()

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
