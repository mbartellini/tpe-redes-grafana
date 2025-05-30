from auth import create_access_token, decode_access_token
from database import Base, SessionLocal, engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models import Media, User
from prometheus_fastapi_instrumentator import Instrumentator
from routers import media, session, users
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()
Instrumentator().instrument(app).expose(app)

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


app.include_router(users.router)
app.include_router(media.router)
app.include_router(session.router)