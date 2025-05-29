from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from models import Media

router = APIRouter()

## GET ##
@router.get("/media/{mediaId}", tags=["media"])
def get_media(mediaId: int, db: Session = Depends(get_db)):
    media = db.query(Media).filter(Media.mediaId == mediaId).first()
    if media is None:
        raise HTTPException(status_code=404, detail="Media not found")
    return media

@router.get("/media/search/{mediaName}", tags=["media"])
def search_media_by_name(mediaName: str, db: Session = Depends(get_db)):
    media_list = db.query(Media).filter(Media.name.ilike(f"%{mediaName}%")).all()
    if not media_list:
        raise HTTPException(status_code=404, detail="No media found matching the name")
    return media_list
