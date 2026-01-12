from opensearchpy import OpenSearch
from datetime import datetime, timedelta, timezone



# OpenSearch Configuration
OPENSEARCH_HOST = "oe-cont"     # container name from docker-compose
OPENSEARCH_PORT = 9200
AUTH = ("admin", "QWERTYadmin123!@#")
INDEX_NAME = "cpu-index"



# OpenSearch Client
client = OpenSearch(
    hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
    http_auth=AUTH,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)



# Query 1: Last 10 CPU records
def get_last_10_records():
    query = {
        "size": 10,
        "sort": [{"timestamp": {"order": "desc"}}],
        "query": {"match_all": {}}
    }

    resp = client.search(index=INDEX_NAME, body=query)
    hits = resp.get("hits", {}).get("hits", [])

    print("\n=== Last 10 CPU Records ===")
    for h in hits:
        print(h["_source"])



# Query 2: All anomaly records
def get_all_anomalies():
    query = {
        "size": 1000,
        "query": {
            "term": {"anomaly": 1}
        }
    }

    resp = client.search(index=INDEX_NAME, body=query)
    hits = resp.get("hits", {}).get("hits", [])

    print(f"\n=== Anomaly Records (count={len(hits)}) ===")
    for h in hits:
        print(h["_source"])



# Query 3: Average CPU usage (last 1 minute)
def get_avg_cpu_last_minute():
    now = datetime.now(timezone.utc)
    one_min_ago = now - timedelta(minutes=1)

    query = {
        "size": 0,
        "query": {
            "range": {
                "timestamp": {
                    "gte": int(one_min_ago.timestamp()),
                    "lte": int(now.timestamp())
                }
            }
        },
        "aggs": {
            "avg_cpu": {
                "avg": {"field": "cpu_usage"}
            }
        }
    }

    resp = client.search(index=INDEX_NAME, body=query)
    avg_value = resp.get("aggregations", {}).get("avg_cpu", {}).get("value")

    print("\n=== Average CPU Usage (Last 1 Minute) ===")
    print(avg_value)



# Run all queries
if __name__ == "__simulator__":
    print("Running OpenSearch queries...\n")

    get_last_10_records()
    get_all_anomalies()
    get_avg_cpu_last_minute()