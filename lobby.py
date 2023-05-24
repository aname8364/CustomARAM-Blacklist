class Lobby:
    def __init__(self, connection):
        self.connection = connection

    async def GetMembers(self):
        members = await( await self.connection.request("get", "/lol-lobby/v2/lobby/members")).json()
        return members
    
    async def GetMember(self, id):
        members = await self.GetMembers()
        for member in members:
            if member["summonerId"] == id:
                return member
        return None

    async def CreateLobby(self, name="", queueId= -1, mode="CLASSIC", map=11, team_size=5, password=None, mutator=""):
        gameTypeConfig = {
            "id": 1,
        }

        lobby_body = {
            "customGameLobby": {
                "configuration": {
                    "gameTypeConfig": gameTypeConfig,
                    "gameMode": mode,
                    "gameMutator": mutator,
                    "mapId": map,
                    "mutators": gameTypeConfig,
                    "spectatorPolicy": "AllAllowed",
                    "teamSize": team_size,
                },
                "lobbyName": name,
                "lobbyPassword": password,
            },
            "isCustom": True,
            "queueId": queueId
        }
        
        await self.connection.request("post", "/lol-lobby/v2/lobby", data=lobby_body)

    async def Invite(self, id, state="Requested", type="lobby"):
        invite_body = [
            {
                "invitationType": type,
                "state": state,
                "toSummonerId": id,
                "toSummonerName": "string"
            }
        ]
        try:
            await self.connection.request("post", "/lol-lobby/v2/lobby/invitations", data=invite_body)
        except:
            print(f"Invite Error: {id}")

    async def Notify(self, id, reason):
        notify_body = [
            {
                "notificationReason": reason,
                "summonerIds": [
                    id
                ],
            }
        ]

        await self.connection.request("post", "/lol-lobby/v2/notifications", data=notify_body)

    async def Custom_Games(self):
        data = await (await self.connection.request('get', '/lol-lobby/v1/custom-games')).json()
        return data
    
    async def Custom_Game(self, id):
        data = await (await self.connection.request('get', '/lol-lobby/v1/custom-games/' + id)).json()
        return data
    
    async def Cancel_Champ_Select(self):
        await self.connection.request('post', '/lol-lobby/v1/lobby/custom/cancel-champ-select')

    async def Start_Champ_Select(self):
        await self.connection.request('post', '/lol-lobby/v1/lobby/custom/start-champ-select')

    async def Join(self, id, isSpectator=False):
        data = {
            "asSpectator":isSpectator
        }
        await self.connection.request('post', f'/lol-lobby/v1/custom-games/{id}/join', data=data)

    async def Kick(self, id):
        await self.connection.request('post', f'/lol-lobby/v2/lobby/members/{str(id)}/kick')
        