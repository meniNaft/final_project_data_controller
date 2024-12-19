from app.db.postgres.models import SubWeaponType
import app.db.postgres.repositories.generic_repository as generic_repo


def get_all():
    return generic_repo.find_all(SubWeaponType)


def insert_range(sub_weapon_types: list[SubWeaponType]):
    return generic_repo.insert_range(sub_weapon_types)


def insert_one(sub_weapon_type: SubWeaponType):
    return generic_repo.insert(sub_weapon_type)
