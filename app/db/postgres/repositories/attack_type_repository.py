from app.db.postgres.models import AttackType
import app.db.postgres.repositories.generic_repository as generic_repo


def get_all():
    return generic_repo.find_all(AttackType)


def insert_range(attack_types: list[AttackType]):
    return generic_repo.insert_range(attack_types)


def insert_one(attack_type: AttackType):
    return generic_repo.insert(attack_type)
