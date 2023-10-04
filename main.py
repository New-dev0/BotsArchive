import os
import logging
logging.basicConfig(level=logging.INFO)

from importlib import import_module
from client import app, LOG
from config import PLUGINS_PATH

# Import Modules
for file in os.listdir(PLUGINS_PATH):
    if file.startswith("__"):
        continue
    path = os.path.join(PLUGINS_PATH, file).replace("/", ".").replace("\\", ".")[:-3]
    try:
        import_module(path)
        LOG.info(f"Imported {path}!")
    except ModuleNotFoundError as er:
        LOG.exception(er)

# Run Client
app.run()