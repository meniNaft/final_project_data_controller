import os
from threading import Thread
from dotenv import load_dotenv
from app.db.elastic.database_config import init_elastic_index
from app.db.neo4j.database_config import init_neo4j
from app.db.postgres.database_config import init_postgres_db
from app.services.kafka_service.admin import init_topics
from app.services.kafka_service.consumer import main_consumer
from app.services.upload_data_to_db_service import upload_data
import app.db.elastic.repositories.elastic_repository as elastic_repo

load_dotenv(verbose=True)
NEWS_TOPIC = os.environ["NEWS_TOPIC"]

if __name__ == '__main__':
    init_neo4j()
    init_topics()
    init_postgres_db()
    init_elastic_index()
    Thread(name="Consume_teachers", target=lambda: main_consumer(NEWS_TOPIC, elastic_repo.consume_new_document)).start()
    upload_data(
        first_file_path="data_source/terror_attack_data_example.csv",
        second_file_path="data_source/second_csv_example.csv"
    )
