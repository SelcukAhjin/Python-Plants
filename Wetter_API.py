import requests as rq
import API_KEY as ak

global answer,answerWeather

def ladeWetterDaten(sucheStadt):
    global answerWeather,answer
    answer=rq.get(f"https://api.openweathermap.org/data/2.5/forecast?q={sucheStadt}&appid={ak.wetter_api_key}&units=metric")
    answerWeather=rq.get(f"https://api.openweathermap.org/data/2.5/weather?q={sucheStadt}&appid={ak.wetter_api_key}&units=metric")




def durchDieListe():
    global answer
    counter=0
    neueListe=[]
    liste = answer.json()["list"]
    for wetterTage in liste:
        if "12:00:00" in wetterTage["dt_txt"]:
            neueListe.append(wetterTage)
            if(counter==len(neueListe)):
                break
    return neueListe


def wetter():
    global anwerWeather
    wetter = answerWeather.json()["weather"][0]["description"]
    return wetter


def temperatur():
    global answerWeather
    temperatur = int(answerWeather.json()["main"]["temp"])
    return temperatur


def icon():
    global answerWeather
    icon = answerWeather.json()["weather"][0]["icon"]
    return f"https://openweathermap.org/img/wn/{icon}@2x.png"
