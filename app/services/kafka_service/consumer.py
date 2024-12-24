import json
import os
from dotenv import load_dotenv
from kafka import KafkaConsumer

load_dotenv(verbose=True)


def main_consumer(topic: str, callback):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=os.environ["BOOTSTRAP_SERVERS"],
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="latest"
    )

    print(f"consumer Received message from topic: {topic}")
    callback(consumer)
