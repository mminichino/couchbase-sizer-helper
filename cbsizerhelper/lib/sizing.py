##
##

import os
import attr
import ast
import time
from attr.validators import instance_of as io
import uuid
from datetime import date
from enum import Enum
from cbsizerhelper.lib.exceptions import DataError
from typing import Optional


def positive(value):
    if value < 0:
        value = value * -1
    return value


def round_num(value):
    return round(value, 2)


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

    def default_collection(self, bucket: str, items: int):
        collection_data = {
            "bucket": bucket,
            "scope_name": "_default",
            "collection_name": "_default",
            "node": "",
            "mem_used": 0,
            "data_size": 0,
            "items": items,
            "ops_delete": 0,
            "ops_get": 0,
            "ops_store": 0
        }
        self.collections.append(ClusterConfigCollections.from_config(collection_data))

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class ClusterConfigData(object):
    ep_couch_bucket = attr.ib(validator=io(str))
    hostname = attr.ib(validator=io(str))
    cmd_get = attr.ib(validator=attr.validators.instance_of((int, float)))
    cmd_set = attr.ib(validator=attr.validators.instance_of((int, float)))
    curr_connections = attr.ib(validator=attr.validators.instance_of((int, float)))
    curr_items = attr.ib(validator=attr.validators.instance_of((int, float)))
    curr_items_tot = attr.ib(validator=attr.validators.instance_of((int, float)))
    delete_hits = attr.ib(validator=attr.validators.instance_of((int, float)))
    delete_misses = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_active_datatype_json = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_active_datatype_raw = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_active_datatype_snappy = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_active_datatype_snappy_json = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_bg_fetched = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_bg_meta_fetched = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_bucket_type = attr.ib(validator=io(str))
    ep_kv_size = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_max_size = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_mem_high_wat = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_mem_high_wat_percent = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_mem_low_wat = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_mem_low_wat_percent = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_meta_data_memory = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_num_non_resident = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_replica_datatype_json = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_replica_datatype_raw = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_replica_datatype_snappy = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_replica_datatype_snappy_json = attr.ib(validator=attr.validators.instance_of((int, float)))
    ep_value_size = attr.ib(validator=attr.validators.instance_of((int, float)))
    get_hits = attr.ib(validator=attr.validators.instance_of((int, float)))
    get_misses = attr.ib(validator=attr.validators.instance_of((int, float)))
    mem_used = attr.ib(validator=attr.validators.instance_of((int, float)))
    stat_reset = attr.ib(validator=io(str))
    vb_active_curr_items = attr.ib(validator=attr.validators.instance_of((int, float)))
    vb_active_meta_data_memory = attr.ib(validator=attr.validators.instance_of((int, float)))
    vb_active_ops_delete = attr.ib(validator=attr.validators.instance_of((int, float)))
    vb_active_perc_mem_resident = attr.ib(validator=attr.validators.instance_of((int, float)))
    vb_replica_curr_items = attr.ib(validator=attr.validators.instance_of((int, float)))
    vb_replica_meta_data_memory = attr.ib(validator=attr.validators.instance_of((int, float)))
    vb_replica_ops_delete = attr.ib(validator=attr.validators.instance_of((int, float)))
    vb_replica_perc_mem_resident = attr.ib(validator=attr.validators.instance_of((int, float)))
    uptime = attr.ib(validator=attr.validators.instance_of((int, float)))
    avg_cmd_get = attr.ib(validator=attr.validators.instance_of((int, float)))
    avg_cmd_set = attr.ib(validator=attr.validators.instance_of((int, float)))
    avg_delete_hits = attr.ib(validator=attr.validators.instance_of((int, float)))
    avg_key_size = attr.ib(validator=attr.validators.instance_of((int, float)))
    avg_value_size = attr.ib(validator=attr.validators.instance_of((int, float)))
    memory_utilization_percent = attr.ib(validator=attr.validators.instance_of((int, float)))
    resident_ratio = attr.ib(validator=attr.validators.instance_of((int, float)))
    compression_ratio = attr.ib(validator=attr.validators.instance_of((int, float)))
    metadata_utilization_percent = attr.ib(validator=attr.validators.instance_of((int, float)))
    total_metadata_memory = attr.ib(validator=attr.validators.instance_of((int, float)))
    vb_active_itm_memory = attr.ib(validator=attr.validators.optional(attr.validators.instance_of((int, float))), default=None)
    vb_active_itm_memory_uncompressed = attr.ib(validator=attr.validators.optional(attr.validators.instance_of((int, float))), default=None)
    vb_replica_itm_memory = attr.ib(validator=attr.validators.optional(attr.validators.instance_of((int, float))), default=None)
    vb_replica_itm_memory_uncompressed = attr.ib(validator=attr.validators.optional(attr.validators.instance_of((int, float))), default=None)

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
            json_data.get("vb_active_meta_data_memory"),
            json_data.get("vb_active_ops_delete"),
            json_data.get("vb_active_perc_mem_resident"),
            json_data.get("vb_replica_curr_items"),
            json_data.get("vb_replica_meta_data_memory"),
            json_data.get("vb_replica_ops_delete"),
            json_data.get("vb_replica_perc_mem_resident"),
            json_data.get("uptime"),
            json_data.get("avg_cmd_get"),
            json_data.get("avg_cmd_set"),
            json_data.get("avg_delete_hits"),
            int(json_data.get("avg_key_size")),
            int(json_data.get("avg_value_size")),
            json_data.get("memory_utilization_percent"),
            int(json_data.get("resident_ratio")),
            float(json_data.get("compression_ratio")),
            json_data.get("metadata_utilization_percent"),
            json_data.get("total_metadata_memory"),
            json_data.get("vb_active_itm_memory"),
            json_data.get("vb_active_itm_memory_uncompressed"),
            json_data.get("vb_replica_itm_memory"),
            json_data.get("vb_replica_itm_memory_uncompressed"),
            )

    @property
    def as_dict(self):
        block = {k: v for k, v in self.__dict__.items() if v is not None}
        return block


