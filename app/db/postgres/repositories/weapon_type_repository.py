from app.db.postgres.models import WeaponType
import app.db.postgres.repositories.generic_repository as generic_repo


def get_all():
    return generic_repo.find_all(WeaponType)


def insert_range(weapon_types: list[WeaponType]):
    return generic_repo.insert_range(weapon_types)


def insert_one(weapon_type: WeaponType):
    return generic_repo.insert(weapon_type)
