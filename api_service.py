import requests as rq
import API_KEY as ak


def suchePflanze(suchbegriff):
    mock_daten = {
        "common_name": f"Dummy {suchbegriff.capitalize()}",
        "scientific_name": "Monstera deliciosa (Mock)",
        "light": "Viel indirektes Sonnenlicht",
        "watering": "Einmal pro Woche gießen",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/04/Monstera_deliciosa3.jpg"
            }

    name = mock_daten["common_name"]
    sciName = mock_daten["scientific_name"]
    sonne = mock_daten["light"]
    bild = mock_daten["image_url"]

    return name, sciName, sonne, bild

"""def suchePflanze(suchbegriff):
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
"""

def getPflegeDaten(suchbegriff):
    url = "https://house-plants2.p.rapidapi.com/search"
    querystring = {"query": suchbegriff}
    headers = {
        "x-rapidapi-key": ak.API_KEY,
        "x-rapidapi-host": "house-plants2.p.rapidapi.com"
    }
    response = rq.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def getRohDaten(suchbegriff):
    url = "https://house-plants2.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": ak.API_KEY,
        "x-rapidapi-host": "house-plants2.p.rapidapi.com"
    }
    querystring = {"query": suchbegriff}
    response = rq.get(url, headers=headers, params=querystring)

    daten_liste = response.json()
    return daten_liste[0]

a=suchePflanze("monstera")
