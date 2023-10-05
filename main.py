import os
import discord

# intents
intents = discord.Intents.default()

# client
client = discord.Client(intents=intents)


# print when active
@client.event
async def on_ready():
  print('discord version: ' + discord.__version__)
  print('Ready!')


# run client
client.run(os.environ['DISCORD_BOT'])
