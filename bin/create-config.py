#!/usr/bin/env python3

import json
import warnings
import sys
import logging
from lib.args import Parameters
from lib.logging import CustomFormatter
from lib.exceptions import InputFileReadError
from lib.sizing import ClusterConfig, SizingConfig

warnings.filterwarnings("ignore")
logger = logging.getLogger()
VERSION = '1.0'


class RunMain(object):

    def __init__(self, parameters):
        self.input_file = parameters.input
        self.output_file = parameters.output
        self.data = {}
        self.read_file()

    def read_file(self) -> None:
        try:
            with open(self.input_file, 'r') as input_file:
                self.data = json.load(input_file)
        except Exception as err:
            raise InputFileReadError(f"can not read sizing file {self.input_file}: {err}")

    def process(self):
        logger.info(f"Create Sizer Import ({VERSION})")
        config = ClusterConfig.from_config(self.data)
        sizing = SizingConfig.from_config(config)
        print(json.dumps(sizing.as_dict, indent=2))


def main():
    global logger
    arg_parser = Parameters()
    parameters = arg_parser.args

    try:
        if parameters.debug:
            logger.setLevel(logging.DEBUG)
        elif parameters.verbose:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.ERROR)
    except (ValueError, KeyError):
        pass

    screen_handler = logging.StreamHandler()
    screen_handler.setFormatter(CustomFormatter())
    logger.addHandler(screen_handler)

    task = RunMain(parameters)
    task.process()


if __name__ == '__main__':
    try:
        main()
    except SystemExit as e:
        sys.exit(e.code)
