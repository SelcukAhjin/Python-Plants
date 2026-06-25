import requests as rq

API_KEY = "sk-8VDw6a3ccec036ac818405"

def suchePflanze(suchbegriff):
    antwort = rq.get(f"https://perenual.com/api/species-list?key={API_KEY}&q={suchbegriff}")
    rohDaten = antwort.json()
    

print(suchePflanze("monstera"))