from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import os

from src.bot.cogs.livematch import LiveMatch

bot = commands.Bot(command_prefix = '$')

@bot.command()
async def test(ctx, arg):
    msg = await ctx.send(arg)
    print(type(msg))
    print(msg)
    mid = msg.id
    import time
    time.sleep(10)
    newMsg = await msg.channel.fetch_message(mid)
    print(newMsg.reactions)

bot.add_cog(LiveMatch(bot))

@bot.event
async def on_ready():
    print("Crickot is up")

bot.run(os.getenv("BOT_TOKEN"))