@attr.s
class ClusterConfigClients(object):
    username = attr.ib(validator=io(str))
    bucket: Optional[str] = attr.ib(default=None)
    bucket_index: Optional[int] = attr.ib(default=None)
    agent_name: Optional[str] = attr.ib(default=None)
    internal: Optional[bool] = attr.ib(default=None)
    node: Optional[str] = attr.ib(default=None)
    client_address: Optional[str] = attr.ib(default=None)
    connections: Optional[int] = attr.ib(default=None)

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
    partitioned = attr.ib(validator=io(bool))
    partitionId = attr.ib(validator=attr.validators.instance_of((int, float)))
    numPartition = attr.ib(validator=attr.validators.instance_of((int, float)))
    partitionMap = attr.ib(validator=io(str))
    replicaId = attr.ib(validator=attr.validators.instance_of((int, float)))
    arrkey_size_distribution = attr.ib(validator=io(str))
    avg_array_length = attr.ib(validator=attr.validators.instance_of((int, float)))
    docid_count = attr.ib(validator=attr.validators.instance_of((int, float)))
    key_size_distribution = attr.ib(validator=io(str))
    num_docs_pending = attr.ib(validator=attr.validators.instance_of((int, float)))
    num_docs_processed = attr.ib(validator=attr.validators.instance_of((int, float)))
    num_rows_returned = attr.ib(validator=attr.validators.instance_of((int, float)))
    build_progress = attr.ib(validator=attr.validators.instance_of((int, float)))
    num_docs_queued = attr.ib(validator=attr.validators.instance_of((int, float)))
    num_docs_indexed = attr.ib(validator=attr.validators.instance_of((int, float)))
    num_rows_scanned = attr.ib(validator=attr.validators.instance_of((int, float)))
    disk_size = attr.ib(validator=attr.validators.instance_of((int, float)))
    memory_used = attr.ib(validator=attr.validators.instance_of((int, float)))
    data_size = attr.ib(validator=attr.validators.instance_of((int, float)))
    items_count = attr.ib(validator=attr.validators.instance_of((int, float)))
    avg_scan_rate = attr.ib(validator=attr.validators.instance_of((int, float)))
    avg_mutation_rate = attr.ib(validator=attr.validators.instance_of((int, float)))
    avg_drain_rate = attr.ib(validator=attr.validators.instance_of((int, float)))
    cache_hits = attr.ib(validator=attr.validators.instance_of((int, float)))
    cache_misses = attr.ib(validator=attr.validators.instance_of((int, float)))
    recs_in_mem = attr.ib(validator=attr.validators.instance_of((int, float)))
    recs_on_disk = attr.ib(validator=attr.validators.instance_of((int, float)))
    num_completed_requests = attr.ib(validator=attr.validators.instance_of((int, float)))
    avg_scan_latency = attr.ib(validator=attr.validators.instance_of((int, float)))
    avg_scan_request_latency = attr.ib(validator=attr.validators.instance_of((int, float)))
    resident_percent = attr.ib(validator=attr.validators.instance_of((int, float)))
    cache_hit_percent = attr.ib(validator=attr.validators.instance_of((int, float)))
    num_completed_requests_range = attr.ib(validator=attr.validators.instance_of((int, float)))
    num_rows_returned_range = attr.ib(validator=attr.validators.instance_of((int, float)))
    num_rows_scanned_range = attr.ib(validator=attr.validators.instance_of((int, float)))
    num_completed_requests_aggr = attr.ib(validator=attr.validators.instance_of((int, float)))
    num_rows_returned_aggr = attr.ib(validator=attr.validators.instance_of((int, float)))
    num_rows_scanned_aggr = attr.ib(validator=attr.validators.instance_of((int, float)))
    where = attr.ib(validator=attr.validators.optional(io(str)), default=None)
    lastScanTime = attr.ib(validator=attr.validators.optional(io(str)), default=None)
    data_size_on_disk = attr.ib(validator=attr.validators.optional(attr.validators.instance_of((int, float))), default=None)
    log_space_on_disk = attr.ib(validator=attr.validators.optional(attr.validators.instance_of((int, float))), default=None)
    raw_data_size = attr.ib(validator=attr.validators.optional(attr.validators.instance_of((int, float))), default=None)
    last_known_scan_time = attr.ib(validator=attr.validators.optional(io(str)), default=None)
    avg_item_size = attr.ib(validator=attr.validators.optional(attr.validators.instance_of((int, float))), default=None)
    key_size_stats_since = attr.ib(validator=attr.validators.optional(io(str)), default=None)

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
            json_data.get("partitioned"),
            json_data.get("partitionId"),
            json_data.get("numPartition"),
            json_data.get("partitionMap"),
            json_data.get("replicaId"),
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
            json_data.get("items_count"),
            json_data.get("avg_scan_rate"),
            json_data.get("avg_mutation_rate"),
            json_data.get("avg_drain_rate"),
            json_data.get("cache_hits"),
            json_data.get("cache_misses"),
            json_data.get("recs_in_mem"),
            json_data.get("recs_on_disk"),
            json_data.get("num_completed_requests"),
            json_data.get("avg_scan_latency"),
            json_data.get("avg_scan_request_latency"),
            json_data.get("resident_percent"),
            json_data.get("cache_hit_percent"),
            json_data.get("num_completed_requests_range"),
            json_data.get("num_rows_returned_range"),
            json_data.get("num_rows_scanned_range"),
            json_data.get("num_completed_requests_aggr"),
            json_data.get("num_rows_returned_aggr"),
            json_data.get("num_rows_scanned_aggr"),
            json_data.get("where"),
            json_data.get("lastScanTime"),
            json_data.get("data_size_on_disk"),
            json_data.get("log_space_on_disk"),
            json_data.get("raw_data_size"),
            json_data.get("last_known_scan_time", time.strftime('%Y-%m-%dT%H:%M:%S')),
            json_data.get("avg_item_size"),
            json_data.get("key_size_stats_since"),
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
    version = attr.ib(validator=io(int))
    archived = attr.ib(validator=io(bool))
    clusters = attr.ib(validator=io(list))

    @classmethod
    def build(cls):
        today = date.today()
        if os.name == 'nt':
            date_str = today.strftime("%#m/%#d/%Y")
        else:
            date_str = today.strftime("%-m/%-d/%Y")
        return cls(
            str(uuid.uuid4()),
            "Sizing",
            "",
            "",
            "",
            date_str,
            "3.0.1",
            1,
            False,
            [],
        )

    @classmethod
    def from_config(cls, cluster: dict):
        today = date.today()
        return cls(
            str(uuid.uuid4()),
            "Sizing",
            "",
            "",
            "",
            today.strftime("%-m/%-d/%Y"),
            "3.0.1",
            1,
            False,
            [cluster],
            )

    def cluster(self, cluster: dict):
        self.clusters.append(cluster)
        return self

    @property
    def as_dict(self):
        return self.__dict__


