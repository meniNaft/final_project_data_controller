from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.postgres.models import Base
from app.db.postgres.models.event_sub_target_type_association import event_sub_target_type


class SubTargetType(Base):
    __tablename__ = 'sub_target_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sub_type = Column(String, nullable=False)
    target_type_id = Column(Integer, ForeignKey('target_type.id', ondelete='CASCADE'))
    target_type = relationship("TargetType", uselist=False, back_populates="sub_target_types")
    events = relationship("Event", secondary=event_sub_target_type, back_populates="sub_target_types")
