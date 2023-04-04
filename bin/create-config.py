#!/usr/bin/env python3

import json
import warnings
import sys
import logging
from datetime import datetime
from lib.args import Parameters
from lib.logging import CustomFormatter
from lib.exceptions import InputFileReadError, OutputFileWriteError
from lib.sizing import (ClusterConfig, SizingConfig, SizingCluster, SizingClusterData, SizingClusterBuckets, SizingClusterBucket, SizingClusterScope, SizingClusterCollection,
                        SizingClusterIndex, SizingClusterIndexEntry, SizingClusterPlasmaIndexes, SizingClusterQuery, SizingServiceGroup)

warnings.filterwarnings("ignore")
logger = logging.getLogger()
VERSION = '1.0'


class RunMain(object):

    def __init__(self, parameters):
        self.input_file = parameters.input
        self.output_file = parameters.output
        self.data = {}
        self.name = parameters.name
        self.skip = parameters.skip
        self.cloud = parameters.cloud
        self.self_managed = parameters.self
        self.read_file()

    def read_file(self) -> None:
        try:
            with open(self.input_file, 'r') as input_file:
                self.data = json.load(input_file)
        except Exception as err:
            raise InputFileReadError(f"can not read sizing file {self.input_file}: {err}")

    def write_file(self, data: dict) -> None:
        try:
            with open(self.output_file, 'w') as output_file:
                json.dump(data, output_file, indent=2)
        except Exception as err:
            raise OutputFileWriteError(f"can not write output file {self.output_file}: {err}")

    def process(self):
        bucket_map = {}
        bucket_scope_map = {}
        bucket_collection_map = {}

        logger.info(f"Create Sizer Import ({VERSION})")
        config = ClusterConfig.from_config(self.data)
        cluster = SizingCluster.build(self.name, self.cloud, self.self_managed)
        data = SizingClusterData.build()
        buckets = SizingClusterBuckets.build()

        bucket_count = 0
        for item in config.data:
            if item.ep_couch_bucket.endswith(" totals:"):
                bucket_name = item.ep_couch_bucket.split(" totals:")[0]
                bucket = SizingClusterBucket.build(str(bucket_count), bucket_name, item)
                bucket_map[bucket_name] = str(bucket_count)
                scope_set = set([c.scope_name for c in config.collections if c.bucket == bucket_name])
                scopes = (list(scope_set))
                scope_count = 0
                for scope_name in scopes:
                    scope = SizingClusterScope.build(str(scope_count), scope_name)
                    bucket_scope_map[bucket_name] = {}
                    bucket_scope_map[bucket_name][scope_name] = str(scope_count)
                    collection_set = set([c.collection_name for c in config.collections if c.scope_name == scope_name])
                    collections = (list(collection_set))
                    collection_count = 0
                    for collection in collections:
                        collection_total = 0
                        for collection_item in config.collections:
                            if collection_item.collection_name == collection and collection_item.scope_name == scope_name and collection_item.bucket == bucket_name:
                                collection_total += collection_item.items
                        collection = SizingClusterCollection.from_config(str(collection_count), collection, collection_total, item)
                        bucket_collection_map[bucket_name] = {}
                        bucket_collection_map[bucket_name][scope_name] = {}
                        bucket_collection_map[bucket_name][scope_name][collection.name] = str(collection_count)
                        scope.collection(collection.as_dict)
                        collection_count += 1
                    bucket.scope(scope.as_dict)
                    scope_count += 1
                buckets.bucket(bucket.as_dict)
                bucket_count += 1
        data.bucket(buckets.as_dict)
        cluster.service(data.as_dict)

        cluster.service_group(SizingServiceGroup.create(["data"], self.cloud).as_dict)

        if len(config.indexes) > 0:
            epoch_time = datetime(1970, 1, 1)
            index = SizingClusterIndex.build()
            indexes = SizingClusterPlasmaIndexes.build()
            replica_set = set([i.indexName for i in config.indexes if i.replicaId > 0])
            index_count = 0
            for item in config.indexes:
                if item.replicaId > 0:
                    continue
                last_scanned = datetime.strptime(item.last_known_scan_time, '%Y-%m-%dT%H:%M:%S')
                if (last_scanned.timestamp() - epoch_time.timestamp()) == 0:
                    if self.skip:
                        continue
                bucket = bucket_map[item.bucket]
                scope = bucket_scope_map[item.bucket][item.scope]
                collection = bucket_collection_map[item.bucket][item.scope][item.collection]
                if any(i.startswith(item.indexName) for i in replica_set):
                    replicas = 1
                else:
                    replicas = 0
                index_entry = SizingClusterIndexEntry.from_config(str(index_count), bucket, scope, collection, replicas, item)
                indexes.index(index_entry.as_dict)
                index_count += 1
            index.indexes(indexes.as_dict)
            cluster.service(index.as_dict)
            cluster.service(SizingClusterQuery.create().as_dict)
            cluster.service_group(SizingServiceGroup.create(["index", "query"], self.cloud).as_dict)

        sizing = SizingConfig.from_config(cluster.as_dict)
        self.write_file(sizing.as_dict)


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
