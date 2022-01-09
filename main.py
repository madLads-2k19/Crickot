from discord.ext import commands
import discord
from dotenv import load_dotenv
load_dotenv()
import os

from src.config import Settings

from src.bot.cogs.livematch import LiveMatch

class Crickot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix = '$')
    
    async def on_ready(self):
        print("Crickot is up!")
    
    # @commands.command()
    async def re(self):
        self.unload_extension("src.bot.livematch")
        self.load_extension("src.bot.livematch")

bot = Crickot()

@bot.command()
async def re(ctx):
    bot.unload_extension("src.bot.cogs.livematch")
    bot.load_extension("src.bot.cogs.livematch")

if __name__ == "__main__":
    for cog in Settings.get_settings()["cogNames"]:
        bot.load_extension(cog)

    bot.run(os.getenv("BOT_TOKEN"))