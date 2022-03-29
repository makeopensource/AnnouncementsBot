from dotenv import load_dotenv
import discord
import os
import requests
import json

load_dotenv()

host = os.getenv("HOST")
port = os.getenv("PORT")
token = os.getenv("TOKEN")
channel_id = int(os.getenv("CHANNEL_ID"))


bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'logged in!')
    await handle(bot)

@bot.event
async def on_message(message):
    await handle(bot)

@bot.event
async def on_raw_message_delete(payload):
    await handle(bot)

@bot.event
async def on_raw_message_edit(payload):
    await handle(bot)

@bot.event
async def on_raw_reaction_add(payload):
    await handle(bot)

@bot.event
async def on_raw_reaction_remove(payload):
    await handle(bot)



async def handle(client):
    channel = client.get_channel(channel_id)
    messages = await channel.history(limit=200).flatten()
    parsed = {'messages': [std_message(_) for _ in messages]}
    response = requests.post(f'http://{host}:{port}/announcements', data=json.dumps(parsed))
    print(f'{response.status_code}{response.text}')



def std_message(message):
    return {
        'author': message.author.name,
        'message': message.content,
        'createdAt': message.created_at.strftime('%m/%d/%Y'),
        'reactions': [std_reaction(_) for _ in message.reactions],
        'attachments': [std_attachment(_) for _ in message.attachments]
    }

def std_reaction(reaction):
    if reaction.is_custom_emoji():
        return {
            'type': 'custom',
            'content': f'https://cdn.discordapp.com/emojis/{reaction.emoji.id}.png',
            'count': reaction.count
        }
    else:
        return {
            'type': 'emoji',
            'content': reaction.emoji,
            'count': reaction.count
        }

def std_attachment(attachement):
    return attachement.url

bot.run(token)
