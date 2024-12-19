from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.postgres.models import Base
from app.db.postgres.models.event_attack_type_association import event_attack_type


class AttackType(Base):
    __tablename__ = 'attack_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    events = relationship("Event", secondary=event_attack_type, back_populates="attack_types")
