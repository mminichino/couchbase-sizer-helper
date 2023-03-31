##
##

import argparse


class Parameters(object):

    def __init__(self):
        parent_parser = argparse.ArgumentParser(add_help=False)
        parent_parser.add_argument('-i', '--input', action='store', help="Sizing output", required=True)
        parent_parser.add_argument('-o', '--output', action='store', help="Output file", default="cluster_config.json")
        parent_parser.add_argument('-n', '--name', action='store', help="Name", default="Cluster1")
        parent_parser.add_argument('-d', '--debug', action='store_true', help="Debug output")
        parent_parser.add_argument('-v', '--verbose', action='store_true', help="Verbose output")
        parent_parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show help message')
        self.parameters = parent_parser.parse_args()

    @property
    def args(self):
        return self.parameters
