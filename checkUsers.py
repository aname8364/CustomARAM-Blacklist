from lcu_driver import Connector

from chat  import Chat
from lobby import Lobby
from summoner import Summoner

from bs4 import BeautifulSoup

import requests

connector = Connector()

@connector.ws.register('/lol-chat/v1/conversations/', event_types=("UPDATE",))
async def onPlayerJoin(connection, event):
    leagueChat  = Chat(connection)
    leagueLobby = Lobby(connection)

    if event.uri.find("participants") != -1:
        if "gameName" in event.data:
            name = event.data["name"]
            id = event.data["summonerId"]
            badUsers = BeautifulSoup(requests.get("https://anametest.000webhostapp.com/badusers.html").text, 'html.parser')
            
            badData = {
                user.split("-", 1)[0].strip(): user.split("-", 1)[1].strip() if "-" in user else "?"
                for i, user in enumerate(badUsers.text.splitlines())
                if i > 8 and len(user) > 1
            }

            if name in badData:
                print(f"[강퇴] {name}")
                await leagueChat.SendMessage(f"checkUsers:: {name} ({id}) reason: {badData[name]}")
                await leagueLobby.Kick(id)


connector.start()
