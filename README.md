# annbot

### setup
1. [Create and authenticate Discord
   bot](https://discord.com/developers/docs/topics/oauth2)

2. Create `config.json` in the main directory
```json
{
    "host": "<insert host here>",
    "port": "insert port here",
    "token": "<insert token here>",
    "channel_id": "<insert channel_id here>"
}
```

The local default is as follows:
```json
{
    "host": "localhost",
    "port": "8000",
    "token": "<token>",
    "channel_id": "848699200337870878"
}

```
*note that the channel id corresponds to the MakeOpenSource announcements
channel_id, and that the token is redacted (for security reasons)*

3. Install modules
```
npm install
```

4. Run discord bot
```
node .
```


### Output

The expected JSON output will be as follows:

```javascript
{
    "messages": [
        {
            "author": "ProminentOperator",  // whoever wrote the announcement
            "message": "🐙 Hi @everyone!",  // the announcement message
            "createdAt": "2022-01-01T18:51:58.151Z",  // the announcement post time
            "reactions": [
                {
                  "type": "custom",  // "custom" means that the "content" is a link to the image
                  "content": "https://cdn.discordapp.com/emojis/889568829796143155.png",
                  "count": 6
                },
                {
                  "type": "emoji",  // "emoji" means that the "content" is a utf-8 emoji
                  "content": "🎉",
                  "count": 5
                }
            ]
        },

        {
            "author": "ProminentOperator", 
            "message": "🦩 Hey @everyone!",
            "createdAt": "2021-12-21T19:59:28.957Z",
            "reactions": []  // if "reactions" is empty, the message had no reactions
        }
    ]
}
```
