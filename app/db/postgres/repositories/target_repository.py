from app.db.postgres.models import Target
import app.db.postgres.repositories.generic_repository as generic_repo


def get_all():
    return generic_repo.find_all(Target)


def insert_range(targets: list[Target]):
    return generic_repo.insert_range(targets)


def insert_one(target: Target):
    return generic_repo.insert(target)
