from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from models import Media, Review, User
from schemas.forms import ReviewForm
from auth import get_current_user

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

## GET ##
@router.get("/media/{mediaId}/reviews/{reviewId}", tags=["media"])
def get_review(mediaId: int, reviewId: int, db: Session = Depends(get_db)):
    media = db.query(Media).filter(Media.mediaId == mediaId).first()
    if media is None:
        raise HTTPException(status_code=404, detail="Media not found")
    review = db.query(Review).filter(Review.reviewId == reviewId).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.get("/media/{mediaId}/reviews", tags=["media"])
def get_reviews_for_media(mediaId: int, db: Session = Depends(get_db)):

    # Check if the media exists
    media = db.query(Media).filter(Media.mediaId == mediaId).first()
    if media is None:
        raise HTTPException(status_code=404, detail="Media not found")

    reviews = db.query(
        Review.reviewId,
        Review.content,
        User.name
    ).join(
        User, Review.userId == User.id
    ).filter(
        Review.mediaId == mediaId
    ).all()

    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this media")

    return [
        {
            "reviewId": r.reviewId,
            "content": r.content,
            "name": r.name,
        }
        for r in reviews
    ]

## POST ##
@router.post("/media/{mediaId}/reviews", status_code=status.HTTP_201_CREATED, tags=["media"])
def create_review(mediaId: int ,review: ReviewForm, db: Session = Depends(get_db), current_user: User = Depends(get_current_user) ):
    db_review = Review(
        userId=current_user.id, mediaId= mediaId, content=review.content
    )

    # Check if the media exists
    media = db.query(Media).filter(Media.mediaId == mediaId).first()
    if media is None:
        raise HTTPException(status_code=404, detail="Media not found")

    # Check if the user exists
    user = db.query(User).filter(User.id == current_user.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the user has already reviewed this media
    existing_review = db.query(Review).filter(
        Review.userId == current_user.id, Review.mediaId == mediaId
    ).first()
    if existing_review:
        raise HTTPException(status_code=400, detail="User has already reviewed this media")

    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
