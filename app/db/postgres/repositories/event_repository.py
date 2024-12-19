from app.db.postgres.models import Event
import app.db.postgres.repositories.generic_repository as generic_repo


def get_all():
    return generic_repo.find_all(Event)


def insert_range(events: list[Event]):
    return generic_repo.insert_range(events)


def insert_one(event: Event):
    return generic_repo.insert(event)
