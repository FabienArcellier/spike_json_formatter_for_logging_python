import logging
import os
import sys
from datetime import datetime

from pythonjsonlogger import jsonlogger


class CliFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CliFormatter, self).add_fields(log_record, record, message_dict)
        now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        log_record['timestamp'] = now
        log_record['level'] = record.levelname


def get_logger(name: str, force_debug: bool = None) -> logging.Logger:
    debug = force_debug or os.getenv('APP_DEBUG') == '1'
    level_info = logging.DEBUG if debug else logging.INFO

    log_stderr = logging.StreamHandler(stream=sys.stderr)
    json_formatter = CliFormatter(
        "(timestamp) (name) (level) (filename) (lineno) (message)",
    )

    log_stderr.setFormatter(json_formatter)
    logger = logging.getLogger(name)
    logger.addHandler(log_stderr)
    logger.setLevel(level_info)
    return logger
