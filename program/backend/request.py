import requests
"""
    This file uses the location in the session to get the weather for that specific location. It can get a specific day
    (forecast can fetch 5 days max) temperature or gives a filtered list of the current weather with only the necessary
    data needed to display on the frontend.
"""



def get_current_weather(location):
    url = "https://api.openweathermap.org/data/2.5/weather?q={},nl&units=metric&lang=nl&appid=df791e0435796b142477640396f9ef61"

    response = requests.get(url.format(location))
    data = response.json()

    return data


def get_forecast(location):
    url = "https://api.openweathermap.org/data/2.5/forecast?q={},nl&units=metric&lang=nl&appid=df791e0435796b142477640396f9ef61"

    response = requests.get(url.format(location))
    data = response.json()

    return data


def get_correct_forecast_day(dates, location):
    data = get_forecast(location)

    average_temps = {}
    for date in dates:
        temps = []
        # we use dt_txt to compare with the dat but it is a datetime so we split it and use the first item (the date)
        for x in data['list']:
            datetime = x['dt_txt']
            dt = datetime.split(" ")
            if date == dt[0]:
                temps.append(x['main']['feels_like'])

        # if the len is 0 it means the user asked for a date that the api couldn't fetch
        if len(temps) == 0:
            a_tmp = "none"
        else:
            a_tmp = get_average_temp(temps)

        average_temps[date] = a_tmp

    return average_temps


def get_average_temp(temps):
    # this function checks all the temperature on a day and calculates the average
    if len(temps) > 1:
        total = 0
        for temp in temps:
            total += temp

        avg_temp = round(total/len(temps), 2)
    else:
        avg_temp = round(temps[0], 2)

    return avg_temp


def filter_current_weather(location):
    data = get_current_weather(location)
    # if the location doesn't exist it returns this
    if data['cod'] != 200:
        return "not found"

    else:
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
