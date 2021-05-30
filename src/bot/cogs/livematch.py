import datetime
import pytz
from discord.ext import commands, tasks
import discord

from src.dependencies.bs4.query_live_overview import QueryLiveOverviews
from src.dependencies.bs4.query_live_match import QueryLiveMatch

from src.bot.models.live_match_overview import LiveMatchOverview
from src.bot.models.live_match_data import LiveMatchData
from src.bot.models.url_request import UrlRequest

from src.config import Settings

SETTINGS = Settings.get_settings()

# Cog for live Matches

class LiveMatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embedMessages = []
        self.live_overviews = []
        
        self.url_requests = []

        self.update_alerts.start()

    @commands.command()
    async def live(self, ctx):

        cardsHtml = await QueryLiveOverviews.query_live_overviews()

        self.live_overviews = [LiveMatchOverview(card) for card in cardsHtml]

        embed = {
            "title": ":cricket_game:  Live Cricket Matches !!!  :cricket_game:",
            "description": "The Live Cricket Matches happening around the world!",
            "fields": [],
            "color": 65484,
            "provider": {"name": "ESPNCricinfo", "url": "https://www.espncricinfo.com"},
            "footer": {"text": f"Valid for 10 minutes. (Generation Time:{datetime.datetime.now().strftime(SETTINGS['botDateTimeFormat'])} IST)"}
        }
        
        for live_overview in self.live_overviews:
            embed["fields"].append(live_overview.get_embed_field())
        

        embedData = discord.Embed.from_dict(embed)


        message = await ctx.send(embed=embedData)

        self.embedMessages.append(message)

        i = 0
        while i < len(self.live_overviews) and i <= 8:
            if self.live_overviews[i].is_live():
                await message.add_reaction(SETTINGS["numberToEmoji"][str(i+1)])
            i += 1

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.bot.user.id == user.id:
            return

        emoji = str(reaction.emoji)

        if emoji not in SETTINGS["emojiToNumber"].keys():
            return

        embed = reaction.message.embeds[0]
        embedFooter = embed.footer.text
        embedDate = embedFooter[embedFooter.index(':') + 1 : -5]
        embedDate = datetime.datetime.strptime(embedDate, SETTINGS["botDateTimeFormat"])
        curChannel = reaction.message.channel

        if reaction.message not in self.embedMessages:
            return

        if not self.live_overviews:
            await curChannel.send("Internal error")
            raise Exception("URL list does not exist")
        
        maxDiffTime = datetime.timedelta(minutes = SETTINGS["maxDiffMinutes"])

        if datetime.datetime.now() - embedDate > maxDiffTime:
            await curChannel.send("The embed that you are attempting to react to is outdated. Use $live to obtain an updated list")
            return

        try:
            selectedMatch = self.live_overviews[SETTINGS["emojiToNumber"][emoji] - 1]
        except IndexError:
            return

        if not selectedMatch.is_live():
            if "IST" in selectedMatch.status:
                await curChannel.send("Selected match is not currently live, the match will start at " + selectedMatch.status)
            else:
                await curChannel.send("The selected match is not currently live.")
            return

        fullUrl = selectedMatch.url
        pageUrl = fullUrl[ : fullUrl.rindex('/')]
        
        new_url_req = UrlRequest(pageUrl)
        await new_url_req.append(curChannel)
        self.url_requests.append(new_url_req)

    @tasks.loop(minutes = SETTINGS["taskLoopMinutes"])
    async def update_alerts(self):
        await self.bot.wait_until_ready()
        for url_req in self.url_requests:
            await url_req.query_and_update()
        


def setup(bot):
    bot.add_cog(LiveMatch(bot))