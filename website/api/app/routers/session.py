from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from schemas.forms import LoginForm
from models import User
from sqlalchemy.orm import Session
from utils import verify_password

router = APIRouter()


## POST ##
@router.post("/login/", tags=["session"])
def login(user: LoginForm, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == user.username).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid username or password1")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password2")

    # TODO

    return {"message": "Login successful", "userId": db_user.id}


@router.post("/logout/", tags=["session"])
def logout():

    # TODO

    return {"message": "Logout successful"}
