from sqlalchemy import Table, Column, Integer, ForeignKey
from . import Base

# Association table
event_sub_target_type = Table(
    'event_sub_target_type', Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    Column('sub_target_type_id', Integer, ForeignKey('sub_target_type.id'), primary_key=True)
)