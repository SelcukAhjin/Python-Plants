import flet as ft
import ssl
import api_service

ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    page.title = "Flower Power At your Hour"
    page.window.width = 400
    page.window.height = 700

    meinLabel = ft.Text(value ="Willkommen zum Botaniker")
    meinEingabefeld = ft.TextField(label="Nach welcher Pflanze suchen Sie ?")
    ergebnisName = ft.Text(value="")
    ergebnisBotanisch = ft.Text(value="")
    ergebnisSonne = ft.Text(value="")

    def buttonWurdeGeklickt(e):
        meinLabel.value = f"Wird nach {meinEingabefeld.value} Gesucht"
        gefundenerName1,gefundenerName2 = api_service.suchePflanze(meinEingabefeld.value)
        ergebnisName.value = f"Gefunden: {gefundenerName1}"
        ergebnisBotanisch.value = f"Gefunden: {gefundenerName2}"

        page.update()
    meinButton = ft.Button("Suche Starten", on_click=buttonWurdeGeklickt)

    meinLayoutSpalte = ft.Column(
        controls = [
            meinLabel,
            meinEingabefeld,
            meinButton,
            ergebnisName,
            ergebnisBotanisch,
            ergebnisSonne
        ],
        spacing=20
    )

    page.add(meinLayoutSpalte)

if __name__ == "__main__":
    ft.run(main)
