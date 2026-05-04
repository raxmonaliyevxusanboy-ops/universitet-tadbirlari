from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: Optional[str] = "student"

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True