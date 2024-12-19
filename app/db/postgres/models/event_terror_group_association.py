from sqlalchemy import Table, Column, Integer, ForeignKey
from . import Base

event_terror_group = Table(
    'event_terror_group', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('terror_group_id', Integer, ForeignKey('terror_groups.id'))
)