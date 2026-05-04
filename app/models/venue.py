from sqlalchemy import Column, Integer, String
from app.config import Base

class Venue(Base):
    __tablename__ = "venues"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String, unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    equipment = Column(String, nullable=True)