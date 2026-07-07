import flet as ft
import ssl
import datetime
from flet import TextField
import API_Service
import LocalSpeicher
import Wetter_API as wa
from deep_translator import GoogleTranslator as gt, GoogleTranslator


ssl._create_default_https_context = ssl._create_unverified_context

async def main(page: ft.Page):
    meinSpeicher = LocalSpeicher.LocalSpeicher(page)

    spacingText=ft.Text(value="")
    page.title = "Flower Power At your Hour"
    page.window.width = 400
    page.window.height = 700
    page.window.maximizable = False
    page.window.resizable = False
    page.update()
    wa.ladeWetterDaten("Berlin")
    Titel = ft.Text(value ="Willkommen zum Botaniker", size=30 )
    PflanzenSucheFeld = ft.TextField(label="Nach welcher Pflanze suchen Sie ?")
    ergebnisName = ft.Text(value="")
    ergebnisBotanisch = ft.Text(value="")
    ergebnisSonne = ft.Text(value="")
    aktuelle_maxtemp = None
    aktuelle_mintemp = None
    PflanzenBild = ft.Image(src="https://via.placeholder.com/150", width=200, height=200)
    alarmText = ft.Text(value="", weight="bold", size=16, visible=False)
    alarmTipp = ft.Text(value="", size=14, color=ft.Colors.GREY_400, italic=True, visible=False)
    wetterTempText = ft.Text(value=f"{wa.temperatur()}°C", size=40, weight="bold")
    wetterBeschreibung=ft.Text(wa.wetter().capitalize(),size=16, color="grey")
    wetterIcon=ft.Image(src=wa.icon(),width=100, height=100)
    wetterOrt = TextField(label="Geben Sie Ihre Stadt ein")
    ladekreisSuche = ft.ProgressRing(width=20,height=20,visible=False,)
    ladekreisWetter = ft.ProgressRing(width=20,height=20,visible=False,)
    vorhersageReihe = ft.Row(scroll="auto")

    def ladeDatenImHintergrund():
        wa.ladeWetterDaten(wetterOrt.value)
        wetterTempText.value=f"{wa.temperatur()}°C"
        wetterBeschreibung.value = wa.wetter().capitalize()
        wetterIcon.src = wa.icon()
        vorhersageReihe.controls.clear()
        wetterDatenListe = wa.durchDieListe()

        for eintrag in wetterDatenListe:
            wetterKarteKleinTemp = int(eintrag["main"]["temp"])
            wetterKarteKleinWetter = eintrag["weather"][0]["description"]
            wetterKarteKleinIcon = eintrag["weather"][0]["icon"]

            datum_str = eintrag["dt_txt"]
            datum_obj = datetime.datetime.strptime(datum_str, "%Y-%m-%d %H:%M:%S")
            wochentag = datum_obj.strftime("%A")

            kleineKarte = ft.Card(
                elevation=5,
                content=ft.Container(
                    padding=20,
                    content=ft.Row(
                        controls=[
                            ft.Image(src=f"https://openweathermap.org/img/wn/{wetterKarteKleinIcon}@2x.png", width=50, height=50),
                            ft.Column(
                                controls=[
                                    ft.Text(value=wochentag, weight="bold", color=ft.Colors.BLUE_400),
                                    ft.Text(value=f"{wetterKarteKleinTemp}°C",size=20, weight="bold"),
                                    ft.Text(wetterKarteKleinWetter,size=8, color="grey")
                                ]
                            )
                        ]
                    )
                )
            )
            vorhersageReihe.controls.append(kleineKarte)
        alarmPruefen()
        ladekreisWetter.visible = False
        page.update()


    def sucheImHintergrundStarten():
        nonlocal aktuelle_maxtemp, aktuelle_mintemp
        uebersetzter=GoogleTranslator(source="de",target="en")
        Titel.value = f"Wird nach {PflanzenSucheFeld.value} Gesucht"
        gefundenerName1,gefundenerName2,gefundeneSonne,Bild,maxtemp, mintemp = API_Service.suchePflanze(uebersetzter.translate(PflanzenSucheFeld.value))
        aktuelle_mintemp = mintemp
        aktuelle_maxtemp = maxtemp
        ergebnisName.value = f"Gefunden: {gefundenerName1}"
        if gefundenerName1 == "Pflanze nicht gefunden":
            ergebnisName.value = "Pflanze leider nicht gefunden."
            ergebnisBotanisch.value=""
            ergebnisSonne.value=""
            PflanzenBild.src="http://via.placeholder.com/150"
            alarmText.visible = False
            alarmTipp.visible = False
            ladekreisSuche.visible = False
            inMeinGarten.visible = False
            page.update()
            return
        ergebnisBotanisch.value = f"Gefunden: {gefundenerName2}"
        ergebnisSonne.value= f"gefunden: {gefundeneSonne}"
        PflanzenBild.src = Bild

        aktuelle_maxtemp = maxtemp
        aktuelle_mintemp = mintemp
        alarmPruefen()

        ladekreisSuche.visible=False
        page.update()

    def alarmPruefen():
        if aktuelle_maxtemp is None or aktuelle_mintemp is None:
            return  # Wenn noch keine Pflanze gesucht wurde, brechen wir hier einfach ab.

        temp = wa.temperatur()

        if temp == -99:
            alarmText.visible = True
            alarmText.value = "Keine Wetterdaten verfügbar"
        elif temp >= aktuelle_maxtemp:
            alarmText.value = "Achtung: Es ist zu warm!"
            alarmText.visible = True
            alarmText.color = ft.Colors.RED
            alarmTipp.value = "Tipp: Pflanze in den Schatten"
            alarmTipp.visible = True
        elif temp <= aktuelle_mintemp:
            alarmText.value = "Achtung: Es ist zu kalt!"
            alarmText.visible = True
            alarmText.color = ft.Colors.RED
            alarmTipp.value = "Tipp: Pflanze am besten reinnehmen"
            alarmTipp.visible = True
        else:
            alarmText.value = "Temperatur ist optimal!"
            alarmText.visible = True
            alarmText.color = ft.Colors.GREEN
            alarmTipp.visible = False

        page.update()

    def wetterSuche(e):
        ladekreisWetter.visible=True
        ladekreisWetter.update()
        page.run_thread(ladeDatenImHintergrund)

    wetterButton = ft.Button("Wetter für Stadt suchen", on_click=wetterSuche)

    def buttonWurdeGeklickt(e):
        ladekreisSuche.visible=True
        ladekreisSuche.update()
        page.run_thread(sucheImHintergrundStarten)
        inMeinGarten.visible=True

    meinButton = ft.Button("Suche Starten", on_click=buttonWurdeGeklickt)

    async def pflanzeSpeichern(e):
        nameSpeichern=ft.Text(value=ergebnisName.value)
        botanischSpeichern=ft.Text(value=ergebnisBotanisch.value)
        sonneSpeichern=ft.Text(value=ergebnisSonne.value)
        bildSpeichern=ft.Image(src=PflanzenBild.src)

        async def deleteButtonKlick(e):
            await meinSpeicher.loeschePflanzen(e.control.data["name"])
            meinGartenSpalte.controls.remove(e.control.data["karte"])
            page.update()

        deleteButton = ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=deleteButtonKlick)
        pflanzeSpeicherKarte = ft.Card(
            elevation=5,
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        bildSpeichern,
                        nameSpeichern,
                        botanischSpeichern,
                        sonneSpeichern,
                        deleteButton,
                    ]
                )
            )
        )

        deleteButton.data = dict = {"name":nameSpeichern.value,"karte":pflanzeSpeicherKarte}

        meinGartenSpalte.controls.append(pflanzeSpeicherKarte)
        neuePflanzeDaten = {
            "name": ergebnisName.value,
            "botanisch": ergebnisBotanisch.value,
            "sonne": ergebnisSonne.value,
            "bildUrl": PflanzenBild.src
        }

        await meinSpeicher.speicherePflanzen(neuePflanzeDaten)
        page.update()

    inMeinGarten = ft.Button("In den Garten pflanzen", on_click=pflanzeSpeichern, visible=False)

    wetterDatenListe = wa.durchDieListe()
    for eintrag in wetterDatenListe:
        wetterKarteKleinTemp = int(eintrag["main"]["temp"])
        wetterKarteKleinWetter = eintrag["weather"][0]["description"]
        wetterKarteKleinIcon = eintrag["weather"][0]["icon"]

        datum_str = eintrag["dt_txt"]
        datum_obj = datetime.datetime.strptime(datum_str, "%Y-%m-%d %H:%M:%S")
        wochentag = datum_obj.strftime("%A")

        kleineKarte = ft.Card(
            elevation=5,
            content=ft.Container(
                padding=20,
                content=ft.Row(
                    controls=[
                        ft.Image(src=f"https://openweathermap.org/img/wn/{wetterKarteKleinIcon}@2x.png", width=50,
                                 height=50),
                        ft.Column(
                            controls=[
                                ft.Text(value=wochentag, weight="bold", color=ft.Colors.BLUE_400),
                                ft.Text(value=f"{wetterKarteKleinTemp}°C", size=20, weight="bold"),
                                ft.Text(wetterKarteKleinWetter, size=8, color="grey")
                            ]
                        )
                    ]
                )
            )
        )
        vorhersageReihe.controls.append(kleineKarte)



    wetterKarte = ft.Card(
        elevation=5,
        content=ft.Container(
            padding=20,
            content=ft.Row(
                controls=[
                    wetterIcon,
                    ft.Column(
                        controls=[
                            wetterTempText,
                            wetterBeschreibung,
                            alarmText,
                            alarmTipp
                        ]
                    )
                ]
            )
        )
    )

    meineSucheSpalte = ft.Column(
        controls = [
            Titel,
            PflanzenSucheFeld,
            ft.Row(controls=[meinButton,ladekreisSuche],),
            ergebnisName,
            ergebnisBotanisch,
            ergebnisSonne,
            PflanzenBild,
            inMeinGarten,
        ],
        spacing=10,
        scroll="auto",
        expand=True,
    )

    meineWetterSpalte=ft.Column(
        controls=[
            spacingText,
            wetterOrt,
            ft.Row(controls=[wetterButton,ladekreisWetter,],),
            wetterKarte,
            vorhersageReihe,
        ],
        spacing=10,
        scroll="auto",

    )
    meinGartenSpalte = await meinSpeicher.ladeGarten()

    meinGartenSpalte.spacing = 10
    meinGartenSpalte.scroll = "auto"
    meinGartenSpalte.expand = True


    meineLeiste = ft.TabBar(
        tabs=[
            ft.Tab(label="Suche"),
            ft.Tab(label="Wetter"),
            ft.Tab(label="Mein Garten")
        ]
    )

    meineInhalte = ft.TabBarView(
        expand=True,
        controls=[
            meineSucheSpalte,
            meineWetterSpalte,
            meinGartenSpalte
        ]
    )

    meinHauptOrdner = ft.Tabs(
        length=3,
        selected_index=0,
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                meineLeiste,
                meineInhalte,
            ]
        )
    )

    page.add(meinHauptOrdner)

if __name__ == "__main__":
    ft.run(main)
