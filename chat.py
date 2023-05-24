class Chat:
    def __init__(self, connection):
        self.connection = connection

    async def GetRoomID(self):
        data = await (await self.connection.request('get', '/lol-chat/v1/conversations')).json()
        roomData = {}
        for i in data:
            if i['type'] == 'customGame':
                roomData = i
                break
        return roomData['id']
    
    async def GetRoom(self, id):
        data = await (await self.connection.request('get', '/lol-chat/v1/conversations')).json()
        for i in data:
            if i['id'] == id:
                return i
        return 0

    async def GetMe(self):
       data = await (await self.connection.request('get', '/lol-chat/v1/me')).json()
       return data

    async def SetMe(self, data):
        await self.connection.request('put', '/lol-chat/v1/me', data=data)

    async def GetParticipants(self):
        roomID = await self.GetRoomID()
        members = (await (await self.connection.request('get', '/lol-chat/v1/conversations/' + roomID + "/participants/")).json())
        return members

    async def GetParticipant(self, pid):
        roomID = await self.GetRoomID()
        member = (await (await self.connection.request('get', '/lol-chat/v1/conversations/' + roomID + "/participants/" + str(pid))).json())
        return member

    async def SendMessage(self, message, type="groupchat"):
        "groupchat chat system"
        try:
            roomID = await self.GetRoomID()
            Me     = await self.GetMe()
            messageDataBody = {
                "body": message,
                "type": type,
            }
            await self.connection.request('post', '/lol-chat/v1/conversations/' + roomID + '/messages', data=messageDataBody)
        except Exception as e:
            print(e)

    async def GetMessages(self):
        roomID = await self.GetRoomID()
        s = await (await self.connection.request("get", "/lol-chat/v1/conversations/" + roomID + "/messages")).json()
        return s
