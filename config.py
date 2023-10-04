from decouple import config

BOT_TOKEN = config("BOT_TOKEN", default="")

PLUGINS_PATH = config("PLUGINS", default="plugins")
VERIF_GROUP = config("VERIFY_GROUP", default="")
POST_CHANNEL = config("POST_CHANNEL", default="")

REDIS_URL = config("REDIS_URL", default="")
REDIS_PASSWORD = config("REDIS_PASSWORD", default="")
