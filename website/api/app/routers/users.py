from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from forms import CreateUserForm
from utils import hash_password

router = APIRouter()

## GET ##
@router.get("/users/{userId}")
def get_user(userId: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == userId).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


## POST ##
@router.post("/users/")
def create_user(user: CreateUserForm, db: Session = Depends(get_db)):
    db_user = User(name=user.username, password=hash_password(user.password))

    existing_user = db.query(User).filter(User.name == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

