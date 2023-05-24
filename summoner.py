class Summoner:
    def __init__(self, connection):
        self.connection = connection

    async def GetSummoners(self, name):
        param = {
            "name": name
        }
        summoners = await (await self.connection.request("get", "/lol-summoner/v1/summoners", params=param)).json()
        return summoners
    
    async def GetSummonerWithId(self, id):
        summoners = await (await self.connection.request("get", "/lol-summoner/v1/summoners/" + str(id))).json()
        return summoners