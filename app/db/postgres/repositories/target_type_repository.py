from app.db.postgres.models import TargetType
import app.db.postgres.repositories.generic_repository as generic_repo


def get_all():
    return generic_repo.find_all(TargetType)


def insert_range(target_types: list[TargetType]):
    return generic_repo.insert_range(target_types)


def insert_one(target_type: TargetType):
    return generic_repo.insert(target_type)
