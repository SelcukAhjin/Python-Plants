import requests as rq
import API_KEY as ak

response=None
responseWeather=None

def ladeWetterDaten(sucheStadt):
    global responseWeather,response
    try:
        response=rq.get(f"https://api.openweathermap.org/data/2.5/forecast?q={sucheStadt}&appid={ak.wetter_api_key}&units=metric")
        response.raise_for_status()
        responseWeather=rq.get(f"https://api.openweathermap.org/data/2.5/weather?q={sucheStadt}&appid={ak.wetter_api_key}&units=metric")
        responseWeather.raise_for_status()
    except rq.exceptions.RequestException:
        return None



def durchDieListe():
    global response
    counter=0
    neueListe=[]
    try:
        liste = response.json()["list"]
        for wetterTage in liste:
            if "12:00:00" in wetterTage["dt_txt"]:
                neueListe.append(wetterTage)
                if(counter==len(neueListe)):
                    break
        return neueListe
    except (KeyError,AttributeError):
        return []

def wetter():
    global responseWeather
    try:
        wetter = responseWeather.json()["weather"][0]["description"]
        return wetter
    except (KeyError,AttributeError):
        return "Ort nicht gefunden"

def temperatur():
    global responseWeather
    try:
        temperatur = int(responseWeather.json()["main"]["temp"])
        return temperatur
    except ((KeyError,AttributeError)):
        return -99

def icon():
    global responseWeather
    try:
        icon = responseWeather.json()["weather"][0]["icon"]
        return f"https://openweathermap.org/img/wn/{icon}@2x.png"
    except (KeyError,AttributeError):
        return "https://via.placeholder.com/150"