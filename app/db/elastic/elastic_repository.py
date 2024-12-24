from kafka import KafkaConsumer
from elasticsearch import helpers
from app.db.elastic.database_config import index_name, expected_schema, es


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
