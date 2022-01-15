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
