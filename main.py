import os
from typing import Literal
import discord
from discord import app_commands

from zoneinfo import ZoneInfo
import datetime
import time
import calendar

# intents
intents = discord.Intents.default()
intents.message_content = True

# client
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# guild id
MY_GUILD_ID = os.environ['GUILD_ID']


# print when active
@client.event
async def on_ready():
  await tree.sync(guild=discord.Object(id=MY_GUILD_ID))
  print('discord version: ' + discord.__version__)
  print('Ready!')


# hello
@tree.command(name='hello',
              description='Say hello!',
              guild=discord.Object(id=MY_GUILD_ID))
async def hello(interaction):
  await interaction.response.send_message('Hello')


# print command
@tree.command(name='test',
              description='print a number and a string',
              guild=discord.Object(id=MY_GUILD_ID))
async def test(interaction, number: int, string: str):
  await interaction.response.send_message(f'{number} and {string}')


# time zones
timeZone = Literal['Seoul']

timeZoneDict = {'Seoul': 'Asia/Seoul'}


# convert from time zone to epoch
@tree.command(name='convert',
              description='Convert time to epoch',
              guild=discord.Object(id=MY_GUILD_ID))
@app_commands.describe(
    timezone='Select the timezone of the date/time to convert to epoch',
    hour='hour in 24 hour format')
async def convert(interaction, timezone: timeZone,
                  year: app_commands.Range[int, 1, 9999],
                  month: app_commands.Range[int, 1, 12],
                  day: app_commands.Range[int, 1,
                                          31], hour: app_commands.Range[int, 0,
                                                                        23],
                  minute: app_commands.Range[int, 0, 59],
                  second: app_commands.Range[int, 0, 59]):
  try:
    dt = datetime.datetime(year,
                           month,
                           day,
                           hour=hour,
                           minute=minute,
                           second=second,
                           tzinfo=ZoneInfo(timeZoneDict[timezone]))
    dtUtc = dt.astimezone(ZoneInfo('UTC')).strftime('%Y-%m-%d %H:%M:%S')
    epochTime = calendar.timegm(time.strptime(dtUtc, '%Y-%m-%d %H:%M:%S'))
  except (AttributeError, ValueError):
    epochTime = 'Invalid date entered'
  await interaction.response.send_message(f'{epochTime}')


# run client
client.run(os.environ['DISCORD_BOT'])
