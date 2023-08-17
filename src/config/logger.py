import logging
import os
import sys
from logging.handlers import RotatingFileHandler

if not os.path.exists("/tmp/logs/"):
    os.makedirs("/tmp/logs/")

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    "[%(levelname)s] %(asctime)s %(funcName)s -> %(message)s")
ch.setFormatter(formatter)

handler = RotatingFileHandler(
    f"/tmp/logs/gerador.log", mode="a", maxBytes=50000, backupCount=10
)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.addHandler(ch)
logger.addHandler(handler)
