from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.postgres.models import Base
from app.db.postgres.models.event_attack_type_association import event_attack_type
from app.db.postgres.models.event_sub_target_type_association import event_sub_target_type
from app.db.postgres.models.event_sub_weapon_type_association import event_sub_weapon_type
from app.db.postgres.models.event_target_association import event_target
from app.db.postgres.models.event_terror_group_association import event_terror_group


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    civilian_killed_count = Column(Integer)
    civilian_injured_count = Column(Integer)
    terrorist_killed_count = Column(Integer)
    terrorist_injured_count = Column(Integer)
    terrorist_participants = Column(Integer)
    attack_motive = Column(String)

    city_id = Column(Integer, ForeignKey('cities.id', ondelete='CASCADE'))
    city = relationship("City", uselist=False, back_populates="events")
    sub_target_types = relationship("SubTargetType", secondary=event_sub_target_type, back_populates="events")
    sub_weapon_types = relationship("SubWeaponType", secondary=event_sub_weapon_type, back_populates="events")
    terror_groups = relationship("TerrorGroup", secondary=event_terror_group, back_populates="events")
    attack_types = relationship("AttackType", secondary=event_attack_type, back_populates="events")
    targets = relationship("Target", secondary=event_target, back_populates="events")
