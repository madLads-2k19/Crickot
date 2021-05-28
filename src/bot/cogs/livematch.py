import datetime
import pytz
from discord.ext import commands
import discord

from src.dependencies.bs4.query_live_overview import QueryLiveOverviews
from src.dependencies.bs4.query_live_match import QueryLiveMatch

from src.bot.models.live_match_overview import LiveMatchOverview
from src.bot.models.live_match_data import LiveMatchData

from src.config import Settings

from timer import Timer

SETTINGS = Settings.get_settings()

# Cog for live Matches

class LiveMatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embedMessages = []
        self.live_overviews = []

    @commands.command()
    async def live(self, ctx):
        Timer.setStartTime()

        cardsHtml = await QueryLiveOverviews.query_live_overviews()

        Timer.checkpoint("Query done, beginning parsing")
        self.live_overviews = [LiveMatchOverview(card) for card in cardsHtml]
        Timer.checkpoint("Completed parsing all cards, beginning to fetch embeds")

        embed = {
            "title": ":cricket_game:  Live Cricket Matches  :cricket_game:",
            "description": "The Live Cricket Matches happening around the world!",
            "fields": [],
            "color": 65484,
            "provider": {"name": "ESPNCricinfo", "url": "https://www.espncricinfo.com"},
            "footer": {"text": f"Valid for 10 minutes. (Generation Time:{datetime.datetime.now().strftime(SETTINGS['botDateTimeFormat'])} IST)"}
        }
        
        for live_overview in self.live_overviews:
            embed["fields"].append(live_overview.get_embed_field())
        
        Timer.checkpoint("Fetched all embeds")

        embedData = discord.Embed.from_dict(embed)

        Timer.checkpoint("Embed dictionary constructed")

        message = await ctx.send(embed=embedData)

        Timer.checkpoint("Embed sent")

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
        livePageUrl = pageUrl + "/live-cricket-score"
        result = await QueryLiveMatch.query_live_match(livePageUrl)
        embed =  LiveMatchData(*result).get_embed()
        await curChannel.send(embed = discord.Embed.from_dict(embed))

def setup(bot):
    bot.add_cog(LiveMatch(bot))