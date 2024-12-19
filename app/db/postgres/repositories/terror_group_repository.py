from app.db.postgres.models import TerrorGroup
import app.db.postgres.repositories.generic_repository as generic_repo


def get_all():
    return generic_repo.find_all(TerrorGroup)


def insert_range(terror_groups: list[TerrorGroup]):
    return generic_repo.insert_range(terror_groups)


def insert_one(terror_group: TerrorGroup):
    return generic_repo.insert(terror_group)
