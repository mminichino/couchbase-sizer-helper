##
##

import attr
# from typing import Union
from attr.validators import instance_of as io


@attr.s
class ClusterConfig(object):
    data = attr.ib(validator=io(list))
    clients = attr.ib(validator=io(list))
    timings = attr.ib(validator=io(list))
    collections = attr.ib(validator=io(list))
    indexes = attr.ib(validator=io(list))
    fts = attr.ib(validator=io(list))
    fts_slow_queries = attr.ib(validator=io(list))

    @classmethod
    def from_config(cls, json_data: dict):
        return cls(
            [ClusterConfigData.from_config(e) for e in json_data.get("data", [])],
            [ClusterConfigClients.from_config(e) for e in json_data.get("clients", [])],
            [ClusterConfigTimings.from_config(e) for e in json_data.get("timings", [])],
            [ClusterConfigCollections.from_config(e) for e in json_data.get("collections", [])],
            [ClusterConfigIndexes.from_config(e) for e in json_data.get("indexes", [])],
            json_data.get("fts", []),
            json_data.get("fts_slow_queries", []),
            )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class ClusterConfigData(object):
    ep_couch_bucket = attr.ib(validator=io(str))
    hostname = attr.ib(validator=io(str))
    cmd_get = attr.ib(validator=io(int))
    cmd_set = attr.ib(validator=io(int))
    curr_connections = attr.ib(validator=io(int))
    curr_items = attr.ib(validator=io(int))
    curr_items_tot = attr.ib(validator=io(int))
    delete_hits = attr.ib(validator=io(int))
    delete_misses = attr.ib(validator=io(int))
    ep_active_datatype_json = attr.ib(validator=io(int))
    ep_active_datatype_raw = attr.ib(validator=io(int))
    ep_active_datatype_snappy = attr.ib(validator=io(int))
    ep_active_datatype_snappy_json = attr.ib(validator=io(int))
    ep_bg_fetched = attr.ib(validator=io(int))
    ep_bg_meta_fetched = attr.ib(validator=io(int))
    ep_bucket_type = attr.ib(validator=io(str))
    ep_kv_size = attr.ib(validator=io(int))
    ep_max_size = attr.ib(validator=io(int))
    ep_mem_high_wat = attr.ib(validator=io(int))
    ep_mem_high_wat_percent = attr.ib(validator=io(float))
    ep_mem_low_wat = attr.ib(validator=io(int))
    ep_mem_low_wat_percent = attr.ib(validator=io(float))
    ep_meta_data_memory = attr.ib(validator=io(int))
    ep_num_non_resident = attr.ib(validator=io(int))
    ep_replica_datatype_json = attr.ib(validator=io(int))
    ep_replica_datatype_raw = attr.ib(validator=io(int))
    ep_replica_datatype_snappy = attr.ib(validator=io(int))
    ep_replica_datatype_snappy_json = attr.ib(validator=io(int))
    ep_value_size = attr.ib(validator=io(int))
    get_hits = attr.ib(validator=io(int))
    get_misses = attr.ib(validator=io(int))
    mem_used = attr.ib(validator=io(int))
    stat_reset = attr.ib(validator=io(str))
    vb_active_curr_items = attr.ib(validator=io(int))
    vb_active_itm_memory = attr.ib(validator=io(int))
    vb_active_itm_memory_uncompressed = attr.ib(validator=io(int))
    vb_active_meta_data_memory = attr.ib(validator=io(int))
    vb_active_ops_delete = attr.ib(validator=io(int))
    vb_active_perc_mem_resident = attr.ib(validator=io(int))
    vb_replica_curr_items = attr.ib(validator=io(int))
    vb_replica_itm_memory = attr.ib(validator=io(int))
    vb_replica_itm_memory_uncompressed = attr.ib(validator=io(int))
    vb_replica_meta_data_memory = attr.ib(validator=io(int))
    vb_replica_ops_delete = attr.ib(validator=io(int))
    vb_replica_perc_mem_resident = attr.ib(validator=io(int))
    uptime = attr.ib(validator=io(int))
    avg_cmd_get = attr.ib(validator=attr.validators.instance_of((int, float)))
    avg_cmd_set = attr.ib(validator=attr.validators.instance_of((int, float)))
    avg_delete_hits = attr.ib(validator=attr.validators.instance_of((int, float)))
    avg_key_size = attr.ib(validator=io(int))
    avg_value_size = attr.ib(validator=io(float))
    memory_utilization_percent = attr.ib(validator=io(float))
    resident_ratio = attr.ib(validator=io(int))
    compression_ratio = attr.ib(validator=io(float))
    metadata_utilization_percent = attr.ib(validator=io(float))
    total_metadata_memory = attr.ib(validator=io(int))

    @classmethod
    def from_config(cls, json_data: dict):
        return cls(
            json_data.get("ep_couch_bucket"),
            json_data.get("hostname"),
            json_data.get("cmd_get"),
            json_data.get("cmd_set"),
            json_data.get("curr_connections"),
            json_data.get("curr_items"),
            json_data.get("curr_items_tot"),
            json_data.get("delete_hits"),
            json_data.get("delete_misses"),
            json_data.get("ep_active_datatype_json"),
            json_data.get("ep_active_datatype_raw"),
            json_data.get("ep_active_datatype_snappy"),
            json_data.get("ep_active_datatype_snappy,json"),
            json_data.get("ep_bg_fetched"),
            json_data.get("ep_bg_meta_fetched"),
            json_data.get("ep_bucket_type"),
            json_data.get("ep_kv_size"),
            json_data.get("ep_max_size"),
            json_data.get("ep_mem_high_wat"),
            json_data.get("ep_mem_high_wat_percent"),
            json_data.get("ep_mem_low_wat"),
            json_data.get("ep_mem_low_wat_percent"),
            json_data.get("ep_meta_data_memory"),
            json_data.get("ep_num_non_resident"),
            json_data.get("ep_replica_datatype_json"),
            json_data.get("ep_replica_datatype_raw"),
            json_data.get("ep_replica_datatype_snappy"),
            json_data.get("ep_replica_datatype_snappy,json"),
            json_data.get("ep_value_size"),
            json_data.get("get_hits"),
            json_data.get("get_misses"),
            json_data.get("mem_used"),
            json_data.get("stat_reset"),
            json_data.get("vb_active_curr_items"),
            json_data.get("vb_active_itm_memory"),
            json_data.get("vb_active_itm_memory_uncompressed"),
            json_data.get("vb_active_meta_data_memory"),
            json_data.get("vb_active_ops_delete"),
            json_data.get("vb_active_perc_mem_resident"),
            json_data.get("vb_replica_curr_items"),
            json_data.get("vb_replica_itm_memory"),
            json_data.get("vb_replica_itm_memory_uncompressed"),
            json_data.get("vb_replica_meta_data_memory"),
            json_data.get("vb_replica_ops_delete"),
            json_data.get("vb_replica_perc_mem_resident"),
            json_data.get("uptime"),
            json_data.get("avg_cmd_get"),
            json_data.get("avg_cmd_set"),
            json_data.get("avg_delete_hits"),
            json_data.get("avg_key_size"),
            json_data.get("avg_value_size"),
            json_data.get("memory_utilization_percent"),
            json_data.get("resident_ratio"),
            json_data.get("compression_ratio"),
            json_data.get("metadata_utilization_percent"),
            json_data.get("total_metadata_memory"),
            )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class ClusterConfigClients(object):
    username = attr.ib(validator=io(str))
    bucket = attr.ib(validator=io(str))
    bucket_index = attr.ib(validator=io(int))
    agent_name = attr.ib(validator=io(str))
    internal = attr.ib(validator=io(bool))
    node = attr.ib(validator=io(str))
    client_address = attr.ib(validator=io(str))
    connections = attr.ib(validator=io(int))

    @classmethod
    def from_config(cls, json_data: dict):
        return cls(
            json_data.get("username"),
            json_data.get("bucket"),
            json_data.get("bucket_index"),
            json_data.get("agent_name"),
            json_data.get("internal"),
            json_data.get("node"),
            json_data.get("client_address"),
            json_data.get("connections"),
            )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class ClusterConfigTimings(object):
    bucket = attr.ib(validator=io(str))
    stat = attr.ib(validator=io(str))
    hostname = attr.ib(validator=io(str))
    avg = attr.ib(validator=io(str))
    total = attr.ib(validator=io(str))

    @classmethod
    def from_config(cls, json_data: dict):
        return cls(
            json_data.get("bucket"),
            json_data.get("stat"),
            json_data.get("hostname"),
            json_data.get("avg"),
            json_data.get("total"),
            )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class ClusterConfigCollections(object):
    bucket = attr.ib(validator=io(str))
    scope_name = attr.ib(validator=io(str))
    collection_name = attr.ib(validator=io(str))
    node = attr.ib(validator=io(str))
    mem_used = attr.ib(validator=io(int))
    data_size = attr.ib(validator=io(int))
    items = attr.ib(validator=io(int))
    ops_delete = attr.ib(validator=io(int))
    ops_get = attr.ib(validator=io(int))
    ops_store = attr.ib(validator=io(int))

    @classmethod
    def from_config(cls, json_data: dict):
        return cls(
            json_data.get("bucket"),
            json_data.get("scope_name"),
            json_data.get("collection_name"),
            json_data.get("node"),
            json_data.get("mem_used"),
            json_data.get("data_size"),
            json_data.get("items"),
            json_data.get("ops_delete"),
            json_data.get("ops_get"),
            json_data.get("ops_store"),
            )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class ClusterConfigIndexes(object):
    bucket = attr.ib(validator=io(str))
    scope = attr.ib(validator=io(str))
    collection = attr.ib(validator=io(str))
    indexName = attr.ib(validator=io(str))
    hostname = attr.ib(validator=io(str))
    hosts = attr.ib(validator=io(str))
    indexType = attr.ib(validator=io(str))
    definition = attr.ib(validator=io(str))
    secExprs = attr.ib(validator=io(str))
    where = attr.ib(validator=io(str))
    partitioned = attr.ib(validator=io(bool))
    partitionId = attr.ib(validator=io(int))
    numPartition = attr.ib(validator=io(int))
    partitionMap = attr.ib(validator=io(str))
    replicaId = attr.ib(validator=io(int))
    lastScanTime = attr.ib(validator=io(str))
    arrkey_size_distribution = attr.ib(validator=io(str))
    avg_array_length = attr.ib(validator=io(int))
    docid_count = attr.ib(validator=io(int))
    key_size_distribution = attr.ib(validator=io(str))
    num_docs_pending = attr.ib(validator=io(int))
    num_docs_processed = attr.ib(validator=io(int))
    num_rows_returned = attr.ib(validator=io(int))
    build_progress = attr.ib(validator=io(int))
    num_docs_queued = attr.ib(validator=io(int))
    num_docs_indexed = attr.ib(validator=io(int))
    num_rows_scanned = attr.ib(validator=io(int))
    disk_size = attr.ib(validator=io(int))
    memory_used = attr.ib(validator=io(int))
    data_size = attr.ib(validator=io(int))
    data_size_on_disk = attr.ib(validator=io(int))
    log_space_on_disk = attr.ib(validator=io(int))
    raw_data_size = attr.ib(validator=io(int))
    items_count = attr.ib(validator=io(int))
    avg_scan_rate = attr.ib(validator=io(int))
    avg_mutation_rate = attr.ib(validator=io(int))
    avg_drain_rate = attr.ib(validator=io(int))
    cache_hits = attr.ib(validator=io(int))
    cache_misses = attr.ib(validator=io(int))
    recs_in_mem = attr.ib(validator=io(int))
    recs_on_disk = attr.ib(validator=io(int))
    last_known_scan_time = attr.ib(validator=io(str))
    num_completed_requests = attr.ib(validator=io(int))
    avg_scan_latency = attr.ib(validator=io(int))
    avg_item_size = attr.ib(validator=io(int))
    avg_scan_request_latency = attr.ib(validator=io(int))
    key_size_stats_since = attr.ib(validator=io(str))
    resident_percent = attr.ib(validator=io(int))
    cache_hit_percent = attr.ib(validator=io(int))
    num_completed_requests_range = attr.ib(validator=io(int))
    num_rows_returned_range = attr.ib(validator=io(int))
    num_rows_scanned_range = attr.ib(validator=io(int))
    num_completed_requests_aggr = attr.ib(validator=io(int))
    num_rows_returned_aggr = attr.ib(validator=io(int))
    num_rows_scanned_aggr = attr.ib(validator=io(int))

    @classmethod
    def from_config(cls, json_data: dict):
        return cls(
            json_data.get("bucket"),
            json_data.get("scope"),
            json_data.get("collection"),
            json_data.get("indexName"),
            json_data.get("hostname"),
            json_data.get("hosts"),
            json_data.get("indexType"),
            json_data.get("definition"),
            json_data.get("secExprs"),
            json_data.get("where"),
            json_data.get("partitioned"),
            json_data.get("partitionId"),
            json_data.get("numPartition"),
            json_data.get("partitionMap"),
            json_data.get("replicaId"),
            json_data.get("lastScanTime"),
            json_data.get("arrkey_size_distribution"),
            json_data.get("avg_array_length"),
            json_data.get("docid_count"),
            json_data.get("key_size_distribution"),
            json_data.get("num_docs_pending"),
            json_data.get("num_docs_processed"),
            json_data.get("num_rows_returned"),
            json_data.get("build_progress"),
            json_data.get("num_docs_queued"),
            json_data.get("num_docs_indexed"),
            json_data.get("num_rows_scanned"),
            json_data.get("disk_size"),
            json_data.get("memory_used"),
            json_data.get("data_size"),
            json_data.get("data_size_on_disk"),
            json_data.get("log_space_on_disk"),
            json_data.get("raw_data_size"),
            json_data.get("items_count"),
            json_data.get("avg_scan_rate"),
            json_data.get("avg_mutation_rate"),
            json_data.get("avg_drain_rate"),
            json_data.get("cache_hits"),
            json_data.get("cache_misses"),
            json_data.get("recs_in_mem"),
            json_data.get("recs_on_disk"),
            json_data.get("last_known_scan_time"),
            json_data.get("num_completed_requests"),
            json_data.get("avg_scan_latency"),
            json_data.get("avg_item_size"),
            json_data.get("avg_scan_request_latency"),
            json_data.get("key_size_stats_since"),
            json_data.get("resident_percent"),
            json_data.get("cache_hit_percent"),
            json_data.get("num_completed_requests_range"),
            json_data.get("num_rows_returned_range"),
            json_data.get("num_rows_scanned_range"),
            json_data.get("num_completed_requests_aggr"),
            json_data.get("num_rows_returned_aggr"),
            json_data.get("num_rows_scanned_aggr"),
            )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SizingConfig(object):
    id = attr.ib(validator=io(str))
    name = attr.ib(validator=io(str))
    account = attr.ib(validator=io(str))
    application = attr.ib(validator=io(str))
    username = attr.ib(validator=io(str))
    date = attr.ib(validator=io(str))
    sizing_version = attr.ib(validator=io(str))
    clusters = attr.ib(validator=io(list))

    @classmethod
    def from_config(cls, json_data: dict):
        return cls(
            json_data.get("id"),
            json_data.get("name"),
            json_data.get("account"),
            json_data.get("application"),
            json_data.get("username"),
            json_data.get("date"),
            json_data.get("sizing_version"),
            json_data.get("clusters"),
            )

    @property
    def as_dict(self):
        return self.__dict__
