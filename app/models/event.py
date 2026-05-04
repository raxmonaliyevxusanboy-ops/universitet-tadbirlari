from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.config import Base

class EventSchedule(Base):
    __tablename__ = "event_schedules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    organizer_id = Column(Integer, ForeignKey("users.id"))
    venue_id = Column(Integer, ForeignKey("venues.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, default="pending")