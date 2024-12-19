from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.postgres.models import Base


class TargetType(Base):
    __tablename__ = 'target_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    sub_target_types = relationship("SubTargetType", back_populates="target_type")
