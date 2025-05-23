from database import Base, SessionLocal, engine
from fastapi import FastAPI
from models import Media, User
from prometheus_fastapi_instrumentator import Instrumentator
from routers import media, session, users

Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()
Instrumentator().instrument(app).expose(app)


app.include_router(users.router)
app.include_router(media.router)
app.include_router(session.router)
