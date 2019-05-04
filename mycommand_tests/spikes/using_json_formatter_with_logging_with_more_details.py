import logging
import sys

from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(stream=sys.stdout)
formatter = jsonlogger.JsonFormatter('(asctime) (levelname) (message)')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("hello world")
