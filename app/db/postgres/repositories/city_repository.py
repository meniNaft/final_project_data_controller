from app.db.postgres.models import City
import app.db.postgres.repositories.generic_repository as generic_repo


def get_all():
    return generic_repo.find_all(City)


def insert_range(cities: list[City]):
    return generic_repo.insert_range(cities)


def insert_one(city: City):
    return generic_repo.insert(city)
