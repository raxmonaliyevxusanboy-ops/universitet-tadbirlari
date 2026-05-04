from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.config import get_db
from app.models.event import EventSchedule
from app.schemas.event import EventCreate, EventResponse

router = APIRouter()


@router.post("/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    try:
        new_event = EventSchedule(
            title=event.title,
            description=event.description,
            venue_id=event.venue_id,
            organizer_id=event.organizer_id,
            start_time=event.start_time,
            end_time=event.end_time
        )
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        return new_event
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Xatolik: {str(e)}")


@router.get("/", response_model=List[EventResponse])
def get_events(db: Session = Depends(get_db)):
    return db.query(EventSchedule).all()


@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: int, updated_event: EventCreate, db: Session = Depends(get_db)):
    db_event = db.query(EventSchedule).filter(EventSchedule.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Tadbir topilmadi")

    try:
        db_event.title = updated_event.title
        db_event.description = updated_event.description
        db_event.venue_id = updated_event.venue_id
        db_event.organizer_id = updated_event.organizer_id
        db_event.start_time = updated_event.start_time
        db_event.end_time = updated_event.end_time

        db.commit()
        db.refresh(db_event)
        return db_event
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Xatolik: {str(e)}")


@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(EventSchedule).filter(EventSchedule.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Tadbir topilmadi")

    try:
        db.delete(db_event)
        db.commit()
        return {"message": "Tadbir o'chirildi"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Xatolik: {str(e)}")