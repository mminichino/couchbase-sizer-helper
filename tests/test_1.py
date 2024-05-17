#!/usr/bin/env python3

import logging
import unittest
import time
import warnings
import os
import json
from tests.common import cli_run

warnings.filterwarnings("ignore")
current = os.path.dirname(os.path.realpath(__file__))

input_path = os.path.join(current, 'sample_data.json')
output_path = os.path.join(current, 'pytest_output.json')


class TestMain(unittest.TestCase):
    command = None

    def setUp(self):
        self.command = 'create_import'

    def tearDown(self):
        time.sleep(1)
        loggers = [logging.getLogger()] + list(logging.Logger.manager.loggerDict.values())
        for logger in loggers:
            handlers = getattr(logger, 'handlers', [])
            for handler in handlers:
                logger.removeHandler(handler)

    def test_1(self):
        args = ["-i", input_path, "-o", output_path]
        result, output = cli_run(self.command, *args)
        f = open(output_path)
        data = json.load(f)
        assert data.get('clusters', [{}])[0].get('services', {}).get('data', {}).get('buckets', [{}])[0].get('name') == 'mybucket'
        assert result == 0

    def test_2(self):
        pass
