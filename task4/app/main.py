from opensearchpy import OpenSearch
import time
import random
import sys
from datetime import datetime, timedelta, timezone

# OpenSearch Configuration
OPENSEARCH_HOST = "oe-cont"     
OPENSEARCH_PORT = 9200
AUTH = ("admin", "QWERTYadmin123!@#")
INDEX_NAME = "cpu-index"

TELEMETRY_INTERVAL = 1         
ANOMALY_PROBABILITY = 0.05        
ANOMALY_DURATION = 30            
CPU_BASE = 20
CPU_ANOMALY = 80
DELTA_PERCENT = 20             
HOST_NAME = "host-1"