from app.db.postgres.models import Region
import app.db.postgres.repositories.generic_repository as generic_repo


def get_all():
    return generic_repo.find_all(Region)


def insert_range(regions: list[Region]):
    return generic_repo.insert_range(regions)


def insert_one(region: Region):
    return generic_repo.insert(region)
