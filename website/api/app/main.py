from database import Base, SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException
from models import Media, User
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session

# This does create TABLE IF NOT EXIST
Base.metadata.create_all(bind=engine)

# API set up
app = FastAPI()
Instrumentator().instrument(app).expose(app)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


### USER ENDPOINTS ###


## POST ##
@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


### MEDIA ENDPOINTS ###


## GET ##

# Search media by id #
@app.get("/media/{mediaId}")
def get_media(mediaId: int, db: Session = Depends(get_db)):
    media = db.query(Media).filter(Media.mediaId == mediaId).first()
    if media is None:
        raise HTTPException(status_code=404, detail="Media not found")
    return media

