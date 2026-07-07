import requests as rq
import API_KEY as ak



"""def suchePflanze(suchbegriff):
    mock_daten = {
        "temp_max":20,
        "temp_min": 15,
        "common_name": f"Dummy {suchbegriff.capitalize()}",
        "scientific_name": "Monstera deliciosa (Mock)",
        "light": "Viel indirektes Sonnenlicht",
        "watering": "Einmal pro Woche gießen",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/04/Monstera_deliciosa3.jpg"
            }

    temp_max = mock_daten['temp_max']
    temp_min = mock_daten['temp_min']
    name = mock_daten["common_name"]
    sciName = mock_daten["scientific_name"]
    sonne = mock_daten["light"]
    bild = mock_daten["image_url"]

    return name, sciName, sonne, bild, temp_max, temp_min
"""

def suchePflanze(suchbegriff):
    Daten = getRohDaten(suchbegriff)
    if Daten is None:
        return "Pflanze nicht gefunden", "", "", "[https://via.placeholder.com/150](https://via.placeholder.com/150)", 0, 0
    name = Daten["item"]["Common name (fr.)"]
    sciName = Daten["item"]['Latin name']
    id = Daten["refIndex"]
    img=Daten["item"]["Img"]
    temp_max = Daten["item"]["Temperature max"]["C"]
    temp_min = Daten["item"]["Temperature min"]["C"]
    sonne = Daten["item"]["Light ideal"]
    return name,sciName,sonne,img,temp_max,temp_min

def getRohDaten(suchbegriff):
    try:
        url = "https://house-plants2.p.rapidapi.com/search"
        headers = {
            "x-rapidapi-key": ak.API_KEY,
            "x-rapidapi-host": "house-plants2.p.rapidapi.com"
        }
        querystring = {"query": suchbegriff}
        response = rq.get(url, headers=headers, params=querystring)
        response.raise_for_status()
    except rq.exceptions.RequestException:
        return None
    try:
        daten_liste = response.json()
        return daten_liste[0]
    except IndexError:
        return None
