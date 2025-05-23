from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Media

router = APIRouter()

## GET ##
@router.get("/media/{mediaId}")
def get_media(mediaId: int, db: Session = Depends(get_db)):
    media = db.query(Media).filter(Media.mediaId == mediaId).first()
    if media is None:
        raise HTTPException(status_code=404, detail="Media not found")
    return media
