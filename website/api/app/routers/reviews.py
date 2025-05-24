from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models import Review,Media,User
from schemas.forms import ReviewForm
from sqlalchemy.orm import Session

router = APIRouter()


## GET ##
@router.get("/reviews/{reviewId}")
def get_review(reviewId: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == reviewId).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


## POST ##
@router.post("/reviews/")
def create_review(review: ReviewForm, db: Session = Depends(get_db)):
    db_review = Review(
        userId=review.userId, mediaId=review.mediaId, content=review.content
    )
    
    # Check if the media exists
    media = db.query(Media).filter(Media.mediaId == review.mediaId).first()
    if media is None:
        raise HTTPException(status_code=404, detail="Media not found")
    
    # Check if the user exists
    user = db.query(User).filter(User.id == review.userId).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the user has already reviewed this media
    existing_review = db.query(Review).filter(
        Review.userId == review.userId, Review.mediaId == review.mediaId
    ).first()
    if existing_review:
        raise HTTPException(status_code=400, detail="User has already reviewed this media")
    


    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
