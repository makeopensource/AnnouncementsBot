import discord
import datetime
from dotenv import load_dotenv
import os
import requests

# initializers
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
ANNOUNCEMENTS_ID = os.getenv('ANNOUNCEMENTS_ID')
ANNOUNCEMENTS_TOKEN = os.getenv('ANNOUNCEMENTS_TOKEN')
head = {'Authorization': 'Token ' + ANNOUNCEMENTS_TOKEN}

intents = discord.Intents.all()
intents.members = True

client = discord.Client()


###################################
# database manipulation functions #
###################################


# ensure that announcements database reflects discord channel with routine checks
def sync_announcements():
    # channel = client.get_channel(ANNOUNCEMENTS_ID)
    # messages = channel.history(limit=200).flatten()
    pass


# add new announcement to database
def add_announcement(message):
    new_announcement = {
        'text': message.content,
        'discord_id': message.id,
        'created_at': message.created_at
    }
    response = requests.post('http://127.0.0.1:8000/announcements/', new_announcement, headers=head)
    return response.status_code


# edit announcement to reflect discord channel
def edit_announcement(message):
    edited_announcement = {
        'text': message.content,
        'discord_id': message.id,
        'created_at': message.created_at
    }
    response = requests.patch(f'http://127.0.0.1:8000/announcements/{message.id}/', edited_announcement, headers=head)
    return response.status_code


# remove announcement
def remove_announcement(message):
    response = requests.delete(f'http://127.0.0.1:8000/announcements/{message.id}/', headers=head)
    return response.status_code



@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))
    sync_announcements()
    print('announcements synced')

@client.event
async def on_message(message):
    print(message.content)
    print(message.id)
    print(message.created_at)
    add_announcement(message)

@client.event
async def on_message_edit(message_before, message_after):
    edit_announcement(message_after)

@client.event
async def on_message_delete(message):
    remove_announcement(message)


client.run(DISCORD_TOKEN)
