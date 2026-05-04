from pydantic import BaseModel
from typing import Optional

class VenueBase(BaseModel):
    room_number: str
    capacity: int
    equipment: Optional[str] = None

class VenueCreate(VenueBase):
    pass

class VenueResponse(VenueBase):
    id: int

    class Config:
        from_attributes = True