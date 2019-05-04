import logging
import sys
from datetime import datetime

from pythonjsonlogger import jsonlogger


class Iso8601JsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(Iso8601JsonFormatter, self).add_fields(log_record, record, message_dict)
        now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        log_record['timestamp'] = now


logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(stream=sys.stdout)
formatter = Iso8601JsonFormatter('(timestamp) (levelname) (message)')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("hello world")
