from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    venue_id: int
    organizer_id: int
    start_time: datetime
    end_time: datetime

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    status: str

    class Config:
        from_attributes = True