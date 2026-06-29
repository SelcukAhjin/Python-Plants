import requests as rq
import API_KEY as ak

stadt = "Berlin"

answer=rq.get(f"https://api.openweathermap.org/data/2.5/weather?q={stadt}&appid={ak.wetter_api_key}&units=metric")
def wetter():
    wetter = answer.json()["weather"][0]["description"]
    print(wetter)
    return wetter

def temperatur():
    temperatur = int(answer.json()["main"]["temp"])
    print(f"{temperatur}°C")
    return temperatur

a=wetter()
b=temperatur()
