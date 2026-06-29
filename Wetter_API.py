import requests as rq
import API_KEY as ak

stadt = "Berlin"

answer=rq.get(f"https://api.openweathermap.org/data/2.5/forecast?q={stadt}&appid={ak.wetter_api_key}&units=metric")
answerWeather=rq.get(f"https://api.openweathermap.org/data/2.5/weather?q={stadt}&appid={ak.wetter_api_key}&units=metric")


def durchDieListe():
    counter=0
    neueListe=[]
    liste = answer.json()["list"]
    for wetterTage in liste:
        if "12:00:00" in wetterTage["dt_txt"]:
            neueListe.append(wetterTage)
            if(counter==len(neueListe)):
                break
    print(neueListe)
    return neueListe


def wetter():
    wetter = answerWeather.json()["weather"][0]["description"]
    return wetter


def temperatur():
    temperatur = int(answerWeather.json()["main"]["temp"])
    return temperatur


def icon():
    icon = answerWeather.json()["weather"][0]["icon"]
    return f"https://openweathermap.org/img/wn/{icon}@2x.png"
durchDieListe()