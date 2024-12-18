from sqlalchemy import Table, Column, Integer, ForeignKey
from . import Base

event_terror_group = Table(
    'event_terror_group', Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    Column('terror_group_id', Integer, ForeignKey('terror_groups.id'), primary_key=True)
)