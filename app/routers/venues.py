from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.config import get_db
from app.models.venue import Venue
from app.schemas.venue import VenueCreate, VenueResponse

router = APIRouter()


@router.post("/", response_model=VenueResponse)
def create_venue(venue: VenueCreate, db: Session = Depends(get_db)):
    db_venue = db.query(Venue).filter(Venue.room_number == venue.room_number).first()
    if db_venue:
        raise HTTPException(status_code=400, detail="Bu xona allaqachon mavjud")

    try:
        new_venue = Venue(
            room_number=venue.room_number,
            capacity=venue.capacity,
            equipment=venue.equipment
        )
        db.add(new_venue)
        db.commit()
        db.refresh(new_venue)
        return new_venue
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Xatolik: {str(e)}")


@router.get("/", response_model=List[VenueResponse])
def get_venues(db: Session = Depends(get_db)):
    return db.query(Venue).all()


@router.put("/{venue_id}", response_model=VenueResponse)
def update_venue(venue_id: int, updated_venue: VenueCreate, db: Session = Depends(get_db)):
    # 1. Xona mavjudligini tekshirish
    db_venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not db_venue:
        raise HTTPException(status_code=404, detail="Xona topilmadi")

    # 2. Xona raqami boshqa xonalarda band emasligini tekshirish
    existing_venue = db.query(Venue).filter(
        Venue.room_number == updated_venue.room_number,
        Venue.id != venue_id
    ).first()
    if existing_venue:
        raise HTTPException(status_code=400, detail="Bu xona raqami allaqachon mavjud")

    try:
        # Ma'lumotlarni yangilash
        db_venue.room_number = updated_venue.room_number
        db_venue.capacity = updated_venue.capacity
        db_venue.equipment = updated_venue.equipment

        db.commit()
        db.refresh(db_venue)
        return db_venue
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Baza bilan ishlashda xatolik: {str(e)}")


@router.delete("/{venue_id}")
def delete_venue(venue_id: int, db: Session = Depends(get_db)):
    db_venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not db_venue:
        raise HTTPException(status_code=404, detail="Xona topilmadi")

    try:
        db.delete(db_venue)
        db.commit()
        return {"message": "Xona muvaffaqiyatli o'chirildi"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Ushbu xonani o'chirib bo'lmaydi, chunki unga bog'langan tadbirlar mavjud!"
        )