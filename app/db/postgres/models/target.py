from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.postgres.models import Base
from app.db.postgres.models.event_target_association import event_target


class Target(Base):
    __tablename__ = 'targets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    target = Column(String, nullable=False)
    events = relationship("Event", secondary=event_target, back_populates="targets")
