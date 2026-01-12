from opensearchpy import OpenSearch
import time
import random


print("Starting CPU data simulator...")
time.sleep(30)  # Allow OpenSearch to initialize


# --- Configuration ---
OPENSEARCH_HOST = "oe-cont"
OPENSEARCH_PORT = 9200
AUTH = ("admin", "QWERTYadmin123!@#")
INDEX_NAME = "cpu-index"
TELEMETRY_INTERVAL = 1
ANOMALY_PROBABILITY = 0.02
ANOMALY_DURATION = 30
CPU_BASE = 20
CPU_ANOMALY = 80
DELTA_PERCENT = 20


# --- OpenSearch Setup ---
client = OpenSearch(
    hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
    http_auth=AUTH,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)


index_mapping = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "timestamp": {"type": "date", "format": "epoch_second"},
            "cpu_usage": {"type": "float"},
            "anomaly": {"type": "integer"}
        }
    }
}


client.indices.delete(index=INDEX_NAME, ignore=[404])
client.indices.create(index=INDEX_NAME, body=index_mapping)


# --- Simulation Logic ---
def generate_data(cpu_base, is_anomaly):
    timestamp = int(time.time())
    variation = cpu_base * random.uniform(-DELTA_PERCENT, DELTA_PERCENT) / 100
    usage = cpu_base + variation
    return {
        "name": "CPU_usage",
        "timestamp": timestamp,
        "cpu_usage": usage,
        "anomaly": int(is_anomaly)
    }


def send_data(cpu_base, is_anomaly):
    data = generate_data(cpu_base, is_anomaly)
    print(data)
    client.index(index=INDEX_NAME, id=data["timestamp"], body=data)
    time.sleep(TELEMETRY_INTERVAL)


# --- Main Loop ---
while True:
    if random.random() < ANOMALY_PROBABILITY:
        print("Anomaly detected")
        for _ in range(ANOMALY_DURATION):
            send_data(CPU_ANOMALY, True)
    else:
        send_data(CPU_BASE, False)
