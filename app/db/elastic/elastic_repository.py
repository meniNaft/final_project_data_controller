import datetime

from elasticsearch import Elasticsearch, helpers
from kafka import KafkaConsumer

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


def validate_document(document):
    for field, expected_type in expected_schema.items():
        if field not in document:
            print(f"Missing field: {field}")
            return False
        if not isinstance(document[field], expected_type):
            print(f"Incorrect type for field '{field}'. Expected {expected_type}, got {type(document[field])}.")
            return False
    return True


def consume_new_document(messages: KafkaConsumer):
    for message in messages:
        insert_new_documents([message.value])


def insert_new_documents(documents: list):
    try:
        actions = [{
            "_index": index_name,
            "_source": doc
        } for doc in documents if validate_document(doc)]
        if actions:
            helpers.bulk(es, actions)
            print(f"Inserted {len(actions)} documents.")
    except Exception as e:
        print(e)
    print("complete insert documents")