class ClusterType(Enum):
    CAPELLA = "Capella"
    ON_PREM = "Self-Managed"


class ClusterVersion(Enum):
    V7_0 = "7.0"
    V7_1 = "7.1"


class CapellaPlan(Enum):
    BASIC = "Basic"
    PRO = "Developer Pro"
    ENTERPRISE = "Enterprise"


class CloudProvider(Enum):
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"


class CloudRegion(Enum):
    aws = "us-east-1"
    gcp = "us-east1"
    azure = "eastus"
    vm = ""


class CloudService(Enum):
    aws = "EC2"
    gcp = "Compute Engine"
    azure = "Virtual Machine"
    vm = None


class ClusterInfrastructure(Enum):
    aws = "AWS"
    gcp = "GCP"
    azure = "Azure"
    vm = "Virtual Machines"


class CloudHardware(Enum):
    aws = {
        "instance": "c5.2xlarge",
        "cpu": 8,
        "ram": 16,
        "disk_type": "gp3",
        "disk_io": 3000,
        "network": 1
    }
    gcp = {
        "instance": "n2-standard-8",
        "cpu": 8,
        "ram": 32,
        "disk_type": "pd-ssd",
        "disk_io": 3000,
        "network": 1
    }
    azure = {
        "instance": "Standard_D8s_v5",
        "cpu": 8,
        "ram": 32,
        "disk_type": "P6",
        "disk_io": 240,
        "network": 1
    }
    vm = {
        "instance": "Custom",
        "cpu": 8,
        "ram": 32,
        "disk_type": "SSD",
        "disk_io": 10000,
        "network": 1
    }


