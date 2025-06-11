from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from schemas.forms import LoginForm
from models import User
from sqlalchemy.orm import Session
from utils import verify_password
from auth import create_access_token
from logger import logger
import time

router = APIRouter()

## POST ##
@router.post("/login/", tags=["session"])
def login(user: LoginForm, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == user.username).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = create_access_token(data={"sub": db_user.name})
    logger.info(f"user {db_user.id} logged in", extra={"user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer", "user_id": db_user.id}

@router.get("/wait", tags=["utils"])
def wait():
    time.sleep(5)
    return "Slept 5 seconds"


