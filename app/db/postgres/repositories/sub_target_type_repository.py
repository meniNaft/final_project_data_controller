from app.db.postgres.models import SubTargetType
import app.db.postgres.repositories.generic_repository as generic_repo


def get_all():
    return generic_repo.find_all(SubTargetType)


def insert_range(sub_target_types: list[SubTargetType]):
    return generic_repo.insert_range(sub_target_types)


def insert_one(sub_target_type: SubTargetType):
    return generic_repo.insert(sub_target_type)
