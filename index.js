const { Client, Intents } = require('discord.js');
const axios = require('axios')
const fetch_all = require('discord-fetch-all');
require('dotenv').config();

const client = new Client({ 
    intents: [Intents.FLAGS.GUILDS], 
    partials: ['MESSAGE', 'CHANNEL', 'REACTION'] 
});


client.once('ready', () => handle(client));
client.once('messageCreate', () => handle(client));
client.once('messageDelete', () => handle(client));
client.once('messageUpdate', () => handle(client));


async function handle(client) {
    let channel = client.channels.cache.get(process.env.CHANNEL_ID);
    const messages = await fetch_all.messages(channel, {userOnly: true});
    const message_filter = (message) => {
        return {
            'author': message.author.username, 
            'message': message.content,
            'createdAt': message.createdAt
        }
    }

    const parsed_messages = JSON.stringify({"messages": messages.map(message_filter)});
    post_messages(parsed_messages);
}


async function post_messages(m) {
    console.log(m);
    axios
        .post(
            `http://${process.env.HOST}:${process.env.PORT}/announcements`, m)
        .then(res => {
            console.log(`status code: ${res.status}`)
        })
}

client.login(process.env.DISCORD_TOKEN);
