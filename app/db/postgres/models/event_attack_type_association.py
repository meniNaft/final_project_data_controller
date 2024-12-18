from sqlalchemy import Table, Column, Integer, ForeignKey
from . import Base

event_attack_type = Table(
    'event_attack_type', Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    Column('attack_type_id', Integer, ForeignKey('attack_type.id'), primary_key=True)
)