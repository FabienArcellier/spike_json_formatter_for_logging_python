# coding=utf-8
import json
import sys
import unittest
from io import StringIO

from mycommand.cli_logger import get_logger


class CliLoggerTest(unittest.TestCase):
    def setUp(self):
        self.stderr = sys.stderr
        self.stderr_mock = StringIO()
        sys.stderr = self.stderr_mock

    def tearDown(self):
        sys.stderr = self.stderr

    def test_logger_should_log_on_stdout(self):
        # Assign
        logger = get_logger('logger1')

        # Acts
        logger.info('hello world')

        # Assert
        logs = self.stderr_mock.getvalue().split('\n')
        self.assertEqual(2, len(logs))

    def test_logger_should_log_in_json(self):
        # Assign
        logger = get_logger('logger1')

        # Acts
        logger.info('hello world')

        # Assert
        logs = self.stderr_mock.getvalue().split('\n')
        log = logs[0]
        log_record = json.loads(log)
        self.assertEqual('hello world', log_record['message'])
