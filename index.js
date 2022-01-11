const { Client, Intents } = require('discord.js');
const { token } = require('./config.json');
const axios = require('axios')
const fetch_all = require('discord-fetch-all');

const ann_channel_id = '848699200337870878';
const client = new Client({ 
    intents: [Intents.FLAGS.GUILDS], 
    partials: ['MESSAGE', 'CHANNEL', 'REACTION'] 
});


client.once('ready', () => handle(client));
client.once('messageCreate', () => handle(client));
client.once('messageDelete', () => handle(client));
client.once('messageUpdate', () => handle(client));


async function handle(client) {
    let channel = client.channels.cache.get(ann_channel_id);
    const messages = await fetch_all.messages(channel, {userOnly: true});
    const message_filter = (message) => {
        return {
            'author': message.author.username, 
            'message': message.content,
            'createdAt': message.createdAt
        }
    }

    const parsed_messages = new Set(messages.map(message_filter));
    console.log(parsed_messages);
    post_messages(parsed_messages);
}


async function post_messages(messages) {
    axios
        .post(
            'https://makeopensource.org/announcements',
            {'messages': messages}
        )
        .then(res => {
            console.log(`status code: ${res.status}`)
        })
}


client.login(token);
