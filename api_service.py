import requests as rq

API_KEY = "sk-8VDw6a3ccec036ac818405"

def suchePflanze(suchbegriff):
    Daten = getRohDaten(suchbegriff)
    name = Daten["common_name"]
    sciName = Daten['scientific_name'][0]
    id = Daten['id']
    return name,sciName



def getRohDaten(suchbegriff):
    antwort = rq.get(f"https://perenual.com/api/species-list?key={API_KEY}&q={suchbegriff}")
    rohDaten = antwort.json()
    schritt1 = rohDaten["data"]
    schritt2 = schritt1[0]
    return schritt2
