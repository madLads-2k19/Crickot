from src.dependencies.bs4.query_live_match import QueryLiveMatch
from src.bot.models.live_match_data import LiveMatchData

class UrlRequest:

    @staticmethod
    async def getEmbed(url):
        result = await QueryLiveMatch.query_live_match(url)
        embed =  LiveMatchData(*result).get_embed()
        return embed

    def __init__(self, url):
        self.url = url
        self.messages = []
    
    async def append(self, channel):
        embed = await UrlRequest.getEmbed(self.url)
        message = await channel.send(embed = embed)
        self.messages.append(message)
    
    def remove(self, message):
        self.messages.remove(message)
    
    def __len__(self):
        return len(self.messages)
    
    def __bool__(self):
        return bool(self.messages)
    
    async def query_and_update(self):
        i = 0
        
        while i < len(self.messages):
            embed = await UrlRequest.getEmbed(self.url)
            new_msg = await self.messages[i].channel.send(embed = embed)
            await self.messages[i].delete()
            self.messages[i] = new_msg
            i += 1