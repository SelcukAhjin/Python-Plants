import requests as rq
import API_KEY as ak

def suchePflanze(suchbegriff):
    Daten = getRohDaten(suchbegriff)
    print(Daten)
    name = Daten["common_name"]
    print(name)
    sciName = Daten['scientific_name']
    print(sciName)
    id = Daten["id"]
    details = getPflegeDaten(id)
    print(details)
    return name,sciName

def getPflegeDaten(pflanzen_id):
    antwort = rq.get(f"https://trefle.io/api/v1/species/{pflanzen_id}?token={ak.API_KEY}")
    if antwort.status_code == 200:
        rohDaten = antwort.json()
        schritt1 = rohDaten["data"]
        return schritt1
    else:
        print(antwort.status_code)
        print(antwort.text)
        return "Nicht verfügbar (API LIMIT)"

def getRohDaten(suchbegriff):
    antwort = rq.get(f"https://trefle.io/api/v1/plants/search?token={ak.API_KEY}&q={suchbegriff}")
    rohDaten = antwort.json()
    schritt1 = rohDaten["data"][0]
    schritt2 = schritt1
    return schritt2

a,b=suchePflanze("monstera")
