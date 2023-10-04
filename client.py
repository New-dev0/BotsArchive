from config import BOT_TOKEN
from swibots import Client
from logging import getLogger

LOG = getLogger("Archive")

# create swibots client

app = Client(
    token=BOT_TOKEN
)