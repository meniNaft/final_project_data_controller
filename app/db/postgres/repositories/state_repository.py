from app.db.postgres.models import State
import app.db.postgres.repositories.generic_repository as generic_repo


def get_all():
    return generic_repo.find_all(State)


def insert_range(states: list[State]):
    return generic_repo.insert_range(states)


def insert_one(state: State):
    return generic_repo.insert(state)