@attr.s
class BackupConfig(object):
    backup_enabled: Optional[bool] = attr.ib(default=True)
    retention_period: Optional[int] = attr.ib(default=30)
    full_frequency: Optional[str] = attr.ib(default="Daily")
    incremental_frequency: Optional[int] = attr.ib(default=4)
    daily_change_rate: Optional[float] = attr.ib(default=0.05)

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SizingCluster(object):
    id = attr.ib(validator=io(str))
    is_basic = attr.ib(validator=io(bool))
    name = attr.ib(validator=io(str))
    type = attr.ib(validator=io(str))
    couchbase_version = attr.ib(validator=io(str))
    cloud_provider = attr.ib(validator=io(str))
    cloud_region = attr.ib(validator=io(str))
    capella_plan = attr.ib(validator=io(str))
    infrastructure = attr.ib(validator=io(str))
    cloud_service = attr.ib(validator=io(str))
    operating_system = attr.ib(validator=io(str))
    capella_credits = attr.ib(validator=io(int))
    backup = attr.ib(validator=io(dict))
    services = attr.ib(validator=io(dict))
    service_groups = attr.ib(validator=io(list))

    @classmethod
    def build(cls, name: str, cloud: str, self_managed: bool):
        if self_managed:
            cluster_type = ClusterType.ON_PREM.value
        else:
            cluster_type = ClusterType.CAPELLA.value
        return cls(
            str(uuid.uuid4()),
            False,
            name,
            cluster_type,
            ClusterVersion.V7_1.value,
            cloud,
            CloudRegion[cloud].value,
            CapellaPlan.PRO.value,
            ClusterInfrastructure[cloud].value,
            CloudService[cloud].value,
            "Linux",
            0,
            BackupConfig().as_dict,
            {},
            []
            )

    def service(self, service: dict):
        self.services.update(service)
        return self

    def service_group(self, group: dict):
        self.service_groups.append(group)
        return self

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SizingClusterBuckets(object):
    buckets = attr.ib(validator=io(list))

    @classmethod
    def build(cls):
        return cls(
            []
        )

    def bucket(self, bucket: dict):
        self.buckets.append(bucket)
        return self

    def get_bucket(self, name: str):
        for entry in self.buckets:
            if entry["name"] == name:
                return SizingClusterBucket.from_config(entry)
        raise DataError(f"Bucket {name} not found")

    def bucket_exists(self, name: str) -> bool:
        for entry in self.buckets:
            if entry["name"] == name:
                return True
        return False

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SizingClusterData(object):
    data = attr.ib(validator=io(dict))

    @classmethod
    def build(cls):
        return cls(
            {}
        )

    def bucket(self, buckets: dict):
        self.data.update(buckets)
        return self

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SizingClusterBucket(object):
    id = attr.ib(validator=io(str))
    name = attr.ib(validator=io(str))
    description = attr.ib(validator=io(str))
    bucket_type = attr.ib(validator=io(str))
    storage_engine = attr.ib(validator=io(str))
    eviction_policy = attr.ib(validator=io(str))
    value_format = attr.ib(validator=io(str))
    purge_frequency = attr.ib(validator=io(int))
    number_replicas = attr.ib(validator=io(int))
    default_compression = attr.ib(validator=io(bool))
    in_memory_compression_ratio = attr.ib(validator=io(float))
    on_disk_compression_ratio = attr.ib(validator=io(float))
    scopes = attr.ib(validator=io(list))

    @classmethod
    def from_config(cls, json_data: dict):
        return cls(
            json_data.get("id"),
            json_data.get("name"),
            json_data.get("description"),
            json_data.get("bucket_type"),
            json_data.get("storage_engine"),
            json_data.get("eviction_policy"),
            json_data.get("value_format"),
            json_data.get("purge_frequency"),
            json_data.get("number_replicas"),
            json_data.get("default_compression"),
            json_data.get("in_memory_compression_ratio"),
            json_data.get("on_disk_compression_ratio"),
            [SizingClusterScope.from_config(s) for s in json_data.get("scopes", [])],
        )

    def get_scope(self, name: str):
        for scope in self.scopes:
            if scope.name == name:
                return scope
        return None

    @classmethod
    def build(cls, bucket_id: str, name: str, config: ClusterConfigData):
        ratio = config.compression_ratio
        compression = ratio / 100
        return cls(
            bucket_id,
            name,
            "Imported Bucket",
            "Couchbase",
            "Couchstore",
            "Value",
            "JSON/Text",
            3,
            1,
            True,
            compression,
            compression,
            []
        )

    def scope(self, scope: dict):
        self.scopes.append(scope)
        return self

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SizingClusterScope(object):
    id = attr.ib(validator=io(str))
    name = attr.ib(validator=io(str))
    collections = attr.ib(validator=io(list))

    @classmethod
    def from_config(cls, json_data: dict):
        return cls(
            json_data.get("id"),
            json_data.get("name"),
            [SizingClusterCollection.from_config(c) for c in json_data.get("collections", [])],
        )

    def get_collection(self, name: str):
        for collection in self.collections:
            if collection.name == name:
                return collection
        raise DataError(f"Collection {name} not found")

    @classmethod
    def build(cls, scope_id: str, name: str):
        return cls(
            scope_id,
            name,
            []
        )

    def collection(self, collection: dict):
        self.collections.append(collection)
        return self

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SizingClusterCollection(object):
    id = attr.ib(validator=io(str))
    name = attr.ib(validator=io(str))
    description = attr.ib(validator=io(str))
    total_documents_keys = attr.ib(validator=io(int))
    working_set = attr.ib(validator=io(float))
    avg_key_id_size = attr.ib(validator=io(int), converter=positive)
    avg_document_size = attr.ib(validator=io(int), converter=positive)
    read_ops_per_sec = attr.ib(validator=io(float), converter=round_num)
    write_ops_per_sec = attr.ib(validator=io(float), converter=round_num)
    delete_ops_per_sec = attr.ib(validator=io(float))
    ttl_expiration = attr.ib(validator=io(int))
    outbound_xdcr_streams = attr.ib(validator=io(int))
    inbound_xdcr_streams = attr.ib(validator=io(int))
    xdcr_active_active = attr.ib(validator=io(bool))
    uses_gsi = attr.ib(validator=io(bool))
    use_bucket_compression = attr.ib(validator=io(bool))
    in_memory_compression_ratio = attr.ib(validator=io(float))
    on_disk_compression_ratio = attr.ib(validator=io(float))

    @classmethod
    def from_config(cls, json_data: dict):
        return cls(
            json_data.get("id"),
            json_data.get("name"),
            json_data.get("description"),
            json_data.get("total_documents_keys"),
            json_data.get("working_set"),
            json_data.get("avg_key_id_size"),
            json_data.get("avg_document_size"),
            json_data.get("read_ops_per_sec"),
            json_data.get("write_ops_per_sec"),
            json_data.get("delete_ops_per_sec"),
            json_data.get("ttl_expiration"),
            json_data.get("outbound_xdcr_streams"),
            json_data.get("inbound_xdcr_streams"),
            json_data.get("xdcr_active_active"),
            json_data.get("uses_gsi"),
            json_data.get("use_bucket_compression"),
            json_data.get("in_memory_compression_ratio"),
            json_data.get("on_disk_compression_ratio"),
        )

    @classmethod
    def build(cls, collection_id: str, name: str, count: int, config: ClusterConfigData, resident_ratio: str = None, read: str = None, write: str = None, delete: str = None):
        ratio = config.compression_ratio
        compression = ratio / 100
        effective_resident_ratio = config.resident_ratio if not resident_ratio else int(resident_ratio)
        read_ops_per_sec = config.avg_cmd_get if not read else read
        write_ops_per_sec = config.avg_cmd_set if not write else write
        delete_ops_per_sec = config.avg_delete_hits if not delete else delete
        return cls(
            collection_id,
            name,
            "Imported Collection",
            int(count),
            effective_resident_ratio / 100,
            int(config.avg_key_size),
            int(config.avg_value_size),
            float(read_ops_per_sec),
            float(write_ops_per_sec),
            float(delete_ops_per_sec),
            0,
            0,
            0,
            False,
            False,
            True,
            compression,
            compression
        )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SizingClusterIndex(object):
    index = attr.ib(validator=io(dict))

    @classmethod
    def build(cls):
        return cls(
            {}
        )

    def indexes(self, indexes: dict):
        self.index.update(indexes)
        return self

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SizingClusterPlasmaIndexes(object):
    index_type = attr.ib(validator=io(str))
    indexes = attr.ib(validator=io(list))
    config = attr.ib(validator=io(dict))

    @classmethod
    def build(cls):
        return cls(
            "plasma",
            [],
            SizingClusterConfigBlock.create().as_contents
        )

    def index(self, index: dict):
        self.indexes.append(index)
        return self

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SizingClusterIndexEntry(object):
    id: Optional[str] = attr.ib(default="0")
    name: Optional[str] = attr.ib(default="Index")
    description: Optional[str] = attr.ib(default="")
    bucket: Optional[str] = attr.ib(default="0")
    scope: Optional[str] = attr.ib(default="0")
    collection: Optional[str] = attr.ib(default="0")
    absolute_documents_in_index: Optional[int] = attr.ib(default=0)
    primary_index: Optional[bool] = attr.ib(default=False)
    default_index: Optional[bool] = attr.ib(default=False)
    resident_ratio: Optional[float] = attr.ib(default=0.1)
    total_secondary_bytes: Optional[int] = attr.ib(default=0)
    rollback_points: Optional[int] = attr.ib(default=2)
    mutation_ingest_rate: Optional[int] = attr.ib(default=0)
    scan_rate: Optional[int] = attr.ib(default=0)
    scans_timeout: Optional[int] = attr.ib(default=120)
    array_index_elem_size: Optional[int] = attr.ib(default=0)
    array_length: Optional[int] = attr.ib(default=0)
    size_of_nonarray_fields: Optional[int] = attr.ib(default=0)
    number_replicas: Optional[int] = attr.ib(default=1)
    plasma_key_size: Optional[int] = attr.ib(default=0)

    @classmethod
    def from_config(cls,
                    index_id: str,
                    bucket: SizingClusterBucket,
                    scope: SizingClusterScope,
                    collection: SizingClusterCollection,
                    replica: int,
                    config: ClusterConfigIndexes,
                    working_set_ratio: int = 10):
        resident_ratio = working_set_ratio / 100
        plasma_key_size = cls.calc_dist_value(config.key_size_distribution)
        if config.definition.startswith("CREATE PRIMARY INDEX"):
            primary_index = True
            total_secondary_bytes = 0
            array_index_size_of_each_element = 0
            array_length = 0
        else:
            primary_index = False
            total_secondary_bytes = plasma_key_size
            if len(config.arrkey_size_distribution) > 0:
                array_index_size_of_each_element = cls.calc_dist_value(config.arrkey_size_distribution)
            else:
                array_index_size_of_each_element = 0
            array_length = config.avg_array_length
        return cls(
            index_id,
            config.indexName,
            "Imported Index",
            bucket.id,
            scope.id,
            collection.id,
            config.items_count,
            primary_index,
            False,
            float(resident_ratio),
            int(total_secondary_bytes),
            0,
            config.avg_mutation_rate,
            config.avg_scan_rate,
            0,
            array_index_size_of_each_element,
            array_length,
            0,
            replica,
            plasma_key_size
        )

    @staticmethod
    def calc_dist_value(text: str) -> int:
        if len(text) == 0:
            return 64
        s = text
        s = s.replace('(', '"(')
        s = s.replace(')', ')"')
        s = '{' + s
        s = s + '}'
        dist = ast.literal_eval(s)
        highest = [k for k, v in sorted(dist.items(), key=lambda item: item[1])][-1]
        value = highest.split('-')[-1].strip(')')
        if value == 'max':
            value = 102401
        return int(value)

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SizingClusterConfigBlock(object):
    config = attr.ib(validator=io(dict))

    @classmethod
    def create(cls):
        return cls(
            {
                "os_mem_reserved": 0.2,
                "minimum_number_of_cores": 8,
                "disk_space_buffer": 0.3,
                "core_headroom": 0.2,
                "memory_growth_headroom": 0.1
            }
        )

    @property
    def as_dict(self):
        return self.__dict__

    @property
    def as_contents(self):
        return self.__dict__['config']


