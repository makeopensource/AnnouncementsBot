import discord
import datetime
from dotenv import load_dotenv
import os
import requests


# initializers
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
ANNOUNCEMENTS_ID = os.getenv('ANNOUNCEMENTS_ID')  # ID of Announcements channel
ANNOUNCEMENTS_TOKEN = os.getenv('ANNOUNCEMENTS_TOKEN')  # auth token for announcements API
BASE_URL = os.getenv('BASE_URL')  # root URL for requests (including '/' at end)
head = {'Authorization': 'Token ' + ANNOUNCEMENTS_TOKEN}

intents = discord.Intents.all()
intents.members = True

client = discord.Client()



###################################
# database manipulation functions #
###################################

# ensure that announcements database reflects discord channel with routine checks
async def sync_announcements():
    channel = client.get_channel(int(ANNOUNCEMENTS_ID))  # announcements channel
    announcements = await channel.history().flatten()  # all announcement channel messages
    announcement_ids = set([ann.id for ann in announcements])
    response = requests.get(f'{BASE_URL}announcements/api/', headers=head)
    
    if response.status_code == 200:
        # add announcement if not present in database
        for ann in announcements:
            ann_exists = requests.get(f'{BASE_URL}/announcements/api/{ann.id}/')
            if ann_exists.status_code == 404:
                add_announcement(ann)
       
        # delete announcement if not present in announcements channel
        for db_ann in response.json()['results']:
            if db_ann['discord_id'] not in announcement_ids:
                requests.delete(f'{BASE_URL}announcements/api/{db_ann["discord_id"]}/', headers=head)


# add new announcement to database
def add_announcement(message):
    new_announcement = {
        'text': message.content,
        'discord_id': message.id,
        'created_at': message.created_at,
        'reaction_set': [],
    }
    response = requests.post(f'{BASE_URL}announcements/api/', new_announcement, headers=head)
    return response.status_code


# edit announcement to reflect discord channel
def edit_announcement(message):
    edited_announcement = {
        'text': message.content,
        'discord_id': message.id,
        'created_at': message.created_at
    }
    response = requests.patch(f'{BASE_URL}/announcements/api/{message.id}/', edited_announcement, headers=head)
    return response.status_code


# remove announcement
def remove_announcement(message):
    response = requests.delete(f'{BASE_URL}/announcements/api/{message.id}/', headers=head)
    return response.status_code



######################
# discord bot events #
######################

# respond to all user toggled changes
# to reflect those changes live on the
# announcements page

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))
    await sync_announcements()
    print('announcements synced')


@client.event
async def on_message(message):
    if message.channel.id == int(ANNOUNCEMENTS_ID):
        status = add_announcement(message)
        print(f'{status} {message.created_at}: new announcement')


@client.event
async def on_message_edit(message_before, message_after):
    if message_after.channel.id == int(ANNOUNCEMENTS_ID):
        status = edit_announcement(message_after)
        print(f'{status} {message_after.created_at}: edited announcement')


@client.event
async def on_message_delete(message):
    if message.channel.id == int(ANNOUNCEMENTS_ID):
        status = remove_announcement(message)
        print(f'{status} {message.created_at}: deleted announcement')


@client.event 
async def on_raw_reaction_add(payload): 
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id) 
    reaction = payload.emoji.name 
  
    if payload.emoji.is_unicode_emoji(): 
        # send a post request with reaction=payload.emoji.name 
        pass 
    elif payload.emoji.is_custom_emoji(): 
        # send post request with reaction=payload.emoji.url 
       pass 
    print('reaction added') 
 
 
@client.event 
async def on_raw_reaction_remove(payload): 
    print('reaction removed') 
    # send remove request to remove reaction from message 
    pass 



client.run(DISCORD_TOKEN)
