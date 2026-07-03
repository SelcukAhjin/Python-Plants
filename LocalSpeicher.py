import flet as ft
import json as js



class LocalSpeicher:


    def __init__(self,page):
        self.page = page


    async def ladeGarten(self):
        answer = await self.page.shared_preferences.get("mein_garten")
        meinGartenSpalte = ft.Column()
        if answer is None:
            return ft.Column()
        else:
            try:
                pflanzenListe = js.loads(answer)
            except js.JSONDecodeError:
                pflanzenListe = []
        for pflanzen in pflanzenListe:
            nameSpeichern = ft.Text(value=pflanzen["name"])
            botanischSpeichern = ft.Text(value=pflanzen["botanisch"])
            sonneSpeichern = ft.Text(value=pflanzen["sonne"])
            bildSpeichern = ft.Image(src=pflanzen["bildUrl"])
            async def deleteButtonKlick(e):
                await self.loeschePflanzen(e.control.data)
                meinGartenSpalte.controls.remove(pflanzeSpeicherKarte)
                self.page.update()


            deleteButton = ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=deleteButtonKlick)
            deleteButton.data = nameSpeichern.value
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
            meinGartenSpalte.controls.append(pflanzeSpeicherKarte)
        return meinGartenSpalte


    async def speicherePflanzen(self,pflanzenDaten):
        answer = await self.page.shared_preferences.get("mein_garten")
        if answer is None:
            pflanzenListe = []
        else:
            try:
                pflanzenListe = js.loads(answer)
            except js.JSONDecodeError:
                pflanzenListe = []
        pflanzenListe.append(pflanzenDaten)
        await self.page.shared_preferences.set("mein_garten",js.dumps(pflanzenListe))


    async def loeschePflanzen(self, pflanzenNamen):
        answer = await self.page.shared_preferences.get("mein_garten")
        if answer is None:
            pflanzenListe = []
        else:
            try:
                pflanzenListe = js.loads(answer)
            except js.JSONDecodeError:
                pflanzenListe = []
        for pflanzen in pflanzenListe:
            if pflanzen["name"] == pflanzenNamen:
                pflanzenListe.remove(pflanzen)
                break
        await self.page.shared_preferences.set("mein_garten",js.dumps(pflanzenListe))
