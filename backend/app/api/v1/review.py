from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.models.review import Review


router = APIRouter(prefix="/review", tags=["Human Review"])

@router.post("/")
def review_content(content_id: int, decision: str, db: Session = Depends(get_db)):
    review = Review(
        content_id=content_id,
        reviewer = "admin",
        decision = decision
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return {"status":"review saved"}
