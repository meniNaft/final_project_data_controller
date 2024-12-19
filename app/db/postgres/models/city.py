from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.postgres.models import Base


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    lat = Column(Float)
    lon = Column(Float)
    state_id = Column(Integer, ForeignKey('states.id', ondelete='CASCADE'))
    state = relationship("State", uselist=False, back_populates="cities")
    events = relationship("Event", back_populates="city")
