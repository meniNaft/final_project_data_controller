from app.db.postgres.database_config import init_postgres_db
from app.services.upload_data_to_db_service import upload_data, populate_maps

if __name__ == '__main__':
    init_postgres_db()
    populate_maps()
    # upload_data("data_source/terror_attack_data_example.csv")
    upload_data("data_source/terror_attack_full_data.csv")
