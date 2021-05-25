from discord.ext import commands
import discord
from dotenv import load_dotenv
load_dotenv()
from cogwatch import watch
import os

from src.bot.cogs.livematch import LiveMatch

class Crickot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix = '$')
    
    # @watch(path = 'src')
    async def on_ready(self):
        print("Crickot is up!")

async def test(ctx):
    msg = await ctx.send(arg)

bot = Crickot()

bot.add_cog(LiveMatch(bot))

bot.run(os.getenv("BOT_TOKEN"))