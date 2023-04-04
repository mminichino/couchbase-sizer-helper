##
##

import attr
import ast
from attr.validators import instance_of as io
import uuid
from datetime import date
from enum import Enum


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
        self.collections = [ClusterConfigCollections.from_config(collection_data)]

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
    avg_value_size = attr.ib(validator=io(int))
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
            int(json_data.get("avg_key_size")),
            int(json_data.get("avg_value_size")),
            json_data.get("memory_utilization_percent"),
            int(json_data.get("resident_ratio")),
            float(json_data.get("compression_ratio")),
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
    where = attr.ib(default=None)

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
            json_data.get("where"),
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
    def from_config(cls, cluster: dict):
        today = date.today()
        return cls(
            str(uuid.uuid4()),
            "Sizing",
            "",
            "",
            "",
            today.strftime("%-m/%-d/%Y"),
            "2.2.1",
            [cluster],
            )

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
class SizingCluster(object):
    id = attr.ib(validator=io(str))
    name = attr.ib(validator=io(str))
    type = attr.ib(validator=io(str))
    couchbase_version = attr.ib(validator=io(str))
    cloud_provider = attr.ib(validator=io(str))
    cloud_region = attr.ib(validator=io(str))
    capella_plan = attr.ib(validator=io(str))
    infrastructure = attr.ib(validator=io(str))
    operating_system = attr.ib(validator=io(str))
    capella_credits = attr.ib(validator=io(int))
    services = attr.ib(validator=io(dict))
    service_groups = attr.ib(validator=io(list))
    cloud_service = attr.ib(default=None)

    @classmethod
    def build(cls, name: str, cloud: str, self_managed: bool):
        if self_managed:
            cluster_type = ClusterType.ON_PREM.value
        else:
            cluster_type = ClusterType.CAPELLA.value
        return cls(
            str(uuid.uuid4()),
            name,
            cluster_type,
            ClusterVersion.V7_1.value,
            cloud,
            CloudRegion[cloud].value,
            CapellaPlan.PRO.value,
            ClusterInfrastructure[cloud].value,
            "Linux",
            0,
            {},
            [],
            CloudService[cloud].value
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
    avg_key_id_size = attr.ib(validator=io(int))
    avg_document_size = attr.ib(validator=io(int))
    read_ops_per_sec = attr.ib(validator=io(float))
    write_ops_per_sec = attr.ib(validator=io(float))
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
    def from_config(cls, collection_id: str, name: str, count: int, config: ClusterConfigData):
        ratio = config.compression_ratio
        compression = ratio / 100
        return cls(
            collection_id,
            name,
            "Imported Collection",
            int(count),
            config.resident_ratio / 100,
            int(config.avg_key_size),
            int(config.avg_value_size),
            float(config.avg_cmd_get),
            float(config.avg_cmd_set),
            float(config.avg_delete_hits),
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
    id = attr.ib(validator=io(str))
    name = attr.ib(validator=io(str))
    description = attr.ib(validator=io(str))
    bucket = attr.ib(validator=io(str))
    scope = attr.ib(validator=io(str))
    collection = attr.ib(validator=io(str))
    primary_index = attr.ib(validator=io(bool))
    resident_ratio = attr.ib(validator=io(float))
    total_secondary_bytes = attr.ib(validator=io(int))
    array_index_size_of_each_element = attr.ib(validator=io(int))
    array_length = attr.ib(validator=io(int))
    number_replicas = attr.ib(validator=io(int))
    percentage_documents_in_index = attr.ib(validator=io(int))
    avg_index_scans_per_sec = attr.ib(validator=io(int))
    plasma_key_size = attr.ib(validator=io(int))
    purge_ratio = attr.ib(validator=io(float))
    compression = attr.ib(validator=io(float))
    compression_ratio = attr.ib(validator=io(float))
    jemalloc_fragmentation = attr.ib(validator=io(float))

    @classmethod
    def from_config(cls, index_id: str, bucket: str, scope: str, collection: str, replica: int, config: ClusterConfigIndexes):
        ratio = config.resident_percent
        resident_ratio = ratio / 100
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
            bucket,
            scope,
            collection,
            primary_index,
            resident_ratio,
            total_secondary_bytes,
            array_index_size_of_each_element,
            array_length,
            replica,
            1,
            config.avg_scan_rate,
            plasma_key_size,
            0.2,
            0.5,
            0.25,
            0.4
        )

    @staticmethod
    def calc_dist_value(text: str) -> int:
        s = text
        s = s.replace('(', '"(')
        s = s.replace(')', ')"')
        s = '{' + s
        s = s + '}'
        dist = ast.literal_eval(s)
        highest = [k for k, v in sorted(dist.items(), key=lambda item: item[1])][-1]
        value = highest.split('-')[-1].strip(')')
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
    def create(cls):
        return cls(
            {
                "simple_query_stale_ok": 0,
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
