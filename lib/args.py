##
##

import argparse


def name_arg(value):
    if value in ("aws", "gcp", "azure", "vm"):
        return value
    else:
        raise argparse.ArgumentTypeError("cloud should be aws, gcp, or azure")


class Parameters(object):

    def __init__(self):
        parent_parser = argparse.ArgumentParser(add_help=False)
        parent_parser.add_argument('-i', '--input', action='store', help="Sizing output", required=True)
        parent_parser.add_argument('-o', '--output', action='store', help="Output file", default="cluster_config.json")
        parent_parser.add_argument('-n', '--name', action='store', help="Name", default="Cluster1")
        parent_parser.add_argument('-c', '--cloud', action='store', help="Cloud", default="aws")
        parent_parser.add_argument('-S', '--self', action='store_true', help="Self Managed")
        parent_parser.add_argument('-s', '--skip', action='store_true', help="Skip unused indexes")
        parent_parser.add_argument('-d', '--debug', action='store_true', help="Debug output")
        parent_parser.add_argument('-v', '--verbose', action='store_true', help="Verbose output")
        parent_parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show help message')
        self.parameters = parent_parser.parse_args()

    @property
    def args(self):
        return self.parameters
