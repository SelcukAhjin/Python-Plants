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
    alarmText = ft.Text(value="", weight="bold", size=16, visible=False)



    def buttonWurdeGeklickt(e):
        meinLabel.value = f"Wird nach {meinEingabefeld.value} Gesucht"
        gefundenerName1,gefundenerName2,gefundeneSonne,Bild,maxtemp, mintemp = api_service.suchePflanze(meinEingabefeld.value)
        ergebnisName.value = f"Gefunden: {gefundenerName1}"
        ergebnisBotanisch.value = f"Gefunden: {gefundenerName2}"
        ergebnisSonne.value= f"gefunden: {gefundeneSonne}"
        meinBild.src = Bild
        
        if wa.temperatur() > maxtemp:
            alarmText.value = "Achtung: Es ist zu warm!"
            alarmText.visible = True
            alarmText.color = ft.Colors.RED

        elif wa.temperatur() < mintemp:
            alarmText.value = "Achtung: Es ist zu kalt!"
            alarmText.visible = True
            alarmText.color = ft.Colors.RED

        else:
            alarmText.value = "Temperatur ist optimal!"
            alarmText.visible = False
            alarmText.color = ft.Colors.GREEN

        alarmText.update()
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
        spacing=20,
        scroll="auto",
        expand=True,
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
                            ft.Text(wa.wetter().capitalize(),size=16, color="grey"),
                            alarmText
                        ]
                    )
                ]
            )
        )
    )


    vorhersageReihe = ft.Row(scroll="auto")
    wetterDatenListe = wa.durchDieListe()
    for eintrag in wetterDatenListe:
        wetterKarteKleinTemp = int(eintrag["main"]["temp"])
        wetterKarteKleinWetter = eintrag["weather"][0]["description"]
        wetterKarteKleinIcon = eintrag["weather"][0]["icon"]
        kleineKarte = ft.Card(
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
        vorhersageReihe.controls.append(kleineKarte)


    meineWetterSpalte=ft.Column(
        controls=[
            wetterKarte,
            vorhersageReihe,
        ],
        spacing=10,
        scroll="auto",
        expand=True,
    )
    # 1. Die Tab-Leiste (TabBar - nur für die Beschriftung zuständig)
    meineLeiste = ft.TabBar(
        tabs=[
            ft.Tab(label="Suche"),
            ft.Tab(label="Wetter"),
        ]
    )

    # 2. Die Tab-Ansicht (TabBarView - hier kommen die Spalten rein)
    meineInhalte = ft.TabBarView(
        expand=True,
        controls=[
            meineSucheSpalte,
            meineWetterSpalte,
        ]
    )

    meinHauptOrdner = ft.Tabs(
        length=2,
        selected_index=0,
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                meineLeiste,
                meineInhalte
            ]
        )
    )

    page.add(meinHauptOrdner)

if __name__ == "__main__":
    ft.run(main)
