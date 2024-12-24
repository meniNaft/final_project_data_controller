import os
from datetime import datetime
from threading import Thread
from dotenv import load_dotenv
from app.db.elastic.elastic_repository import init_elastic_index
from app.db.postgres.database_config import init_postgres_db
from app.services.kafka_service.admin import init_topics
from app.services.kafka_service.consumer import main_consumer
from app.services.upload_data_to_db_service import upload_data
import app.db.elastic.elastic_repository as elastic_repo

load_dotenv(verbose=True)
NEWS_TOPIC = os.environ["NEWS_TOPIC"]

if __name__ == '__main__':
    print(str(datetime.now().date()))
    init_topics()
    init_postgres_db()
    init_elastic_index()
    Thread(name="Consume_teachers", target=lambda: main_consumer(NEWS_TOPIC, elastic_repo.consume_new_document)).start()
    upload_data("data_source/terror_attack_data_example.csv")
