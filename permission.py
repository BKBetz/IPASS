import geocoder


def getlocation():
    answer = input('Mag het programma gebruik maken van je locatie (JA/NEE)')
    while True:
        answer = answer.upper()
        if answer == "JA":
            loc = geocoder.ip('me')
            location = loc.city
            break
        elif answer == "NEE":
            location = input('Vul een locatie in waar je het weer van wilt zien')
            break
        else:
            answer = input("Voer ja of nee in")

    return location

