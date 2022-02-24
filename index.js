const { Client, Intents } = require('discord.js');
const axios = require('axios')
const fetch_all = require('discord-fetch-all');
const { host, port, token, channel_id } = require('./config.json');

const client = new Client({ 
    intents: [Intents.FLAGS.GUILDS], 
    partials: ['MESSAGE', 'CHANNEL', 'REACTION'] 
});


client.once('ready', () => {
    console.log('Ready!');
    handle(client);
});

client.once('messageCreate', () => handle(client));
client.once('messageDelete', () => handle(client));
client.once('messageUpdate', () => handle(client));


async function handle(client) {
    let channel = client.channels.cache.get(channel_id);
    const messages = await fetch_all.messages(channel, {userOnly: true});

    console.log('fetched messages');
   
    const reaction_filter = (reaction) => {
        if (!reaction._emoji.id) {
            return {
                "type": "emoji",
                "content": reaction._emoji.name,
                "count": reaction.count
            }
        } else {
            return {
                "type": "custom",
                "content": `https://cdn.discordapp.com/emojis/${reaction._emoji.id}.png`,
                "count": reaction.count
            }
        }
    }   

    const message_filter = (message) => {
        return {
            'author': message.author.username, 
            'message': message.content,
            'createdAt': message.createdAt,
            'reactions': message.reactions.cache.map(reaction_filter)

            /* {
                "type": ("emoji" or "reaction"),
                "content": (if emoji, emoji. if reaction, link),
                "frequency": number
            } */
        }
    }

    const parsed_messages = JSON.stringify({"messages": messages.map(message_filter)});
    post_messages(parsed_messages);
    console.log('message sent!')
}


async function post_messages(message) {
    axios
        .post(`http://${host}:${port}/announcements`, message)
        .then(res => {console.log(`status code: ${res.status}`)})
}

client.login(token);
