import discord

import datetime
from dotenv import load_dotenv
import os
import requests

# initializers
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_IDS = [int(os.getenv('GUILD_IDS',0))]

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, description=DESCRIPTION,intents=intents)


###################################
# database manipulation functions #
###################################

# ensure that announcements database reflects discord channel with routine checks
def sync_annountements():
    pass


# add new announcement to database
def add_announcement(message):
    pass


# edit announcement to reflect discord channel
def edit_announcement(message):
    pass


# remove announcement
def remove_announcement(message):
    pass


@bot.event
async def onReady():
    sync_announcements()

@bot.event
async def on_message(message):
    add_announcement(message)

@bot.event
async def on_message_edit(message):
    edit_announcement(message)

@bot.event
async def on_message_delete(message):
    remove_announcement(message)
