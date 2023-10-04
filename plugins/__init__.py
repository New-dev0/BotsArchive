from swibots import BotCommand
from client import LOG, app
from config import VERIF_GROUP, POST_CHANNEL

# Add commands to bot
app.set_bot_commands([
    BotCommand("start", "Get Start message", True),
    BotCommand("submit", "Submit your bot", True),
    BotCommand("help", "Get help message", True)
])

# to store chat ids to listen messages
AskMode = set()
GroupInfo = app._loop.run_until_complete(app.get_group(VERIF_GROUP))
PostInfo = app._loop.run_until_complete(app.get_channel(POST_CHANNEL))