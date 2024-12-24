import os
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError


def init_topics():
    client = KafkaAdminClient(bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'])
    topics_names = [os.environ["NEWS_TOPIC"]]

    existing_topics = client.list_topics()

    topics = [NewTopic(
        name=name,
        num_partitions=int(os.environ['NUM_PARTITIONS']),
        replication_factor=int(os.environ['REPLICATION_FACTOR'])
    ) for name in topics_names if name not in existing_topics]
    try:
        client.create_topics(topics)
    except TopicAlreadyExistsError as e:
        print(str(e))
    finally:
        client.close()
