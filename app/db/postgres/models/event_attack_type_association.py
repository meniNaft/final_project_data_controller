from sqlalchemy import Table, Column, Integer, ForeignKey
from . import Base

event_attack_type = Table(
    'event_attack_type', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('attack_type_id', Integer, ForeignKey('attack_type.id'))
)