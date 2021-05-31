from src.dependencies.bs4.query_live_match import QueryLiveMatch
from src.dependencies.bs4.query_scorecard import QueryScorecard
from src.bot.models.live_match_data import LiveMatchData
from src.bot.models.scorecard import Scorecard
from src.bot.update.update_manager import UpdateManager
import discord

class UrlRequest:

    async def getEmbed(self):
        liveUrl = self.url + "/live-cricket-score"
        result = await QueryLiveMatch.query_live_match(liveUrl)
        embed =  LiveMatchData(*result).get_embed()

        scorecardUrl = self.url + "/full-scorecard"
        matchHeader, scorecardHtml = await QueryScorecard().query_latest_scorecard(scorecardUrl)
        scorecard = Scorecard(matchHeader, scorecardHtml)

        updateFields = self.update_mgr.get_update_fields(scorecard)
        if updateFields:
            embed["fields"].extend(updateFields)
        return discord.Embed.from_dict(embed)

    def __init__(self, url):
        self.url = url
        self.messages = []
    
    async def init_update_mgr(self):
        scorecardUrl = self.url + "/full-scorecard"
        matchHeader, scorecardHtml = await QueryScorecard().query_latest_scorecard(scorecardUrl)
        scorecard = Scorecard(matchHeader, scorecardHtml)
        self.update_mgr = UpdateManager(self.url, scorecard)
    
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