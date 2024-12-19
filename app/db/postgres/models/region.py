from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.postgres.models import Base


class Region(Base):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    countries = relationship("Country", back_populates="region")