@attr.s
class SizingClusterQuery(object):
    query = attr.ib(validator=io(dict))

    @classmethod
    def create(cls, ops: int):
        return cls(
            {
                "simple_query_stale_ok": ops,
                "simple_query_stale_false": 0,
                "medium_query_stale_ok": 0,
                "medium_query_stale_false": 0,
                "complex_query_stale_ok": 0,
                "complex_query_stale_false": 0,
                "config": SizingClusterConfigBlock.create().as_contents
            }
        )

    @property
    def as_dict(self):
        return self.__dict__

    @property
    def as_contents(self):
        return self.__dict__['query']


@attr.s
class SizingServiceGroups(object):
    service_groups = attr.ib(validator=io(list))

    @classmethod
    def build(cls):
        return cls(
            []
        )

    def add(self, group: dict):
        self.service_groups.append(group)
        return self

    @property
    def as_dict(self):
        return self.__dict__

    @property
    def as_contents(self):
        return self.__dict__['service_groups']


@attr.s
class SizingServiceGroup(object):
    id = attr.ib(validator=io(str))
    services = attr.ib(validator=io(list))
    hardware = attr.ib(validator=io(dict))

    @classmethod
    def create(cls, services: list, cloud: str):
        return cls(
            str(uuid.uuid4()),
            services,
            CloudHardware[cloud].value
        )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SizingSearch(object):
    indexes: Optional[list] = attr.ib(default=[])
    config: Optional[dict] = attr.ib(default={})

    @classmethod
    def default(cls):
        return cls(
            [SearchIndex().as_dict],
            SearchConfig().as_dict
        )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SearchIndex(object):
    id: Optional[str] = attr.ib(default="0")
    name: Optional[str] = attr.ib(default="Index")
    description: Optional[str] = attr.ib(default="")
    bucket: Optional[str] = attr.ib(default="0")
    scope: Optional[str] = attr.ib(default="0")
    collection: Optional[str] = attr.ib(default="0")
    field_name: Optional[str] = attr.ib(default="")
    index_type: Optional[str] = attr.ib(default="Text")
    index: Optional[bool] = attr.ib(default=False)
    store: Optional[bool] = attr.ib(default=False)
    include_in_all_fields: Optional[bool] = attr.ib(default=False)
    include_term_vectors: Optional[bool] = attr.ib(default=False)
    docvalues: Optional[bool] = attr.ib(default=False)
    num_partitions: Optional[int] = attr.ib(default=1)
    percentage_documents_in_index: Optional[int] = attr.ib(default=0)
    analyzer: Optional[str] = attr.ib(default="Keyword")
    num_of_replica: Optional[int] = attr.ib(default=0)
    max_size: Optional[int] = attr.ib(default=0)
    max_from: Optional[int] = attr.ib(default=0)
    scans_per_sec: Optional[int] = attr.ib(default=0)
    avg_key_size: Optional[int] = attr.ib(default=0)
    avg_field_length: Optional[int] = attr.ib(default=0)
    rollback_points: Optional[int] = attr.ib(default=4)

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SearchConfig(object):
    os_mem_reserved: Optional[float] = attr.ib(default=0.2)
    minimum_number_of_cores: Optional[int] = attr.ib(default=8)
    disk_space_buffer: Optional[float] = attr.ib(default=0.3)
    core_headroom: Optional[float] = attr.ib(default=0.2)
    memory_growth_headroom: Optional[float] = attr.ib(default=0.1)

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SizingEventing(object):
    functions: Optional[list] = attr.ib(default=[])
    config: Optional[dict] = attr.ib(default={})

    @classmethod
    def default(cls):
        return cls(
            [EventingFunction().as_dict],
            EventingConfig().as_dict
        )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class EventingFunction(object):
    id: Optional[str] = attr.ib(default="0")
    bucket: Optional[str] = attr.ib(default="0")
    scope: Optional[str] = attr.ib(default="0")
    collection: Optional[str] = attr.ib(default="0")
    name: Optional[str] = attr.ib(default="Function")
    description: Optional[str] = attr.ib(default="")
    number_of_handlers: Optional[int] = attr.ib(default=1)
    number_of_workers: Optional[int] = attr.ib(default=1)
    function_intensity_cpu_factor: Optional[int] = attr.ib(default=1)
    destination_bucket: Optional[str] = attr.ib(default="")
    percentage_documents_satisfying_condition: Optional[int] = attr.ib(default=0)
    number_of_read_ops_per_execution: Optional[int] = attr.ib(default=0)
    read_avg_key_id_size: Optional[int] = attr.ib(default=0)
    read_avg_document_size: Optional[int] = attr.ib(default=0)
    number_of_write_ops_per_execution: Optional[int] = attr.ib(default=0)
    write_avg_key_id_size: Optional[int] = attr.ib(default=0)
    write_avg_document_size: Optional[int] = attr.ib(default=0)
    number_of_delete_ops_per_execution: Optional[int] = attr.ib(default=0)
    delete_avg_key_id_size: Optional[int] = attr.ib(default=0)
    number_of_timers_created_per_execution: Optional[int] = attr.ib(default=0)
    avg_timer_context_size: Optional[int] = attr.ib(default=0)
    number_of_n1ql_queries_per_execution: Optional[int] = attr.ib(default=0)
    avg_n1ql_query_size: Optional[int] = attr.ib(default=0)
    avg_n1ql_query_latency: Optional[int] = attr.ib(default=0)
    avg_n1ql_query_response_size: Optional[int] = attr.ib(default=0)
    number_of_log_statements_per_execution: Optional[int] = attr.ib(default=0)
    log_avg_message_size: Optional[int] = attr.ib(default=0)
    number_of_curl_statements_per_execution: Optional[int] = attr.ib(default=0)
    avg_curl_latency: Optional[int] = attr.ib(default=0)
    avg_curl_request_body_size: Optional[int] = attr.ib(default=0)
    avg_curl_response_size: Optional[int] = attr.ib(default=0)

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class EventingConfig(object):
    os_mem_reserved: Optional[float] = attr.ib(default=0.2)
    minimum_number_of_cores: Optional[int] = attr.ib(default=8)
    disk_space_buffer: Optional[float] = attr.ib(default=0.3)
    core_headroom: Optional[float] = attr.ib(default=0.2)
    memory_growth_headroom: Optional[float] = attr.ib(default=0.1)

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SizingAnalytics(object):
    number_replicas: Optional[int] = attr.ib(default=1)
    collections: Optional[list] = attr.ib(default=[])
    indexes: Optional[list] = attr.ib(default=[])
    config: Optional[dict] = attr.ib(default={})

    @classmethod
    def default(cls):
        return cls(
            1,
            [AnalyticsCollection().as_dict],
            [AnalyticsIndex().as_dict],
            AnalyticsConfig().as_dict
        )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class AnalyticsCollection(object):
    id: Optional[str] = attr.ib(default="0")
    name: Optional[str] = attr.ib(default="collection")
    description: Optional[str] = attr.ib(default="")
    bucket: Optional[str] = attr.ib(default="0")
    scope: Optional[str] = attr.ib(default="0")
    collection: Optional[str] = attr.ib(default="0")
    percentage_documents_in_collection: Optional[int] = attr.ib(default=0)
    query_temp_space_allowance: Optional[int] = attr.ib(default=2)

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class AnalyticsIndex(object):
    id: Optional[str] = attr.ib(default="0")
    name: Optional[str] = attr.ib(default="index")
    description: Optional[str] = attr.ib(default="")
    analytics_collection: Optional[str] = attr.ib(default="0")
    total_secondary_bytes: Optional[int] = attr.ib(default=0)
    percentage_documents_in_index: Optional[int] = attr.ib(default=0)

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class AnalyticsConfig(object):
    os_mem_reserved: Optional[float] = attr.ib(default=0.2)
    minimum_number_of_cores: Optional[int] = attr.ib(default=8)
    disk_space_buffer: Optional[float] = attr.ib(default=0.3)
    core_headroom: Optional[float] = attr.ib(default=0.2)
    memory_growth_headroom: Optional[float] = attr.ib(default=0.1)

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SizingAppServices(object):
    databases: Optional[list] = attr.ib(default=[])

    @classmethod
    def default(cls):
        return cls(
            [AppServiceDatabase().as_dict]
        )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class AppServiceDatabase(object):
    id: Optional[int] = attr.ib(default=0)
    name: Optional[str] = attr.ib(default="Database")
    bucket: Optional[str] = attr.ib(default="0")
    scope: Optional[str] = attr.ib(default="0")
    collection: Optional[str] = attr.ib(default="0")
    num_of_docs: Optional[int] = attr.ib(default=0)
    writes_per_sec: Optional[int] = attr.ib(default=0)
    reads_per_sec: Optional[int] = attr.ib(default=0)
    deletes_per_sec: Optional[int] = attr.ib(default=0)
    num_of_channels: Optional[int] = attr.ib(default=0)
    avg_docs_per_channel: Optional[int] = attr.ib(default=0)
    client_connections: Optional[int] = attr.ib(default=0)
    version: Optional[str] = attr.ib(default="3.0")
    num_of_users: Optional[int] = attr.ib(default=0)
    avg_channels_per_user: Optional[int] = attr.ib(default=0)
    num_of_roles: Optional[int] = attr.ib(default=0)
    avg_channels_per_role: Optional[int] = attr.ib(default=0)

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class SearchService(object):
    search = attr.ib(validator=io(dict))

    @classmethod
    def default(cls):
        return cls(
            SizingSearch().default().as_dict
        )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class EventingService(object):
    eventing = attr.ib(validator=io(dict))

    @classmethod
    def default(cls):
        return cls(
            SizingEventing().default().as_dict
        )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class AnalyticsService(object):
    analytics = attr.ib(validator=io(dict))

    @classmethod
    def default(cls):
        return cls(
            SizingAnalytics().default().as_dict
        )

    @property
    def as_dict(self):
        return self.__dict__


@attr.s
class AppServices(object):
    app_services = attr.ib(validator=io(dict))

    @classmethod
    def default(cls):
        return cls(
            SizingAppServices().default().as_dict
        )

    @property
    def as_dict(self):
        return self.__dict__
