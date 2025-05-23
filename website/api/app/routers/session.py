from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from forms import LoginForm
from utils import verify_password

router = APIRouter()

## POST ##
@router.post("/login/")
def login(user: LoginForm, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == user.username).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    #TODO

    return {"message": "Login successful", "userId": db_user.id}

@router.post("/logout/")
def logout():

    #TODO
    
    return {"message": "Logout successful"}


