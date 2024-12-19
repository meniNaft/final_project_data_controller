from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.postgres.models import Base


class State(Base):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id', ondelete='CASCADE'))
    country = relationship("Country", uselist=False, back_populates="states")
    cities = relationship("City", back_populates="state")
