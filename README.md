# annbot

### setup
1. [Create and authenticate Discord
   bot](https://discord.com/developers/docs/topics/oauth2)

2. Create `.env` in the main directory
```
HOST="web"
PORT="8000"
TOKEN="<token>"
CHANNEL_ID="848699200337870878"
```

The local default is as follows:
```
HOST="web"
PORT="8000"
TOKEN="<token>"
CHANNEL_ID="848699200337870878"
```
*note that the channel id corresponds to the MakeOpenSource announcements
channel_id, and that the token is redacted (for security reasons)*

3. Install modules
```
python3 -m pip install -r requirements.txt
```

4. Run discord bot
```
python3 annbot.py
```
