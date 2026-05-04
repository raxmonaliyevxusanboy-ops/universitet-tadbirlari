from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.config import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Bu email allaqachon ro'yxatdan o'tgan")

    try:
        new_user = User(
            full_name=user.full_name,
            email=user.email,
            role=user.role,
            password_hash=None
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Baza bilan ishlashda xatolik: {str(e)}")


@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    existing_user = db.query(User).filter(
        User.email == updated_user.email,
        User.id != user_id
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Bu email boshqa tashkilotchi tomonidan band qilingan")

    try:
        db_user.full_name = updated_user.full_name
        db_user.email = updated_user.email
        db_user.role = updated_user.role

        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Xatolik: {str(e)}")


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    try:
        db.delete(db_user)
        db.commit()
        return {"message": "Foydalanuvchi o'chirildi"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Ushbu tashkilotchini o'chirib bo'lmaydi, chunki unga bog'langan tadbirlar mavjud!"
        )