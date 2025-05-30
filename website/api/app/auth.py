from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from models import User
SECRET_KEY = "clave_secreta_super_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
    

# TOKEN MANAGEMENT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = db.query(User).filter(User.name == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user
