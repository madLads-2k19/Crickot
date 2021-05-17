import discord
from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from scorequery import ScoreQuery
client = discord.Client()

querier = None
url = None

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global querier, url
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('$seturl'):
        msg_content = message.content[8:]
        print(msg_content)
        [interval, url] = msg_content.split(" ")
        querier = ScoreQuery(url, float(interval), message.channel, asyncio.get_event_loop())
        await message.channel.send(f'Started following {url}')
    
    if message.content.startswith('$delurl'):
        querier.clear()
        await message.channel.send(f'Stopped following {url}')


client.run(os.getenv('BOT_TOKEN'))