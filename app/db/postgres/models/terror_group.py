from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.postgres.models import Base
from app.db.postgres.models.event_terror_group_association import event_terror_group


class TerrorGroup(Base):
    __tablename__ = 'terror_groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    events = relationship("Event", secondary=event_terror_group, back_populates="terror_groups")
