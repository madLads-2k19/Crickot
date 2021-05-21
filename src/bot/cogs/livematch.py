from discord.ext import commands
import discord
from src.dependencies.bs4.query_data import QueryCricketData
from src.bot.models.live_match_overview import LiveMatchOverview

# Cog for live Matches

class LiveMatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def live(self, ctx):
        cardsHtml = await QueryCricketData.query_live_matches()
        live_overviews = [LiveMatchOverview(card) for card in cardsHtml]

        embed = {
            "title": ":cricket_game: __Live Cricket Matches__ :cricket_game:",
            "description": "The live cricket matches happening around the world right now",
            "fields": [],
            "color": 65484,
            "provider": {"name": "ESPNCricinfo", "url": "https://www.espncricinfo.com"}
        }

        for live_overview in live_overviews:
            embed["fields"].append(live_overview.get_embed_field())
        
        await ctx.send(embed=discord.Embed.from_dict(embed))

