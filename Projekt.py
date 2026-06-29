import flet as ft
import ssl
import api_service
import Wetter_API as wa

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
    meinBild = ft.Image(src="https://via.placeholder.com/150", width=200, height=200)

    def buttonWurdeGeklickt(e):
        meinLabel.value = f"Wird nach {meinEingabefeld.value} Gesucht"
        gefundenerName1,gefundenerName2,gefundeneSonne,Bild = api_service.suchePflanze(meinEingabefeld.value)
        ergebnisName.value = f"Gefunden: {gefundenerName1}"
        ergebnisBotanisch.value = f"Gefunden: {gefundenerName2}"
        ergebnisSonne.value= f"gefunden: {gefundeneSonne}"
        meinBild.src = Bild
        meinBild.update()
        page.update()
    meinButton = ft.Button("Suche Starten", on_click=buttonWurdeGeklickt)


    meineSucheSpalte = ft.Column(
        controls = [
            meinLabel,
            meinEingabefeld,
            meinButton,
            ergebnisName,
            ergebnisBotanisch,
            ergebnisSonne,
            meinBild,
        ],
        spacing=20
    )

    wetterKarte = ft.Card(
        elevation=5,
        content=ft.Container(
            padding=20,
            content=ft.Row(
                controls=[
                    ft.Image(src=wa.icon(),width=100, height=100),
                    ft.Column(
                        controls=[
                            ft.Text(value=f"{wa.temperatur()}°C",size=40, weight="bold"),
                            ft.Text(wa.wetter().capitalize(),size=16, color="grey")
                        ]
                    )
                ]
            )
        )
    )


    vorhersageReihe = ft.Row(scroll="auto")
    wetter_daten_liste = wa.durchDieListe()
    for eintrag in wetter_daten_liste:
        wetterKarteKleinTemp = int(eintrag["main"]["temp"])
        wetterKarteKleinWetter = eintrag["weather"][0]["description"]
        wetterKarteKleinIcon = eintrag["weather"][0]["icon"]
        kleine_karte = ft.Card(
            elevation=5,
            content=ft.Container(
                padding=20,
                content=ft.Row(
                    controls=[
                        ft.Image(src=f"https://openweathermap.org/img/wn/{wetterKarteKleinIcon}@2x.png", width=50, height=50),
                        ft.Column(
                            controls=[
                                ft.Text(value=f"{wetterKarteKleinTemp}°C",size=20, weight="bold"),
                                ft.Text(wetterKarteKleinWetter,size=8, color="grey")
                            ]
                        )
                    ]
                )
            )
        )
        vorhersageReihe.controls.append(kleine_karte)

    meineWetterSpalte = ft.Column(
        controls = [
            wetterKarte,
            vorhersageReihe
        ],
        spacing=20
    )
    meine_leiste = ft.TabBar(
        tabs=[
            ft.Tab(label="Suche"),
            ft.Tab(label="Wetter"),
        ]
    )

    meine_inhalte = ft.TabBarView(
        expand=True,
        controls=[
            meineSucheSpalte,
            meineWetterSpalte,
        ],
    )
    mein_haupt_ordner = ft.Tabs(
        length=2,
        selected_index=0,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                meine_leiste,
                meine_inhalte
            ]
        )
    )
    page.add(mein_haupt_ordner)
if __name__ == "__main__":
    ft.run(main)
