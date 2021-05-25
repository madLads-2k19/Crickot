import datetime
import pytz
from discord.ext import commands
import discord
from src.dependencies.bs4.query_data import QueryCricketData
from src.bot.models.live_match_overview import LiveMatchOverview

# Cog for live Matches


numberEmojis = {'1️⃣' : 1, '2️⃣' : 2, '3️⃣' : 3, '4️⃣' : 4, '5️⃣' : 5, '6️⃣' : 6, '7️⃣' : 7, '8️⃣' : 8, '9️⃣' : 9}
maxDiff = datetime.timedelta(minutes = 10)
istTimeZone = pytz.timezone('Asia/Kolkata')
standardDateTimeFormat = "%Y-%m-%d %H:%M:%S"

class LiveMatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embedMessages = []
        self.urls = []

    @commands.command()
    async def live(self, ctx):
        
        cardsHtml = await QueryCricketData.query_live_matches()
        live_overviews = [LiveMatchOverview(card) for card in cardsHtml]

        embed = {
            "title": ":cricket_game:  Live Cricket Matches  :cricket_game:",
            "description": "The Live Cricket Matches happening around the world!",
            "fields": [],
            "color": 65484,
            "provider": {"name": "ESPNCricinfo", "url": "https://www.espncricinfo.com"},
            "footer": {"text": f"Valid for 10 minutes. (Generation Time:{datetime.datetime.now().strftime(standardDateTimeFormat)} IST)"}
        }

        refreshUrls = False
        if not self.urls:
            refreshUrls = True
        
        for live_overview in live_overviews:
            if refreshUrls:
                self.urls.append(live_overview.url)
            embed["fields"].append(live_overview.get_embed_field())
        
        embedData = discord.Embed.from_dict(embed)
        message = await ctx.send(embed=embedData)
        self.embedMessages.append(message)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        emoji = str(reaction.emoji)
        
        if emoji in numberEmojis.keys():
            print("Number found")
            embed = reaction.message.embeds[0]
            embedFooter = embed.footer.text
            embedDate = embedFooter[embedFooter.index(':') + 1 : -5]
            print(embedDate)
            embedDate = datetime.datetime.strptime(embedDate, standardDateTimeFormat)
            if reaction.message in self.embedMessages:
                if not self.urls:
                    raise Exception("URL list does not exist")
                if datetime.datetime.now() - embedDate > maxDiff:
                    raise Exception("Outdated Embed")
                # print(self.urls)
                print(self.urls[numberEmojis[emoji] - 1])
