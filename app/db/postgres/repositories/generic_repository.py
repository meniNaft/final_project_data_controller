from typing import TypeVar, List
from sqlalchemy.exc import SQLAlchemyError
from returns.result import Result, Success, Failure
from returns.maybe import Maybe, Nothing
from app.db.postgres.database_config import session_maker

T = TypeVar('T')


def find_by_id(model: type[T], entity_id: int) -> Maybe[T]:
    with session_maker() as session:
        return Maybe.from_optional(
            session.query(model).filter(getattr(model, get_primary_key_name(model)) == entity_id).first())


def find_all(model: type[T], limit: int = 100) -> List[T]:
    with session_maker() as session:
        res = session.query(model).limit(limit).all()
        return res


def insert(entity: T) -> Result[T, str]:
    with session_maker() as session:
        try:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return Success(entity)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))


def insert_range(entities: List[T]) -> Result[List[T], str]:
    with session_maker() as session:
        try:
            session.add_all(entities)
            session.flush()
            session.commit()
            return Success(entities)
        except SQLAlchemyError as e:
            session.rollback()
            raise e
            # return Failure(str(e))


def update(model: type[T], entity_id: int, updated_entity: T) -> Result[T, str]:
    with session_maker() as session:
        try:
            entity_to_update = session.query(model).get(entity_id)
            if not entity_to_update:
                return Failure(f"No {model.__name__} with id: {entity_id} found")

            for key, value in updated_entity.__dict__.items():
                if key != get_primary_key_name(model) and key in model.__dict__:
                    setattr(entity_to_update, key, value)

            session.commit()
            return Success(entity_to_update)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))


def delete(model: type[T], entity_id: int) -> Result[T, str]:
    with session_maker() as session:
        try:
            maybe_entity = find_by_id(model, entity_id)
            if maybe_entity is Nothing:
                return Failure(f"No {model.__name__} with id: {entity_id} found")
            entity_to_delete = maybe_entity.unwrap()
            session.delete(entity_to_delete)
            session.commit()
            return Success(entity_to_delete)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))


def get_primary_key_name(model: type[T]):
    primary_key_name = model.__name__.lower() + "_id"
    if primary_key_name == "targettype_id":
        primary_key_name = "target_type_id"
    return primary_key_name
