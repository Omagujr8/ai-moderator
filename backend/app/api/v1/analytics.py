from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.datase import get_db
from app.models.moderation_result import ModerationResult

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get(
    "/summary",
    dependencies=[Depends(require_role("admin"))]
)

def admin_analytics():
    return {"message": "Admin-only analytics data"}

def summary(db: Session = Depends(get_db)):
    return db.query(
        ModerationResult.category,
        func.count().label("count")
    ).group_by(ModerationResult.category).all()

