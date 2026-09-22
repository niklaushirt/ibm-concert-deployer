"""
Constants for IBM AIOps DemoUI.

Centralizes hardcoded values that were previously scattered across
functions.py, functions_NG.py, and views.py.
"""

# IBM AIOps subscription identifier (previously hardcoded ~20 times)
SUBSCRIPTION_ID: str = "cfd95b7e-3bc7-4006-a4a8-a73a79c71255"

# API base paths
DATALAYER_API_PATH: str = "/irdatalayer.aiops.io/active/v1"
TOPOLOGY_API_PATH: str = "/1.0/topology"
METRICS_API_PATH: str = "/aiops/api/app/metric-api/v1/metrics"

# Kafka defaults
KAFKA_SECURITY_PROTOCOL: str = "SASL_SSL"
KAFKA_SASL_MECHANISM: str = "SCRAM-SHA-512"

# Default tenant header
DEFAULT_TENANT_ID: str = SUBSCRIPTION_ID
DEFAULT_USERNAME_HEADER: str = "admin"

# Metric injection defaults
DEFAULT_METRIC_ITERATIONS: int = 80
DEFAULT_METRIC_BATCH_SIZE: int = 40  # inner loop iterations per batch

# Log injection defaults
DEFAULT_LOG_ITERATIONS: int = 5
DEFAULT_LOG_TIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S.000000"
DEFAULT_LOG_TIME_STEPS: int = 1000
DEFAULT_LOG_TIME_SKEW: int = 60
DEFAULT_LOG_TIME_ZONE: int = -1

# Event injection defaults
DEFAULT_EVENTS_TIME_SKEW: int = 10

# Metric time defaults
DEFAULT_METRIC_TIME_SKEW: int = 240
DEFAULT_METRIC_TIME_STEP: int = 100

# Topology defaults
DEFAULT_CUSTOM_TOPOLOGY_TAG: str = ""
DEFAULT_CUSTOM_TOPOLOGY_APP_NAME: str = ""
DEFAULT_CUSTOM_TOPOLOGY_FORCE_RELOAD: str = "False"

# RobotShop defaults
DEFAULT_ROBOTSHOP_PROPERTY_RESOURCE_NAME: str = "mysql"
DEFAULT_ROBOTSHOP_PROPERTY_RESOURCE_TYPE: str = "deployment"
DEFAULT_ROBOTSHOP_PROPERTY_VALUES_NOK: str = (
    '{"innodb_buffer_pool_size": "8GB","last_change_by": "Niklaus Hirt"}'
)
DEFAULT_ROBOTSHOP_PROPERTY_VALUES_OK: str = (
    '{"innodb_buffer_pool_size": "8GB","last_change_by": "Scott James"}'
)

# Instance defaults
DEFAULT_INSTANCE_NAME: str = "IBMAIOPS"
DEFAULT_GET_CONFIG: str = "false"

# External URL placeholders
DEFAULT_EXTERNAL_URL: str = "NONE"
