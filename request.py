import requests
from permission import getlocation


def getalldata():
    location = getlocation()
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=df791e0435796b142477640396f9ef61"

    response = requests.get(url.format(location))
    data = response.json()

    return data


def filterdata():
    data = getalldata()
    filtered = []

    print(data)

    temp = data['main']['temp']
    fl = data['main']['feels_like']
    weather = data['weather'][0]['main']
    location = data['name']

    filtered.append(temp)
    filtered.append(fl)
    filtered.append(weather)
    filtered.append(location)

    return filtered

print(filterdata())