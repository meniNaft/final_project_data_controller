from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.postgres.models import Base


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    region_id = Column(Integer, ForeignKey('regions.id', ondelete='CASCADE'))
    region = relationship("Region", uselist=False, back_populates="countries")
    states = relationship("State", back_populates="country")
