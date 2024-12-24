import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
index_name = "terror_attack_data"
expected_schema = {
    "body": str,
    "title": str,
    "lat": float,
    "lon": float,
    "date": datetime.date,
    "category": str,
}


def init_elastic_index():
    mapping = {
        "mappings": {
            "properties": {
                "body": {"type": "text"},
                "title": {"type": "text"},
                "lot": {"type": "float"},
                "lan": {"type": "float"},
                "date": {"type": "date"},
                "category": {"type": "keyword"},
            }
        }
    }
    try:
        es.indices.delete(index=index_name)
    except:
        pass
    es.indices.create(index=index_name, body=mapping)
    print(f"Index '{index_name}' created successfully.")
