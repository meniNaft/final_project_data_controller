from sqlalchemy import Table, Column, Integer, ForeignKey
from . import Base

# Association table
event_target = Table(
    'event_target', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('target_id', Integer, ForeignKey('targets.id'))
)