from database import get_db
from fastapi import APIRouter, Depends, HTTPException,status
from models import User
from schemas.forms import CreateUserForm
from schemas.Out import UserOut
from sqlalchemy.orm import Session
from utils import hash_password
from logger import logger

router = APIRouter()


## GET ##
@router.get("/users/{userId}", response_model=UserOut, tags=["users"])
def get_user(userId: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == userId).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


## POST ##
@router.post("/users/", response_model=UserOut, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(user: CreateUserForm, db: Session = Depends(get_db)):
    db_user = User(name=user.username, password=hash_password(user.password))

    existing_user = db.query(User).filter(User.name == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created: {db_user.name}", extra={"user_id": db_user.id})
    return db_user
