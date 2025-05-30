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

app.include_router(users.router)
app.include_router(media.router)
app.include_router(session.router)