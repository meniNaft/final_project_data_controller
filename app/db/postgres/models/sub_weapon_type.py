from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.postgres.models import Base
from app.db.postgres.models.event_sub_weapon_type_association import event_sub_weapon_type


class SubWeaponType(Base):
    __tablename__ = 'sub_weapon_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sub_type = Column(String, nullable=False)
    weapon_type_id = Column(Integer, ForeignKey('weapon_type.id', ondelete='CASCADE'))
    weapon_type = relationship("WeaponType", uselist=False, back_populates="sub_weapon_types")
    events = relationship("Event", secondary=event_sub_weapon_type, back_populates="sub_weapon_types")
