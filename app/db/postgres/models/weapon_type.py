from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.postgres.models import Base


class WeaponType(Base):
    __tablename__ = 'weapon_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    sub_weapon_types = relationship("SubWeaponType", back_populates="weapon_type")

