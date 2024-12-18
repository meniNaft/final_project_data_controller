import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.postgres.models import Base

load_dotenv(verbose=True)
postgres_url = os.getenv("POSTGRES_URL")
engine = create_engine(postgres_url)
session_maker = sessionmaker(bind=engine)


def init_postgres_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
