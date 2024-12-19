from app.db.postgres.models import Country
import app.db.postgres.repositories.generic_repository as generic_repo


def get_all():
    return generic_repo.find_all(Country)


def insert_range(countries: list[Country]):
    return generic_repo.insert_range(countries)


def insert_one(country: Country):
    return generic_repo.insert(country)
