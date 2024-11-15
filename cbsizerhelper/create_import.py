#!/usr/bin/env python3

import os
import json
import warnings
import sys
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime, timezone
from cbsizerhelper import __version__ as VERSION
from cbsizerhelper.lib.args import Parameters
from cbsizerhelper.lib.logging import CustomDisplayFormatter, CustomLogFormatter
from cbsizerhelper.lib.exceptions import InputFileReadError, OutputFileWriteError
from cbsizerhelper.lib.sizing import (ClusterConfig, SizingConfig, SizingCluster, SizingClusterData, SizingClusterBuckets, SizingClusterBucket, SizingClusterScope,
                                      SizingClusterCollection, SizingClusterIndex, SizingClusterIndexEntry, SizingClusterPlasmaIndexes, SizingClusterQuery, SizingServiceGroup,
                                      SearchService, EventingService, AnalyticsService, AppServices)

warnings.filterwarnings("ignore")
logger = logging.getLogger()


class RunMain(object):

    def __init__(self, parameters):
        self.input_files = parameters.input
        self.output_file = parameters.output
        self.name = parameters.name
        self.skip = parameters.skip
        self.cloud = parameters.cloud
        self.self_managed = parameters.self
        self.bucket_ratio = parameters.bucket_ratio
        self.index_ratio = parameters.index_ratio if parameters.index_ratio else 10
        self.read_rate = parameters.read
        self.write_rate = parameters.write
        self.delete_rate = parameters.delete

        logger.info(f"Create Sizer Import Utility ({VERSION})")

        sizer_config = SizingConfig.build()

        if parameters.combine:
            cluster = self.process(1, self.input_files)
            sizer_config.cluster(cluster)
        else:
            for count, input_file in enumerate(self.input_files):
                cluster = self.process(count + 1, [input_file])
                sizer_config.cluster(cluster)

        self.write_file(sizer_config.as_dict, self.output_file)

    @staticmethod
    def read_file(file_name: str) -> dict:
        try:
            with open(file_name, 'r') as input_file:
                return json.load(input_file)
        except Exception as err:
            raise InputFileReadError(f"can not read sizing file {file_name}: {err}")

    @staticmethod
    def write_file(data: dict, file_name: str) -> None:
        try:
            with open(file_name, 'w') as output_file:
                json.dump(data, output_file, indent=2)
                output_file.write("\n")
        except Exception as err:
            raise OutputFileWriteError(f"can not write output file {file_name}: {err}")

    def process(self, count: int, input_file_list: list[str]) -> dict:
        ops_sec = 0
        config_list = []
        epoch_time = datetime(1970, 1, 1).replace(tzinfo=timezone.utc)

        for input_file in input_file_list:
            data = self.read_file(input_file)
            config_list.append(ClusterConfig.from_config(data))
        cluster = SizingCluster.build(f"{self.name}{count}", self.cloud, self.self_managed)
        data = SizingClusterData.build()
        buckets = SizingClusterBuckets.build()
        index = SizingClusterIndex.build()
        indexes = SizingClusterPlasmaIndexes.build()
        bucket_count = 0
        index_count = 0

        for config in config_list:
            collections_null = False
            if len(config.collections) == 0:
                collections_null = True
            for item in config.data:
                if item.ep_couch_bucket.endswith(" totals:"):
                    bucket_name = item.ep_couch_bucket.split(" totals:")[0]
                    logger.debug(f"Processing bucket {bucket_name}")
                    bucket = SizingClusterBucket.build(str(bucket_count), bucket_name, item)
                    ops_sec += int(item.avg_cmd_get + item.avg_cmd_set)
                    if collections_null:
                        config.default_collection(bucket_name, item.curr_items)
                    scope_set = set([c.scope_name for c in config.collections if c.bucket == bucket_name])
                    scopes = (list(scope_set))
                    scope_count = 0
                    for scope_name in scopes:
                        if scope_name == "_system":
                            continue
                        logger.debug(f"Processing scope {scope_name}")
                        scope = SizingClusterScope.build(str(scope_count), scope_name)
                        collection_set = set([c.collection_name for c in config.collections if c.scope_name == scope_name])
                        collections = (list(collection_set))
                        collection_count = 0
                        for collection in collections:
                            logger.info(f"Processing keyspace {bucket_name}.{scope_name}.{collection}")
                            collection_total = 0
                            for collection_item in config.collections:
                                if collection_item.collection_name == collection and collection_item.scope_name == scope_name and collection_item.bucket == bucket_name:
                                    collection_total += collection_item.items
                            collection = SizingClusterCollection.build(str(collection_count), collection, collection_total, item,
                                                                       self.bucket_ratio, self.read_rate, self.write_rate, self.delete_rate)
                            scope.collection(collection.as_dict)
                            collection_count += 1
                        bucket.scope(scope.as_dict)
                        scope_count += 1
                    buckets.bucket(bucket.as_dict)
                    bucket_count += 1

            if len(config.indexes) > 0:
                index_table = {}
                logger.debug(f"Found {len(config.indexes)} index record(s)")
                replica_set = set([i.indexName for i in config.indexes if i.replicaId > 0])
                for item in config.indexes:
                    if item.replicaId > 0:
                        continue
                    last_scanned = datetime.strptime(item.last_known_scan_time, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)
                    if (last_scanned.timestamp() - epoch_time.timestamp()) == 0:
                        if self.skip:
                            continue
                    if item.scope == "_system":
                        logger.debug(f"Skipping index scope {item.scope}")
                        continue
                    keyspace = f"{item.bucket}.{item.scope}.{item.collection}"
                    if not index_table.get(keyspace):
                        index_table[keyspace] = {}
                    if not index_table[keyspace].get(item.indexName):
                        index_table[keyspace][item.indexName] = {}
                        index_table[keyspace][item.indexName]['records'] = []
                    index_table[keyspace][item.indexName]['records'].append(item)

                    # index_entry = SizingClusterIndexEntry.from_config(str(index_count), bucket, scope, collection, replicas, item, self.index_ratio)
                    # logger.debug(f"Processing index {bucket.name}.{scope.name}.{collection.name}.{index_entry.name}")
                    # indexes.index(index_entry.as_dict)
                    # index_count += 1

                for _keyspace, _indexes in index_table.items():
                    logger.debug(f"Index keyspace {_keyspace}:")
                    for _index_name, _index_data in index_table[_keyspace].items():
                        _index_data['summary'] = _index_data['records'][0]
                        if len(_index_data['records']) > 1:
                            _items_count = sum(_item.items_count for _item in _index_data['records'])
                            _index_data['summary'].items_count = _items_count

                        bucket = buckets.get_bucket(_index_data['summary'].bucket)
                        scope = bucket.get_scope(_index_data['summary'].scope)
                        collection = scope.get_collection(_index_data['summary'].collection)
                        if any(i.startswith(_index_data['summary'].indexName) for i in replica_set):
                            replicas = 1
                        else:
                            replicas = 0

                        index_entry = SizingClusterIndexEntry.from_config(str(index_count), bucket, scope, collection, replicas, _index_data['summary'], self.index_ratio)
                        logger.info(f"Adding index {index_count + 1} ({_index_name}) from keyspace {_keyspace}")
                        indexes.index(index_entry.as_dict)
                        index_count += 1

                logger.info(f"Processed {len(indexes.indexes)} indexes")
            else:
                indexes.index(SizingClusterIndexEntry().as_dict)

        bucket_list = []
        for count, bucket in enumerate(buckets.buckets):
            bucket_name = bucket["name"]
            if bucket_name in bucket_list:
                n = 1
                while f"{bucket_name}_{n}" in bucket_list:
                    n += 1
                bucket_name = f"{bucket_name}_{n}"
                buckets.buckets[count]["name"] = bucket_name
            bucket_list.append(bucket_name)

        data.bucket(buckets.as_dict)
        cluster.service(data.as_dict)
        cluster.service_group(SizingServiceGroup.create(["data"], self.cloud).as_dict)

        if len(indexes.indexes) > 0:
            index.indexes(indexes.as_dict)
            index_list = []
            for count, index_entry in enumerate(index.index["indexes"]):
                index_name = index_entry["name"]
                if index_name in index_list:
                    n = 1
                    while f"{index_name}_{n}" in index_list:
                        n += 1
                    index_name = f"{index_name}_{n}"
                    index.index["indexes"][count]["name"] = index_name
                index_list.append(index_name)
            cluster.service(index.as_dict)
            cluster.service(SizingClusterQuery.create(ops_sec).as_dict)

        cluster.service(SearchService.default().as_dict)
        cluster.service(EventingService.default().as_dict)
        cluster.service(AnalyticsService.default().as_dict)
        cluster.service(AppServices.default().as_dict)

        return cluster.as_dict


def main():
    global logger
    arg_parser = Parameters()
    parameters = arg_parser.args
    debug_file = os.path.join(Path.home(), "cbsizerhelper.log")

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
    screen_handler.setFormatter(CustomDisplayFormatter())
    screen_handler.setLevel(logging.INFO)
    logger.addHandler(screen_handler)

    file_handler = logging.FileHandler(debug_file, mode="w")
    file_handler.setFormatter(CustomLogFormatter())
    logger.addHandler(file_handler)

    logger.setLevel(logging.DEBUG)

    RunMain(parameters)


if __name__ == '__main__':
    try:
        main()
    except SystemExit as e:
        sys.exit(e.code)
