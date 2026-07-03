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
            pflanzenListe = js.loads(answer)
        for pflanzen in pflanzenListe:
            nameSpeichern = ft.Text(value=pflanzen["name"])
            botanischSpeichern = ft.Text(value=pflanzen["botanisch"])
            sonneSpeichern = ft.Text(value=pflanzen["sonne"])
            bildSpeichern = ft.Image(src=pflanzen["bildUrl"])
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
            pflanzenListe = js.loads(answer)
        pflanzenListe.append(pflanzenDaten)
        await self.page.shared_preferences.set("mein_garten",js.dumps(pflanzenListe))


    def loeschePflanzen(self,pflanzenNamen):
        pass
