from src.dependencies.bs4.query_live_match import QueryLiveMatch
from src.dependencies.bs4.query_scorecard import QueryScorecard
from src.bot.models.live_match_data import LiveMatchData
from src.bot.models.scorecard import Scorecard

class UrlRequest:

    async def getEmbed(self):
        liveUrl = self.url + "/live-cricket-score"
        result = await QueryLiveMatch.query_live_match(liveUrl)
        embed =  LiveMatchData(*result).get_embed()

        scorecardUrl = self.url + "/full-scorecard"
        scorecardHtml =await  QueryScorecard().query_latest_scorecard(scorecardUrl)
        scorecard = Scorecard(scorecardHtml)
        return embed

    def __init__(self, url):
        self.url = url
        self.messages = []
    
    async def append(self, channel):
        embed = await self.getEmbed()
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
            embed = await self.getEmbed()
            new_msg = await self.messages[i].channel.send(embed = embed)
            await self.messages[i].delete()
            self.messages[i] = new_msg
            i += 1